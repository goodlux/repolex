"""
🟡 Oxigraph Client - PAC-MAN's semantic database chomper!

WAKA WAKA WAKA! This is PAC-MAN's interface to the Oxigraph maze!
Every graph is a level, every triple is a dot to chomp!

The Oxigraph client provides:
- Fast graph insertion (PAC-MAN eating dots)
- Nuclear graph removal (power pellets clearing ghosts)
- SPARQL queries (PAC-MAN's navigation system)
- Graph listing (viewing the maze levels)
- Connection management (staying alive in the maze)

🌟 "In the game of semantic intelligence, you either chomp or get chomped!" 🟡
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Generator
from dataclasses import dataclass
import pyoxigraph as ox
from pyoxigraph import Store, NamedNode, Triple, Quad, QuerySolutions

from ..models.exceptions import StorageError, ValidationError, CodeDocError
from ..models.graph import GraphInfo, GraphStatistics
from ..utils.validation import validate_graph_uri, validate_sparql_query

logger = logging.getLogger(__name__)

@dataclass
class GraphInsertResult:
    """
    🟡 Result of PAC-MAN chomping through graph insertion!
    
    Like PAC-MAN's score after eating all the dots in a level.
    """
    graph_uri: str
    triples_inserted: int  
    processing_time_ms: float
    success: bool
    ghost_errors: Optional[List[str]] = None  # Any ghosts (errors) encountered

    def __str__(self) -> str:
        if self.success:
            return f"🟡 WAKA! Chomped {self.triples_inserted} triples in {self.processing_time_ms:.1f}ms"
        else:
            return f"👻 GHOST! Failed to chomp graph: {self.ghost_errors}"

@dataclass  
class QueryResult:
    """
    🟡 SPARQL query results - PAC-MAN's maze navigation report!
    
    Contains the treasures PAC-MAN found while navigating the semantic maze.
    """
    results: List[Dict[str, Any]]
    execution_time_ms: float
    result_count: int
    query_hash: str  # For caching
    success: bool
    ghost_errors: Optional[List[str]] = None

    def __str__(self) -> str:
        if self.success:
            return f"🟡 WAKA! Found {self.result_count} semantic dots in {self.execution_time_ms:.1f}ms"
        else:
            return f"👻 GHOST! Query failed: {self.ghost_errors}"

class OxigraphClient:
    """
    🟡 PAC-MAN's Oxigraph Client - The Semantic Maze Master!
    
    WAKA WAKA WAKA! This is PAC-MAN's interface to the semantic maze.
    Every operation is like PAC-MAN navigating through levels, eating dots,
    and avoiding ghosts (errors)!
    
    The client manages:
    - 19 graphs per repository (19 maze levels!)
    - Triples as dots to chomp
    - Named graphs as maze levels
    - SPARQL queries as navigation commands
    - Nuclear updates as power pellets
    
    🌟 "Game Over? Never! PAC-MAN always finds another quarter!" 🟡
    """
    
    def __init__(self, 
                 db_path: Optional[Path] = None,
                 max_connections: int = 10,
                 query_timeout_ms: int = 30000):
        """
        🟡 Initialize PAC-MAN's semantic maze!
        
        Args:
            db_path: Path to the Oxigraph maze (defaults to ~/.codedoc/graph)
            max_connections: Maximum concurrent PAC-MANs in the maze
            query_timeout_ms: How long PAC-MAN waits before giving up
        """
        self.db_path = db_path or Path.home() / ".codedoc" / "oxigraph"
        self.max_connections = max_connections
        self.query_timeout_ms = query_timeout_ms
        
        # Ensure the maze directory exists
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize the Oxigraph store (the maze itself!)
        try:
            self._store = Store(str(self.db_path))
            logger.info(f"🟡 WAKA! PAC-MAN entered the semantic maze at {self.db_path}")
        except Exception as e:
            raise StorageError(
                f"👻 GHOST! Failed to initialize Oxigraph maze: {e}",
                suggestions=[
                    "🟡 Check if directory is writable",
                    "🟡 Ensure sufficient disk space",
                    "🟡 Try removing corrupted database files"
                ]
            )
    
    @property
    def store(self) -> Store:
        """🟡 Access to the raw Oxigraph maze - handle with care!"""
        return self._store
    
    def chomp_triples(self, 
                     graph_uri: str, 
                     triples: List[Triple],
                     batch_size: int = 1000) -> GraphInsertResult:
        """
        🟡 PAC-MAN chomps through triples like eating dots!
        
        WAKA WAKA WAKA! Insert triples into a named graph with the
        efficiency of PAC-MAN clearing a maze level!
        
        Args:
            graph_uri: The maze level (named graph) to chomp in
            triples: List of semantic dots (triples) to eat
            batch_size: How many dots PAC-MAN eats at once
            
        Returns:
            GraphInsertResult: PAC-MAN's chomping report
            
        Raises:
            StorageError: When ghosts (errors) block PAC-MAN's path
        """
        import time
        start_time = time.perf_counter()
        
        try:
            # Validate the maze level URI
            validate_graph_uri(graph_uri)
            
            if not triples:
                logger.warning(f"🟡 WAKA? No dots to chomp in {graph_uri}")
                return GraphInsertResult(
                    graph_uri=graph_uri,
                    triples_inserted=0,
                    processing_time_ms=0.0,
                    success=True
                )
            
            # Convert graph URI to NamedNode
            graph_node = NamedNode(graph_uri)
            chomped_count = 0
            ghost_errors = []
            
            # Batch chomp for efficiency (PAC-MAN power pellet mode!)
            for i in range(0, len(triples), batch_size):
                batch = triples[i:i + batch_size]
                
                try:
                    # Create quads (triples + graph)
                    quads = [Quad(triple.subject, triple.predicate, triple.object, graph_node) 
                            for triple in batch]
                    
                    # CHOMP! Insert the batch
                    for quad in quads:
                        self._store.add(quad)
                    
                    chomped_count += len(batch)
                    
                    # Progress log for large datasets
                    if i > 0 and i % (batch_size * 10) == 0:
                        logger.info(f"🟡 WAKA! Chomped {chomped_count}/{len(triples)} dots in {graph_uri}")
                
                except Exception as e:
                    ghost_error = f"👻 Batch {i}-{i+len(batch)}: {str(e)}"
                    ghost_errors.append(ghost_error)
                    logger.warning(ghost_error)
            
            end_time = time.perf_counter()
            processing_time_ms = (end_time - start_time) * 1000
            
            success = len(ghost_errors) == 0
            result = GraphInsertResult(
                graph_uri=graph_uri,
                triples_inserted=chomped_count,
                processing_time_ms=processing_time_ms,
                success=success,
                ghost_errors=ghost_errors if ghost_errors else None
            )
            
            if success:
                logger.info(f"🟡 WAKA! {result}")
            else:
                logger.error(f"👻 GHOST! {result}")
            
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            processing_time_ms = (end_time - start_time) * 1000
            
            raise StorageError(
                f"👻 GHOST! PAC-MAN couldn't chomp triples in {graph_uri}: {e}",
                suggestions=[
                    "🟡 Check if graph URI is valid",
                    "🟡 Ensure database is not corrupted",
                    "🟡 Try smaller batch sizes",
                    f"🟡 Failed after {processing_time_ms:.1f}ms"
                ]
            )
    
    def power_pellet_clear_graph(self, graph_uri: str) -> bool:
        """
        🟡 PAC-MAN's power pellet! Clear entire graph like eating a power pellet!
        
        WAKA WAKA WAKA! This is PAC-MAN's nuclear option - clear an entire
        maze level (named graph) in one chomp! Perfect for nuclear updates
        where we need to rebuild a graph completely.
        
        Args:
            graph_uri: The maze level to completely clear
            
        Returns:
            bool: True if successfully cleared, False if graph didn't exist
            
        Raises:
            StorageError: When ghosts block the power pellet effect
        """
        try:
            validate_graph_uri(graph_uri)
            
            # Check if graph exists first
            if not self.maze_has_level(graph_uri):
                logger.warning(f"🟡 WAKA? Maze level {graph_uri} doesn't exist - nothing to clear")
                return False
            
            # Get triple count before clearing (for logging)
            count_before = self.count_dots_in_level(graph_uri)
            
            # POWER PELLET ACTIVATED! Clear the entire graph
            graph_node = NamedNode(graph_uri)
            
            # Remove all quads in this graph
            self._store.remove_graph(graph_node)
            
            logger.info(f"🟡 POWER PELLET! Cleared {count_before} dots from maze level {graph_uri}")
            return True
            
        except Exception as e:
            raise StorageError(
                f"👻 GHOST! Power pellet failed to clear {graph_uri}: {e}",
                suggestions=[
                    "🟡 Check if graph URI is valid", 
                    "🟡 Ensure database is not locked",
                    "🟡 Try restarting PAC-MAN (the client)"
                ]
            )
    
    def navigate_maze(self, 
                     sparql_query: str,
                     result_format: str = "dict") -> QueryResult:
        """
        🟡 PAC-MAN navigates the semantic maze with SPARQL!
        
        WAKA WAKA WAKA! PAC-MAN uses his advanced AI to navigate
        through the semantic maze and find the treasures (query results)!
        
        Args:
            sparql_query: Navigation instructions (SPARQL query)
            result_format: How to format treasures found ("dict", "json", "turtle")
            
        Returns:
            QueryResult: PAC-MAN's navigation report with treasures found
            
        Raises:
            StorageError: When ghosts block PAC-MAN's navigation
        """
        import time
        import hashlib
        
        start_time = time.perf_counter()
        
        try:
            # Security check - no ghost queries allowed!
            validate_sparql_query(sparql_query)
            
            # Create query hash for caching
            query_hash = hashlib.md5(sparql_query.encode()).hexdigest()[:8]
            
            logger.debug(f"🟡 WAKA! PAC-MAN navigating maze with query {query_hash}")
            
            # Execute the navigation command
            query_results = self._store.query(sparql_query)
            
            # Process results based on format
            processed_results = self._process_navigation_results(query_results, result_format)
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            result = QueryResult(
                results=processed_results,
                execution_time_ms=execution_time_ms,
                result_count=len(processed_results),
                query_hash=query_hash,
                success=True
            )
            
            logger.info(f"🟡 WAKA! {result}")
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            ghost_error = f"👻 Navigation failed: {str(e)}"
            
            result = QueryResult(
                results=[],
                execution_time_ms=execution_time_ms,
                result_count=0,
                query_hash="error",
                success=False,
                ghost_errors=[ghost_error]
            )
            
            logger.error(f"👻 GHOST! {result}")
            
            raise StorageError(
                f"👻 GHOST! PAC-MAN's navigation failed: {e}",
                suggestions=[
                    "🟡 Check SPARQL query syntax",
                    "🟡 Ensure referenced graphs exist",
                    "🟡 Try simpler query to test connection",
                    f"🟡 Query failed after {execution_time_ms:.1f}ms"
                ]
            )
    
    def _process_navigation_results(self, 
                                  query_results: QuerySolutions, 
                                  result_format: str) -> List[Dict[str, Any]]:
        """
        🟡 Process PAC-MAN's navigation results into treasure format!
        
        Internal method to convert Oxigraph query results into
        the format that makes PAC-MAN happy!
        """
        processed = []
        
        try:
            for solution in query_results:
                result_dict = {}
                for variable, term in solution:
                    variable_name = str(variable)
                    
                    # Convert RDF terms to PAC-MAN friendly format
                    if hasattr(term, 'value'):
                        # Literal value
                        result_dict[variable_name] = term.value
                    else:
                        # URI or other term
                        result_dict[variable_name] = str(term)
                
                processed.append(result_dict)
                
        except Exception as e:
            logger.warning(f"🟡 WAKA? Error processing result: {e}")
        
        return processed
    
    def explore_maze_levels(self, filter_prefix: Optional[str] = None) -> List[GraphInfo]:
        """
        🟡 PAC-MAN explores all available maze levels!
        
        WAKA WAKA WAKA! Get a list of all the maze levels (named graphs)
        that PAC-MAN can explore, with statistics about each level.
        
        Args:
            filter_prefix: Only show levels starting with this prefix
            
        Returns:
            List[GraphInfo]: Information about each maze level
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
            
            result = self.navigate_maze(graph_query)
            
            for row in result.results:
                graph_uri = row.get('graph', '')
                
                # Apply filter if provided
                if filter_prefix and not graph_uri.startswith(filter_prefix):
                    continue
                
                # Get statistics for this graph
                stats = self.analyze_maze_level(graph_uri)
                
                graph_info = GraphInfo(
                    uri=graph_uri,
                    triple_count=stats.triple_count,
                    last_modified=stats.last_modified,
                    size_bytes=stats.size_bytes,
                    graph_type=self._classify_graph_type(graph_uri)
                )
                
                all_graphs.append(graph_info)
            
            logger.info(f"🟡 WAKA! Explored {len(all_graphs)} maze levels")
            return all_graphs
            
        except Exception as e:
            raise StorageError(
                f"👻 GHOST! Couldn't explore maze levels: {e}",
                suggestions=[
                    "🟡 Check database connection",
                    "🟡 Ensure graphs exist",
                    "🟡 Try without filter first"
                ]
            )
    
    def analyze_maze_level(self, graph_uri: str) -> GraphStatistics:
        """
        🟡 PAC-MAN analyzes a specific maze level for treasures and ghosts!
        
        Get detailed statistics about a specific graph, like PAC-MAN
        analyzing a level before playing it.
        
        Args:
            graph_uri: The maze level to analyze
            
        Returns:
            GraphStatistics: Detailed analysis of the maze level
        """
        try:
            validate_graph_uri(graph_uri)
            
            # Count dots (triples) in this level
            triple_count = self.count_dots_in_level(graph_uri)
            
            # Get unique subjects (entities)
            subject_query = f"""
            SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {{
                GRAPH <{graph_uri}> {{ ?s ?p ?o }}
            }}
            """
            subject_result = self.navigate_maze(subject_query)
            subject_count = int(subject_result.results[0].get('count', 0))
            
            # Get unique predicates (relationships)
            predicate_query = f"""
            SELECT (COUNT(DISTINCT ?p) AS ?count) WHERE {{
                GRAPH <{graph_uri}> {{ ?s ?p ?o }}
            }}
            """
            predicate_result = self.navigate_maze(predicate_query)
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
                ghost_count=0  # No ghosts in healthy graphs!
            )
            
        except Exception as e:
            raise StorageError(
                f"👻 GHOST! Couldn't analyze maze level {graph_uri}: {e}",
                suggestions=[
                    "🟡 Check if graph exists",
                    "🟡 Ensure valid graph URI",
                    "🟡 Try simpler analysis query"
                ]
            )
    
    def count_dots_in_level(self, graph_uri: str) -> int:
        """
        🟡 Count the dots (triples) in a maze level!
        
        Quick method to count how many semantic dots PAC-MAN
        can chomp in a specific graph.
        """
        try:
            count_query = f"""
            SELECT (COUNT(*) AS ?count) WHERE {{
                GRAPH <{graph_uri}> {{ ?s ?p ?o }}
            }}
            """
            
            result = self.navigate_maze(count_query)
            return int(result.results[0].get('count', 0))
            
        except Exception:
            return 0  # Return 0 if count fails
    
    def maze_has_level(self, graph_uri: str) -> bool:
        """
        🟡 Check if PAC-MAN's maze has a specific level!
        
        Quick check if a named graph exists in the database.
        """
        try:
            return self.count_dots_in_level(graph_uri) > 0
        except Exception:
            return False
    
    def _classify_graph_type(self, graph_uri: str) -> str:
        """
        🟡 Classify what type of maze level this is!
        
        Based on the URI pattern, determine if this is an ontology graph,
        function graph, git intelligence graph, etc.
        """
        if "/ontology/" in graph_uri:
            return "ontology"
        elif "/functions/" in graph_uri:
            return "functions"
        elif "/git/" in graph_uri:
            return "git_intelligence"
        elif "/abc/" in graph_uri:
            return "abc_events"
        elif "/evolution/" in graph_uri:
            return "evolution"
        elif "/files/" in graph_uri:
            return "file_structure"
        elif "/meta/" in graph_uri:
            return "metadata"
        else:
            return "unknown"
    
    def get_maze_stats(self) -> Dict[str, Any]:
        """
        🟡 Get overall statistics about PAC-MAN's entire semantic maze!
        
        Returns comprehensive statistics about the whole database,
        like PAC-MAN's high score and game statistics.
        """
        try:
            graphs = self.explore_maze_levels()
            
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
                "pac_man_status": "🟡 WAKA WAKA WAKA!"
            }
            
        except Exception as e:
            logger.error(f"👻 GHOST! Couldn't get maze stats: {e}")
            return {
                "error": str(e),
                "pac_man_status": "👻 GHOST DETECTED!"
            }
    
    def backup_maze(self, backup_path: Path) -> bool:
        """
        🟡 PAC-MAN backs up his precious semantic maze!
        
        Create a backup of the entire Oxigraph database so PAC-MAN
        never loses his high scores and semantic treasures.
        """
        try:
            import shutil
            
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Simple file copy backup
            if self.db_path.is_file():
                shutil.copy2(self.db_path, backup_path)
            else:
                shutil.copytree(self.db_path, backup_path, dirs_exist_ok=True)
            
            logger.info(f"🟡 WAKA! Maze backed up to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"👻 GHOST! Backup failed: {e}")
            return False
    
    def __enter__(self):
        """🟡 PAC-MAN enters the maze! (Context manager support)"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """🟡 PAC-MAN exits the maze safely!"""
        # Oxigraph handles cleanup automatically
        if exc_type:
            logger.error(f"👻 GHOST! PAC-MAN encountered error: {exc_val}")
        else:
            logger.info("🟡 WAKA! PAC-MAN exited maze safely")
    
    def __str__(self) -> str:
        """🟡 PAC-MAN's status report!"""
        stats = self.get_maze_stats()
        return (f"🟡 PAC-MAN's Semantic Maze:\n"
                f"   📍 Location: {stats.get('db_path', 'Unknown')}\n"
                f"   🎮 Levels: {stats.get('total_graphs', 0)} graphs\n"
                f"   🔸 Dots: {stats.get('total_triples', 0):,} triples\n"
                f"   📊 Size: {stats.get('total_size_bytes', 0):,} bytes\n"
                f"   🌟 Status: {stats.get('pac_man_status', '❓')}")
