# CodeDoc CLI/TUI Complete Implementation Specification

*Production-ready command structure for both CLI and TUI interfaces with comprehensive error handling, security, and user experience*

## 🎯 Core Design Principles

### **Command Pattern: Group-Action-Target**
```bash
codedoc {repo|graph|export|query} <action> <target> [options]
```

### **Command Groups**
- `repo` - Repository file operations (clone, update, remove)
- `graph` - Semantic analysis operations (parse, rebuild, remove graphs)
- `export` - Generate output files (opml, msgpack, docs)
- `query` - Search and query operations (sparql, functions)
- `show` - Display information (config, status)
- `update` - Modify settings (config)

### **Standardized Actions (Within Groups)**
- `add` - Create new resource
- `remove` - Delete resource  
- `list` - Show resources
- `show` - Show detailed info about specific resource
- `update` - Refresh/sync existing resource

## 📋 Complete Command Reference

### **Repository Management (File Operations)**
```bash
codedoc repo add <org/repo>             # Clone repository, download releases
codedoc repo remove <org/repo>          # Remove repository files entirely  
codedoc repo list                       # List all repositories
codedoc repo show <org/repo>            # Show repository details
codedoc repo update <org/repo>          # Git pull, fetch new releases
```

**Examples:**
```bash
codedoc repo add pixeltable/pixeltable              # Clone repo, get all releases
codedoc repo show pixeltable/pixeltable             # Show available releases
codedoc repo update pixeltable/pixeltable           # Git pull for updates
codedoc repo remove pixeltable/pixeltable           # Delete repo files
```

### **Graph Operations (Semantic Analysis)**
```bash
codedoc graph add <org/repo> [release]   # Parse and store in semantic database
codedoc graph remove <org/repo> [release] # Remove from semantic database
codedoc graph list [org/repo]           # List graphs in database
codedoc graph show <org/repo> [release] # Show graph details/statistics
codedoc graph update <org/repo> [release] # Reparse graphs (nuclear rebuild)
```

**Examples:**
```bash
codedoc graph add pixeltable/pixeltable v0.4.14     # Parse specific release
codedoc graph add pixeltable/pixeltable             # Parse latest release
codedoc graph remove pixeltable/pixeltable v0.4.14  # Remove specific release graphs
codedoc graph remove pixeltable/pixeltable          # Remove ALL graphs for repo
codedoc graph update pixeltable/pixeltable v0.4.14  # Nuclear rebuild graphs
```

### **Export Operations**

#### **OPML Export**
```bash
codedoc export opml <org/repo> <tag> [--output <path>]
```
- **Default Output**: `~/.codedoc/exports/<org>/<repo>/<tag>.opml`
- **Custom Output**: `--output /path/to/custom/location.opml`

#### **MsgPack Export**
```bash
codedoc export msgpack <org/repo> <tag> [--output <path>]
```
- **Default Output**: `~/.codedoc/exports/<org>/<repo>/<tag>.msgpack`
- **Custom Output**: `--output /path/to/custom/location.msgpack`

#### **Documentation Export**
```bash
codedoc export docs <org/repo> <tag> --format <format> --output <directory>
```
- **Formats**: `mdx`, `html`, `markdown`
- **Required**: `--output` directory path
- **Optional**: `--template <template-name>` for custom styling

**Examples:**
```bash
# Export to default locations
codedoc export opml pixeltable/pixeltable v0.4.14
# Output: ~/.codedoc/exports/pixeltable/pixeltable/v0.4.14.opml

# Export to custom location  
codedoc export msgpack pixeltable/pixeltable v0.4.14 --output ./semantic-package.msgpack

# Export documentation
codedoc export docs pixeltable/pixeltable v0.4.14 --format mdx --output ./docs/sdk/latest/
codedoc export docs pixeltable/pixeltable v0.4.14 --format html --output ./website/api/ --template mintlify
```

### **Query Operations**
```bash
codedoc query sparql "<query>" [--format <format>] [--output <file>]
codedoc query functions <search-term> [--repo <org/repo>] [--release <tag>]
```

**Query Formats**: `table`, `json`, `turtle`, `csv`

**Examples:**
```bash
codedoc query sparql "SELECT ?name WHERE { ?f woc:hasName ?name }" --format table
codedoc query functions "create table" --repo pixeltable/pixeltable
codedoc query functions "image processing" --repo pixeltable/pixeltable --release v0.4.14
```

### **System Management**
```bash
codedoc show config                         # Show current configuration
codedoc update config <key> <value>         # Update configuration
codedoc show status                         # Show system status
codedoc remove everything                   # Nuclear option (with confirmation)
```

**Examples:**
```bash
codedoc show config
codedoc update config github-token ghp_xxxxxxxxxxxx
codedoc update config storage-path ~/my-codedoc-data
```

## 🛡️ Production-Ready Error Handling

### **Comprehensive Error Hierarchy**
```python
# codedoc/models/exceptions.py
class CodeDocError(Exception):
    """Base exception for all CodeDoc errors with user-friendly messages."""
    def __init__(self, message: str, suggestions: List[str] = None):
        super().__init__(message)
        self.message = message
        self.suggestions = suggestions or []

class GitError(CodeDocError):
    """Git operations failed (clone, checkout, pull)."""
    pass

class ProcessingError(CodeDocError):
    """AST parsing or semantic analysis failed."""
    pass

class StorageError(CodeDocError):
    """Oxigraph operations failed."""
    pass

class ValidationError(CodeDocError):
    """Input validation failed."""
    pass

class SecurityError(CodeDocError):
    """Security validation failed."""
    pass

class ExportError(CodeDocError):
    """Export generation failed."""
    pass

class NetworkError(CodeDocError):
    """Network operations failed."""
    pass

class ConfigurationError(CodeDocError):
    """Configuration validation failed."""
    pass
```

