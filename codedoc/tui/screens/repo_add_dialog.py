"""
➕ PAC-MAN's Repository Add Dialog ➕

The ultimate repository addition screen - PAC-MAN style!
Add new repositories to the semantic maze with full validation!

WAKA WAKA! Let's add more mazes to explore!
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from pathlib import Path

from textual import on, work
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Static, Button, Input, Label, Log, ProgressBar, Checkbox
)
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.validation import Function, ValidationResult, Validator

logger = logging.getLogger(__name__)


class RepoUrlValidator(Validator):
    """🟡 PAC-MAN's repository URL validator"""
    
    def validate(self, value: str) -> ValidationResult:
        """Validate repository URL or org/repo format"""
        if not value.strip():
            return self.failure("Repository URL cannot be empty")
        
        value = value.strip()
        
        # Check for org/repo format (e.g., "microsoft/vscode")
        if '/' in value and not value.startswith('http'):
            parts = value.split('/')
            if len(parts) == 2 and all(part.strip() for part in parts):
                # Valid org/repo format
                return self.success()
            else:
                return self.failure("Use format: org/repo (e.g., microsoft/vscode)")
        
        # Check for full URL format
        if value.startswith(('http://', 'https://', 'git://', 'ssh://')):
            # Accept URLs that contain common Git hosting domains or end with .git
            git_indicators = ['github.com', 'gitlab.com', 'bitbucket.org', '.git']
            if any(indicator in value for indicator in git_indicators):
                return self.success()
            else:
                return self.failure("Please use a valid Git repository URL")
        
        return self.failure("Use either 'org/repo' format or full Git URL")


