"""
📚 PAC-MAN's Repository Browser Widget 📚

A specialized Textual widget for browsing and managing repositories!
Navigate through your code maze collection with PAC-MAN style!

WAKA WAKA! Exploring the repository maze!
"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from textual import on, work
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Static, Button, Input, DataTable, Tree, Label, 
    ProgressBar, Select, Tabs, TabbedContent, TabPane
)
from textual.reactive import reactive
from textual.message import Message
from textual.widget import Widget
from textual.app import ComposeResult

logger = logging.getLogger(__name__)


class RepoInfoPanel(Static):
    """📚 Repository information display panel"""
    
    DEFAULT_CSS = """
    RepoInfoPanel {
        border: solid $primary;
        padding: 1;
        height: auto;
        margin: 1;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_repo = None
    
    def update_repo_info(self, repo_data: Dict[str, Any]) -> None:
        """📚 Update displayed repository information"""
        if not repo_data:
            self.update("🟡 No repository selected\n\nSelect a repository from the list to view details!")
            return
        
        # Format repository information
        info_text = f"""[bold]📚 {repo_data.get('name', 'Unknown Repository')}[/bold]

🔗 URL: {repo_data.get('url', 'N/A')}
📅 Last Updated: {repo_data.get('last_updated', 'Never')}
📦 Releases: {repo_data.get('release_count', 0)}
🧠 Graphs: {repo_data.get('graph_count', 0)}
📁 Storage: {repo_data.get('storage_size', '0 MB')}

🟡 Status: {repo_data.get('status', 'Unknown')}
"""
        
        self.update(info_text)
        self.current_repo = repo_data


class RepoActionPanel(Container):
    """⚡ Repository action buttons panel"""
    
    DEFAULT_CSS = """
    RepoActionPanel {
        height: auto;
        margin: 1;
    }
    
    RepoActionPanel Button {
        margin: 0 1;
        width: auto;
    }
    """
    
    def compose(self) -> ComposeResult:
        """⚡ Build action buttons"""
        with Horizontal():
            yield Button("➕ Add Repo", id="add-repo", variant="primary")
            yield Button("🔄 Update", id="update-repo", variant="success")
            yield Button("🧠 Process Graphs", id="process-graphs", variant="default")
            yield Button("📤 Export", id="export-repo", variant="default")
            yield Button("🗑️ Remove", id="remove-repo", variant="error")


class RepoTable(DataTable):
    """📊 Repository data table with PAC-MAN styling"""
    
    DEFAULT_CSS = """
    RepoTable {
        height: 100%;
        border: solid $primary;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repos_data: List[Dict[str, Any]] = []
    
    def on_mount(self) -> None:
        """📊 Set up table columns"""
        self.add_columns(
            "🟡", "Repository", "Status", "Releases", "Graphs", "Last Updated"
        )
        self.cursor_type = "row"
        self.zebra_stripes = True
        
        # Load sample data for demo
        self.load_sample_repos()
    
    def load_sample_repos(self) -> None:
        """📊 Load sample repository data"""
        sample_repos = [
            {
                "name": "🟡 No repositories loaded yet",
                "url": "",
                "status": "Empty",
                "release_count": 0,
                "graph_count": 0,
                "last_updated": "Never",
                "storage_size": "0 MB"
            }
        ]
        
        for repo in sample_repos:
            self.add_row(
                "🟡",
                repo["name"],
                repo["status"],
                str(repo["release_count"]),
                str(repo["graph_count"]),
                repo["last_updated"]
            )
        
        self.repos_data = sample_repos
    
    def refresh_repos(self, repos_data: List[Dict[str, Any]]) -> None:
        """📊 Refresh repository table data"""
        self.clear()
        self.repos_data = repos_data
        
        if not repos_data:
            self.add_row("🟡", "No repositories found", "Empty", "0", "0", "Never")
            return
        
        for repo in repos_data:
            status_icon = "✅" if repo.get("status") == "Ready" else "⏳" if repo.get("status") == "Processing" else "❌"
            
            self.add_row(
                status_icon,
                repo.get("name", "Unknown"),
                repo.get("status", "Unknown"),
                str(repo.get("release_count", 0)),
                str(repo.get("graph_count", 0)),
                repo.get("last_updated", "Never")
            )
    
    def get_selected_repo(self) -> Optional[Dict[str, Any]]:
        """📊 Get currently selected repository data"""
        if self.cursor_row < len(self.repos_data):
            return self.repos_data[self.cursor_row]
        return None


class RepoBrowser(Container):
    """📚 PAC-MAN's Repository Browser - The ultimate repo navigator!"""
    
    DEFAULT_CSS = """
    RepoBrowser {
        height: 100%;
        padding: 1;
    }
    
    RepoBrowser .repo-browser-main {
        height: 100%;
    }
    
    RepoBrowser .repo-list-section {
        width: 60%;
        height: 100%;
    }
    
    RepoBrowser .repo-info-section {
        width: 40%;
        height: 100%;
    }
    """
    
    # Message classes for widget communication
    class RepoSelected(Message):
        """Message sent when a repository is selected"""
        def __init__(self, repo_data: Dict[str, Any]) -> None:
            self.repo_data = repo_data
            super().__init__()
    
    class RepoActionRequested(Message):
        """Message sent when a repository action is requested"""
        def __init__(self, action: str, repo_data: Optional[Dict[str, Any]] = None) -> None:
            self.action = action
            self.repo_data = repo_data
            super().__init__()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo_table: Optional[RepoTable] = None
        self.repo_info: Optional[RepoInfoPanel] = None
    
    def compose(self) -> ComposeResult:
        """📚 Build the repository browser layout"""
        
        with Container(classes="repo-browser-main"):
            with Horizontal():
                # Left side: Repository list and actions
                with Vertical(classes="repo-list-section"):
                    yield Label("📚 Repository Collection")
                    self.repo_table = RepoTable()
                    yield self.repo_table
                    yield RepoActionPanel()
                
                # Right side: Repository information
                with Vertical(classes="repo-info-section"):
                    yield Label("📋 Repository Details")
                    self.repo_info = RepoInfoPanel()
                    yield self.repo_info
    
    @on(DataTable.RowSelected, "RepoTable")
    def on_repo_selected(self, event: DataTable.RowSelected) -> None:
        """📚 Handle repository selection"""
        if self.repo_table:
            selected_repo = self.repo_table.get_selected_repo()
            if selected_repo and self.repo_info:
                self.repo_info.update_repo_info(selected_repo)
                # Send message to parent about selection
                self.post_message(self.RepoSelected(selected_repo))
    
    @on(Button.Pressed, "#add-repo")
    def on_add_repo_pressed(self) -> None:
        """📚 Handle add repository action"""
        self.post_message(self.RepoActionRequested("add"))
        self.notify("🟡 PAC-MAN says: Use 'codedoc repo add <org/repo>' to add repositories!", severity="information")
    
    @on(Button.Pressed, "#update-repo")
    def on_update_repo_pressed(self) -> None:
        """📚 Handle update repository action"""
        selected_repo = self.repo_table.get_selected_repo() if self.repo_table else None
        self.post_message(self.RepoActionRequested("update", selected_repo))
        
        if selected_repo:
            self.notify(f"🟡 PAC-MAN updating: {selected_repo.get('name', 'Unknown')}", severity="information")
        else:
            self.notify("🟡 PAC-MAN says: Select a repository first!", severity="warning")
    
    @on(Button.Pressed, "#process-graphs")
    def on_process_graphs_pressed(self) -> None:
        """📚 Handle process graphs action"""
        selected_repo = self.repo_table.get_selected_repo() if self.repo_table else None
        self.post_message(self.RepoActionRequested("process_graphs", selected_repo))
        
        if selected_repo:
            self.notify(f"🟡 PAC-MAN processing graphs for: {selected_repo.get('name', 'Unknown')}", severity="information")
        else:
            self.notify("🟡 PAC-MAN says: Select a repository first!", severity="warning")
    
    @on(Button.Pressed, "#export-repo")
    def on_export_repo_pressed(self) -> None:
        """📚 Handle export repository action"""
        selected_repo = self.repo_table.get_selected_repo() if self.repo_table else None
        self.post_message(self.RepoActionRequested("export", selected_repo))
        
        if selected_repo:
            self.notify(f"🟡 PAC-MAN exporting: {selected_repo.get('name', 'Unknown')}", severity="information")
        else:
            self.notify("🟡 PAC-MAN says: Select a repository first!", severity="warning")
    
    @on(Button.Pressed, "#remove-repo")
    def on_remove_repo_pressed(self) -> None:
        """📚 Handle remove repository action"""
        selected_repo = self.repo_table.get_selected_repo() if self.repo_table else None
        self.post_message(self.RepoActionRequested("remove", selected_repo))
        
        if selected_repo:
            self.notify(f"🟡 PAC-MAN says: Removing {selected_repo.get('name', 'Unknown')} - Are you sure?", severity="warning")
        else:
            self.notify("🟡 PAC-MAN says: Select a repository first!", severity="warning")
    
    def refresh_data(self, repos_data: List[Dict[str, Any]]) -> None:
        """📚 Refresh repository browser data"""
        if self.repo_table:
            self.repo_table.refresh_repos(repos_data)
            
        # Clear info panel if no repos
        if not repos_data and self.repo_info:
            self.repo_info.update_repo_info({})
    
    def select_repo_by_name(self, repo_name: str) -> bool:
        """📚 Select a repository by name"""
        if not self.repo_table:
            return False
        
        for idx, repo in enumerate(self.repo_table.repos_data):
            if repo.get("name") == repo_name:
                self.repo_table.move_cursor(row=idx)
                return True
        
        return False