### **Error Handler Decorator**
```python
# codedoc/cli/error_handling.py
import click
from rich.console import Console
from codedoc.models.exceptions import *

console = Console()

def handle_errors(func):
    """Decorator to handle common errors with user-friendly messages."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            console.print(f"❌ [bold red]Validation Error:[/bold red] {e.message}")
            if e.suggestions:
                console.print("💡 [bold blue]Suggestions:[/bold blue]")
                for suggestion in e.suggestions:
                    console.print(f"   • {suggestion}")
            raise click.Abort()
        except SecurityError as e:
            console.print(f"🛡️ [bold red]Security Error:[/bold red] {e.message}")
            if e.suggestions:
                console.print("💡 [bold blue]Suggestions:[/bold blue]")
                for suggestion in e.suggestions:
                    console.print(f"   • {suggestion}")
            raise click.Abort()
        except GitError as e:
            console.print(f"🔧 [bold red]Git Error:[/bold red] {e.message}")
            if e.suggestions:
                console.print("💡 [bold blue]Try this:[/bold blue]")
                for suggestion in e.suggestions:
                    console.print(f"   • {suggestion}")
            raise click.Abort()
        except NetworkError as e:
            console.print(f"🌐 [bold red]Network Error:[/bold red] {e.message}")
            if e.suggestions:
                console.print("💡 [bold blue]Try this:[/bold blue]")
                for suggestion in e.suggestions:
                    console.print(f"   • {suggestion}")
            raise click.Abort()
        except CodeDocError as e:
            console.print(f"💥 [bold red]Error:[/bold red] {e.message}")
            if e.suggestions:
                console.print("💡 [bold blue]Try this:[/bold blue]")
                for suggestion in e.suggestions:
                    console.print(f"   • {suggestion}")
            raise click.Abort()
        except Exception as e:
            console.print(f"💥 [bold red]Unexpected Error:[/bold red] {str(e)}")
            console.print("💡 [bold blue]This might be a bug. Please check logs for details.[/bold blue]")
            logger.exception("Unexpected error in CLI")
            raise click.Abort()
    return wrapper
```

## 🔒 Input Validation & Security

### **Comprehensive Validation**
```python
# codedoc/utils/validation.py
import re
from pathlib import Path
from typing import Optional
from codedoc.models.exceptions import ValidationError, SecurityError

def validate_org_repo(org_repo: str) -> None:
    """
    Validate org/repo format and prevent security issues.
    
    Raises:
        ValidationError: If format is invalid
        SecurityError: If contains dangerous characters
    """
    if not org_repo or not isinstance(org_repo, str):
        raise ValidationError(
            "org/repo must be a non-empty string",
            suggestions=["Use format: organization/repository"]
        )
    
    # Check format
    if not re.match(r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$', org_repo):
        raise ValidationError(
            f"Invalid org/repo format: {org_repo}",
            suggestions=[
                "Use format: organization/repository",
                "Only alphanumeric, dots, dashes, underscores allowed",
                "Examples: pixeltable/pixeltable, microsoft/typescript"
            ]
        )
    
    # Security checks
    if '..' in org_repo or org_repo.startswith('/') or '\\' in org_repo:
        raise SecurityError(
            "Invalid characters detected in org/repo",
            suggestions=["Avoid path traversal characters (.. / \\)"]
        )
    
    # Length checks
    if len(org_repo) > 100:
        raise ValidationError(
            "Repository name too long (max 100 characters)",
            suggestions=["Use shorter organization/repository names"]
        )

def validate_release_tag(tag: str) -> None:
    """Validate release tag format."""
    if not tag or not isinstance(tag, str):
        raise ValidationError(
            "Release tag must be a non-empty string",
            suggestions=["Examples: v1.0.0, 2.1.3, release-2024-01"]
        )
    
    # Basic sanity checks
    if len(tag) > 100:
        raise ValidationError(
            "Release tag too long (max 100 characters)",
            suggestions=["Use standard versioning like v1.0.0"]
        )
    
    if any(char in tag for char in [' ', '\n', '\t']):
        raise ValidationError(
            "Release tag cannot contain whitespace",
            suggestions=["Use hyphens or dots instead of spaces"]
        )
    
    # Security check
    if '..' in tag or '/' in tag or '\\' in tag:
        raise SecurityError(
            "Invalid characters in release tag",
            suggestions=["Use only letters, numbers, dots, hyphens"]
        )

def validate_file_path(path: Path, base_path: Path) -> None:
    """Validate file path is within allowed base directory."""
    try:
        resolved_path = path.resolve()
        resolved_base = base_path.resolve()
        resolved_path.relative_to(resolved_base)
    except ValueError:
        raise SecurityError(
            f"Path {path} is outside allowed directory {base_path}",
            suggestions=[
                "Use paths within ~/.codedoc/ directory",
                "Avoid path traversal attempts"
            ]
        )

def validate_sparql_query(query: str) -> None:
    """Basic SPARQL query validation for security."""
    if not query or not isinstance(query, str):
        raise ValidationError(
            "SPARQL query must be a non-empty string",
            suggestions=["Example: SELECT ?name WHERE { ?f woc:hasName ?name }"]
        )
    
    # Length check
    if len(query) > 10000:
        raise ValidationError(
            "SPARQL query too long (max 10000 characters)",
            suggestions=["Break complex queries into smaller parts"]
        )
    
    # Basic security checks
    dangerous_keywords = ['UPDATE', 'DELETE', 'INSERT', 'DROP', 'CREATE']
    query_upper = query.upper()
    
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            raise SecurityError(
                f"Dangerous SPARQL operation detected: {keyword}",
                suggestions=[
                    "Only SELECT queries are allowed",
                    "Use read-only SPARQL operations"
                ]
            )
```

