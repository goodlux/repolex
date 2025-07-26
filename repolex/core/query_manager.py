"""
Query Manager

Provides high-level query interface for semantic data retrieval.
Connects CLI commands to the underlying Oxigraph database.
"""

import logging
from typing import Optional, Any, Callable, List, Dict
from pathlib import Path
import json

from ..storage.oxigraph_client import get_oxigraph_client
from ..models.exceptions import RepolexError
from ..models.results import QueryResult, ResultStatus

logger = logging.getLogger(__name__)


class QueryManager:
    """Query management for semantic data retrieval."""
    
    def __init__(self, config_manager):
        """Initialize query manager."""
        self.config_manager = config_manager
        self.oxigraph_client = None
        logger.info("Query Manager initialized")
    
    def initialize(self):
        """Set up query systems."""
        self.oxigraph_client = get_oxigraph_client()
        logger.info("Query Manager ready")
    
    def query_sparql(self, query: str, format: str = "table", output_file: Optional[Path] = None) -> QueryResult:
        """Execute SPARQL query against the database."""
        if not self.oxigraph_client:
            raise RepolexError("Query manager not initialized")
            
        try:
            logger.info("Executing SPARQL query")
            oxigraph_result = self.oxigraph_client.query_sparql(query, "dict")
            
            # Format the output
            formatted_output = self._format_query_results(oxigraph_result.results, format)
            
            # Create QueryResult object
            result = QueryResult(
                status=ResultStatus.SUCCESS,
                message="Query executed successfully",
                query=query,
                query_type="sparql",
                results=oxigraph_result.results,
                result_count=len(oxigraph_result.results),
                query_time_seconds=oxigraph_result.execution_time_ms / 1000,
                formatted_output=formatted_output,
                output_format=format
            )
            
            if output_file:
                # Write results to file if specified
                self._write_results_to_file(oxigraph_result.results, output_file, format)
            
            return result
            
        except Exception as e:
            logger.error(f"SPARQL query failed: {e}")
            return QueryResult(
                status=ResultStatus.FAILED,
                message=f"Query execution failed: {e}",
                query=query,
                query_type="sparql",
                results=[],
                result_count=0,
                errors=[str(e)]
            )
    
    def search_functions(self, search_term: str, progress_callback: Optional[Callable] = None) -> QueryResult:
        """Search for functions matching the search term."""
        if not self.oxigraph_client:
            raise RepolexError("Query manager not initialized")
            
        try:
            logger.info(f"Searching for functions: {search_term}")
            
            # Build SPARQL query for function search
            sparql_query = f"""
            PREFIX woc: <http://rdf.webofcode.org/woc/>
            
            SELECT ?function ?name ?module ?signature WHERE {{
                ?function a woc:Function ;
                         woc:canonicalName ?name ;
                         woc:module ?module .
                OPTIONAL {{ ?function woc:signature ?signature }}
                
                FILTER(CONTAINS(LCASE(?name), LCASE("{search_term}")))
            }}
            ORDER BY ?name
            LIMIT 50
            """
            
            # Execute the query
            oxigraph_result = self.oxigraph_client.query_sparql(sparql_query)
            
            # Format the output
            formatted_output = self._format_query_results(oxigraph_result.results, "table")
            
            result = QueryResult(
                status=ResultStatus.SUCCESS,
                message=f"Found {len(oxigraph_result.results)} functions",
                query=sparql_query,
                query_type="function_search",
                results=oxigraph_result.results,
                result_count=len(oxigraph_result.results),
                query_time_seconds=oxigraph_result.execution_time_ms / 1000,
                formatted_output=formatted_output,
                output_format="table"
            )
            
            logger.info(f"Found {len(oxigraph_result.results)} functions")
            return result
            
        except Exception as e:
            logger.error(f"Function search failed: {e}")
            return QueryResult(
                status=ResultStatus.FAILED,
                message=f"Function search failed: {e}",
                query="",
                query_type="function_search",
                results=[],
                result_count=0,
                errors=[str(e)]
            )
    
    def _format_query_results(self, results: List[Dict], format: str) -> str:
        """Format query results for display."""
        if not results:
            return "No results found"
            
        if format.lower() == "json":
            return json.dumps(results, indent=2)
        elif format.lower() == "table":
            return self._format_as_table(results)
        else:
            # Default to table format
            return self._format_as_table(results)
    
    def _format_as_table(self, results: List[Dict]) -> str:
        """Format results as a simple text table."""
        if not results:
            return "No results found"
            
        # Get all unique keys from all results
        all_keys = set()
        for result in results:
            all_keys.update(result.keys())
        
        if not all_keys:
            return "No data to display"
            
        keys = sorted(list(all_keys))
        
        # Calculate column widths
        col_widths = {}
        for key in keys:
            col_widths[key] = max(len(key), max(len(str(result.get(key, ""))) for result in results))
        
        # Build table
        lines = []
        
        # Header
        header_line = " | ".join(key.ljust(col_widths[key]) for key in keys)
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Rows
        for result in results:
            row_line = " | ".join(str(result.get(key, "")).ljust(col_widths[key]) for key in keys)
            lines.append(row_line)
        
        return "\n".join(lines)
    
    def _write_results_to_file(self, results: List[Dict], output_file: Path, format: str) -> None:
        """Write query results to file."""
        try:
            import json
            import csv
            
            if format.lower() == "json":
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
            elif format.lower() == "csv":
                if results:
                    with open(output_file, 'w', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=results[0].keys())
                        writer.writeheader()
                        writer.writerows(results)
            else:
                # Default to JSON
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
                    
            logger.info(f"Results written to {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to write results to file: {e}")
    
    def cleanup(self):
        """Clean up query resources."""
        logger.info("Query Manager cleanup complete")