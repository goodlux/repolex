"""
🟡 PAC-MAN's SPARQL Engine - Navigate the Semantic Maze! 🟡

The ultimate SPARQL query execution powerhouse!
PAC-MAN chomps through semantic graphs and delivers results!

WAKA WAKA! Let's query all the dots in the semantic maze!
"""

import asyncio
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import json
import re

from ..models.exceptions import SPARQLError, ValidationError, SecurityError
from ..models.results import QueryResult, QueryMetadata
from ..storage.oxigraph_client import OxigraphClient
from ..utils.validation import validate_sparql_query


class SPARQLEngine:
    """
    🟡 PAC-MAN's SPARQL Engine - The Ultimate Semantic Navigator! 🟡
    
    Executes SPARQL queries against the semantic maze with style!
    Features:
    - Security validation (no ghost attacks!)
    - Result formatting in multiple formats
    - Query optimization and caching
    - Performance monitoring
    - PAC-MAN themed error messages
    
    WAKA WAKA! Navigate through semantic data like a true PAC-MAN!
    """
    
    def __init__(self, oxigraph_client: OxigraphClient):
        self.oxigraph_client = oxigraph_client
        self.query_cache = {}  # Simple in-memory cache
        self.query_stats = {
            'total_queries': 0,
            'successful_queries': 0,
            'cached_hits': 0,
            'avg_execution_time': 0.0
        }
    
    async def execute_sparql(
        self,
        query: str,
        format: str = "table",
        limit: Optional[int] = None,
        timeout: float = 30.0,
        use_cache: bool = True
    ) -> QueryResult:
        """
        🟡 Execute SPARQL query with PAC-MAN power!
        
        Args:
            query: SPARQL query string
            format: Output format ('table', 'json', 'turtle', 'csv')
            limit: Maximum number of results (safety limit)
            timeout: Query timeout in seconds
            use_cache: Whether to use query cache
            
        Returns:
            QueryResult with formatted results and metadata
            
        Raises:
            SPARQLError: If query execution fails
            ValidationError: If query format is invalid
            SecurityError: If query contains dangerous operations
        """
        start_time = datetime.now()
        
        try:
            # Step 1: Validate and secure the query
            self._validate_query_security(query)
            
            # Step 2: Normalize query for caching
            normalized_query = self._normalize_query(query)
            cache_key = f"{normalized_query}|{format}|{limit}"
            
            # Step 3: Check cache first
            if use_cache and cache_key in self.query_cache:
                self.query_stats['cached_hits'] += 1
                cached_result = self.query_cache[cache_key]
                
                return QueryResult(
                    success=True,
                    results=cached_result['results'],
                    format=format,
                    query=query,
                    execution_time=0.001,  # Cached result
                    result_count=cached_result['count'],
                    from_cache=True,
                    metadata=QueryMetadata(
                        query_type=self._detect_query_type(query),
                        graphs_queried=self._extract_graphs_from_query(query),
                        execution_engine="PAC-MAN SPARQL Cache 🟡"
                    )
                )
            
            # Step 4: Execute query with timeout
            try:
                raw_results = await asyncio.wait_for(
                    self.oxigraph_client.query_sparql(query),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                raise SPARQLError(
                    f"🟡 PAC-MAN got stuck in the maze! Query timeout after {timeout}s",
                    suggestions=[
                        "Try a simpler query",
                        "Add LIMIT clause to reduce results",
                        "Use more specific filters"
                    ]
                )
            
            # Step 5: Apply limit if specified
            if limit and len(raw_results) > limit:
                raw_results = raw_results[:limit]
            
            # Step 6: Format results
            formatted_results = self._format_results(raw_results, format)
            
            # Step 7: Cache successful results
            if use_cache and len(raw_results) < 10000:  # Don't cache huge results
                self.query_cache[cache_key] = {
                    'results': formatted_results,
                    'count': len(raw_results),
                    'timestamp': datetime.now()
                }
                
                # Limit cache size
                if len(self.query_cache) > 100:
                    oldest_key = min(self.query_cache.keys(), 
                                   key=lambda k: self.query_cache[k]['timestamp'])
                    del self.query_cache[oldest_key]
            
            # Step 8: Update statistics
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            self.query_stats['total_queries'] += 1
            self.query_stats['successful_queries'] += 1
            
            # Update average execution time
            current_avg = self.query_stats['avg_execution_time']
            total_queries = self.query_stats['total_queries']
            self.query_stats['avg_execution_time'] = (
                (current_avg * (total_queries - 1) + execution_time) / total_queries
            )
            
            return QueryResult(
                success=True,
                results=formatted_results,
                format=format,
                query=query,
                execution_time=execution_time,
                result_count=len(raw_results),
                from_cache=False,
                metadata=QueryMetadata(
                    query_type=self._detect_query_type(query),
                    graphs_queried=self._extract_graphs_from_query(query),
                    execution_engine="PAC-MAN SPARQL Engine 🟡"
                )
            )
            
        except SPARQLError:
            raise
        except ValidationError:
            raise
        except SecurityError:
            raise
        except Exception as e:
            self.query_stats['total_queries'] += 1
            
            raise SPARQLError(
                f"🟡 PAC-MAN encountered a ghost in the query maze! {str(e)}",
                suggestions=[
                    "Check SPARQL syntax",
                    "Verify graph URIs exist",
                    "Try a simpler query first"
                ]
            )
    
    async def get_query_statistics(self) -> Dict[str, Any]:
        """📊 Get PAC-MAN's query statistics"""
        return {
            'total_queries': self.query_stats['total_queries'],
            'successful_queries': self.query_stats['successful_queries'],
            'success_rate': (
                self.query_stats['successful_queries'] / max(1, self.query_stats['total_queries'])
            ) * 100,
            'cached_hits': self.query_stats['cached_hits'],
            'cache_hit_rate': (
                self.query_stats['cached_hits'] / max(1, self.query_stats['total_queries'])
            ) * 100,
            'avg_execution_time': self.query_stats['avg_execution_time'],
            'cache_size': len(self.query_cache),
            'pac_man_status': "🟡 WAKA WAKA! Ready to chomp more queries!"
        }
    
    async def clear_cache(self) -> None:
        """🧹 Clear PAC-MAN's query cache"""
        self.query_cache.clear()
    
    def _validate_query_security(self, query: str) -> None:
        """🛡️ Validate query security (ghost detection!)"""
        
        # Basic SPARQL validation
        validate_sparql_query(query)
        
        # Additional security checks
        query_lower = query.lower()
        
        # Prevent dangerous operations
        dangerous_patterns = [
            r'insert\s+data',
            r'delete\s+data', 
            r'delete\s+where',
            r'drop\s+graph',
            r'clear\s+graph',
            r'load\s+<',
            r'service\s+<http[^>]*>',  # Prevent SPARQL federation attacks
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query_lower):
                raise SecurityError(
                    f"🟡 PAC-MAN detected a dangerous ghost! Query contains prohibited operation: {pattern}",
                    suggestions=[
                        "Use SELECT queries only",
                        "Remove INSERT/DELETE operations",
                        "Avoid SERVICE clauses"
                    ]
                )
        
        # Prevent extremely complex queries (performance protection)
        if query.count('UNION') > 10:
            raise ValidationError(
                "🟡 Too many UNION operations! PAC-MAN needs simpler paths through the maze.",
                suggestions=["Reduce UNION clauses", "Break into multiple queries"]
            )
        
        if query.count('OPTIONAL') > 20:
            raise ValidationError(
                "🟡 Too many OPTIONAL patterns! PAC-MAN is getting confused in the maze.",
                suggestions=["Reduce OPTIONAL clauses", "Make some patterns required"]
            )
    
    def _normalize_query(self, query: str) -> str:
        """🧹 Normalize query for caching"""
        # Remove extra whitespace and normalize formatting
        normalized = re.sub(r'\s+', ' ', query.strip())
        
        # Convert to uppercase for keywords (but preserve URIs and literals)
        # This is a simplified normalization - could be more sophisticated
        return normalized
    
    def _detect_query_type(self, query: str) -> str:
        """🔍 Detect the type of SPARQL query"""
        query_upper = query.upper().strip()
        
        if query_upper.startswith('SELECT'):
            return 'SELECT'
        elif query_upper.startswith('CONSTRUCT'):
            return 'CONSTRUCT'
        elif query_upper.startswith('ASK'):
            return 'ASK'
        elif query_upper.startswith('DESCRIBE'):
            return 'DESCRIBE'
        else:
            return 'UNKNOWN'
    
    def _extract_graphs_from_query(self, query: str) -> List[str]:
        """📊 Extract graph URIs mentioned in query"""
        # Simple regex to find GRAPH clauses
        graph_pattern = r'GRAPH\s+<([^>]+)>'
        matches = re.findall(graph_pattern, query, re.IGNORECASE)
        return list(set(matches))  # Remove duplicates
    
    def _format_results(self, raw_results: List[Dict[str, Any]], format: str) -> Any:
        """🎨 Format query results in the requested format"""
        
        if not raw_results:
            return self._format_empty_results(format)
        
        if format == 'json':
            return {
                'head': {'vars': list(raw_results[0].keys()) if raw_results else []},
                'results': {
                    'bindings': raw_results
                }
            }
        
        elif format == 'table':
            return self._format_as_table(raw_results)
        
        elif format == 'csv':
            return self._format_as_csv(raw_results)
        
        elif format == 'turtle':
            return self._format_as_turtle(raw_results)
        
        else:
            raise ValidationError(
                f"🟡 PAC-MAN doesn't know this format: {format}",
                suggestions=["Use: 'table', 'json', 'csv', or 'turtle'"]
            )
    
    def _format_empty_results(self, format: str) -> Any:
        """🚫 Format empty results"""
        if format == 'json':
            return {'head': {'vars': []}, 'results': {'bindings': []}}
        elif format == 'table':
            return "🟡 No dots found in this part of the maze! (0 results)"
        elif format == 'csv':
            return ""
        elif format == 'turtle':
            return "# No triples found"
        else:
            return []
    
    def _format_as_table(self, results: List[Dict[str, Any]]) -> str:
        """📊 Format results as ASCII table (PAC-MAN style!)"""
        if not results:
            return "🟡 No dots found in the maze!"
        
        # Get column headers
        headers = list(results[0].keys())
        
        # Calculate column widths
        col_widths = {}
        for header in headers:
            col_widths[header] = max(
                len(header),
                max(len(str(row.get(header, ''))) for row in results)
            )
        
        # Build table
        table_lines = []
        
        # Header row
        header_line = "🟡 " + " | ".join(
            header.ljust(col_widths[header]) for header in headers
        ) + " 🟡"
        table_lines.append(header_line)
        
        # Separator
        separator = "=" * len(header_line)
        table_lines.append(separator)
        
        # Data rows
        for row in results:
            data_line = "📍 " + " | ".join(
                str(row.get(header, '')).ljust(col_widths[header]) 
                for header in headers
            ) + " 📍"
            table_lines.append(data_line)
        
        # Footer
        table_lines.append(separator)
        table_lines.append(f"🟡 WAKA WAKA! Found {len(results)} semantic dots! 🟡")
        
        return "\n".join(table_lines)
    
    def _format_as_csv(self, results: List[Dict[str, Any]]) -> str:
        """📄 Format results as CSV"""
        if not results:
            return ""
        
        import csv
        import io
        
        output = io.StringIO()
        headers = list(results[0].keys())
        
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        
        for row in results:
            writer.writerow(row)
        
        return output.getvalue()
    
    def _format_as_turtle(self, results: List[Dict[str, Any]]) -> str:
        """🐢 Format results as Turtle RDF (when applicable)"""
        # This is a simplified turtle formatter
        # In practice, you'd want more sophisticated RDF serialization
        
        if not results:
            return "# No triples found"
        
        turtle_lines = [
            "# 🟡 PAC-MAN's Turtle Results 🟡",
            "# Generated by PAC-MAN SPARQL Engine",
            ""
        ]
        
        # Add prefixes if we can detect them
        prefixes = self._extract_prefixes_from_results(results)
        for prefix, uri in prefixes.items():
            turtle_lines.append(f"@prefix {prefix}: <{uri}> .")
        
        if prefixes:
            turtle_lines.append("")
        
        # Convert results to turtle format (simplified)
        for i, row in enumerate(results):
            turtle_lines.append(f"# Result {i + 1}")
            
            # Try to create RDF triples from the row
            if 'subject' in row and 'predicate' in row and 'object' in row:
                turtle_lines.append(f"{row['subject']} {row['predicate']} {row['object']} .")
            else:
                # Fallback: comment format
                turtle_lines.append("# " + " | ".join(f"{k}: {v}" for k, v in row.items()))
            
            turtle_lines.append("")
        
        turtle_lines.append("# 🟡 End of PAC-MAN results 🟡")
        
        return "\n".join(turtle_lines)
    
    def _extract_prefixes_from_results(self, results: List[Dict[str, Any]]) -> Dict[str, str]:
        """🔍 Extract common prefixes from result URIs"""
        prefixes = {}
        
        # Common prefixes
        common_prefixes = {
            'woc': 'http://rdf.webofcode.org/woc/',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'codedoc': 'http://codedoc.org/',
            'xsd': 'http://www.w3.org/2001/XMLSchema#'
        }
        
        # Check which prefixes are actually used in results
        all_values = []
        for row in results:
            all_values.extend(str(v) for v in row.values())
        
        result_text = " ".join(all_values)
        
        for prefix, uri in common_prefixes.items():
            if uri in result_text:
                prefixes[prefix] = uri
        
        return prefixes


class QueryOptimizer:
    """
    🟡 PAC-MAN's Query Optimizer - Make Queries Faster! 🟡
    
    Optimizes SPARQL queries for better performance in the semantic maze.
    """
    
    @staticmethod
    def optimize_query(query: str) -> str:
        """🚀 Optimize SPARQL query for better performance"""
        
        optimized = query
        
        # Add LIMIT if missing (prevent runaway queries)
        if 'LIMIT' not in optimized.upper() and 'SELECT' in optimized.upper():
            optimized += '\nLIMIT 1000'
        
        # Add optimization hints
        # This is where you'd add more sophisticated optimizations
        
        return optimized
    
    @staticmethod
    def estimate_query_complexity(query: str) -> Dict[str, Any]:
        """📊 Estimate query complexity"""
        
        complexity_score = 0
        factors = {}
        
        query_upper = query.upper()
        
        # Count various complexity factors
        factors['joins'] = query_upper.count('.')
        factors['unions'] = query_upper.count('UNION')
        factors['optionals'] = query_upper.count('OPTIONAL')
        factors['filters'] = query_upper.count('FILTER')
        factors['graphs'] = query_upper.count('GRAPH')
        
        # Calculate complexity score
        complexity_score = (
            factors['joins'] * 1 +
            factors['unions'] * 3 +
            factors['optionals'] * 2 +
            factors['filters'] * 1 +
            factors['graphs'] * 2
        )
        
        # Determine complexity level
        if complexity_score < 10:
            level = "🟡 Simple (PAC-MAN can handle this easily!)"
        elif complexity_score < 25:
            level = "🟠 Moderate (PAC-MAN needs to be careful)"
        elif complexity_score < 50:
            level = "🔴 Complex (PAC-MAN might get tired)"
        else:
            level = "👻 Very Complex (Ghost territory!)"
        
        return {
            'complexity_score': complexity_score,
            'complexity_level': level,
            'factors': factors,
            'estimated_execution_time': f"{complexity_score * 0.1:.1f}s",
            'pac_man_advice': QueryOptimizer._get_optimization_advice(factors)
        }
    
    @staticmethod
    def _get_optimization_advice(factors: Dict[str, int]) -> List[str]:
        """💡 Get optimization advice based on query factors"""
        advice = []
        
        if factors['unions'] > 5:
            advice.append("🟡 Consider breaking down UNION operations")
        
        if factors['optionals'] > 10:
            advice.append("🟡 Too many OPTIONAL patterns - make some required")
        
        if factors['joins'] > 20:
            advice.append("🟡 Simplify join patterns for better performance")
        
        if not advice:
            advice.append("🟡 Query looks good! PAC-MAN is ready to chomp!")
        
        return advice