## 📊 Progress Indicators & User Experience

### **Progress Callback System**
```python
# codedoc/models/progress.py
from typing import Callable, Optional
from dataclasses import dataclass
from enum import Enum

class ProgressStage(Enum):
    INITIALIZING = "initializing"
    DOWNLOADING = "downloading"
    PARSING = "parsing"
    ANALYZING = "analyzing"
    STORING = "storing"
    EXPORTING = "exporting"
    COMPLETING = "completing"

@dataclass
class ProgressUpdate:
    percentage: int  # 0-100
    stage: ProgressStage
    message: str
    details: Optional[str] = None
    current_item: Optional[str] = None
    total_items: Optional[int] = None

ProgressCallback = Callable[[ProgressUpdate], None]

# codedoc/cli/progress.py
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from codedoc.models.progress import ProgressUpdate, ProgressCallback

def create_cli_progress_callback() -> ProgressCallback:
    """Create progress callback for CLI with rich progress bars."""
    
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    )
    
    task_id = None
    
    def update_progress(update: ProgressUpdate) -> None:
        nonlocal task_id
        
        if task_id is None:
            task_id = progress.add_task("Processing...", total=100)
            progress.start()
        
        description = f"{update.stage.value.title()}: {update.message}"
        if update.current_item and update.total_items:
            description += f" ({update.current_item}/{update.total_items})"
        
        progress.update(task_id, completed=update.percentage, description=description)
        
        if update.percentage >= 100:
            progress.stop()
    
    return update_progress
```

### **Streaming Export Operations**
```python
# codedoc/exporters/streaming_exporter.py
from typing import AsyncGenerator, Dict, Any
import asyncio
from pathlib import Path

class StreamingExporter:
    """Base class for streaming exports to handle large datasets."""
    
    async def stream_export(self, org_repo: str, release: str, output_path: Path, 
                          progress_callback: Optional[ProgressCallback] = None) -> Path:
        """Export with streaming to handle large repositories efficiently."""
        
        try:
            # Get total count for progress
            total_functions = await self.count_functions(org_repo, release)
            processed = 0
            
            with open(output_path, 'w') as f:
                # Write header
                await self.write_header(f)
                
                if progress_callback:
                    progress_callback(ProgressUpdate(
                        percentage=10,
                        stage=ProgressStage.EXPORTING,
                        message="Starting export",
                        total_items=total_functions
                    ))
                
                # Stream functions in chunks
                async for function_chunk in self.stream_functions(org_repo, release, chunk_size=50):
                    chunk_content = await self.format_chunk(function_chunk)
                    f.write(chunk_content)
                    
                    processed += len(function_chunk)
                    percentage = min(90, 10 + (processed / total_functions) * 80)
                    
                    if progress_callback:
                        progress_callback(ProgressUpdate(
                            percentage=int(percentage),
                            stage=ProgressStage.EXPORTING,
                            message="Exporting functions",
                            current_item=str(processed),
                            total_items=total_functions
                        ))
                
                # Write footer
                await self.write_footer(f)
                
                if progress_callback:
                    progress_callback(ProgressUpdate(
                        percentage=100,
                        stage=ProgressStage.COMPLETING,
                        message="Export complete"
                    ))
            
            return output_path
            
        except Exception as e:
            raise ExportError(
                f"Failed to export {org_repo} {release}",
                suggestions=[
                    "Check disk space",
                    "Verify output directory permissions",
                    "Try a different output location"
                ]
            ) from e
    
    async def stream_functions(self, org_repo: str, release: str, 
                             chunk_size: int = 50) -> AsyncGenerator[List[Dict[str, Any]], None]:
        """Stream functions in chunks to avoid memory issues."""
        
        offset = 0
        while True:
            chunk = await self.query_manager.get_functions_chunk(
                org_repo, release, offset=offset, limit=chunk_size
            )
            
            if not chunk:
                break
                
            yield chunk
            offset += chunk_size
            
            # Small delay to prevent overwhelming the database
            await asyncio.sleep(0.01)
```

## ⚙️ Configuration Management