class RepoAddDialog(ModalScreen):
    """➕ PAC-MAN's Repository Addition Dialog"""
    
    BINDINGS = [
        Binding("escape", "dismiss", "Cancel", show=True),
        Binding("ctrl+s", "add_repository", "Add Repository", show=True),
        Binding("enter", "add_repository", "Add Repository", show=False),
    ]
    
    DEFAULT_CSS = """
    RepoAddDialog {
        align: center middle;
    }
    
    #add-repo-container {
        width: 70%;
        height: 70%;
        background: $surface;
        border: thick $primary;
    }
    
    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1;
    }
    
    .input-row {
        height: auto;
        margin: 1 0;
    }
    
    .input-label {
        width: 25%;
        text-align: right;
        padding-right: 2;
        color: $accent;
    }
    
    .input-field {
        width: 75%;
    }
    
    .button-row {
        height: auto;
        margin: 2 1;
        align: center middle;
    }
    
    .progress-panel {
        border: solid $primary;
        padding: 1;
        margin: 1;
        height: 8;
    }
    
    .add-log {
        height: 6;
        border: solid $primary;
    }
    
    .help-text {
        color: $text-muted;
        margin: 1;
        text-align: center;
    }
    
    .examples {
        color: $text-muted;
        margin: 1;
        padding: 1;
        border: solid $primary;
    }
    """
    
    def __init__(self, manager=None, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.is_adding = False
    
    def compose(self) -> ComposeResult:
        """➕ Build repository add dialog interface"""
        
        with Container(id="add-repo-container"):
            yield Label("🟡 PAC-MAN Repository Wizard 🟡", classes="title")
            
            # Help text
            yield Static(
                "Add a new repository to PAC-MAN's semantic maze collection!",
                classes="help-text"
            )
            
            # Input fields
            with Horizontal(classes="input-row"):
                yield Label("Repository:", classes="input-label")
                yield Input(
                    placeholder="org/repo or full Git URL",
                    id="repo-input",
                    classes="input-field",
                    validators=[RepoUrlValidator()]
                )
            
            # Options
            with Horizontal(classes="input-row"):
                yield Label("Options:", classes="input-label")
                with Vertical(classes="input-field"):
                    yield Checkbox("Discover releases", value=True, id="discover-releases")
            
            # Examples
            yield Static(
                "📋 Examples:\n"
                "  • microsoft/vscode\n"
                "  • python/cpython\n"
                "  • https://github.com/octocat/Hello-World.git",
                classes="examples"
            )
            
            # Progress panel (initially hidden)
            with Container(classes="progress-panel", id="progress-panel") as progress_container:
                progress_container.display = False
                yield Label("➕ Adding Repository...")
                yield ProgressBar(id="add-progress")
                yield Log(classes="add-log", id="add-log")
            
            # Action buttons
            with Horizontal(classes="button-row"):
                yield Button("❌ Cancel", id="cancel-btn", variant="error")
                yield Button("🚀 Add & Clone Repository", id="add-btn", variant="primary")
    
    def on_mount(self) -> None:
        """➕ Initialize the dialog"""
        # Focus on the input field
        repo_input = self.query_one("#repo-input", Input)
        repo_input.focus()
    
    @on(Button.Pressed, "#cancel-btn")
    def on_cancel_pressed(self) -> None:
        """➕ Handle cancel button"""
        if not self.is_adding:
            self.dismiss()
        else:
            # TODO: Cancel ongoing operation
            self.app.notify("🟡 Repository addition cancellation not yet implemented", severity="warning")
    
    @on(Button.Pressed, "#add-btn")
    def on_add_pressed(self) -> None:
        """➕ Handle add repository button"""
        if not self.is_adding:
            self.add_repository()
    
    @on(Input.Submitted, "#repo-input")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """➕ Handle Enter key in input field"""
        if not self.is_adding:
            self.add_repository()
    
    def action_add_repository(self) -> None:
        """➕ Add repository action (keyboard shortcut)"""
        if not self.is_adding:
            self.add_repository()
    
    def add_repository(self) -> None:
        """➕ Start the repository addition process"""
        repo_input = self.query_one("#repo-input", Input)
        repo_url = repo_input.value.strip()
        
        if not repo_url:
            self.app.notify("🟡 Please enter a repository URL or org/repo", severity="error")
            repo_input.focus()
            return
        
        # Validate input
        validator = RepoUrlValidator()
        result = validator.validate(repo_url)
        if not result.is_valid:
            self.app.notify(f"🟡 {result.failure_descriptions[0]}", severity="error")
            repo_input.focus()
            return
        
        # Get options - always clone immediately
        clone_immediately = True  # Always clone
        discover_releases = self.query_one("#discover-releases", Checkbox).value
        
        # Start the addition process
        self.is_adding = True
        
        # Show progress panel
        progress_panel = self.query_one("#progress-panel")
        progress_panel.display = True
        
        # Update button states
        add_btn = self.query_one("#add-btn", Button)
        add_btn.disabled = True
        add_btn.label = "🔄 Adding & Cloning..."
        
        # Start the async operation
        self.perform_add_repository(repo_url, clone_immediately, discover_releases)
    
    @work(exclusive=True)
    async def perform_add_repository(self, repo_url: str, clone_immediately: bool, discover_releases: bool) -> None:
        """➕ Perform the actual repository addition"""
        progress_bar = self.query_one("#add-progress", ProgressBar)
        log_widget = self.query_one("#add-log", Log)
        
        try:
            log_widget.write_line(f"🟡 Adding repository: {repo_url}")
            progress_bar.progress = 0.1
            
            if not self.manager:
                raise Exception("No manager available")
            
            # Step 1: Add repository
            log_widget.write_line("🟡 PAC-MAN is entering the new maze...")
            progress_bar.progress = 0.2
            
            # Call the actual repository manager
            result = await self.manager.repo_manager.add_repository(
                repo_url,
                clone_immediately=clone_immediately,
                discover_releases=discover_releases
            )
            
            progress_bar.progress = 0.6
            log_widget.write_line(f"✅ Repository added: {result.org_repo}")
            
            if clone_immediately:
                log_widget.write_line("🟡 Cloning repository...")
                progress_bar.progress = 0.8
                # Cloning is handled by the repo manager
                
            if discover_releases:
                log_widget.write_line("🟡 Discovering releases...")
                progress_bar.progress = 0.9
                # Release discovery is handled by the repo manager
            
            progress_bar.progress = 1.0
            log_widget.write_line("🎉 Repository successfully added to PAC-MAN's maze!")
            
            # Show success notification
            self.app.notify(f"🟡 Repository {repo_url} added successfully!", severity="success")
            
            # Auto-dismiss after success
            await asyncio.sleep(2)
            self.dismiss(result=result)
            
        except Exception as e:
            logger.error(f"Repository addition failed: {e}")
            log_widget.write_line(f"❌ Failed to add repository: {e}")
            self.app.notify(f"🟡 Failed to add repository: {e}", severity="error")
            progress_bar.progress = 0
        
        finally:
            self.is_adding = False
            add_btn = self.query_one("#add-btn", Button)
            add_btn.disabled = False
            add_btn.label = "🚀 Add & Clone Repository"


# Helper function to show the repository add dialog
def show_repo_add_dialog(app, manager=None, callback=None):
    """➕ Show the repository addition dialog"""
    def on_dialog_dismissed(result):
        """Handle dialog dismissal"""
        if result:
            # Repository was added
            app.notify("🟡 Repository added successfully!", severity="success")
        
        # Call the provided callback if any
        if callback:
            callback(result)
    
    dialog = RepoAddDialog(manager=manager)
    app.push_screen(dialog, callback=on_dialog_dismissed)