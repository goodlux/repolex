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
            # Get system status (this would call actual manager methods)
            status_info = "🟡 PAC-MAN Active | 🗄️ 0 Repos | 🧠 0 Graphs | 🔍 Ready for queries"
            self.update(f"[dim]{status_info}[/dim]")
        except Exception as e:
            self.update(f"[red]Status error: {e}[/red]")


class MainDashboard(Screen):
    """🎮 PAC-MAN's main dashboard screen - the arcade cabinet!"""
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "switch_to_repos", "Repositories", show=True),
        Binding("g", "switch_to_graphs", "Graphs", show=True),
        Binding("s", "switch_to_query", "Query", show=True),
        Binding("ctrl+r", "refresh", "Refresh", show=True),
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
                                Static("No repositories loaded yet\n\nUse 'codedoc repo add <org/repo>' to start!", classes="info-box"),
                                classes="panel"
                            ),
                            Container(
                                Label("🧠 Semantic Graphs"),
                                Static("No graphs available yet\n\nAdd a repository first, then use 'codedoc graph add'!", classes="info-box"),
                                classes="panel"
                            ),
                            classes="dashboard-row"
                        ),
                        Horizontal(
                            Container(
                                Label("🔍 Quick Actions"),
                                Vertical(
                                    Button("➕ Add Repository", id="add-repo", variant="primary"),
                                    Button("🧠 Process Graphs", id="process-graphs", variant="success"),
                                    Button("🔍 Run Query", id="run-query", variant="default"),
                                    Button("📤 Export Data", id="export-data", variant="default"),
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
    
    @on(Button.Pressed, "#add-repo")
    def on_add_repo_pressed(self) -> None:
        """🟡 Handle add repository button"""
        self.notify("🟡 PAC-MAN says: Use 'codedoc repo add <org/repo>' in CLI!", severity="information")
    
    @on(Button.Pressed, "#process-graphs")
    def on_process_graphs_pressed(self) -> None:
        """🟡 Handle process graphs button"""
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
        self.notify("🟡 PAC-MAN says: Use 'codedoc export' commands in CLI!", severity="information")
    
    @on(Button.Pressed, "#execute-query")
    def on_execute_query_pressed(self) -> None:
        """🟡 Handle execute query button"""
        query_input = self.query_one("#query-input", Input)
        query_log = self.query_one(Log)
        
        if query_input.value.strip():
            query_log.write_line(f"🟡 Executing query: {query_input.value}")
            query_log.write_line("🟡 PAC-MAN says: SPARQL execution coming soon!")
            query_input.clear()
        else:
            self.notify("🟡 PAC-MAN says: Enter a SPARQL query first!", severity="warning")
    
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


class CodeDocTUI(App):
    """🎮 PAC-MAN's Main TUI Application - The Arcade Cabinet!"""
    
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
    """
    
    TITLE = "🟡 PAC-MAN CodeDoc Dashboard"
    SUB_TITLE = "Semantic Code Intelligence - WAKA WAKA!"
    
    def __init__(self, manager: Optional[CodeDocManager] = None, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager or self._create_default_manager()
    
    def _create_default_manager(self) -> CodeDocManager:
        """🟡 Create default manager if none provided"""
        # This would create a manager, but for now we'll create a stub
        logger.info("🟡 Creating default CodeDoc manager for TUI")
        # return CodeDocManager()  # Commented out until we test integration
        return None  # Temporary stub
    
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
        self.exit()


async def run_tui(manager: Optional[CodeDocManager] = None) -> None:
    """🎮 Launch PAC-MAN's TUI - Start the arcade experience!"""
    logger.info("🟡 Launching PAC-MAN TUI Dashboard - WAKA WAKA!")
    
    app = CodeDocTUI(manager)
    await app.run_async()


if __name__ == "__main__":
    # Quick test run
    asyncio.run(run_tui())