### **Comprehensive Configuration System**
```python
# codedoc/models/config.py
from typing import Optional, Dict, Any, List
from pathlib import Path
from pydantic import BaseModel, Field, validator
import json

class CodeDocConfig(BaseModel):
    """System configuration with validation and defaults."""
    
    # Storage settings
    storage_path: Path = Field(default_factory=lambda: Path.home() / ".codedoc")
    database_path: Optional[Path] = None  # Defaults to storage_path / "graph"
    export_path: Optional[Path] = None    # Defaults to storage_path / "exports"
    
    # Authentication
    github_token: Optional[str] = None  # For private repositories
    
    # Logging
    log_level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    log_file: Optional[Path] = None  # Defaults to storage_path / "logs" / "codedoc.log"
    
    # Processing settings
    processing_timeout: int = Field(default=300, ge=30, le=3600)  # 30 seconds to 1 hour
    max_file_size_mb: int = Field(default=10, ge=1, le=100)  # Max file size to parse
    max_concurrent_parsers: int = Field(default=4, ge=1, le=16)
    
    # Export settings
    export_templates: Dict[str, str] = Field(default_factory=lambda: {
        "mdx": "default",
        "html": "clean",
        "markdown": "github"
    })
    
    # Performance settings
    cache_size_mb: int = Field(default=500, ge=100, le=2000)
    query_timeout: int = Field(default=30, ge=5, le=300)
    
    # Safety settings
    allow_large_repositories: bool = False  # Repositories with >10k files
    require_confirmation_for_destructive: bool = True
    backup_before_destructive: bool = True
    
    # Network settings
    request_timeout: int = Field(default=30, ge=5, le=120)
    max_retries: int = Field(default=3, ge=0, le=10)
    
    @validator('storage_path')
    def validate_storage_path(cls, v):
        """Ensure storage path is accessible."""
        path = Path(v).expanduser().resolve()
        try:
            path.mkdir(parents=True, exist_ok=True)
            return path
        except Exception as e:
            raise ValueError(f"Cannot create storage directory {path}: {e}")
    
    @validator('github_token')
    def validate_github_token(cls, v):
        """Basic GitHub token validation."""
        if v is not None:
            if not v.startswith(('ghp_', 'github_pat_')):
                raise ValueError("GitHub token should start with 'ghp_' or 'github_pat_'")
            if len(v) < 20:
                raise ValueError("GitHub token too short")
        return v
    
    class Config:
        use_enum_values = True
        validate_assignment = True

# codedoc/core/config_manager.py
class ConfigManager:
    """Manage system configuration with validation and migration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".codedoc" / "config" / "config.json"
        self._config: Optional[CodeDocConfig] = None
    
    async def load_config(self) -> CodeDocConfig:
        """Load configuration from file or create defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                
                # Handle config migration if needed
                data = self._migrate_config(data)
                
                self._config = CodeDocConfig(**data)
                logger.info(f"Loaded configuration from {self.config_path}")
                
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
                self._config = CodeDocConfig()
                await self.save_config()
        else:
            logger.info("No config file found, creating defaults")
            self._config = CodeDocConfig()
            await self.save_config()
        
        return self._config
    
    async def save_config(self) -> None:
        """Save current configuration to file."""
        if self._config:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert paths to strings for JSON serialization
            config_dict = self._config.dict()
            for key, value in config_dict.items():
                if isinstance(value, Path):
                    config_dict[key] = str(value)
            
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2, default=str)
            
            logger.info(f"Saved configuration to {self.config_path}")
    
    async def update_setting(self, key: str, value: str) -> bool:
        """Update a configuration setting with validation."""
        config = await self.load_config()
        
        try:
            # Get current config as dict
            current_data = config.dict()
            
            # Handle type conversion based on field type
            converted_value = self._convert_value(key, value, config)
            current_data[key] = converted_value
            
            # Validate new config
            new_config = CodeDocConfig(**current_data)
            
            self._config = new_config
            await self.save_config()
            logger.info(f"Updated config: {key} = {converted_value}")
            return True
            
        except Exception as e:
            raise ConfigurationError(
                f"Invalid config value for {key}: {e}",
                suggestions=[
                    f"Check valid values for {key}",
                    "Use 'codedoc show config' to see current settings"
                ]
            )
    
    def _convert_value(self, key: str, value: str, config: CodeDocConfig) -> Any:
        """Convert string value to appropriate type based on config field."""
        field = config.__fields__.get(key)
        if not field:
            raise ValueError(f"Unknown configuration key: {key}")
        
        field_type = field.type_
        
        # Handle different types
        if field_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        elif field_type == int:
            return int(value)
        elif field_type == Path:
            return Path(value).expanduser().resolve()
        elif field_type == str:
            return value
        else:
            # For complex types, try JSON parsing
            try:
                import json
                return json.loads(value)
            except:
                return value
    
    def _migrate_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle configuration migration between versions."""
        # Add any migration logic here for future config changes
        return data
```

## 🎨 Enhanced TUI Design

