"""
🎮 PAC-MAN's Main TUI Application 🎮

This is the arcade cabinet! The main Textual application that brings
PAC-MAN's semantic code intelligence to life in a beautiful TUI!

WAKA WAKA! Welcome to the PAC-MAN semantic maze arcade!
"""

import asyncio
import logging
from typing import Optional, Any, Dict
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, Button, Input, Log, 
    DataTable, ProgressBar, Label, Tree, Tabs, TabbedContent, TabPane
)
from textual.reactive import reactive
from textual.message import Message
from textual.screen import Screen
from textual.binding import Binding

from ..core.manager import CodeDocManager
from ..models.exceptions import CodeDocError

logger = logging.getLogger(__name__)


class PAC_MAN_Header(Static):
    """🟡 PAC-MAN themed header with animated dots!"""
    
    DEFAULT_CSS = """
    PAC_MAN_Header {
        dock: top;
        height: 3;
        background: $boost;
        color: $text;
        content-align: center middle;
    }
    """
    
    dots_animation = reactive(0)
    
    def on_mount(self) -> None:
        """🟡 Start PAC-MAN animation when mounted"""
        self.set_interval(0.5, self.animate_dots)
    
    def animate_dots(self) -> None:
        """🟡 Animate the PAC-MAN dot chomping"""
        self.dots_animation = (self.dots_animation + 1) % 4
        
        # Create animated dots pattern
        dots = "🟡" + "·" * self.dots_animation + "👻" + "·" * (3 - self.dots_animation)
        
        self.update(f"""
[bold yellow]🟡 CodeDoc - PAC-MAN Semantic Code Intelligence 🟡[/bold yellow]
{dots} WAKA WAKA! Navigate the maze of code! {dots}
""")


