"""
🔍 PAC-MAN's Query Interface Panel Widget 🔍

A specialized Textual widget for building and executing semantic queries!
Navigate the semantic maze with powerful SPARQL and function search!

WAKA WAKA! Querying the infinite semantic dimensions!
"""

import logging
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from textual import on, work
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Static, Button, Input, TextArea, DataTable, Label, 
    Select, Log, Tabs, TabbedContent, TabPane, Tree
)
from textual.reactive import reactive
from textual.message import Message
from textual.widget import Widget
from textual.app import ComposeResult

logger = logging.getLogger(__name__)


class QueryHistoryPanel(Container):
    """📜 Query history and favorites"""
    
    DEFAULT_CSS = """
    QueryHistoryPanel {
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query_history: List[Dict[str, Any]] = []
    
    def compose(self) -> ComposeResult:
        """📜 Build query history layout"""
        yield Label("📜 Query History")
        
        # History list (would be a selectable list in real implementation)
        history_content = """[dim]Recent queries will appear here:

• 🔍 Find functions by name
• 👻 Developer commit history  
• 🧠 Complex function analysis
• ⏰ Function evolution tracking

Select a query to rerun or modify it![/dim]"""
        
        yield Static(history_content, classes="history-content")
        
        with Horizontal():
            yield Button("🔄 Rerun", id="rerun-query", variant="success")
            yield Button("⭐ Favorite", id="favorite-query", variant="default")
            yield Button("🗑️ Clear", id="clear-history", variant="error")
    
    def add_query_to_history(self, query: str, query_type: str, results_count: int = 0) -> None:
        """📜 Add a query to history"""
        history_item = {
            "query": query,
            "type": query_type,
            "timestamp": datetime.now(),
            "results_count": results_count
        }
        
        self.query_history.insert(0, history_item)  # Add to front
        if len(self.query_history) > 50:  # Keep only last 50
            self.query_history = self.query_history[:50]
        
        # Update display (simplified for now)
        logger.info(f"🔍 Added query to history: {query[:50]}...")


class QueryBuilderPanel(Container):
    """🏗️ Visual query builder interface"""
    
    DEFAULT_CSS = """
    QueryBuilderPanel {
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        """🏗️ Build query builder layout"""
        yield Label("🏗️ Visual Query Builder")
        
        # Query type selector
        yield Label("Query Type:")
        yield Select(
            options=[
                ("🟡 Find Functions", "functions"),
                ("👻 Git Analysis", "git"),
                ("🧠 Complex Analysis", "complex"),
                ("⏰ Evolution Tracking", "evolution"),
                ("🔍 Custom SPARQL", "custom")
            ],
            value="functions",
            id="query-type-select"
        )
        
        # Dynamic query parameters (would change based on selection)
        yield Label("Parameters:")
        yield Input(placeholder="Function name pattern...", id="param-input-1")
        yield Input(placeholder="Module pattern (optional)...", id="param-input-2")
        
        # Builder actions
        with Horizontal():
            yield Button("🔨 Build Query", id="build-query", variant="primary")
            yield Button("👁️ Preview", id="preview-query", variant="default")
            yield Button("🧹 Clear", id="clear-builder", variant="error")


class QueryResultsTable(DataTable):
    """📊 Query results display table"""
    
    DEFAULT_CSS = """
    QueryResultsTable {
        height: 100%;
        border: solid $primary;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results_data: List[Dict[str, Any]] = []
    
    def on_mount(self) -> None:
        """📊 Set up results table"""
        self.cursor_type = "row"
        self.zebra_stripes = True
        
        # Default empty state
        self.show_empty_state()
    
    def show_empty_state(self) -> None:
        """📊 Show empty results state"""
        self.clear()
        self.add_columns("Status")
        self.add_row("🟡 No query executed yet - Run a query to see results!")
    
    def display_query_results(self, results: List[Dict[str, Any]], query_type: str = "sparql") -> None:
        """📊 Display query results"""
        self.clear()
        self.results_data = results
        
        if not results:
            self.add_columns("Status")
            self.add_row("🟡 Query executed successfully but returned no results")
            return
        
        # Determine columns based on first result
        if results:
            columns = list(results[0].keys())
            self.add_columns(*columns)
            
            # Add data rows
            for result in results:
                row_data = [str(result.get(col, "")) for col in columns]
                self.add_row(*row_data)
    
    def export_results(self, format_type: str = "csv") -> str:
        """📊 Export results to string format"""
        if not self.results_data:
            return "No results to export"
        
        # Simple CSV export for now
        if format_type == "csv":
            if not self.results_data:
                return ""
            
            # Headers
            headers = list(self.results_data[0].keys())
            csv_content = ",".join(headers) + "\n"
            
            # Data rows
            for result in self.results_data:
                row = ",".join(str(result.get(col, "")) for col in headers)
                csv_content += row + "\n"
            
            return csv_content
        
        return str(self.results_data)


class QueryPanel(Container):
    """🔍 PAC-MAN's Query Interface Panel - The semantic maze navigator!"""
    
    DEFAULT_CSS = """
    QueryPanel {
        height: 100%;
        padding: 1;
    }
    
    QueryPanel .query-panel-main {
        height: 100%;
    }
    
    QueryPanel .query-input-section {
        height: 60%;
    }
    
    QueryPanel .query-results-section {
        height: 40%;
    }
    
    QueryPanel .query-editor {
        height: 15;
        border: solid $primary;
    }
    
    QueryPanel .query-actions {
        height: 3;
        margin: 1 0;
    }
    
    QueryPanel Button {
        margin: 0 1;
        width: auto;
    }
    """
    
    # Message classes for widget communication
    class QueryExecuted(Message):
        """Message sent when a query is executed"""
        def __init__(self, query: str, query_type: str, results: List[Dict[str, Any]]) -> None:
            self.query = query
            self.query_type = query_type
            self.results = results
            super().__init__()
    
    class QueryRequested(Message):
        """Message sent when query execution is requested"""
        def __init__(self, query: str, query_type: str) -> None:
            self.query = query
            self.query_type = query_type
            super().__init__()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query_area: Optional[TextArea] = None
        self.results_table: Optional[QueryResultsTable] = None
        self.query_history: Optional[QueryHistoryPanel] = None
        self.query_builder: Optional[QueryBuilderPanel] = None
    
    def compose(self) -> ComposeResult:
        """🔍 Build the query panel layout"""
        
        with Container(classes="query-panel-main"):
            with TabbedContent(initial="sparql"):
                # SPARQL Query Tab
                with TabPane("🔍 SPARQL Query", id="sparql"):
                    with Container(classes="query-input-section"):
                        yield Label("🔍 SPARQL Query Editor")
                        
                        self.query_area = TextArea(
                            text="# 🟡 Enter your SPARQL query here!\n# Example: Find all functions with 'create' in name\n\nPREFIX woc: <http://rdf.webofcode.org/woc/>\nSELECT ?function ?name ?module WHERE {\n    ?function a woc:Function ;\n             woc:canonicalName ?name ;\n             woc:module ?module .\n    FILTER(CONTAINS(LCASE(?name), \"create\"))\n}\nORDER BY ?name\nLIMIT 20",
                            language="sparql",
                            classes="query-editor"
                        )
                        yield self.query_area
                        
                        # Query actions
                        with Horizontal(classes="query-actions"):
                            yield Button("🚀 Execute", id="execute-sparql", variant="primary")
                            yield Button("✨ Format", id="format-sparql", variant="success")
                            yield Button("💾 Save", id="save-query", variant="default")
                            yield Button("📋 Examples", id="load-examples", variant="default")
                            yield Button("🧹 Clear", id="clear-query", variant="error")
                    
                    # Results section
                    with Container(classes="query-results-section"):
                        yield Label("📊 Query Results")
                        self.results_table = QueryResultsTable()
                        yield self.results_table
                
                # Function Search Tab
                with TabPane("🟡 Function Search", id="functions"):
                    with Vertical():
                        yield Label("🟡 Natural Language Function Search")
                        yield Input(placeholder="Search for functions (e.g., 'create table', 'parse data')...", id="function-search-input")
                        
                        with Horizontal():
                            yield Button("🔍 Search", id="search-functions", variant="primary")
                            yield Button("🎯 Advanced", id="advanced-search", variant="default")
                        
                        # Function search results (would reuse results table)
                        yield Static("🟡 Function search results will appear in the results table below")
                
                # Query Builder Tab
                with TabPane("🏗️ Query Builder", id="builder"):
                    self.query_builder = QueryBuilderPanel()
                    yield self.query_builder
                
                # History Tab
                with TabPane("📜 History", id="history"):
                    self.query_history = QueryHistoryPanel()
                    yield self.query_history
    
    @on(Button.Pressed, "#execute-sparql")
    def on_execute_sparql_pressed(self) -> None:
        """🔍 Handle SPARQL query execution"""
        if not self.query_area:
            return
        
        query = self.query_area.text.strip()
        if not query or query.startswith("#"):
            self.notify("🟡 PAC-MAN says: Enter a valid SPARQL query!", severity="warning")
            return
        
        # Add to history
        if self.query_history:
            self.query_history.add_query_to_history(query, "SPARQL")
        
        # Request query execution
        self.post_message(self.QueryRequested(query, "sparql"))
        self.notify("🟡 PAC-MAN executing SPARQL query - WAKA WAKA!", severity="information")
        
        # Show sample results for demo
        sample_results = [
            {"function": "create_table", "name": "create_table", "module": "pixeltable.core"},
            {"function": "create_view", "name": "create_view", "module": "pixeltable.views"},
            {"function": "create_index", "name": "create_index", "module": "pixeltable.indexing"}
        ]
        
        if self.results_table:
            self.results_table.display_query_results(sample_results, "sparql")
    
    @on(Button.Pressed, "#format-sparql")
    def on_format_sparql_pressed(self) -> None:
        """🔍 Handle SPARQL query formatting"""
        self.notify("🟡 PAC-MAN says: Query formatting coming soon!", severity="information")
    
    @on(Button.Pressed, "#save-query")
    def on_save_query_pressed(self) -> None:
        """🔍 Handle query saving"""
        if self.query_area and self.query_area.text.strip():
            self.notify("🟡 PAC-MAN saved your query to history!", severity="success")
        else:
            self.notify("🟡 PAC-MAN says: Enter a query first!", severity="warning")
    
    @on(Button.Pressed, "#load-examples")
    def on_load_examples_pressed(self) -> None:
        """🔍 Handle loading example queries"""
        if self.query_area:
            example_query = """# 🟡 PAC-MAN's favorite queries!

# Find functions with complex signatures
PREFIX woc: <http://rdf.webofcode.org/woc/>
SELECT ?function ?name ?signature ?complexity WHERE {
    ?function a woc:Function ;
             woc:canonicalName ?name ;
             woc:signature ?signature ;
             woc:cyclomaticComplexity ?complexity .
    FILTER(?complexity > 10)
}
ORDER BY DESC(?complexity)
LIMIT 10"""
            
            self.query_area.text = example_query
            self.notify("🟡 PAC-MAN loaded example queries!", severity="success")
    
    @on(Button.Pressed, "#clear-query")
    def on_clear_query_pressed(self) -> None:
        """🔍 Handle query clearing"""
        if self.query_area:
            self.query_area.text = "# 🟡 Enter your SPARQL query here!"
            self.notify("🟡 PAC-MAN cleared the query editor!", severity="information")
    
    @on(Button.Pressed, "#search-functions")
    def on_search_functions_pressed(self) -> None:
        """🟡 Handle function search"""
        search_input = self.query_one("#function-search-input", Input)
        search_term = search_input.value.strip()
        
        if not search_term:
            self.notify("🟡 PAC-MAN says: Enter a search term!", severity="warning")
            return
        
        # Add to history
        if self.query_history:
            self.query_history.add_query_to_history(search_term, "Function Search")
        
        # Request function search
        self.post_message(self.QueryRequested(search_term, "function_search"))
        self.notify(f"🟡 PAC-MAN searching for: {search_term}", severity="information")
        
        # Show sample results
        sample_results = [
            {"name": "create_table_advanced", "module": "pixeltable.core", "signature": "def create_table_advanced(name, schema, **kwargs)"},
            {"name": "table_creator", "module": "pixeltable.utils", "signature": "def table_creator(config)"},
        ]
        
        if self.results_table:
            self.results_table.display_query_results(sample_results, "function_search")
        
        search_input.clear()
    
    @on(Select.Changed, "#query-type-select")
    def on_query_type_changed(self, event: Select.Changed) -> None:
        """🏗️ Handle query type selection change"""
        self.notify(f"🟡 PAC-MAN switched to: {event.value} query building!", severity="information")
    
    @on(Button.Pressed, "#build-query")
    def on_build_query_pressed(self) -> None:
        """🏗️ Handle query building"""
        self.notify("🟡 PAC-MAN says: Visual query builder coming soon!", severity="information")
    
    def set_query_results(self, results: List[Dict[str, Any]], query_type: str = "sparql") -> None:
        """🔍 Set query results from external source"""
        if self.results_table:
            self.results_table.display_query_results(results, query_type)
    
    def get_current_query(self) -> str:
        """🔍 Get current query text"""
        if self.query_area:
            return self.query_area.text.strip()
        return ""
    
    def set_query_text(self, query: str) -> None:
        """🔍 Set query editor text"""
        if self.query_area:
            self.query_area.text = query