### **Rich Dashboard with Real-time Updates**
```python
# codedoc/tui/app.py
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, DataTable, Button, Input, Log
from textual.reactive import reactive
from textual import events
from rich.text import Text
from rich.panel import Panel

class CodeDocTUI(App):
    """Advanced TUI with real-time status updates and interactive features."""
    
    CSS_PATH = "app.css"
    TITLE = "CodeDoc - Semantic Code Intelligence"
    
    # Reactive attributes for real-time updates
    repositories_count = reactive(0)
    graphs_count = reactive(0)
    processing_status = reactive("idle")
    
    BINDINGS = [
        ("a", "add_repo", "Add Repository"),
        ("r", "remove_repo", "Remove Repository"),
        ("p", "parse_graphs", "Parse to Graphs"),
        ("e", "export_menu", "Export Menu"),
        ("q", "query_interface", "Query Interface"),
        ("c", "show_config", "Configuration"),
        ("h", "help", "Help"),
        ("ctrl+c", "quit", "Quit"),
    ]
    
    def __init__(self):
        super().__init__()
        self.core = CodeDocManager()
        self.current_repos = []
        self.selected_repo = None
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Horizontal():
            # Left panel - Repository browser
            with Vertical(classes="left-panel"):
                yield Static("📚 Repositories", classes="panel-title")
                yield DataTable(id="repos-table")
                yield Button("Add Repository", id="add-repo-btn", variant="primary")
            
            # Center panel - Main content
            with Vertical(classes="center-panel"):
                yield Static("🧠 Processing Status", classes="panel-title")
                yield Static(id="status-display")
                yield Log(id="activity-log")
            
            # Right panel - Quick actions
            with Vertical(classes="right-panel"):
                yield Static("🔧 Quick Actions", classes="panel-title")
                yield Button("Parse Latest", id="parse-btn")
                yield Button("Export OPML", id="export-opml-btn")
                yield Button("Export MsgPack", id="export-msgpack-btn")
                yield Button("Query Functions", id="query-btn")
                yield Button("System Status", id="status-btn")
        
        yield Footer()
    
    async def on_mount(self) -> None:
        """Initialize TUI with current system state."""
        await self.refresh_repositories()
        await self.refresh_status()
        
        # Set up periodic refresh
        self.set_interval(5.0, self.refresh_status)
    
    async def refresh_repositories(self) -> None:
        """Refresh repository list."""
        try:
            repos = await self.core.repo_list()
            self.current_repos = repos
            self.repositories_count = len(repos)
            
            # Update table
            table = self.query_one("#repos-table", DataTable)
            table.clear()
            table.add_columns("Repository", "Releases", "Graphs", "Status")
            
            for repo in repos:
                status_icon = "✅" if repo.status == "ready" else "⚠️" if repo.status == "processing" else "❌"
                table.add_row(
                    repo.org_repo,
                    str(len(repo.releases)),
                    str(getattr(repo, 'graphs_count', 0)),
                    status_icon
                )
                
        except Exception as e:
            self.log_activity(f"❌ Error refreshing repositories: {e}")
    
    async def refresh_status(self) -> None:
        """Refresh system status display."""
        try:
            status = await self.core.show_status()
            
            status_text = Text()
            status_text.append(f"📊 Database: {status.database_size_mb:.1f}MB\n")
            status_text.append(f"🗂️ Repositories: {status.repository_count}\n")
            status_text.append(f"📈 Graphs: {status.graph_count}\n")
            status_text.append(f"📤 Exports: {status.export_count}\n")
            
            if status.recent_errors:
                status_text.append(f"⚠️ Recent Errors: {len(status.recent_errors)}\n", style="red")
            
            status_display = self.query_one("#status-display", Static)
            status_display.update(Panel(status_text, title="System Status", border_style="blue"))
            
        except Exception as e:
            self.log_activity(f"❌ Error refreshing status: {e}")
    
    def log_activity(self, message: str) -> None:
        """Add message to activity log."""
        log = self.query_one("#activity-log", Log)
        log.write_line(message)
    
    # Action handlers
    async def action_add_repo(self) -> None:
        """Add repository action."""
        org_repo = await self.get_text_input("Enter repository (org/repo):")
        if org_repo:
            try:
                validate_org_repo(org_repo)
                self.log_activity(f"🔄 Adding repository {org_repo}...")
                
                # Create progress callback
                def progress_callback(update: ProgressUpdate):
                    self.log_activity(f"[{update.percentage}%] {update.message}")
                
                result = await self.core.repo_add(org_repo, progress_callback=progress_callback)
                self.log_activity(f"✅ Added {org_repo}: {len(result.releases)} releases found")
                await self.refresh_repositories()
                
            except (ValidationError, SecurityError) as e:
                self.log_activity(f"❌ Validation error: {e.message}")
                for suggestion in e.suggestions:
                    self.log_activity(f"💡 {suggestion}")
            except Exception as e:
                self.log_activity(f"❌ Error adding repository: {e}")
    
    async def action_parse_graphs(self) -> None:
        """Parse repository to graphs."""
        if not self.selected_repo:
            selected_repo = await self.select_repository()
            if not selected_repo:
                return
        else:
            selected_repo = self.selected_repo
        
        try:
            self.log_activity(f"🧠 Parsing {selected_repo} to semantic graphs...")
            
            def progress_callback(update: ProgressUpdate):
                self.log_activity(f"[{update.percentage}%] {update.stage.value}: {update.message}")
            
            result = await self.core.graph_add(selected_repo, progress_callback=progress_callback)
            self.log_activity(f"✅ Parsed {selected_repo}: {result.functions_found} functions, {result.graphs_created} graphs")
            await self.refresh_repositories()
            
        except Exception as e:
            self.log_activity(f"❌ Error parsing graphs: {e}")
    
    async def get_text_input(self, prompt: str) -> Optional[str]:
        """Get text input from user via modal dialog."""
        # Implement modal dialog for text input
        # This would be a more complex widget implementation
        pass
    
    async def select_repository(self) -> Optional[str]:
        """Let user select from available repositories."""
        # Implement repository selection dialog
        pass
```

## 💾 Technical Stack & Dependencies

### **Modern Python Packaging with uv**
```toml
# pyproject.toml
[project]
name = "codedoc"
version = "0.1.0"
description = "Semantic Code Intelligence System"
authors = [
    {name = "CodeDoc Team", email = "team@codedoc.dev"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"

dependencies = [
    # CLI and TUI frameworks
    "click>=8.0.0",           # Robust CLI framework
    "textual>=0.50.0",        # Modern TUI framework
    "rich>=13.0.0",           # Beautiful terminal output
    
    # Core functionality
    "pyoxigraph>=0.4.0",      # RDF database
    "GitPython>=3.1.0",       # Git operations
    "msgpack>=1.0.0",         # Compact serialization
    "lxml>=4.9.0",            # XML processing for OPML
    
    # Data handling and validation
    "pydantic>=2.0.0",        # Data validation and settings
    "aiofiles>=23.0.0",       # Async file operations
    "httpx>=0.25.0",          # Modern HTTP client
    
    # Logging and monitoring
    "loguru>=0.7.0",          # Enhanced logging
    "psutil>=5.9.0",          # System monitoring
    
    # AST parsing and analysis
    "ast-comments>=1.0.0",    # Enhanced AST parsing
    "libcst>=1.0.0",          # Concrete syntax tree
    
    # Export and templating
    "jinja2>=3.1.0",          # Template engine
    "markdown>=3.5.0",        # Markdown processing
]

[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    
    # Code quality
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
    
    # Documentation
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]

[project.scripts]
codedoc = "codedoc.__main__:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
# uv-specific configuration
dev-dependencies = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1",
    "mypy>=1.0",
]

[tool.black]
line-length = 100
target-version = ['py39']

[tool.ruff]
line-length = 100
target-version = "py39"
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "--cov=codedoc --cov-report=term-missing"
```

