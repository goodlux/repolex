"""
🧠 PAC-MAN's Graph Statistics Viewer Widget 🧠

A specialized Textual widget for visualizing semantic graph statistics!
See PAC-MAN's maze intelligence in beautiful charts and data!

WAKA WAKA! Exploring the semantic maze statistics!
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from textual import on, work
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import (
    Static, Button, DataTable, Label, ProgressBar, 
    Select, Sparkline, Tabs, TabbedContent, TabPane, Tree
)
from textual.reactive import reactive
from textual.message import Message
from textual.widget import Widget
from textual.app import ComposeResult

logger = logging.getLogger(__name__)


class GraphStatsCard(Static):
    """📊 Individual graph statistics card"""
    
    DEFAULT_CSS = """
    GraphStatsCard {
        border: solid $primary;
        padding: 1;
        margin: 1;
        height: 8;
        min-width: 20;
    }
    
    GraphStatsCard.highlight {
        border: solid $accent;
        background: $boost;
    }
    """
    
    def __init__(self, title: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.stats_data = {}
    
    def update_stats(self, stats: Dict[str, Any]) -> None:
        """📊 Update card statistics"""
        self.stats_data = stats
        
        # Format the statistics display
        content = f"[bold]{self.title}[/bold]\n\n"
        
        if not stats:
            content += "[dim]No data available[/dim]"
        else:
            # Display key statistics
            content += f"🔢 Triples: {stats.get('triple_count', 0):,}\n"
            content += f"🎯 Entities: {stats.get('entity_count', 0):,}\n"
            content += f"📅 Updated: {stats.get('last_updated', 'Never')}\n"
            content += f"💾 Size: {stats.get('size_mb', 0):.1f} MB"
        
        self.update(content)
    
    def highlight(self, enabled: bool = True) -> None:
        """📊 Highlight or unhighlight the card"""
        if enabled:
            self.add_class("highlight")
        else:
            self.remove_class("highlight")


class GraphTypeOverview(Container):
    """🧠 Overview of all graph types in the semantic maze"""
    
    DEFAULT_CSS = """
    GraphTypeOverview {
        height: auto;
        padding: 1;
    }
    
    GraphTypeOverview .graph-grid {
        height: auto;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph_cards: Dict[str, GraphStatsCard] = {}
    
    def compose(self) -> ComposeResult:
        """🧠 Build graph type overview layout"""
        
        yield Label("🧠 Semantic Graph Collection")
        
        with Grid(classes="graph-grid"):
            # Ontology graphs
            self.graph_cards["ontology_woc"] = GraphStatsCard("🔬 WoC Ontology")
            yield self.graph_cards["ontology_woc"]
            
            self.graph_cards["ontology_git"] = GraphStatsCard("🔄 Git Ontology")
            yield self.graph_cards["ontology_git"]
            
            self.graph_cards["ontology_evolution"] = GraphStatsCard("📈 Evolution Ontology")
            yield self.graph_cards["ontology_evolution"]
            
            # Function graphs
            self.graph_cards["functions_stable"] = GraphStatsCard("🟡 Stable Functions")
            yield self.graph_cards["functions_stable"]
            
            self.graph_cards["functions_impl"] = GraphStatsCard("🔧 Function Implementations")
            yield self.graph_cards["functions_impl"]
            
            # Git intelligence graphs
            self.graph_cards["git_commits"] = GraphStatsCard("👻 Git Commits")
            yield self.graph_cards["git_commits"]
            
            self.graph_cards["git_developers"] = GraphStatsCard("👥 Developers")
            yield self.graph_cards["git_developers"]
            
            # ABC events
            self.graph_cards["abc_events"] = GraphStatsCard("⏰ ABC Events")
            yield self.graph_cards["abc_events"]
    
    def update_graph_stats(self, graph_stats: Dict[str, Dict[str, Any]]) -> None:
        """🧠 Update all graph statistics"""
        for graph_type, stats in graph_stats.items():
            if graph_type in self.graph_cards:
                self.graph_cards[graph_type].update_stats(stats)
    
    def highlight_graph(self, graph_type: str) -> None:
        """🧠 Highlight a specific graph type"""
        # Unhighlight all first
        for card in self.graph_cards.values():
            card.highlight(False)
        
        # Highlight selected
        if graph_type in self.graph_cards:
            self.graph_cards[graph_type].highlight(True)


class GraphActivityChart(Container):
    """📈 Graph activity visualization"""
    
    DEFAULT_CSS = """
    GraphActivityChart {
        border: solid $primary;
        padding: 1;
        height: 12;
        margin: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        """📈 Build activity chart"""
        yield Label("📈 Graph Activity Over Time")
        yield Sparkline(
            data=[10, 15, 20, 18, 25, 30, 28, 35, 40, 38, 45, 50],
            summary_function=max,
            name="graph_activity"
        )
        yield Static("[dim]📊 Showing processing activity for the last 12 periods[/dim]")


class GraphDetailTable(DataTable):
    """📋 Detailed graph information table"""
    
    DEFAULT_CSS = """
    GraphDetailTable {
        height: 100%;
        border: solid $primary;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph_details: List[Dict[str, Any]] = []
    
    def on_mount(self) -> None:
        """📋 Set up table columns"""
        self.add_columns(
            "Graph", "Type", "Triples", "Entities", "Size (MB)", "Status", "Updated"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
        
        # Load sample data
        self.load_sample_data()
    
    def load_sample_data(self) -> None:
        """📋 Load sample graph data"""
        sample_graphs = [
            {
                "name": "🟡 No graphs available",
                "type": "None",
                "triple_count": 0,
                "entity_count": 0,
                "size_mb": 0.0,
                "status": "Empty",
                "last_updated": "Never"
            }
        ]
        
        for graph in sample_graphs:
            self.add_row(
                graph["name"],
                graph["type"],
                str(graph["triple_count"]),
                str(graph["entity_count"]),
                f"{graph['size_mb']:.1f}",
                graph["status"],
                graph["last_updated"]
            )
        
        self.graph_details = sample_graphs
    
    def refresh_graph_data(self, graph_data: List[Dict[str, Any]]) -> None:
        """📋 Refresh graph table data"""
        self.clear()
        self.graph_details = graph_data
        
        if not graph_data:
            self.add_row("🟡 No graphs found", "Empty", "0", "0", "0.0", "Empty", "Never")
            return
        
        for graph in graph_data:
            status_icon = "✅" if graph.get("status") == "Ready" else "⏳" if graph.get("status") == "Processing" else "❌"
            
            self.add_row(
                f"{status_icon} {graph.get('name', 'Unknown')}",
                graph.get("type", "Unknown"),
                str(graph.get("triple_count", 0)),
                str(graph.get("entity_count", 0)),
                f"{graph.get('size_mb', 0):.1f}",
                graph.get("status", "Unknown"),
                graph.get("last_updated", "Never")
            )


class GraphActionPanel(Container):
    """⚡ Graph management actions"""
    
    DEFAULT_CSS = """
    GraphActionPanel {
        height: auto;
        margin: 1;
    }
    
    GraphActionPanel Button {
        margin: 0 1;
        width: auto;
    }
    """
    
    def compose(self) -> ComposeResult:
        """⚡ Build action buttons"""
        with Horizontal():
            yield Button("🧠 Process Graphs", id="process-graphs", variant="primary")
            yield Button("🔄 Refresh Stats", id="refresh-stats", variant="success")
            yield Button("🔍 Query Graph", id="query-graph", variant="default")
            yield Button("📤 Export Graph", id="export-graph", variant="default")
            yield Button("🗑️ Remove Graph", id="remove-graph", variant="error")


class GraphViewer(Container):
    """🧠 PAC-MAN's Graph Statistics Viewer - The semantic maze observatory!"""
    
    DEFAULT_CSS = """
    GraphViewer {
        height: 100%;
        padding: 1;
    }
    
    GraphViewer .graph-viewer-main {
        height: 100%;
    }
    
    GraphViewer .graph-overview-section {
        height: 50%;
    }
    
    GraphViewer .graph-details-section {
        height: 50%;
    }
    """
    
    # Message classes for widget communication
    class GraphSelected(Message):
        """Message sent when a graph is selected"""
        def __init__(self, graph_data: Dict[str, Any]) -> None:
            self.graph_data = graph_data
            super().__init__()
    
    class GraphActionRequested(Message):
        """Message sent when a graph action is requested"""
        def __init__(self, action: str, graph_data: Optional[Dict[str, Any]] = None) -> None:
            self.action = action
            self.graph_data = graph_data
            super().__init__()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph_overview: Optional[GraphTypeOverview] = None
        self.graph_table: Optional[GraphDetailTable] = None
        self.activity_chart: Optional[GraphActivityChart] = None
    
    def compose(self) -> ComposeResult:
        """🧠 Build the graph viewer layout"""
        
        with Container(classes="graph-viewer-main"):
            # Top section: Overview and activity
            with Container(classes="graph-overview-section"):
                with Horizontal():
                    # Left: Graph type overview
                    with Vertical():
                        self.graph_overview = GraphTypeOverview()
                        yield self.graph_overview
                    
                    # Right: Activity chart
                    with Vertical():
                        self.activity_chart = GraphActivityChart()
                        yield self.activity_chart
            
            # Bottom section: Detailed table and actions
            with Container(classes="graph-details-section"):
                yield Label("📋 Graph Details")
                self.graph_table = GraphDetailTable()
                yield self.graph_table
                yield GraphActionPanel()
    
    @on(DataTable.RowSelected, "GraphDetailTable")
    def on_graph_selected(self, event: DataTable.RowSelected) -> None:
        """🧠 Handle graph selection"""
        if self.graph_table and self.graph_table.cursor_row < len(self.graph_table.graph_details):
            selected_graph = self.graph_table.graph_details[self.graph_table.cursor_row]
            
            # Highlight in overview
            if self.graph_overview:
                graph_type = selected_graph.get("type", "").lower().replace(" ", "_")
                self.graph_overview.highlight_graph(graph_type)
            
            # Send message to parent
            self.post_message(self.GraphSelected(selected_graph))
    
    @on(Button.Pressed, "#process-graphs")
    def on_process_graphs_pressed(self) -> None:
        """🧠 Handle process graphs action"""
        self.post_message(self.GraphActionRequested("process"))
        self.notify("🟡 PAC-MAN says: Graph processing will be implemented soon!", severity="information")
    
    @on(Button.Pressed, "#refresh-stats")
    def on_refresh_stats_pressed(self) -> None:
        """🧠 Handle refresh statistics action"""
        self.post_message(self.GraphActionRequested("refresh"))
        self.notify("🟡 PAC-MAN refreshing graph statistics - WAKA WAKA!", severity="information")
        
        # Simulate refresh by updating sample data
        self.refresh_sample_data()
    
    @on(Button.Pressed, "#query-graph")
    def on_query_graph_pressed(self) -> None:
        """🧠 Handle query graph action"""
        selected_graph = None
        if self.graph_table and self.graph_table.cursor_row < len(self.graph_table.graph_details):
            selected_graph = self.graph_table.graph_details[self.graph_table.cursor_row]
        
        self.post_message(self.GraphActionRequested("query", selected_graph))
        
        if selected_graph:
            self.notify(f"🟡 PAC-MAN querying: {selected_graph.get('name', 'Unknown')}", severity="information")
        else:
            self.notify("🟡 PAC-MAN says: Select a graph first!", severity="warning")
    
    @on(Button.Pressed, "#export-graph")
    def on_export_graph_pressed(self) -> None:
        """🧠 Handle export graph action"""
        selected_graph = None
        if self.graph_table and self.graph_table.cursor_row < len(self.graph_table.graph_details):
            selected_graph = self.graph_table.graph_details[self.graph_table.cursor_row]
        
        self.post_message(self.GraphActionRequested("export", selected_graph))
        
        if selected_graph:
            self.notify(f"🟡 PAC-MAN exporting: {selected_graph.get('name', 'Unknown')}", severity="information")
        else:
            self.notify("🟡 PAC-MAN says: Select a graph first!", severity="warning")
    
    @on(Button.Pressed, "#remove-graph")
    def on_remove_graph_pressed(self) -> None:
        """🧠 Handle remove graph action"""
        selected_graph = None
        if self.graph_table and self.graph_table.cursor_row < len(self.graph_table.graph_details):
            selected_graph = self.graph_table.graph_details[self.graph_table.cursor_row]
        
        self.post_message(self.GraphActionRequested("remove", selected_graph))
        
        if selected_graph:
            self.notify(f"🟡 PAC-MAN says: Removing {selected_graph.get('name', 'Unknown')} - Are you sure?", severity="warning")
        else:
            self.notify("🟡 PAC-MAN says: Select a graph first!", severity="warning")
    
    def refresh_data(self, graph_data: List[Dict[str, Any]], graph_stats: Dict[str, Dict[str, Any]]) -> None:
        """🧠 Refresh graph viewer data"""
        # Update overview cards
        if self.graph_overview:
            self.graph_overview.update_graph_stats(graph_stats)
        
        # Update detail table
        if self.graph_table:
            self.graph_table.refresh_graph_data(graph_data)
    
    def refresh_sample_data(self) -> None:
        """🧠 Refresh with sample data for demo"""
        sample_stats = {
            "ontology_woc": {
                "triple_count": 15420,
                "entity_count": 3844,
                "last_updated": "2024-07-24",
                "size_mb": 12.3
            },
            "functions_stable": {
                "triple_count": 8932,
                "entity_count": 1247,
                "last_updated": "2024-07-24",
                "size_mb": 8.7
            },
            "git_commits": {
                "triple_count": 5621,
                "entity_count": 892,
                "last_updated": "2024-07-24",
                "size_mb": 4.2
            }
        }
        
        sample_graphs = [
            {
                "name": "🔬 WoC Ontology",
                "type": "Ontology",
                "triple_count": 15420,
                "entity_count": 3844,
                "size_mb": 12.3,
                "status": "Ready",
                "last_updated": "2024-07-24"
            },
            {
                "name": "🟡 Stable Functions",
                "type": "Function",
                "triple_count": 8932,
                "entity_count": 1247,
                "size_mb": 8.7,
                "status": "Ready",
                "last_updated": "2024-07-24"
            }
        ]
        
        self.refresh_data(sample_graphs, sample_stats)