class StatusFooter(Static):
    """📊 PAC-MAN status footer with system info"""
    
    DEFAULT_CSS = """
    StatusFooter {
        dock: bottom;
        height: 2;
        background: $panel;
        color: $text;
    }
    """
    
    def __init__(self, manager: CodeDocManager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
    
    def on_mount(self) -> None:
        """📊 Start status updates"""
        self.set_interval(2.0, self.update_status)
        self.update_status()
    
    def update_status(self) -> None:
        """📊 Update PAC-MAN status information"""
        try:
            if self.manager:
                # For now, show placeholder with manager available
                status_info = "🟡 PAC-MAN Active | 🗄️ Manager Ready | 🧠 Database Connected | 🔍 Ready for queries"
            else:
                status_info = "🟡 PAC-MAN Active | ❌ Manager Unavailable | 📱 TUI Mode Only"
            
            self.update(f"[dim]{status_info}[/dim]")
        except Exception as e:
            self.update(f"[red]Status error: {e}[/red]")


class MainDashboard(Screen):
    """🎮 PAC-MAN's main dashboard screen - the arcade cabinet!"""
    
    BINDINGS = [
        Binding("r", "switch_to_repos", "📚 Repositories", show=True),
        Binding("g", "switch_to_graphs", "🧠 Graphs", show=True),
        Binding("s", "switch_to_query", "🔍 Query", show=True),
        Binding("ctrl+r", "refresh", "🔄 Refresh", show=True),
    ]
    
    def __init__(self, manager: CodeDocManager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
    
    def compose(self) -> ComposeResult:
        """🎮 Build the PAC-MAN dashboard layout"""
        
        yield PAC_MAN_Header()
        
        with TabbedContent(initial="dashboard"):
            with TabPane("🎮 Dashboard", id="dashboard"):
                yield Container(
                    Vertical(
                        Static("🟡 Welcome to PAC-MAN's Semantic Code Intelligence Dashboard!", classes="welcome"),
                        Horizontal(
                            Container(
                                Label("📚 Repositories"),
                                Static("Loading repositories...", classes="info-box", id="repo-status"),
                                Horizontal(
                                    Input(placeholder="org/repo or Git URL", id="repo-add-input"),
                                    Button("➕ Add", id="repo-add-btn", variant="primary"),
                                    classes="add-repo-row"
                                ),
                                classes="panel"
                            ),
                            Container(
                                Label("🧠 Semantic Graphs"),
                                Static("Loading graphs...", classes="info-box", id="graph-status"),
                                classes="panel"
                            ),
                            classes="dashboard-row"
                        ),
                        Horizontal(
                            Container(
                                Label("🔍 Quick Actions"),
                                Vertical(
                                    Button("🧠 Process Graphs", id="process-graphs", variant="success"),
                                    Button("🔍 Run Query", id="run-query", variant="default"),
                                    Button("📤 Export Data", id="export-data", variant="default"),
                                    Button("🚪 Quit PAC-MAN", id="quit-btn", variant="error"),
                                ),
                                classes="panel"
                            ),
                            Container(
                                Label("📊 System Status"),
                                Static("🟡 PAC-MAN Status: Ready\n🖥️ System: OK\n💾 Storage: Available\n⚡ Performance: Optimal", classes="info-box"),
                                classes="panel"
                            ),
                            classes="dashboard-row"
                        ),
                        classes="dashboard-content"
                    ),
                    classes="dashboard-container"
                )
            
            with TabPane("📚 Repositories", id="repositories"):
                yield Container(
                    Static("🟡 Repository Browser - Coming Soon!", classes="placeholder"),
                    classes="tab-content"
                )
            
            with TabPane("🧠 Graphs", id="graphs"):
                yield Container(
                    Static("🟡 Graph Viewer - Coming Soon!", classes="placeholder"),
                    classes="tab-content"
                )
            
            with TabPane("🔍 Query", id="query"):
                yield Container(
                    Vertical(
                        Label("🔍 SPARQL Query Interface"),
                        Input(placeholder="Enter SPARQL query here...", id="query-input"),
                        Button("🚀 Execute Query", id="execute-query", variant="primary"),
                        Log(classes="query-results"),
                    ),
                    classes="tab-content"
                )
        
        yield StatusFooter(self.manager)
    
    @on(Button.Pressed, "#repo-add-btn")
    def on_repo_add_btn_pressed(self) -> None:
        """🟡 Handle add repository button"""
        self.add_repository_from_input()
    
    @on(Input.Submitted, "#repo-add-input")
    def on_repo_input_submitted(self, event: Input.Submitted) -> None:
        """🟡 Handle Enter key in repository input"""
        self.add_repository_from_input()
    
    def add_repository_from_input(self) -> None:
        """🟡 Add repository from input field"""
        repo_input = self.query_one("#repo-add-input", Input)
        repo_url = repo_input.value.strip()
        
        if not repo_url:
            self.notify("🟡 Please enter a repository URL or org/repo", severity="warning")
            return
        
        if self.manager:
            # Disable input while adding
            repo_input.disabled = True
            add_btn = self.query_one("#repo-add-btn", Button)
            add_btn.disabled = True
            add_btn.label = "🔄 Adding..."
            
            # Start the repository addition
            self.perform_repository_add(repo_url, repo_input, add_btn)
        else:
            self.notify("🟡 PAC-MAN says: Use 'codedoc repo add <org/repo>' in CLI!", severity="information")
    
    @work(exclusive=True)
    async def perform_repository_add(self, repo_url: str, repo_input: Input, add_btn: Button) -> None:
        """🟡 Perform repository addition asynchronously"""
        try:
            self.notify("🟡 PAC-MAN is chomping on the new repository...", severity="information")
            
            # Add the repository (always clones and discovers releases by default)
            result = await self.manager.repo_manager.add_repository(repo_url)
            
            # Success!
            self.notify(f"🟡 Repository {repo_url} added successfully!", severity="success")
            repo_input.clear()
            
            # Refresh the dashboard
            self.load_dashboard_data()
            
        except Exception as e:
            logger.error(f"Repository addition failed: {e}")
            self.notify(f"🟡 Failed to add repository: {e}", severity="error")
        
        finally:
            # Re-enable controls
            repo_input.disabled = False
            add_btn.disabled = False
            add_btn.label = "➕ Add"
    
    @on(Button.Pressed, "#process-graphs")
    def on_process_graphs_pressed(self) -> None:
        """🟡 Handle process graphs button"""
        if self.manager:
            # TODO: Open repository/release selection dialog
            self.notify("🟡 Graph processing dialog coming soon! Use CLI for now.", severity="information")
        else:
            self.notify("🟡 PAC-MAN says: Use 'codedoc graph add <org/repo>' in CLI!", severity="information")
    
    @on(Button.Pressed, "#run-query")
    def on_run_query_pressed(self) -> None:
        """🟡 Handle run query button"""
        # Switch to query tab
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "query"
        
        # Focus on query input
        query_input = self.query_one("#query-input", Input)
        query_input.focus()
    
    @on(Button.Pressed, "#export-data")
    def on_export_data_pressed(self) -> None:
        """🟡 Handle export data button"""
        from .screens.export_dialog import show_export_dialog
        show_export_dialog(self.app, self.manager)
    
    @on(Button.Pressed, "#quit-btn")
    def on_quit_button_pressed(self) -> None:
        """🟡 Handle quit button"""
        self.app.action_quit()
    
    @on(Button.Pressed, "#execute-query")
    def on_execute_query_pressed(self) -> None:
        """🟡 Handle execute query button"""
        query_input = self.query_one("#query-input", Input)
        query_log = self.query_one(Log)
        
        if query_input.value.strip():
            query_log.write_line(f"🟡 Executing query: {query_input.value}")
            
            if self.manager:
                # Execute real SPARQL query
                self.execute_sparql_query(query_input.value, query_log)
            else:
                query_log.write_line("🟡 PAC-MAN says: Manager unavailable - use CLI instead!")
            
            query_input.clear()
        else:
            self.notify("🟡 PAC-MAN says: Enter a SPARQL query first!", severity="warning")
    
    @work(exclusive=True)
    async def execute_sparql_query(self, query: str, log_widget: Log) -> None:
        """🟡 Execute SPARQL query asynchronously"""
        try:
            log_widget.write_line("🟡 PAC-MAN processing query...")
            
            # TODO: Actually execute the query through the manager
            # result = await self.manager.query_sparql(query)
            
            # Mock result for now
            await asyncio.sleep(1)  # Simulate processing time
            log_widget.write_line("🟡 Query results:")
            log_widget.write_line("  📊 Mock result: SPARQL execution coming soon!")
            log_widget.write_line("  🔍 Use 'codedoc query sparql' in CLI for now")
            
        except Exception as e:
            log_widget.write_line(f"❌ Query failed: {e}")
            self.notify(f"🟡 Query failed: {e}", severity="error")
    
    def action_switch_to_repos(self) -> None:
        """🟡 Switch to repositories tab"""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "repositories"
    
    def action_switch_to_graphs(self) -> None:
        """🟡 Switch to graphs tab"""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "graphs"
    
    def action_switch_to_query(self) -> None:
        """🟡 Switch to query tab"""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "query"
    
    def action_refresh(self) -> None:
        """🟡 Refresh dashboard data"""
        self.notify("🟡 PAC-MAN refreshing dashboard - WAKA WAKA!", severity="information")
        self.load_dashboard_data()
    
    def on_mount(self) -> None:
        """🟡 Initialize dashboard when mounted"""
        self.load_dashboard_data()
    
    @work(exclusive=True)
    async def load_dashboard_data(self) -> None:
        """🟡 Load dashboard data from manager"""
        try:
            if not self.manager:
                repo_status = self.query_one("#repo-status", Static)
                repo_status.update("No repositories loaded yet\n\nUse 'codedoc repo add <org/repo>' to start!")
                
                graph_status = self.query_one("#graph-status", Static)
                graph_status.update("No graphs available yet\n\nAdd a repository first, then use 'codedoc graph add'!")
                return
            
            # Load repositories
            repo_status = self.query_one("#repo-status", Static)
            repo_status.update("🟡 Loading repositories...")
            
            try:
                repos = await self.manager.repo_manager.list_repositories()
                if repos:
                    repo_text = f"📚 {len(repos)} repositories loaded:\n"
                    for repo in repos[:3]:  # Show first 3
                        repo_text += f"  • {repo.org_repo}\n"
                    if len(repos) > 3:
                        repo_text += f"  ... and {len(repos) - 3} more"
                    repo_status.update(repo_text)
                else:
                    repo_status.update("No repositories loaded yet\n\nUse 'codedoc repo add <org/repo>' to start!")
            except Exception as e:
                repo_status.update(f"❌ Failed to load repositories: {e}")
            
            # Load graphs
            graph_status = self.query_one("#graph-status", Static)
            graph_status.update("🟡 Loading graphs...")
            
            try:
                graphs = await self.manager.graph_manager.list_graphs()
                if graphs:
                    graph_text = f"🧠 {len(graphs)} graphs available:\n"
                    for graph in graphs[:3]:  # Show first 3
                        graph_text += f"  • {graph.uri.split('/')[-1]}\n"
                    if len(graphs) > 3:
                        graph_text += f"  ... and {len(graphs) - 3} more"
                    graph_status.update(graph_text)
                else:
                    graph_status.update("No graphs available yet\n\nAdd a repository first, then use 'codedoc graph add'!")
            except Exception as e:
                graph_status.update(f"❌ Failed to load graphs: {e}")
                
        except Exception as e:
            logger.error(f"Failed to load dashboard data: {e}")
            self.notify(f"🟡 Failed to load dashboard data: {e}", severity="error")


class CodeDocTUI(App):
    """🎮 PAC-MAN's Main TUI Application - The Arcade Cabinet!"""
    
    BINDINGS = [
        Binding("q", "quit", "🚪 Quit", show=True, priority=True),
        Binding("escape", "quit", "🚪 Quit", show=False),
        Binding("ctrl+c", "quit", "🚪 Quit", show=False),
    ]
    
    CSS = """
    /* PAC-MAN Theme Colors */
    * {
        scrollbar-background: $panel;
        scrollbar-color: $primary;
    }
    
    .welcome {
        text-align: center;
        padding: 1;
        background: $boost;
        color: $text;
        margin-bottom: 1;
    }
    
    .panel {
        border: solid $primary;
        padding: 1;
        margin: 1;
        height: auto;
    }
    
    .info-box {
        padding: 1;
        color: $text-muted;
    }
    
    .dashboard-container {
        padding: 1;
    }
    
    .dashboard-content {
        height: 100%;
    }
    
    .dashboard-row {
        height: 50%;
        margin-bottom: 1;
    }
    
    .tab-content {
        padding: 2;
        height: 100%;
    }
    
    .placeholder {
        text-align: center;
        color: $text-muted;
        padding: 4;
    }
    
    .query-results {
        height: 15;
        border: solid $primary;
        margin-top: 1;
    }
    
    Button {
        margin: 1;
        width: 100%;
    }
    
    Label {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    Input {
        margin-bottom: 1;
    }
    
    .add-repo-row {
        height: auto;
        margin-top: 1;
    }
    
    .add-repo-row Input {
        width: 75%;
        margin-right: 1;
        margin-bottom: 0;
    }
    
    .add-repo-row Button {
        width: 25%;
        margin: 0;
    }
    """
    
    TITLE = "🟡 PAC-MAN CodeDoc Dashboard"
    SUB_TITLE = "Semantic Code Intelligence - WAKA WAKA!"
    
    def __init__(self, manager: Optional[CodeDocManager] = None, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager or self._create_default_manager()
    
    def _create_default_manager(self) -> CodeDocManager:
        """🟡 Create default manager if none provided"""
        logger.info("🟡 Creating default CodeDoc manager for TUI")
        try:
            return CodeDocManager()
        except Exception as e:
            logger.error(f"🟡 Failed to create CodeDoc manager: {e}")
            return None
    
    def on_mount(self) -> None:
        """🎮 PAC-MAN TUI startup sequence"""
        logger.info("🟡 PAC-MAN TUI starting up - WAKA WAKA!")
        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE
        
        # Install main dashboard screen
        dashboard = MainDashboard(self.manager)
        self.install_screen(dashboard, name="main")
        self.push_screen("main")
    
    def action_quit(self) -> None:
        """🟡 PAC-MAN shutdown sequence"""
        logger.info("🟡 PAC-MAN TUI shutting down - Thanks for playing!")
        self.bell()  # Sound effect
        self.exit(message="🟡 WAKA WAKA! Thanks for playing PAC-MAN CodeDoc!")


async def run_tui(manager: Optional[CodeDocManager] = None) -> None:
    """🎮 Launch PAC-MAN's TUI - Start the arcade experience!"""
    logger.info("🟡 Launching PAC-MAN TUI Dashboard - WAKA WAKA!")
    
    app = CodeDocTUI(manager)
    await app.run_async()


if __name__ == "__main__":
    # Quick test run
    asyncio.run(run_tui())