## 🚀 Complete Implementation Example

### **Production-Ready CLI Commands**
```python
# codedoc/cli/main.py
import click
import asyncio
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from codedoc.core.manager import CodeDocManager
from codedoc.cli.progress import create_cli_progress_callback
from codedoc.cli.error_handling import handle_errors
from codedoc.utils.validation import validate_org_repo, validate_release_tag
from codedoc.models.exceptions import *

console = Console()

@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, version):
    """CodeDoc - Semantic Code Intelligence System
    
    Transform repositories into queryable semantic intelligence.
    """
    if version:
        console.print("🧠 CodeDoc v0.1.0 - Semantic Code Intelligence")
        return
        
    if ctx.invoked_subcommand is None:
        # Launch TUI when no subcommand
        console.print("🚀 Launching CodeDoc TUI...")
        from codedoc.tui.app import CodeDocTUI
        app = CodeDocTUI()
        app.run()

# Repository Management Commands
@cli.group()
def repo():
    """Repository file operations (clone, update, remove)"""
    pass

@repo.command("add")
@click.argument("org_repo")
@click.option("--private", is_flag=True, help="Repository is private (requires GitHub token)")
@handle_errors
def repo_add(org_repo: str, private: bool):
    """Clone and track a repository
    
    Downloads the repository and discovers available releases.
    Does NOT perform semantic analysis - use 'graph add' for that.
    
    Examples:
        codedoc repo add pixeltable/pixeltable
        codedoc repo add myorg/private-repo --private
    """
    validate_org_repo(org_repo)
    
    async def _add_repo():
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        if private:
            config = await core.show_config()
            if not config.get('github_token'):
                console.print("❌ [bold red]GitHub token required for private repositories[/bold red]")
                console.print("💡 Set token: [bold]codedoc update config github-token YOUR_TOKEN[/bold]")
                return
        
        console.print(f"🔄 Adding repository [bold blue]{org_repo}[/bold blue]...")
        
        try:
            result = await core.repo_add(org_repo, progress_callback=progress_callback)
            
            # Display results
            console.print(Panel(
                f"✅ Successfully added [bold green]{org_repo}[/bold green]\n"
                f"📋 Found {len(result.releases)} releases\n"
                f"📁 Storage: {result.storage_path}\n"
                f"🏷️  Latest: {result.latest_release if result.releases else 'None'}",
                title="Repository Added",
                border_style="green"
            ))
            
            if result.releases:
                console.print(f"💡 [bold blue]Next step:[/bold blue] Run [bold]codedoc graph add {org_repo}[/bold] to parse latest release")
                
                # Show available releases
                if len(result.releases) > 1:
                    console.print(f"📋 [bold blue]Available releases:[/bold blue] {', '.join(result.releases[:5])}")
                    if len(result.releases) > 5:
                        console.print(f"    ... and {len(result.releases) - 5} more")
            else:
                console.print("⚠️  [bold yellow]No releases found - this repository might use main/master branch versioning[/bold yellow]")
                
        except GitError as e:
            if "not found" in str(e).lower():
                raise GitError(
                    f"Repository {org_repo} not found or not accessible",
                    suggestions=[
                        "Check repository name spelling",
                        "Verify repository exists on GitHub",
                        "For private repos, ensure GitHub token is set",
                        "Check network connectivity"
                    ]
                )
            else:
                raise
    
    asyncio.run(_add_repo())

@repo.command("remove")
@click.argument("org_repo")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@handle_errors
def repo_remove(org_repo: str, force: bool):
    """Remove repository and ALL associated data
    
    This removes:
    - Repository files
    - ALL semantic graphs
    - ALL export files
    - Processing metadata
    
    This operation cannot be undone!
    """
    validate_org_repo(org_repo)
    
    async def _remove_repo():
        core = CodeDocManager()
        
        if not force:
            # Show what will be deleted
            try:
                details = await core.repo_show(org_repo)
                
                console.print(f"⚠️  [bold yellow]This will permanently delete:[/bold yellow]")
                console.print(f"   📁 Repository files: {details.storage_path}")
                console.print(f"   📊 Semantic graphs: {details.total_graphs} graphs")
                console.print(f"   📤 Export files: {details.export_count} files")
                console.print(f"   🔄 All processing history")
                console.print(f"   [bold red]This cannot be undone![/bold red]")
                
                if not click.confirm(f"\nReally remove {org_repo} and all data?"):
                    console.print("❌ Cancelled")
                    return
                    
            except Exception:
                # Repository might not exist, ask for simple confirmation
                if not click.confirm(f"Remove {org_repo} and all associated data?"):
                    console.print("❌ Cancelled")
                    return
        
        progress_callback = create_cli_progress_callback()
        console.print(f"🗑️  Removing [bold red]{org_repo}[/bold red] and all data...")
        
        result = await core.repo_remove(org_repo, force=True, progress_callback=progress_callback)
        
        if result:
            console.print(f"✅ [bold green]Successfully removed {org_repo} and all associated data[/bold green]")
        else:
            console.print(f"❌ [bold red]Repository {org_repo} not found[/bold red]")
    
    asyncio.run(_remove_repo())

@repo.command("list")
@click.option("--detailed", is_flag=True, help="Show detailed information")
@handle_errors
def repo_list(detailed: bool):
    """List all tracked repositories"""
    async def _list_repos():
        core = CodeDocManager()
        repos = await core.repo_list()
        
        if not repos:
            console.print("📚 [bold blue]No repositories tracked yet[/bold blue]")
            console.print("💡 Add a repository: [bold]codedoc repo add org/repo[/bold]")
            return
        
        console.print(f"📚 [bold blue]Tracked Repositories ({len(repos)}):[/bold blue]\n")
        
        for repo in repos:
            status_icons = {
                "ready": "✅",
                "processing": "⚠️",
                "error": "❌",
                "unknown": "❓"
            }
            status_icon = status_icons.get(repo.status, "❓")
            
            # Basic info
            console.print(f"  {status_icon} [bold]{repo.org_repo}[/bold]")
            
            if detailed:
                console.print(f"      📋 Releases: {len(repo.releases)}")
                console.print(f"      📊 Graphs: {getattr(repo, 'graphs_count', 0)}")
                console.print(f"      📅 Last Updated: {repo.last_updated}")
                console.print(f"      📁 Path: {repo.storage_path}")
                
                if repo.releases:
                    latest = repo.releases[0] if repo.releases else "None"
                    console.print(f"      🏷️  Latest: {latest}")
                console.print()
            else:
                releases_info = f"{len(repo.releases)} releases" if repo.releases else "no releases"
                graphs_info = f", {getattr(repo, 'graphs_count', 0)} graphs" if hasattr(repo, 'graphs_count') else ""
                console.print(f"      └─ {releases_info}{graphs_info}")
    
    asyncio.run(_list_repos())

# Graph Operations Commands
@cli.group()
def graph():
    """Semantic analysis operations (parse, rebuild, remove)"""
    pass

@graph.command("add")
@click.argument("org_repo")
@click.argument("release", required=False)
@click.option("--force", is_flag=True, help="Overwrite existing graphs")
@handle_errors
def graph_add(org_repo: str, release: Optional[str] = None, force: bool = False):
    """Parse repository to semantic graphs
    
    Performs complete semantic analysis:
    - Parses Python AST to CodeOntology format
    - Analyzes git history and developer intelligence
    - Generates ABC events for changes
    - Builds all 19 graph types
    - Stores in Oxigraph database
    
    Examples:
        codedoc graph add pixeltable/pixeltable           # Parse latest release
        codedoc graph add pixeltable/pixeltable v0.4.14   # Parse specific release
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    async def _add_graph():
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        # Check if repository exists
        try:
            repo_details = await core.repo_show(org_repo)
        except Exception:
            console.print(f"❌ [bold red]Repository {org_repo} not found[/bold red]")
            console.print(f"💡 Add it first: [bold]codedoc repo add {org_repo}[/bold]")
            return
        
        # Determine release
        if not release:
            if repo_details.releases:
                release = repo_details.releases[0]  # Latest
                console.print(f"🏷️  Using latest release: [bold blue]{release}[/bold blue]")
            else:
                console.print(f"❌ [bold red]No releases found for {org_repo}[/bold red]")
                console.print("💡 Repository might use main/master branch versioning")
                return
        
        # Check for existing graphs
        if not force:
            try:
                existing = await core.graph_show(org_repo, release)
                if existing.graphs_count > 0:
                    console.print(f"⚠️  [bold yellow]Graphs already exist for {org_repo} {release}[/bold yellow]")
                    if not click.confirm("Overwrite existing graphs?"):
                        console.print("❌ Cancelled")
                        return
            except Exception:
                pass  # No existing graphs, continue
        
        release_text = f" {release}" if release else " (latest)"
        console.print(f"🧠 Processing semantic analysis for [bold blue]{org_repo}{release_text}[/bold blue]...")
        console.print("This may take several minutes for large repositories...")
        
        try:
            result = await core.graph_add(org_repo, release, progress_callback=progress_callback)
            
            console.print(Panel(
                f"✅ Successfully processed [bold green]{org_repo} {result.actual_release}[/bold green]\n"
                f"📊 Generated {result.graphs_created} graphs\n"
                f"🔍 Analyzed {result.functions_found} functions\n"
                f"📝 Processed {result.files_processed} files\n"
                f"⏱️  Processing time: {result.processing_time:.1f}s",
                title="Semantic Analysis Complete",
                border_style="green"
            ))
            
            console.print(f"💡 [bold blue]Next steps:[/bold blue]")
            console.print(f"   • Export OPML: [bold]codedoc export opml {org_repo} {result.actual_release}[/bold]")
            console.print(f"   • Export msgpack: [bold]codedoc export msgpack {org_repo} {result.actual_release}[/bold]")
            console.print(f"   • Search functions: [bold]codedoc query functions \"your search term\"[/bold]")
            
        except ProcessingError as e:
            console.print(f"❌ [bold red]Processing failed:[/bold red] {e.message}")
            for suggestion in e.suggestions:
                console.print(f"💡 {suggestion}")
        except StorageError as e:
            console.print(f"❌ [bold red]Storage error:[/bold red] {e.message}")
            console.print("💡 Check database permissions and disk space")
    
    asyncio.run(_add_graph())

# Export Operations Commands
@cli.group()
def export():
    """Generate output files (opml, msgpack, docs)"""
    pass

@export.command("opml")
@click.argument("org_repo")
@click.argument("release")
@click.option("--output", type=click.Path(), help="Custom output path")
@click.option("--template", help="OPML template to use")
@handle_errors
def export_opml(org_repo: str, release: str, output: Optional[str] = None, template: Optional[str] = None):
    """Export as OPML for human browsing
    
    Generates hierarchical OPML suitable for tools like:
    - WorkFlowy
    - OmniOutliner  
    - Any OPML-compatible editor
    
    Examples:
        codedoc export opml pixeltable/pixeltable v0.4.14
        codedoc export opml pixeltable/pixeltable v0.4.14 --output ./my-docs.opml
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    async def _export_opml():
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        # Verify graphs exist
        try:
            graphs = await core.graph_show(org_repo, release)
            if graphs.graphs_count == 0:
                console.print(f"❌ [bold red]No graphs found for {org_repo} {release}[/bold red]")
                console.print(f"💡 Parse first: [bold]codedoc graph add {org_repo} {release}[/bold]")
                return
        except Exception:
            console.print(f"❌ [bold red]No graphs found for {org_repo} {release}[/bold red]")
            console.print(f"💡 Parse first: [bold]codedoc graph add {org_repo} {release}[/bold]")
            return
        
        console.print(f"📤 Exporting OPML for [bold blue]{org_repo} {release}[/bold blue]...")
        
        output_path = Path(output) if output else None
        result_path = await core.export_opml(
            org_repo, release, output_path, 
            template=template,
            progress_callback=progress_callback
        )
        
        # Get file size
        file_size = result_path.stat().st_size
        size_kb = file_size / 1024
        
        console.print(Panel(
            f"✅ OPML exported successfully\n"
            f"📁 Location: [bold blue]{result_path}[/bold blue]\n"
            f"📊 Size: {size_kb:.1f}KB\n"
            f"🔍 Functions: {graphs.functions_count}\n"
            f"💡 Open with any OPML editor (WorkFlowy, OmniOutliner, etc.)",
            title="Export Complete",
            border_style="green"
        ))
        
        console.print(f"🚀 [bold blue]Try this:[/bold blue] Open {result_path} in your favorite OPML editor!")
    
    asyncio.run(_export_opml())

# System Management Commands
@cli.command("show")
@click.argument("resource", type=click.Choice(["config", "status"]))
@handle_errors
def show(resource: str):
    """Show system information
    
    Available resources:
        config - System configuration settings
        status - Database size, processing status, errors
    """
    async def _show():
        core = CodeDocManager()
        
        if resource == "config":
            config = await core.show_config()
            
            config_text = Text()
            config_text.append("System Configuration:\n", style="bold blue")
            
            for key, value in config.items():
                config_text.append(f"  {key}: ", style="bold")
                
                # Format special values
                if isinstance(value, Path):
                    config_text.append(f"{value}\n", style="blue")
                elif key == "github_token" and value:
                    config_text.append("***configured***\n", style="green")
                elif key == "github_token" and not value:
                    config_text.append("not set\n", style="yellow")
                else:
                    config_text.append(f"{value}\n")
            
            console.print(Panel(config_text, title="Configuration", border_style="blue"))
            
        elif resource == "status":
            status = await core.show_status()
            
            status_text = Text()
            status_text.append(f"📊 Database Size: {status.database_size_mb:.1f}MB\n")
            status_text.append(f"📚 Repositories: {status.repository_count}\n")
            status_text.append(f"📈 Graphs: {status.graph_count}\n")
            status_text.append(f"📤 Export Files: {status.export_count}\n")
            status_text.append(f"📁 Storage Path: {status.storage_path}\n")
            status_text.append(f"⏱️  Uptime: {status.uptime}\n")
            
            if status.processing_jobs:
                status_text.append(f"\n🔄 Active Jobs: {len(status.processing_jobs)}\n", style="yellow")
                for job in status.processing_jobs:
                    status_text.append(f"   • {job}\n", style="yellow")
            
            if status.recent_errors:
                status_text.append(f"\n⚠️ Recent Errors ({len(status.recent_errors)}):\n", style="red")
                for error in status.recent_errors[-3:]:  # Last 3 errors
                    status_text.append(f"   • {error}\n", style="red")
            else:
                status_text.append(f"\n✅ No recent errors\n", style="green")
            
            console.print(Panel(status_text, title="System Status", border_style="blue"))
    
    asyncio.run(_show())

if __name__ == "__main__":
    cli()
```

