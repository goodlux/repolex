"""
📤 PAC-MAN's Export Configuration Dialog 📤

The ultimate export configuration screen - PAC-MAN style!
Configure and execute exports with full power and precision!

WAKA WAKA! Chomping data into perfect export formats!
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

from textual import on, work
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Static, Button, Input, Select, RadioSet, RadioButton,
    Label, Log, ProgressBar, Checkbox, DirectoryTree
)
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.validation import Function, ValidationResult, Validator

logger = logging.getLogger(__name__)


class ExportPathValidator(Validator):
    """🟡 PAC-MAN's path validator for export destinations"""
    
    def validate(self, value: str) -> ValidationResult:
        """Validate export path"""
        if not value.strip():
            return self.failure("Export path cannot be empty")
        
        try:
            path = Path(value).expanduser()
            parent = path.parent
            
            if not parent.exists():
                return self.failure("Parent directory does not exist")
            
            if not parent.is_dir():
                return self.failure("Parent path is not a directory")
                
            return self.success()
            
        except Exception as e:
            return self.failure(f"Invalid path: {e}")


class ExportConfigPanel(Container):
    """📤 Export configuration panel with all options"""
    
    DEFAULT_CSS = """
    ExportConfigPanel {
        border: solid $primary;
        padding: 1;
        margin: 1;
        height: auto;
    }
    
    .config-row {
        height: auto;
        margin: 1 0;
    }
    
    .config-label {
        width: 20%;
        text-align: right;
        padding-right: 2;
        color: $accent;
    }
    
    .config-input {
        width: 80%;
    }
    """
    
    selected_repo = reactive("")
    selected_release = reactive("")
    export_format = reactive("opml")
    export_path = reactive("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.available_repos = []
        self.available_releases = []
    
    def compose(self) -> ComposeResult:
        """📤 Build export configuration interface"""
        
        yield Label("📤 PAC-MAN Export Configuration", classes="title")
        
        # Repository Selection
        with Horizontal(classes="config-row"):
            yield Label("Repository:", classes="config-label")
            yield Select(
                options=[("Select a repository...", "")],
                id="repo-select",
                classes="config-input"
            )
        
        # Release Selection  
        with Horizontal(classes="config-row"):
            yield Label("Release:", classes="config-label")
            yield Select(
                options=[("Select a release...", "")],
                id="release-select",
                classes="config-input",
                disabled=True
            )
        
        # Export Format
        with Horizontal(classes="config-row"):
            yield Label("Format:", classes="config-label")
            with RadioSet(id="format-radio", classes="config-input"):
                yield RadioButton("📄 OPML (Outline)", value=True, id="opml")
                yield RadioButton("📦 MsgPack (Compact)", id="msgpack")
                yield RadioButton("📚 Documentation (MDX/HTML)", id="docs")
        
        # Export Path
        with Horizontal(classes="config-row"):
            yield Label("Output Path:", classes="config-label")
            yield Input(
                placeholder="~/exports/my-export.opml",
                id="path-input",
                classes="config-input",
                validators=[ExportPathValidator()]
            )
        
        # Additional Options
        with Horizontal(classes="config-row"):
            yield Label("Options:", classes="config-label")
            with Vertical(classes="config-input"):
                yield Checkbox("Include function signatures", value=True, id="include-signatures")
                yield Checkbox("Include docstrings", value=True, id="include-docs")
                yield Checkbox("Include git metadata", value=False, id="include-git")
    
    def update_repositories(self, repos: List[Dict[str, Any]]) -> None:
        """📤 Update available repositories"""
        self.available_repos = repos
        
        repo_select = self.query_one("#repo-select", Select)
        
        options = [("Select a repository...", "")]
        for repo in repos:
            org_repo = repo.get('org_repo', f"{repo.get('org', '')}/{repo.get('name', '')}")
            options.append((org_repo, org_repo))
        
        repo_select.set_options(options)
    
    @on(Select.Changed, "#repo-select")
    def on_repo_selected(self, event: Select.Changed) -> None:
        """📤 Handle repository selection"""
        if event.value:
            self.selected_repo = str(event.value)
            # Enable release selection and load releases
            release_select = self.query_one("#release-select", Select)
            release_select.disabled = False
            
            # TODO: Load actual releases for selected repo
            # For now, show placeholder releases
            release_options = [
                ("Latest release", "latest"),
                ("v1.0.0", "v1.0.0"),
                ("v0.9.0", "v0.9.0"),
            ]
            release_select.set_options(release_options)
        else:
            self.selected_repo = ""
            release_select = self.query_one("#release-select", Select)
            release_select.disabled = True
            release_select.set_options([("Select a release...", "")])
    
    @on(Select.Changed, "#release-select")
    def on_release_selected(self, event: Select.Changed) -> None:
        """📤 Handle release selection"""
        self.selected_release = str(event.value) if event.value else ""
    
    @on(RadioSet.Changed, "#format-radio")
    def on_format_changed(self, event: RadioSet.Changed) -> None:
        """📤 Handle format selection"""
        if event.pressed:
            self.export_format = str(event.pressed.id)
            
            # Update path extension suggestion
            path_input = self.query_one("#path-input", Input)
            current_path = path_input.value
            
            # Suggest appropriate extension
            if self.export_format == "opml":
                suggested_ext = ".opml"
            elif self.export_format == "msgpack":
                suggested_ext = ".msgpack"
            elif self.export_format == "docs":
                suggested_ext = ".zip"
            else:
                suggested_ext = ""
            
            if not current_path and self.selected_repo:
                # Suggest a default path
                repo_name = self.selected_repo.replace('/', '-')
                path_input.value = f"~/exports/{repo_name}-{self.selected_release or 'latest'}{suggested_ext}"
    
    @on(Input.Changed, "#path-input")
    def on_path_changed(self, event: Input.Changed) -> None:
        """📤 Handle path input changes"""
        self.export_path = event.value
    
    def get_export_config(self) -> Dict[str, Any]:
        """📤 Get current export configuration"""
        
        # Get checkbox values
        include_signatures = self.query_one("#include-signatures", Checkbox).value
        include_docs = self.query_one("#include-docs", Checkbox).value
        include_git = self.query_one("#include-git", Checkbox).value
        
        return {
            "repository": self.selected_repo,
            "release": self.selected_release,
            "format": self.export_format,
            "output_path": self.export_path,
            "options": {
                "include_signatures": include_signatures,
                "include_docs": include_docs,
                "include_git": include_git
            }
        }


class ExportProgressPanel(Container):
    """📤 Export progress display panel"""
    
    DEFAULT_CSS = """
    ExportProgressPanel {
        border: solid $success;
        padding: 1;
        margin: 1;
        height: 10;
    }
    """
    
    def compose(self) -> ComposeResult:
        """📤 Build progress interface"""
        yield Label("📤 Export Progress")
        yield ProgressBar(id="export-progress")
        yield Log(id="export-log", classes="export-log")
    
    def update_progress(self, progress: float, message: str) -> None:
        """📤 Update export progress"""
        progress_bar = self.query_one("#export-progress", ProgressBar)
        progress_bar.progress = progress
        
        log_widget = self.query_one("#export-log", Log)
        log_widget.write_line(f"🟡 {message}")


class ExportDialog(ModalScreen):
    """📤 PAC-MAN's Export Configuration Dialog"""
    
    BINDINGS = [
        Binding("escape", "dismiss", "Cancel", show=True),
        Binding("ctrl+s", "start_export", "Start Export", show=True),
    ]
    
    DEFAULT_CSS = """
    ExportDialog {
        align: center middle;
    }
    
    #export-container {
        width: 80%;
        height: 80%;
        background: $surface;
        border: thick $primary;
    }
    
    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin: 1;
    }
    
    .button-row {
        height: auto;
        margin: 1;
        align: center middle;
    }
    
    .export-log {
        height: 6;
        border: solid $primary;
    }
    """
    
    def __init__(self, manager=None, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.config_panel = None
        self.progress_panel = None
        self.is_exporting = False
    
    def compose(self) -> ComposeResult:
        """📤 Build export dialog interface"""
        
        with Container(id="export-container"):
            yield Label("🟡 PAC-MAN Export Wizard 🟡", classes="title")
            
            # Configuration Panel
            self.config_panel = ExportConfigPanel()
            yield self.config_panel
            
            # Progress Panel (initially hidden)
            self.progress_panel = ExportProgressPanel()
            self.progress_panel.display = False
            yield self.progress_panel
            
            # Action Buttons
            with Horizontal(classes="button-row"):
                yield Button("❌ Cancel", id="cancel-btn", variant="error")
                yield Button("🚀 Start Export", id="export-btn", variant="primary")
    
    def on_mount(self) -> None:
        """📤 Initialize export dialog"""
        if self.manager:
            # Load actual repositories from manager
            self.load_repositories()
    
    @work(exclusive=True)
    async def load_repositories(self) -> None:
        """📤 Load repositories from manager"""
        try:
            repos = await self.manager.repo_manager.list_repositories()
            
            # Convert RepoInfo objects to format expected by config panel
            repo_data = []
            for repo in repos:
                # Extract org and name from org_repo string
                if '/' in repo.org_repo:
                    org, name = repo.org_repo.split('/', 1)
                    repo_data.append({
                        "org": org,
                        "name": name,
                        "org_repo": repo.org_repo,
                        "status": repo.status,
                        "releases": repo.releases
                    })
            
            self.config_panel.update_repositories(repo_data)
            
        except Exception as e:
            logger.error(f"Failed to load repositories for export dialog: {e}")
            # Fallback to sample data if loading fails
            sample_repos = [
                {"org": "example", "name": "repo", "org_repo": "example/repo"},
            ]
            self.config_panel.update_repositories(sample_repos)
    
    @on(Button.Pressed, "#cancel-btn")
    def on_cancel_pressed(self) -> None:
        """📤 Handle cancel button"""
        if not self.is_exporting:
            self.dismiss()
        else:
            # TODO: Cancel ongoing export
            self.app.notify("🟡 Export cancellation not yet implemented", severity="warning")
    
    @on(Button.Pressed, "#export-btn")
    def on_export_pressed(self) -> None:
        """📤 Handle export button"""
        if not self.is_exporting:
            self.start_export()
    
    def action_start_export(self) -> None:
        """📤 Start export process"""
        self.start_export()
    
    def start_export(self) -> None:
        """📤 Start the export process"""
        config = self.config_panel.get_export_config()
        
        # Validate configuration
        if not config["repository"]:
            self.app.notify("🟡 Please select a repository", severity="error")
            return
        
        if not config["release"]:
            self.app.notify("🟡 Please select a release", severity="error")
            return
        
        if not config["output_path"]:
            self.app.notify("🟡 Please specify an output path", severity="error")
            return
        
        # Start export process
        self.is_exporting = True
        
        # Show progress panel
        self.progress_panel.display = True
        
        # Update button states
        export_btn = self.query_one("#export-btn", Button)
        export_btn.disabled = True
        export_btn.label = "🔄 Exporting..."
        
        # Start the export (mock for now)
        self.perform_export(config)
    
    @work(exclusive=True)
    async def perform_export(self, config: Dict[str, Any]) -> None:
        """📤 Perform the actual export operation"""
        try:
            # Mock export process with progress updates
            steps = [
                "Initializing export...",
                "Loading repository data...",
                "Processing semantic graphs...",
                "Generating output format...",
                "Writing output file...",
                "Export completed!"
            ]
            
            for i, step in enumerate(steps):
                progress = (i + 1) / len(steps)
                self.progress_panel.update_progress(progress, step)
                
                # Simulate work
                await asyncio.sleep(1)
            
            # TODO: Call actual export functionality
            # if self.manager:
            #     await self.manager.export_data(
            #         config["repository"],
            #         config["release"], 
            #         config["format"],
            #         config["output_path"],
            #         **config["options"]
            #     )
            
            self.app.notify(f"🟡 Export completed: {config['output_path']}", severity="success")
            
            # Auto-dismiss after successful export
            await asyncio.sleep(2)
            self.dismiss()
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            self.progress_panel.update_progress(0, f"Export failed: {e}")
            self.app.notify(f"🟡 Export failed: {e}", severity="error")
        
        finally:
            self.is_exporting = False
            export_btn = self.query_one("#export-btn", Button)
            export_btn.disabled = False
            export_btn.label = "🚀 Start Export"


# Helper function to launch export dialog
def show_export_dialog(app, manager=None):
    """📤 Show the export configuration dialog"""
    dialog = ExportDialog(manager=manager)
    app.push_screen(dialog)