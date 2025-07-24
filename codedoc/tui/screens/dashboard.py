"""
🎮 PAC-MAN's Main Dashboard Screen 🎮

The ultimate semantic code intelligence dashboard - a full-screen experience
with all the widgets working together in perfect PAC-MAN harmony!

WAKA WAKA! The main arcade level with all power-ups activated!
"""

import logging
from typing import Optional, Dict, Any, List

from textual import on, work
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, Button, Label, 
    TabbedContent, TabPane, Log
)
from textual.reactive import reactive
from textual.screen import Screen
from textual.binding import Binding
from textual.app import ComposeResult

from ..widgets.repo_browser import RepoBrowser
from ..widgets.graph_viewer import GraphViewer
from ..widgets.query_panel import QueryPanel

logger = logging.getLogger(__name__)


class DashboardHeader(Static):
    """🟡 Enhanced dashboard header with real-time info"""
    
    DEFAULT_CSS = """
    DashboardHeader {
        dock: top;
        height: 3;
        background: $boost;
        color: $text;
        content-align: center middle;
    }
    """
    
    animation_frame = reactive(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo_count = 0
        self.graph_count = 0
        self.active_queries = 0
    
    def on_mount(self) -> None:
        """🟡 Start header animation and updates"""
        self.set_interval(0.8, self.animate_header)
        self.update_header()
    
    def animate_header(self) -> None:
        """🟡 Animate PAC-MAN header"""
        self.animation_frame = (self.animation_frame + 1) % 4
        self.update_header()
    
    def update_header(self) -> None:
        """🟡 Update header with current stats"""
        # PAC-MAN animation
        pac_frames = ["🟡", "🟡", "🟡", "😮"]  # PAC-MAN opening and closing mouth  
        pac_man = pac_frames[self.animation_frame]
        
        # Ghost animation (they move in opposite direction)
        ghost_frames = ["👻", "👻", "🟦", "🟦"]  # Normal and scared ghosts
        ghost = ghost_frames[self.animation_frame]
        
        # Dots trail
        dots = "·" * (3 - self.animation_frame) + "🟡" + "·" * self.animation_frame
        
        header_text = f"""[bold yellow]{pac_man} CodeDoc - Semantic Intelligence Dashboard {ghost}[/bold yellow]
{dots} 📚 {self.repo_count} repos | 🧠 {self.graph_count} graphs | 🔍 {self.active_queries} queries {dots}"""
        
        self.update(header_text)
    
    def update_stats(self, repo_count: int = 0, graph_count: int = 0, active_queries: int = 0) -> None:
        """🟡 Update header statistics"""
        self.repo_count = repo_count
        self.graph_count = graph_count  
        self.active_queries = active_queries
        self.update_header()


class DashboardFooter(Static):
    """📊 Enhanced footer with system status and shortcuts"""
    
    DEFAULT_CSS = """
    DashboardFooter {
        dock: bottom;
        height: 2;
        background: $panel;
        color: $text;
        padding: 0 2;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.system_status = "Ready"
        self.last_action = "System initialized"
    
    def on_mount(self) -> None:
        """📊 Start footer updates"""
        self.set_interval(5.0, self.update_footer)
        self.update_footer()
    
    def update_footer(self) -> None:
        """📊 Update footer with system info"""
        shortcuts = "F1:Help | F5:Refresh | Tab:Switch | Q:Quit"
        status_line = f"🟡 Status: {self.system_status} | Last: {self.last_action}"
        
        footer_text = f"[dim]{shortcuts}[/dim]\n{status_line}"
        self.update(footer_text)
    
    def update_status(self, status: str, last_action: str = None) -> None:
        """📊 Update system status"""
        self.system_status = status
        if last_action:
            self.last_action = last_action
        self.update_footer()


class DashboardScreen(Screen):
    """🎮 PAC-MAN's Main Dashboard Screen - The ultimate semantic arcade!"""
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("f1", "show_help", "Help", show=True),
        Binding("f5", "refresh_all", "Refresh", show=True),
        Binding("tab", "next_tab", "Next Tab", show=False),
        Binding("shift+tab", "prev_tab", "Prev Tab", show=False),
        Binding("ctrl+r", "refresh_repos", "Refresh Repos", show=False),
        Binding("ctrl+g", "refresh_graphs", "Refresh Graphs", show=False),
        Binding("ctrl+q", "new_query", "New Query", show=False),
    ]
    
    def __init__(self, manager=None, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.header: Optional[DashboardHeader] = None
        self.footer: Optional[DashboardFooter] = None
        self.repo_browser: Optional[RepoBrowser] = None
        self.graph_viewer: Optional[GraphViewer] = None
        self.query_panel: Optional[QueryPanel] = None
        self.activity_log: Optional[Log] = None
    
    def compose(self) -> ComposeResult:
        """🎮 Build the complete dashboard layout"""
        
        # Header
        self.header = DashboardHeader()
        yield self.header
        
        # Main content with tabs
        with TabbedContent(initial="overview"):
            # Overview Tab - Combined view
            with TabPane("🎮 Overview", id="overview"):
                with Container():
                    with Horizontal():
                        # Left side: Repository browser (60%)
                        with Container(classes="overview-left"):
                            self.repo_browser = RepoBrowser()
                            yield self.repo_browser
                        
                        # Right side: Graph stats and activity (40%)
                        with Vertical(classes="overview-right"):
                            # Graph stats (top half)
                            with Container(classes="overview-graphs"):
                                yield Label("🧠 Graph Statistics Overview")
                                yield Static("""[dim]📊 Graph overview will be shown here:

• 🔬 Ontology graphs: 4 types
• 🟡 Function graphs: 2 types  
• 👻 Git intelligence: 4 types
• ⏰ ABC events: 1 type
• 📈 Evolution analysis: 3 types

Total: 19 graphs per repository[/dim]""", classes="graph-overview")
                            
                            # Activity log (bottom half)
                            with Container(classes="overview-activity"):
                                yield Label("📝 Recent Activity")
                                self.activity_log = Log(classes="activity-log")
                                yield self.activity_log
            
            # Repositories Tab - Full repository browser
            with TabPane("📚 Repositories", id="repositories"):
                self.repo_browser_full = RepoBrowser()
                yield self.repo_browser_full
            
            # Graphs Tab - Full graph viewer
            with TabPane("🧠 Graphs", id="graphs"):
                self.graph_viewer = GraphViewer()
                yield self.graph_viewer
            
            # Query Tab - Full query interface
            with TabPane("🔍 Query", id="query"):
                self.query_panel = QueryPanel()
                yield self.query_panel
            
            # System Tab - System information and logs
            with TabPane("⚙️ System", id="system"):
                with Vertical():
                    yield Label("⚙️ System Information")
                    
                    system_info = """🟡 PAC-MAN System Status

🖥️ Platform: Active
💾 Storage: ~/.codedoc/
🗄️ Database: Oxigraph semantic database
⚡ Performance: Optimal

📊 Current Statistics:
• Repositories: 0 loaded
• Graphs: 0 active  
• Queries: 0 executed
• Storage: 0 MB used

🔧 Configuration:
• Theme: PAC-MAN Classic
• Animations: Enabled
• Sounds: WAKA WAKA Mode
• Debug: Info Level"""
                    
                    yield Static(system_info, classes="system-info")
                    yield Button("🔄 Refresh System", id="refresh-system", variant="primary")
        
        # Footer
        self.footer = DashboardFooter()
        yield self.footer
    
    def on_mount(self) -> None:
        """🎮 Dashboard initialization"""
        logger.info("🟡 PAC-MAN Dashboard Screen mounted - WAKA WAKA!")
        
        # Log initial activity
        if self.activity_log:
            self.activity_log.write_line("🟡 PAC-MAN Dashboard initialized")
            self.activity_log.write_line("📚 Ready to load repositories")
            self.activity_log.write_line("🧠 Semantic graph system online")
            self.activity_log.write_line("🔍 Query interface ready")
        
        # Update header stats
        if self.header:
            self.header.update_stats(0, 0, 0)
        
        # Update footer
        if self.footer:
            self.footer.update_status("Ready", "Dashboard initialized")
    
    # Message handlers for widget communication
    @on(RepoBrowser.RepoSelected)
    def on_repo_selected(self, message: RepoBrowser.RepoSelected) -> None:
        """📚 Handle repository selection"""
        repo_name = message.repo_data.get("name", "Unknown")
        
        if self.activity_log:
            self.activity_log.write_line(f"📚 Selected repository: {repo_name}")
        
        if self.footer:
            self.footer.update_status("Ready", f"Selected repo: {repo_name}")
        
        # Could update graph viewer to show graphs for this repo
        logger.info(f"🟡 Repository selected: {repo_name}")
    
    @on(RepoBrowser.RepoActionRequested)
    def on_repo_action_requested(self, message: RepoBrowser.RepoActionRequested) -> None:
        """📚 Handle repository actions"""
        action = message.action
        repo_data = message.repo_data
        
        if self.activity_log:
            repo_name = repo_data.get("name", "Unknown") if repo_data else "None"
            self.activity_log.write_line(f"📚 Repository action: {action} on {repo_name}")
        
        if self.footer:
            self.footer.update_status("Processing", f"Repository {action} requested")
        
        # Here we would integrate with the actual manager to perform actions
        logger.info(f"🟡 Repository action requested: {action}")
    
    @on(GraphViewer.GraphActionRequested)
    def on_graph_action_requested(self, message: GraphViewer.GraphActionRequested) -> None:
        """🧠 Handle graph actions"""
        action = message.action
        graph_data = message.graph_data
        
        if self.activity_log:
            graph_name = graph_data.get("name", "Unknown") if graph_data else "None"
            self.activity_log.write_line(f"🧠 Graph action: {action} on {graph_name}")
        
        if self.footer:
            self.footer.update_status("Processing", f"Graph {action} requested")
        
        logger.info(f"🟡 Graph action requested: {action}")
    
    @on(QueryPanel.QueryRequested)
    def on_query_requested(self, message: QueryPanel.QueryRequested) -> None:
        """🔍 Handle query execution requests"""
        query = message.query
        query_type = message.query_type
        
        if self.activity_log:
            self.activity_log.write_line(f"🔍 Executing {query_type} query")
            self.activity_log.write_line(f"Query: {query[:50]}...")
        
        if self.footer:
            self.footer.update_status("Querying", f"Executing {query_type} query")
        
        # Here we would integrate with the actual query manager
        logger.info(f"🟡 Query requested: {query_type}")
    
    # Action handlers
    def action_show_help(self) -> None:
        """🎮 Show help information"""
        help_text = """🟡 PAC-MAN Dashboard Help

🎮 Navigation:
• Tab / Shift+Tab: Switch between tabs
• Arrow keys: Navigate within widgets
• Enter: Select/activate items
• Escape: Go back/cancel

📚 Repository Commands:
• Add repos with: codedoc repo add <org/repo>
• Update with: codedoc repo update <org/repo>

🧠 Graph Commands:
• Process graphs: codedoc graph add <org/repo>
• View graphs: Use the Graphs tab

🔍 Query Commands:
• Write SPARQL in Query tab
• Use function search for quick finds

⚙️ System:
• F5: Refresh all data
• Ctrl+R: Refresh repositories
• Ctrl+G: Refresh graphs
• Q: Quit application

WAKA WAKA! Happy exploring!"""
        
        self.notify(help_text, title="🟡 PAC-MAN Help", severity="information")
    
    def action_refresh_all(self) -> None:
        """🎮 Refresh all dashboard data"""
        if self.activity_log:
            self.activity_log.write_line("🔄 Refreshing all dashboard data")
        
        if self.footer:
            self.footer.update_status("Refreshing", "Updating all data")
        
        # Refresh individual components
        self.action_refresh_repos()
        self.action_refresh_graphs()
        
        self.notify("🟡 PAC-MAN refreshed all data - WAKA WAKA!", severity="success")
    
    def action_refresh_repos(self) -> None:
        """📚 Refresh repository data"""
        if self.repo_browser:
            # This would call actual manager methods
            sample_repos = [
                {
                    "name": "example/repo",
                    "url": "https://github.com/example/repo",
                    "status": "Ready",
                    "release_count": 5,
                    "graph_count": 19,
                    "last_updated": "2024-07-24",
                    "storage_size": "25.3 MB"
                }
            ]
            self.repo_browser.refresh_data(sample_repos)
    
    def action_refresh_graphs(self) -> None:
        """🧠 Refresh graph data"""
        if self.graph_viewer:
            # This would call actual manager methods
            self.graph_viewer.refresh_sample_data()
    
    def action_new_query(self) -> None:
        """🔍 Focus on query tab and start new query"""
        # Switch to query tab
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "query"
        
        # Clear and focus query editor
        if self.query_panel:
            self.query_panel.set_query_text("# 🟡 New PAC-MAN query!")
        
        self.notify("🟡 PAC-MAN ready for new query!", severity="information")
    
    @on(Button.Pressed, "#refresh-system")
    def on_refresh_system_pressed(self) -> None:
        """⚙️ Handle system refresh"""
        if self.activity_log:
            self.activity_log.write_line("⚙️ System refresh requested")
        
        self.notify("🟡 PAC-MAN system refreshed!", severity="success")