## 🎯 Implementation Priority & Phases

### **Phase 1: Core Foundation (Hours 1-8)**
- Basic project structure with uv packaging
- Error handling hierarchy and validation
- Core interface definitions
- Repository management (add, remove, list)
- Basic configuration system
- Simple CLI commands with rich output

### **Phase 2: Semantic Analysis (Hours 9-16)**
- Python AST parsing pipeline
- Oxigraph integration and graph building
- Graph operations (add, remove, update)
- Progress indicators for long operations
- Basic export functionality (OPML, msgpack)

### **Phase 3: Advanced Features (Hours 17-24)**
- Query system (SPARQL, function search)
- Streaming exports for large datasets
- Advanced error recovery and logging
- Configuration management UI
- Production-ready security validation

### **Phase 4: TUI & Polish (Hours 25-32)**
- Complete TUI application with real-time updates
- Interactive progress indicators
- Advanced export options with templates
- Comprehensive help system and documentation
- Performance optimization and testing

## 🏆 Success Criteria

### **Functional Requirements**
- ✅ Complete workflow: repo add → graph add → export works flawlessly
- ✅ Destructive operations have confirmation prompts and clear warnings
- ✅ All errors provide helpful suggestions and recovery options
- ✅ Progress indicators work for all long-running operations
- ✅ Both CLI and TUI provide equivalent functionality

### **User Experience Requirements**
- ✅ New users can successfully complete basic workflow in <5 minutes
- ✅ Error messages are helpful and actionable, not cryptic
- ✅ No silent failures - all operations provide clear feedback
- ✅ Confirmation prompts prevent accidental data loss
- ✅ System feels responsive and provides progress feedback

### **Production Readiness Requirements**
- ✅ Comprehensive input validation prevents security issues
- ✅ Configuration system supports all deployment scenarios
- ✅ Logging provides sufficient detail for debugging issues
- ✅ Error handling gracefully manages all failure modes
- ✅ Performance scales to repositories with 1000+ functions

---

This specification provides everything needed to build a production-ready CLI/TUI system that users will actually enjoy using! 🚀