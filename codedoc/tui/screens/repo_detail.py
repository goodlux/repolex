"""
📚 PAC-MAN's Repository Detail Screen 📚

A focused screen for exploring a single repository in detail!
Deep dive into repository structure, graphs, and semantic intelligence!

WAKA WAKA! Zooming into the repository maze for detailed exploration!
"""

import logging
from typing import Optional, Dict, Any, List

from textual import on, work
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import (
    Static, Button, Label, DataTable, Tree, ProgressBar,
    TabbedContent, TabPane, Log, Input, Select
)
from textual.reactive import reactive
from textual.screen import Screen
from textual.binding import Binding
from textual.app import ComposeResult

logger = logging.getLogger(__name__)


class RepoInfoHeader(Static):
    """📚 Repository information header"""
    
    DEFAULT_CSS = """
    RepoInfoHeader {
        dock: top;
        height: 5;
        background: $boost;
        color: $text;
        padding: 1;
    }
    """
    
    def __init__(self, repo_data: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.repo_data = repo_data
        self.update_header()
    
    def update_header(self) -> None:
        """📚 Update header with repository information"""
        repo_name = self.repo_data.get("name", "Unknown Repository")
        repo_url = self.repo_data.get("url", "No URL")
        status = self.repo_data.get("status", "Unknown")
        last_updated = self.repo_data.get("last_updated", "Never")
        
        # Status emoji
        status_emoji = "✅" if status == "Ready" else "⏳" if status == "Processing" else "❌"
        
        header_text = f"""[bold yellow]📚 {repo_name}[/bold yellow]
🔗 {repo_url} | {status_emoji} {status} | 📅 Updated: {last_updated}
🟡 PAC-MAN's detailed repository analysis - WAKA WAKA!"""
        
        self.update(header_text)
    
    def update_repo_data(self, repo_data: Dict[str, Any]) -> None:
        """📚 Update repository data"""
        self.repo_data = repo_data
        self.update_header()


class RepoStatsPanel(Static):
    """📊 Repository statistics panel"""
    
    DEFAULT_CSS = """
    RepoStatsPanel {
        border: solid $primary;
        padding: 1;
        height: auto;
        margin: 1;
    }
    """
    
    def __init__(self, repo_data: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.repo_data = repo_data
        self.update_stats()
    
    def update_stats(self) -> None:
        """📊 Update statistics display"""
        stats_text = f"""[bold]📊 Repository Statistics[/bold]

📦 Releases: {self.repo_data.get('release_count', 0)}
🧠 Graphs: {self.repo_data.get('graph_count', 0)}
💾 Storage: {self.repo_data.get('storage_size', '0 MB')}
📁 Files: {self.repo_data.get('file_count', 'Unknown')}
🟡 Functions: {self.repo_data.get('function_count', 'Unknown')}
📊 Classes: {self.repo_data.get('class_count', 'Unknown')}
👻 Developers: {self.repo_data.get('developer_count', 'Unknown')}
📝 Commits: {self.repo_data.get('commit_count', 'Unknown')}

🎯 Complexity Score: {self.repo_data.get('complexity_score', 'N/A')}
⭐ Quality Rating: {self.repo_data.get('quality_rating', 'N/A')}
🔥 Activity Level: {self.repo_data.get('activity_level', 'N/A')}"""
        
        self.update(stats_text)


class ReleaseTable(DataTable):
    """📦 Repository releases table"""
    
    DEFAULT_CSS = """
    ReleaseTable {
        height: 100%;
        border: solid $primary;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.releases_data: List[Dict[str, Any]] = []
    
    def on_mount(self) -> None:
        """📦 Set up releases table"""
        self.add_columns(
            "Release", "Date", "Graphs", "Functions", "Status", "Size"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
        
        # Load sample data
        self.load_sample_releases()
    
    def load_sample_releases(self) -> None:
        """📦 Load sample release data"""
        sample_releases = [
            {
                "name": "v1.0.0",
                "date": "2024-07-20",
                "graph_count": 19,
                "function_count": 245,
                "status": "Ready",
                "size": "15.2 MB"
            },
            {
                "name": "v0.9.5",
                "date": "2024-07-15",
                "graph_count": 19,
                "function_count": 230,  
                "status": "Ready",
                "size": "14.8 MB"
            },
            {
                "name": "v0.9.0",
                "date": "2024-07-10",
                "graph_count": 0,
                "function_count": 220,
                "status": "Not Processed",
                "size": "0 MB"
            }
        ]
        
        for release in sample_releases:
            status_icon = "✅" if release["status"] == "Ready" else "⏳" if release["status"] == "Processing" else "❌"
            
            self.add_row(
                release["name"],
                release["date"],
                str(release["graph_count"]),
                str(release["function_count"]),
                f"{status_icon} {release['status']}",
                release["size"]
            )
        
        self.releases_data = sample_releases


class FileTreeWidget(Tree):
    """📁 Repository file structure tree"""
    
    DEFAULT_CSS = """
    FileTreeWidget {
        height: 100%;
        border: solid $primary;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__("📚 Repository Structure", **kwargs)
    
    def on_mount(self) -> None:
        """📁 Build file tree structure"""
        # Add sample file structure
        src_node = self.root.add("📂 src/")
        src_node.add_leaf("🐍 __init__.py")
        src_node.add_leaf("🐍 main.py")
        src_node.add_leaf("🐍 utils.py")
        
        core_node = src_node.add("📂 core/")
        core_node.add_leaf("🐍 engine.py")
        core_node.add_leaf("🐍 parser.py")
        core_node.add_leaf("🐍 analyzer.py")
        
        tests_node = self.root.add("📂 tests/")
        tests_node.add_leaf("🐍 test_main.py")
        tests_node.add_leaf("🐍 test_utils.py")
        
        docs_node = self.root.add("📂 docs/")
        docs_node.add_leaf("📄 README.md")
        docs_node.add_leaf("📄 API.md")
        
        self.root.add_leaf("📄 pyproject.toml")
        self.root.add_leaf("📄 .gitignore")
        
        self.root.expand()


class GraphStatusTable(DataTable):
    """🧠 Repository graph status table"""
    
    DEFAULT_CSS = """
    GraphStatusTable {
        height: 100%;
        border: solid $primary;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_mount(self) -> None:
        """🧠 Set up graph status table"""
        self.add_columns(
            "Graph Type", "Triples", "Entities", "Status", "Updated"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
        
        # Sample graph data
        sample_graphs = [
            ("🔬 WoC Ontology", "15,420", "3,844", "✅ Ready", "2024-07-24"),
            ("🟡 Stable Functions", "8,932", "1,247", "✅ Ready", "2024-07-24"),
            ("🔧 Function Implementations", "12,156", "1,247", "✅ Ready", "2024-07-24"),
            ("👻 Git Commits", "5,621", "892", "✅ Ready", "2024-07-24"),
            ("👥 Developers", "234", "15", "✅ Ready", "2024-07-24"),
            ("⏰ ABC Events", "1,844", "456", "✅ Ready", "2024-07-24"),
            ("📈 Evolution Analysis", "3,221", "789", "⏳ Processing", "2024-07-24"),
        ]
        
        for graph_data in sample_graphs:
            self.add_row(*graph_data)


class RepoActionPanel(Container):
    """⚡ Repository-specific actions panel"""
    
    DEFAULT_CSS = """
    RepoActionPanel {
        dock: bottom;
        height: 3;
        background: $panel;
        padding: 1;
    }
    
    RepoActionPanel Button {
        margin: 0 1;
        width: auto;
    }
    """
    
    def compose(self) -> ComposeResult:
        """⚡ Build action buttons"""
        with Horizontal():
            yield Button("🔄 Update Repo", id="update-repo", variant="success")
            yield Button("🧠 Process Graphs", id="process-graphs", variant="primary")
            yield Button("📤 Export Data", id="export-repo", variant="default")
            yield Button("🔍 Query Repository", id="query-repo", variant="default")
            yield Button("📊 Generate Report", id="generate-report", variant="default")
            yield Button("⬅️ Back to Dashboard", id="back-dashboard", variant="error")


class RepoDetailScreen(Screen):
    """📚 PAC-MAN's Repository Detail Screen - Deep dive into repository intelligence!"""
    
    BINDINGS = [
        Binding("escape", "back_to_dashboard", "Back", show=True),
        Binding("f5", "refresh_repo", "Refresh", show=True), 
        Binding("ctrl+u", "update_repo", "Update", show=False),
        Binding("ctrl+g", "process_graphs", "Process", show=False),
        Binding("ctrl+e", "export_repo", "Export", show=False),
        Binding("ctrl+q", "query_repo", "Query", show=False),
    ]
    
    def __init__(self, repo_data: Dict[str, Any], manager=None, **kwargs):
        super().__init__(**kwargs)
        self.repo_data = repo_data
        self.manager = manager
        self.repo_header: Optional[RepoInfoHeader] = None
        self.activity_log: Optional[Log] = None
    
    def compose(self) -> ComposeResult:
        """📚 Build the repository detail layout"""
        
        # Repository header
        self.repo_header = RepoInfoHeader(self.repo_data)
        yield self.repo_header
        
        # Main content with detailed tabs
        with TabbedContent(initial="overview"):
            # Overview Tab
            with TabPane("📊 Overview", id="overview"):
                with Horizontal():
                    # Left: Stats and info
                    with Vertical():
                        yield RepoStatsPanel(self.repo_data)
                        
                        # Recent activity
                        yield Label("📝 Recent Activity")
                        self.activity_log = Log(classes="activity-log")
                        yield self.activity_log
                    
                    # Right: File structure
                    with Vertical():
                        yield Label("📁 Repository Structure")
                        yield FileTreeWidget()
            
            # Releases Tab  
            with TabPane("📦 Releases", id="releases"):
                with Vertical():
                    yield Label("📦 Repository Releases") 
                    yield ReleaseTable()
                    
                    with Horizontal():
                        yield Button("🧠 Process Release", id="process-release", variant="primary")
                        yield Button("📊 Compare Releases", id="compare-releases", variant="default")
                        yield Button("📤 Export Release", id="export-release", variant="default")
            
            # Graphs Tab
            with TabPane("🧠 Graphs", id="graphs"):
                with Vertical():
                    yield Label("🧠 Semantic Graph Status")
                    yield GraphStatusTable()
                    
                    with Horizontal():
                        yield Button("🔄 Refresh Graphs", id="refresh-graphs", variant="success")
                        yield Button("🧠 Rebuild All", id="rebuild-graphs", variant="primary")
                        yield Button("🔍 Query Graphs", id="query-graphs", variant="default")
            
            # Analysis Tab
            with TabPane("📈 Analysis", id="analysis"):
                with Vertical():
                    yield Label("📈 Repository Analysis")
                    
                    analysis_content = f"""[bold]🟡 PAC-MAN's Repository Intelligence Analysis[/bold]

📊 **Complexity Analysis:**
• Average function complexity: {self.repo_data.get('avg_complexity', 'N/A')}
• Most complex function: {self.repo_data.get('most_complex_function', 'N/A')}
• Complexity trend: {self.repo_data.get('complexity_trend', 'Stable')}

👻 **Developer Intelligence:**
• Most active developer: {self.repo_data.get('top_developer', 'N/A')}
• Developer count: {self.repo_data.get('developer_count', 'N/A')}
• Collaboration patterns: {self.repo_data.get('collaboration_score', 'N/A')}

⏰ **Evolution Patterns:**
• Function stability: {self.repo_data.get('function_stability', 'N/A')}
• Change frequency: {self.repo_data.get('change_frequency', 'N/A')}
• Breaking changes: {self.repo_data.get('breaking_changes', 'N/A')}

🎯 **Quality Metrics:**
• Documentation coverage: {self.repo_data.get('doc_coverage', 'N/A')}
• Test coverage: {self.repo_data.get('test_coverage', 'N/A')}
• Code quality score: {self.repo_data.get('quality_score', 'N/A')}

🔍 **Recommendations:**
• Consider refactoring complex functions
• Improve documentation coverage
• Add more comprehensive tests
• Monitor function stability trends"""
                    
                    yield Static(analysis_content, classes="analysis-content")
                    
                    with Horizontal():
                        yield Button("📊 Generate Full Report", id="full-report", variant="primary")
                        yield Button("📤 Export Analysis", id="export-analysis", variant="default")
            
            # Query Tab - Repository-specific queries
            with TabPane("🔍 Query", id="query"):
                with Vertical():
                    yield Label("🔍 Repository-Specific Queries")
                    
                    # Quick query buttons
                    with Grid():
                        yield Button("🟡 Find Functions", id="query-functions", variant="primary")
                        yield Button("👻 Developer Stats", id="query-developers", variant="default")
                        yield Button("📈 Evolution History", id="query-evolution", variant="default")
                        yield Button("🧠 Complexity Analysis", id="query-complexity", variant="default")
                    
                    # Query results area
                    yield Label("📊 Query Results")
                    query_results = """[dim]Query results will appear here:

• Function search results
• Developer statistics  
• Evolution analysis
• Complexity metrics
• Cross-graph relationships

Click a query button above to start![/dim]"""
                    
                    yield Static(query_results, classes="query-results")
        
        # Action panel
        yield RepoActionPanel()
    
    def on_mount(self) -> None:
        """📚 Repository detail screen initialization"""
        repo_name = self.repo_data.get("name", "Unknown")
        logger.info(f"🟡 Repository detail screen mounted for: {repo_name}")
        
        if self.activity_log:
            self.activity_log.write_line(f"📚 Analyzing repository: {repo_name}")
            self.activity_log.write_line("🧠 Loading semantic graph data...")
            self.activity_log.write_line("👻 Analyzing developer patterns...")
            self.activity_log.write_line("⏰ Processing evolution history...")
            self.activity_log.write_line("✅ Repository analysis complete")
    
    # Action handlers
    @on(Button.Pressed, "#back-dashboard")
    def on_back_dashboard_pressed(self) -> None:
        """⬅️ Handle back to dashboard"""
        self.action_back_to_dashboard()
    
    @on(Button.Pressed, "#update-repo")
    def on_update_repo_pressed(self) -> None:
        """🔄 Handle repository update"""  
        self.action_update_repo()
    
    @on(Button.Pressed, "#process-graphs")
    def on_process_graphs_pressed(self) -> None:
        """🧠 Handle graph processing"""
        self.action_process_graphs()
    
    @on(Button.Pressed, "#export-repo")
    def on_export_repo_pressed(self) -> None:
        """📤 Handle repository export"""  
        self.action_export_repo()
    
    @on(Button.Pressed, "#query-repo")
    def on_query_repo_pressed(self) -> None:
        """🔍 Handle repository query"""
        self.action_query_repo()
    
    # Quick query handlers
    @on(Button.Pressed, "#query-functions")
    def on_query_functions_pressed(self) -> None:
        """🟡 Handle function query"""
        repo_name = self.repo_data.get("name", "Unknown")
        self.notify(f"🟡 PAC-MAN searching functions in {repo_name}!", severity="information")
    
    @on(Button.Pressed, "#query-developers")
    def on_query_developers_pressed(self) -> None:
        """👻 Handle developer query"""
        repo_name = self.repo_data.get("name", "Unknown")
        self.notify(f"👻 PAC-MAN analyzing developers in {repo_name}!", severity="information")
    
    # Screen actions
    def action_back_to_dashboard(self) -> None:
        """⬅️ Return to main dashboard"""
        logger.info("🟡 Returning to dashboard from repository detail")
        self.app.pop_screen()
    
    def action_refresh_repo(self) -> None:
        """🔄 Refresh repository data"""
        repo_name = self.repo_data.get("name", "Unknown")
        
        if self.activity_log:
            self.activity_log.write_line(f"🔄 Refreshing data for {repo_name}")
        
        self.notify(f"🟡 PAC-MAN refreshing {repo_name} - WAKA WAKA!", severity="information")
    
    def action_update_repo(self) -> None:
        """🔄 Update repository"""
        repo_name = self.repo_data.get("name", "Unknown")
        
        if self.activity_log:
            self.activity_log.write_line(f"🔄 Updating repository: {repo_name}")
        
        self.notify(f"🟡 PAC-MAN updating {repo_name}!", severity="information")
    
    def action_process_graphs(self) -> None:
        """🧠 Process repository graphs"""
        repo_name = self.repo_data.get("name", "Unknown")
        
        if self.activity_log:
            self.activity_log.write_line(f"🧠 Processing graphs for: {repo_name}")
        
        self.notify(f"🟡 PAC-MAN processing graphs for {repo_name}!", severity="information")
    
    def action_export_repo(self) -> None:
        """📤 Export repository data"""
        repo_name = self.repo_data.get("name", "Unknown")
        
        if self.activity_log:
            self.activity_log.write_line(f"📤 Exporting data for: {repo_name}")
        
        self.notify(f"🟡 PAC-MAN exporting {repo_name}!", severity="information")
    
    def action_query_repo(self) -> None:
        """🔍 Switch to query tab"""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "query"
        
        self.notify("🟡 PAC-MAN ready for repository queries!", severity="information")