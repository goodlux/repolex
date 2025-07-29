"""
Oxigraph Database Client

RDF graph database interface using Oxigraph for semantic data storage.
Provides high-performance triple storage, SPARQL queries, and graph management.
"""

import logging
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass
import pyoxigraph as ox
from pyoxigraph import Store, NamedNode as _NamedNode, Literal, Triple, Quad, QuerySolutions
import urllib.parse

def NamedNode(uri: str):
    """Safe wrapper for creating NamedNode that sanitizes URI strings."""
    try:
        return _NamedNode(uri)
    except Exception as e:
        # Enhanced sanitization for problematic characters and strings
        sanitized_uri = uri.strip()  # Remove leading/trailing whitespace
        
        # Replace all problematic characters
        replacements = {
            '[': '_', ']': '_', '<': '_', '>': '_',
            ' ': '_', '\t': '_', '\n': '_', '\r': '_',
            '"': '_', "'": '_', '`': '_', '{': '_', '}': '_',
            '\\': '_', '|': '_', '^': '_', '~': '_'
        }
        
        for char, replacement in replacements.items():
            sanitized_uri = sanitized_uri.replace(char, replacement)
        
        # Collapse multiple underscores into single ones
        while '__' in sanitized_uri:
            sanitized_uri = sanitized_uri.replace('__', '_')
        
        # Ensure URI has valid scheme if it doesn't start with http/https
        if not sanitized_uri.startswith(('http://', 'https://')):
            sanitized_uri = f"http://repolex.org/safe/{sanitized_uri}"
        
        try:
            return _NamedNode(sanitized_uri)
        except Exception as e2:
            # Last resort: create a hash-based URI for extremely problematic strings
            import hashlib
            uri_hash = hashlib.md5(uri.encode('utf-8')).hexdigest()
            fallback_uri = f"http://repolex.org/hash/{uri_hash}"
            try:
                return _NamedNode(fallback_uri)
            except Exception as e3:
                raise StorageError(f"Cannot create valid IRI from: '{uri[:100]}...' (original error: {e}, sanitized error: {e2}, fallback error: {e3})")

from ..models.exceptions import StorageError, ValidationError, RepolexError
from ..models.graph import GraphInfo, GraphStatistics
from ..utils.validation import validate_graph_uri, validate_sparql_query

logger = logging.getLogger(__name__)

@dataclass
class GraphInsertResult:
    """
    Result of graph insertion operation.
    
    Contains metrics and status information from triple insertion.
    """
    graph_uri: str
    triples_inserted: int  
    processing_time_ms: float
    success: bool
    errors: List[str] = None  # Any errors encountered

    def __str__(self) -> str:
        if self.success:
            return f"Inserted {self.triples_inserted} triples in {self.processing_time_ms:.1f}ms"
        else:
            return f"Failed to insert graph: {self.errors}"

@dataclass  
class QueryResult:
    """
    SPARQL query execution results.
    
    Contains query results and execution metadata.
    """
    results: List[dict]
    execution_time_ms: float
    result_count: int
    query_hash: str  # For caching
    success: bool
    errors: List[str] = None

    def __str__(self) -> str:
        if self.success:
            return f"Found {self.result_count} results in {self.execution_time_ms:.1f}ms"
        else:
            return f"Query failed: {self.errors}"

class OxigraphClient:
    """
    Oxigraph RDF database client.
    
    High-performance interface to Oxigraph for semantic data storage.
    
    Features:
    - Fast triple insertion and querying
    - Named graph management
    - SPARQL query execution
    - Graph statistics and analysis
    - Connection pooling and optimization
    
    The client manages a 19-graph semantic architecture where each
    repository can have multiple named graphs for different data types.
    """
    
    def __init__(self, 
                 db_path: Path = None,
                 max_connections: int = 10,
                 query_timeout_ms: int = 30000):
        """
        Initialize Oxigraph database client.
        
        Args:
            db_path: Path to the Oxigraph database (defaults to ~/.repolex/graph)
            max_connections: Maximum concurrent connections
            query_timeout_ms: Query timeout in milliseconds
        """
        self.db_path = db_path or Path.home() / ".repolex" / "graph"
        self.max_connections = max_connections
        self.query_timeout_ms = query_timeout_ms
        
        # Ensure the database directory exists
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize the Oxigraph store
        try:
            self._store = Store(str(self.db_path))
            logger.info(f"Oxigraph database initialized at {self.db_path}")
        except Exception as e:
            raise StorageError(
                f"Failed to initialize Oxigraph database: {e}",
                suggestions=[
                    "Check if directory is writable",
                    "Ensure sufficient disk space",
                    "Try removing corrupted database files"
                ]
            )
    
    @property
    def store(self) -> Store:
        """Access to the raw Oxigraph store - handle with care!"""
        return self._store
    
    def insert_triples(self, 
                      graph_uri: str, 
                      triples: List[str],
                      batch_size: int = 1000) -> GraphInsertResult:
        """
        Insert RDF triples (as strings) into a named graph
        
        This is a convenience method that parses string triples and 
        calls store_all_graphs. Each triple should be a valid N-Triples
        format string ending with a period.
        
        Args:
            graph_uri: The named graph URI
            triples: List of RDF triple strings in N-Triples format
            batch_size: How many triples to insert at once
            
        Returns:
            GraphInsertResult: Result of the insertion
        """
        import re
        
        # Parse string triples into Triple objects
        parsed_triples = []
        for triple_str in triples:
            # Simple N-Triples parser (handles basic cases)
            # Format: <subject> <predicate> <object> .
            # or: <subject> <predicate> "literal" .
            # or: <subject> <predicate> "literal"^^<datatype> .
            match = re.match(r'<([^>]+)>\s+<([^>]+)>\s+(<[^>]+>|"[^"]*"(?:\^\^<[^>]+>)?)\s*\.', triple_str.strip())
            if match:
                subject = NamedNode(match.group(1))
                predicate = NamedNode(match.group(2))
                obj_str = match.group(3)
                
                if obj_str.startswith('<'):
                    # URI object
                    obj = NamedNode(obj_str[1:-1])
                else:
                    # Literal object (with optional datatype)
                    if '^^' in obj_str:
                        # Datatype literal: "value"^^<datatype>
                        literal_part, datatype_part = obj_str.split('^^', 1)
                        literal_value = literal_part[1:-1]  # Remove quotes
                        datatype_uri = datatype_part[1:-1]  # Remove < >
                        obj = Literal(literal_value, datatype=NamedNode(datatype_uri))
                    else:
                        # Simple literal: "value"
                        obj = Literal(obj_str[1:-1])  # Remove quotes
                
                parsed_triples.append(Triple(subject, predicate, obj))
        
        return self.store_all_graphs(graph_uri, parsed_triples, batch_size)
    
    def store_all_graphs(self, 
                     graph_uri: str, 
                     triples: List[Triple],
                     batch_size: int = 1000) -> GraphInsertResult:
        """
        Insert triples into a named graph with batch processing.
        
        Efficiently inserts large numbers of triples using batched operations
        for optimal performance.
        
        Args:
            graph_uri: The named graph to insert into
            triples: List of RDF triples to insert
            batch_size: Number of triples to insert per batch
            
        Returns:
            GraphInsertResult: Result of the insertion operation
            
        Raises:
            StorageError: When insertion operations fail
        """
        import time
        start_time = time.perf_counter()
        
        try:
            # Validate the graph URI
            validate_graph_uri(graph_uri)
            
            if not triples:
                logger.warning(f"No triples to insert in {graph_uri}")
                return GraphInsertResult(
                    graph_uri=graph_uri,
                    triples_inserted=0,
                    processing_time_ms=0.0,
                    success=True
                )
            
            # Convert graph URI to NamedNode
            try:
                graph_node = NamedNode(graph_uri)
            except Exception as e:
                raise StorageError(f"Invalid graph URI contains illegal characters: '{graph_uri}' - {e}")
            
            inserted_count = 0
            errors = []
            
            # Batch insert for efficiency
            for i in range(0, len(triples), batch_size):
                batch = triples[i:i + batch_size]
                
                try:
                    # Create quads (triples + graph)
                    quads = [Quad(triple.subject, triple.predicate, triple.object, graph_node) 
                            for triple in batch]
                    
                    # Insert the batch
                    for quad in quads:
                        self._store.add(quad)
                    
                    inserted_count += len(batch)
                    
                    # Progress log for large datasets
                    if i > 0 and i % (batch_size * 10) == 0:
                        logger.info(f"Inserted {inserted_count}/{len(triples)} triples in {graph_uri}")
                
                except Exception as e:
                    error_msg = f"Batch {i}-{i+len(batch)}: {str(e)}"
                    errors.append(error_msg)
                    logger.warning(error_msg)
            
            end_time = time.perf_counter()
            processing_time_ms = (end_time - start_time) * 1000
            
            success = len(errors) == 0
            result = GraphInsertResult(
                graph_uri=graph_uri,
                triples_inserted=inserted_count,
                processing_time_ms=processing_time_ms,
                success=success,
                errors=errors if errors else None
            )
            
            if success:
                logger.info(f"Successfully inserted {inserted_count} triples")
            else:
                logger.error(f"Insertion completed with {len(errors)} errors")
            
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            processing_time_ms = (end_time - start_time) * 1000
            
            raise StorageError(
                f"Failed to insert triples in {graph_uri}: {e}",
                suggestions=[
                    "Check if graph URI is valid",
                    "Ensure database is not corrupted",
                    "Try smaller batch sizes",
                    f"Failed after {processing_time_ms:.1f}ms"
                ]
            )
    
    def _remove_release_graphs_sync(self, graph_uri: str) -> bool:
        """
        Remove entire named graph from database.
        
        Completely removes all triples in the specified named graph.
        This is a destructive operation used for nuclear updates
        where we need to rebuild a graph completely.
        
        Args:
            graph_uri: The named graph to completely remove
            
        Returns:
            bool: True if successfully removed, False if graph didn't exist
            
        Raises:
            StorageError: When removal operations fail
        """
        try:
            validate_graph_uri(graph_uri)
            
            # Check if graph exists first
            if not self.graph_exists(graph_uri):
                logger.warning(f"Graph {graph_uri} doesn't exist - nothing to remove")
                return False
            
            # Get triple count before removing (for logging)
            count_before = self._count_triples_in_graph_sync(graph_uri)
            
            # Remove the entire graph
            try:
                graph_node = NamedNode(graph_uri)
            except Exception as e:
                raise StorageError(f"Invalid graph URI contains illegal characters: '{graph_uri}' - {e}")
            
            # Remove all quads in this graph
            self._store.remove_graph(graph_node)
            
            logger.info(f"Removed {count_before} triples from graph {graph_uri}")
            return True
            
        except Exception as e:
            raise StorageError(
                f"Failed to remove graph {graph_uri}: {e}",
                suggestions=[
                    "Check if graph URI is valid", 
                    "Ensure database is not locked",
                    "Try restarting the client"
                ]
            )
    
    def query_sparql(self, 
                     sparql_query: str,
                     result_format: str = "dict") -> QueryResult:
        """
        Execute SPARQL query against the database.
        
        Executes SPARQL queries with proper error handling and
        result formatting.
        
        Args:
            sparql_query: SPARQL query string
            result_format: How to format results ("dict", "json", "turtle")
            
        Returns:
            QueryResult: Query execution results
            
        Raises:
            StorageError: When query execution fails
        """
        import time
        import hashlib
        
        start_time = time.perf_counter()
        
        try:
            # Security check - validate query syntax
            validate_sparql_query(sparql_query)
            
            # Create query hash for caching
            query_hash = hashlib.md5(sparql_query.encode()).hexdigest()[:8]
            
            logger.debug(f"Executing SPARQL query {query_hash}")
            
            # Execute the query
            query_results = self._store.query(sparql_query)
            
            # Process results based on format
            processed_results = self._process_query_results(query_results, result_format)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            result = QueryResult(
                results=processed_results,
                execution_time_ms=execution_time_ms,
                result_count=len(processed_results),
                query_hash=query_hash,
                success=True
            )
            
            logger.info(f"Query executed successfully: {len(processed_results)} results")
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            error_msg = f"Query execution failed: {str(e)}"
            
            result = QueryResult(
                results=[],
                execution_time_ms=execution_time_ms,
                result_count=0,
                query_hash="error",
                success=False,
                errors=[error_msg]
            )
            
            logger.error(error_msg)
            
            raise StorageError(
                f"SPARQL query execution failed: {e}",
                suggestions=[
                    "Check SPARQL query syntax",
                    "Ensure referenced graphs exist",
                    "Try simpler query to test connection",
                    f"Query failed after {execution_time_ms:.1f}ms"
                ]
            )
    
    def _process_query_results(self, 
                              query_results: QuerySolutions, 
                              result_format: str) -> List[dict]:
        """
        Process SPARQL query results into the requested format.
        
        Internal method to convert Oxigraph query results into
        structured data formats.
        """
        processed = []
        
        try:
            # Get variable names from query results
            variables = query_results.variables
            
            for solution in query_results:
                result_dict = {}
                # PyOxigraph solution access by variable name
                for variable in variables:
                    # Use variable.value to get the name without ? prefix
                    variable_name = variable.value
                    term = solution[variable_name]
                    
                    # Handle None terms (unbound variables) 
                    if term is None:
                        # For COUNT queries, None usually means 0
                        if 'count' in variable_name.lower():
                            result_dict[variable_name] = 0
                        continue
                    
                    # Convert RDF terms to appropriate format
                    if hasattr(term, 'value'):
                        # Literal value
                        result_dict[variable_name] = term.value
                    else:
                        # URI or other term
                        result_dict[variable_name] = str(term)
                
                processed.append(result_dict)
                
        except Exception as e:
            logger.warning(f"Error processing query result: {e}")
        
        return processed
    
    def list_repository_graphs(self, org_repo: str = None, release: str = None) -> List[str]:
        """
        List repository graphs as URIs
        
        GraphManager expects this signature. Returns list of graph URIs.
        """
        if org_repo:
            filter_prefix = f"http://repolex.org/repo/{org_repo}"
        else:
            filter_prefix = None
        
        graphs = self._list_repository_graphs_sync(filter_prefix)
        return [g.graph_uri for g in graphs]
    
    def _list_repository_graphs_sync(self, filter_prefix: str = None) -> List[GraphInfo]:
        """
        List all available named graphs with metadata.
        
        Gets a list of all named graphs in the database with
        statistics about each graph.
        
        Args:
            filter_prefix: Only show graphs starting with this prefix
            
        Returns:
            List[GraphInfo]: Information about each named graph
        """
        try:
            # Get all graph URIs
            all_graphs = []
            
            # Query for all named graphs
            graph_query = """
            SELECT DISTINCT ?graph WHERE {
                GRAPH ?graph { ?s ?p ?o }
            }
            ORDER BY ?graph
            """
            
            result = self.query_sparql(graph_query)
            
            for row in result.results:
                graph_uri = row.get('graph', '')
                
                # Apply filter if provided
                if filter_prefix and not graph_uri.startswith(filter_prefix):
                    continue
                
                # Get basic triple count for this graph
                triple_count = self._count_triples_in_graph_sync(graph_uri)
                
                # Extract org_repo from URI pattern: http://repolex.org/repo/org/repo/...
                org_repo = "unknown/unknown"
                if "/repo/" in graph_uri:
                    parts = graph_uri.split("/repo/", 1)[1].split("/")
                    if len(parts) >= 2:
                        org_repo = f"{parts[0]}/{parts[1]}"
                
                # Import the required types
                from ..models.graph import GraphType, GraphStatus
                from datetime import datetime
                
                # Map the graph type
                graph_type_str = self._classify_graph_type(graph_uri)
                graph_type = self._map_to_graph_type_enum(graph_type_str)
                
                graph_info = GraphInfo(
                    graph_uri=graph_uri,
                    graph_type=graph_type,
                    org_repo=org_repo,
                    status=GraphStatus.READY,
                    created_at=datetime.now(),  # TODO: Get from metadata
                    updated_at=datetime.now(),  # TODO: Get from metadata
                    triple_count=triple_count
                )
                
                all_graphs.append(graph_info)
            
            logger.info(f"Found {len(all_graphs)} named graphs")
            return all_graphs
            
        except Exception as e:
            raise StorageError(
                f"Failed to list graphs: {e}",
                suggestions=[
                    "Check database connection",
                    "Ensure graphs exist",
                    "Try without filter first"
                ]
            )
    
    def _list_all_graphs_sync(self) -> List[str]:
        """
        List all graph URIs in the database
        
        Returns:
            List[str]: List of all graph URIs
        """
        try:
            graph_query = """
            SELECT DISTINCT ?graph WHERE {
                GRAPH ?graph { ?s ?p ?o }
            }
            ORDER BY ?graph
            """
            
            result = self.query_sparql(graph_query)
            return [row.get('graph', '') for row in result.results]
            
        except Exception as e:
            raise StorageError(
                f"Failed to list all graphs: {e}",
                suggestions=[
                    "Check database connection",
                    "Ensure graphs exist"
                ]
            )
    
    def get_graph_statistics(self, graph_uri: str) -> GraphStatistics:
        """
        Get detailed statistics about a specific graph.
        
        Analyzes a named graph to provide comprehensive statistics
        about its contents and structure.
        
        Args:
            graph_uri: The named graph to analyze
            
        Returns:
            GraphStatistics: Detailed analysis of the graph
        """
        try:
            validate_graph_uri(graph_uri)
            
            # Count triples in this graph
            triple_count = self._count_triples_in_graph_sync(graph_uri)
            
            # Get unique subjects (entities)
            # Escape special characters in URI for SPARQL
            escaped_uri = graph_uri.replace('\\', '\\\\').replace('"', '\\"')
            subject_query = f"""
            SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {{
                GRAPH <{escaped_uri}> {{ ?s ?p ?o }}
            }}
            """
            subject_result = self.query_sparql(subject_query)
            subject_count = int(subject_result.results[0].get('count', 0))
            
            # Get unique predicates (relationships)
            predicate_query = f"""
            SELECT (COUNT(DISTINCT ?p) AS ?count) WHERE {{
                GRAPH <{escaped_uri}> {{ ?s ?p ?o }}
            }}
            """
            predicate_result = self.query_sparql(predicate_query)
            predicate_count = int(predicate_result.results[0].get('count', 0))
            
            # Estimate size (rough calculation)
            estimated_size = triple_count * 100  # Rough bytes estimate
            
            return GraphStatistics(
                graph_uri=graph_uri,
                triple_count=triple_count,
                subject_count=subject_count,
                predicate_count=predicate_count,
                size_bytes=estimated_size,
                last_modified=None,  # TODO: Add timestamp tracking
                error_count=0  # No errors in healthy graphs
            )
            
        except Exception as e:
            raise StorageError(
                f"Failed to analyze graph {graph_uri}: {e}",
                suggestions=[
                    "Check if graph exists",
                    "Ensure valid graph URI",
                    "Try simpler analysis query"
                ]
            )
    
    def _count_triples_in_graph_sync(self, graph_uri: str) -> int:
        """
        Count the triples in a named graph.
        
        Quick method to count how many triples exist
        in a specific named graph.
        """
        try:
            # Escape special characters in URI for SPARQL
            escaped_uri = graph_uri.replace('\\', '\\\\').replace('"', '\\"')
            count_query = f"""
            SELECT (COUNT(*) AS ?count) WHERE {{
                GRAPH <{escaped_uri}> {{ ?s ?p ?o }}
            }}
            """
            
            result = self.query_sparql(count_query)
            return int(result.results[0].get('count', 0))
            
        except Exception:
            return 0  # Return 0 if count fails
    
    def graph_exists(self, graph_uri: str) -> bool:
        """
        Check if a named graph exists in the database.
        
        Quick check if a named graph contains any triples.
        """
        try:
            return self._count_triples_in_graph_sync(graph_uri) > 0
        except Exception:
            return False
    
    def _map_to_graph_type_enum(self, graph_type_str: str):
        """Map string graph type to GraphType enum."""
        from ..models.graph import GraphType
        
        mapping = {
            "ontology": GraphType.ONTOLOGY_WOC,
            "functions": GraphType.FUNCTIONS_STABLE,
            "functions_stable": GraphType.FUNCTIONS_STABLE,
            "functions_implementations": GraphType.FUNCTIONS_IMPL,
            "git_intelligence": GraphType.GIT_COMMITS,
            "git_commits": GraphType.GIT_COMMITS,
            "git_developers": GraphType.GIT_DEVELOPERS,
            "git_branches": GraphType.GIT_BRANCHES,
            "git_tags": GraphType.GIT_TAGS,
            "abc_events": GraphType.ABC_EVENTS,
            "evolution": GraphType.EVOLUTION_STATS,
            "evolution_analysis": GraphType.EVOLUTION_ANALYSIS,
            "evolution_statistics": GraphType.EVOLUTION_STATS,
            "evolution_patterns": GraphType.EVOLUTION_PATTERNS,
            "file_structure": GraphType.FILES_STRUCTURE,
            "metadata": GraphType.PROCESSING_META,
            "text_content": GraphType.TEXT_CONTENT,
            "text_entities": GraphType.TEXT_ENTITIES,
            "text_relationships": GraphType.TEXT_RELATIONSHIPS,
            "text_topics": GraphType.TEXT_TOPICS,
            "unknown": GraphType.ONTOLOGY_WOC  # Default fallback
        }
        
        return mapping.get(graph_type_str, GraphType.ONTOLOGY_WOC)
    
    def _classify_graph_type(self, graph_uri: str) -> str:
        """
        Classify the type of named graph based on URI pattern.
        
        Based on the URI pattern, determine if this is an ontology graph,
        function graph, git intelligence graph, etc.
        """
        if "/ontology/" in graph_uri:
            return "ontology"
        elif "/functions/stable" in graph_uri:
            return "functions_stable"
        elif "/functions/implementations" in graph_uri:
            return "functions_implementations"
        elif "/functions/" in graph_uri:
            return "functions"
        elif "/git/commits" in graph_uri:
            return "git_commits"
        elif "/git/developers" in graph_uri:
            return "git_developers"
        elif "/git/branches" in graph_uri:
            return "git_branches"
        elif "/git/tags" in graph_uri:
            return "git_tags"
        elif "/git/" in graph_uri:
            return "git_intelligence"
        elif "/abc/" in graph_uri:
            return "abc_events"
        elif "/evolution/analysis" in graph_uri:
            return "evolution_analysis"
        elif "/evolution/statistics" in graph_uri:
            return "evolution_statistics"
        elif "/evolution/patterns" in graph_uri:
            return "evolution_patterns"
        elif "/evolution/" in graph_uri:
            return "evolution"
        elif "/files/" in graph_uri:
            return "file_structure"
        elif "/meta/" in graph_uri:
            return "metadata"
        elif "/content/structure" in graph_uri:
            return "text_content"
        elif "/content/topics" in graph_uri:
            return "text_topics"
        elif "/entities/" in graph_uri:
            return "text_entities"
        elif "/relationships/" in graph_uri:
            return "text_relationships"
        else:
            return "unknown"
    
    def get_database_stats(self) -> dict:
        """
        Get comprehensive database statistics.
        
        Returns comprehensive statistics about the entire database,
        including performance metrics and storage information.
        """
        try:
            graphs = self._list_repository_graphs_sync()
            
            total_triples = sum(g.triple_count for g in graphs)
            total_size = sum(g.size_bytes for g in graphs)
            
            # Group by type
            graph_types = {}
            for graph in graphs:
                graph_type = graph.graph_type
                if graph_type not in graph_types:
                    graph_types[graph_type] = 0
                graph_types[graph_type] += 1
            
            return {
                "total_graphs": len(graphs),
                "total_triples": total_triples,
                "total_size_bytes": total_size,
                "graph_types": graph_types,
                "db_path": str(self.db_path),
                "status": "operational"
            }
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def backup_database(self, backup_path: Path) -> bool:
        """
        Create a backup of the entire database.
        
        Creates a backup of the entire Oxigraph database for
        disaster recovery and data preservation.
        """
        try:
            import shutil
            
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Simple file copy backup
            if self.db_path.is_file():
                shutil.copy2(self.db_path, backup_path)
            else:
                shutil.copytree(self.db_path, backup_path, dirs_exist_ok=True)
            
            logger.info(f"Database backed up to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        # Oxigraph handles cleanup automatically
        if exc_type:
            logger.error(f"Database error: {exc_val}")
        else:
            logger.info("Database session completed successfully")
    
    def remove_all_repository_graphs(self, org_repo: str) -> bool:
        """
        Remove all graphs for a repository
        
        Removes all named graphs associated with a specific repository.
        """
        # Get all graphs for this repository
        graphs = self._list_repository_graphs_sync(f"http://repolex.org/repo/{org_repo}")
        removed_count = 0
        
        for graph_info in graphs:
            if self._remove_release_graphs_sync(graph_info.graph_uri):
                removed_count += 1
        
        logger.info(f"Removed {removed_count} graphs for {org_repo}")
        return removed_count > 0
    
    def nuclear_clear_implementation_graphs(self, org_repo: str, release: str) -> bool:
        """
        Nuclear clear implementation graphs for a specific release
        
        Completely removes all implementation graphs for a repository release.
        """
        # Implementation graphs have the release in their URI
        impl_uri = f"http://repolex.org/{org_repo}/implementations/{release}"
        return self._remove_release_graphs_sync(impl_uri)
    
    def get_detailed_graph_info(self, graph_uri: str) -> GraphInfo:
        """
        Get detailed information about a graph
        
        Returns comprehensive information about a specific named graph.
        """
        stats = self.get_graph_statistics(graph_uri)
        
        # Extract org_repo from URI pattern: http://repolex.org/repo/org/repo/...
        org_repo = "unknown/unknown"
        if "/repo/" in graph_uri:
            parts = graph_uri.split("/repo/", 1)[1].split("/")
            if len(parts) >= 2:
                org_repo = f"{parts[0]}/{parts[1]}"
        
        # Import the required types
        from ..models.graph import GraphType, GraphStatus
        from datetime import datetime
        
        # Map the graph type
        graph_type_str = self._classify_graph_type(graph_uri)
        graph_type = self._map_to_graph_type_enum(graph_type_str)
        
        return GraphInfo(
            graph_uri=graph_uri,
            graph_type=graph_type,
            org_repo=org_repo,
            status=GraphStatus.READY,
            created_at=datetime.now(),  # TODO: Get from metadata
            updated_at=datetime.now(),  # TODO: Get from metadata
            triple_count=stats.triple_count
        )
    
    def store_repository_graphs(self, org_repo: str, release: str, graphs_created: List, progress_callback=None):
        """
        Store all graphs for a repository release.
        
        This method signature matches what GraphManager expects.
        """
        # Count total triples across all created graphs
        total_triples = 0
        for graph_uri in graphs_created:
            try:
                triple_count = self._count_triples_in_graph_sync(graph_uri)
                total_triples += triple_count
            except Exception as e:
                logger.warning(f"Could not count triples in {graph_uri}: {e}")
        
        logger.info(f"Stored {total_triples} triples for {org_repo} {release}")
        return total_triples
    
    def list_all_graphs(self) -> List[str]:
        """
        List all named graphs in the database.
        """
        return self._list_all_graphs_sync()
    
    def count_triples_in_graph(self, graph_uri: str) -> int:
        """
        Count triples in a specific named graph.
        """
        return self._count_triples_in_graph_sync(graph_uri)
    
    def remove_release_graphs(self, org_repo: str, release: str) -> bool:
        """
        Remove graphs for a specific repository release.
        """
        # Build the graph URI for this release
        release_uri = f"http://repolex.org/{org_repo}/implementations/{release}"
        return self._remove_release_graphs_sync(release_uri)
    
    def __str__(self) -> str:
        """Database status summary."""
        stats = self.get_database_stats()
        return (f"Oxigraph Database:\n"
                f"   Location: {stats.get('db_path', 'Unknown')}\n"
                f"   Graphs: {stats.get('total_graphs', 0)}\n"
                f"   Triples: {stats.get('total_triples', 0):,}\n"
                f"   Size: {stats.get('total_size_bytes', 0):,} bytes\n"
                f"   Status: {stats.get('status', '?')}")


# Singleton Pattern - Only One Database Connection
_oxigraph_instance: Optional[OxigraphClient] = None

def get_oxigraph_client(db_path: Path = None) -> OxigraphClient:
    """
    Get the singleton Oxigraph client.
    
    This ensures only one database connection is active at a time,
    preventing database lock conflicts.
    
    Args:
        db_path: Database path (only used for first initialization)
        
    Returns:
        OxigraphClient: The singleton database client
    """
    global _oxigraph_instance
    
    if _oxigraph_instance is None:
        logger.info("Creating Oxigraph database client")
        _oxigraph_instance = OxigraphClient(db_path=db_path)
    
    return _oxigraph_instance


def reset_oxigraph_client() -> None:
    """
    Reset the singleton client (for testing or recovery)
    
    Use this when the database client needs a fresh start.
    """
    global _oxigraph_instance
    logger.info("Resetting Oxigraph database client")
    _oxigraph_instance = None