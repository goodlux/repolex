"""
🟡 CodeDoc CLI - Main Command Structure 🟡
Click-based command-line interface with PAC-MAN theme.

WAKA WAKA! Navigate the semantic maze with these commands!
"""

import click
import asyncio
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from codedoc.core.manager import CodeDocManager
from codedoc.cli.progress import (
    create_cli_progress_callback, 
    show_success_panel, 
    show_error_panel, 
    show_info_panel,
    PacManProgress
)
from codedoc.models.exceptions import CodeDocError, ValidationError, SecurityError
from codedoc.utils.validation import validate_org_repo, validate_release_tag

console = Console()

def handle_errors(func):
    """🟡 Decorator to handle errors with PAC-MAN style feedback."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            show_error_panel(
                "Input Validation Error",
                str(e),
                getattr(e, 'suggestions', [])
            )
            raise click.Abort()
        except SecurityError as e:
            show_error_panel(
                "Security Error - GHOST DETECTED!",
                str(e),
                getattr(e, 'suggestions', ["Check your input for dangerous characters"])
            )
            raise click.Abort()
        except CodeDocError as e:
            show_error_panel(
                "CodeDoc Error",
                str(e),
                getattr(e, 'suggestions', [])
            )
            raise click.Abort()
        except Exception as e:
            show_error_panel(
                "Unexpected Error - CHOMP!",
                f"Something went wrong: {str(e)}",
                [
                    "This might be a bug - check logs for details",
                    "Try running with --verbose for more info",
                    "Check 'codedoc show status' for system health"
                ]
            )
            raise click.Abort()
    return wrapper

@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, verbose, version):
    """
    🟡 CodeDoc - Semantic Code Intelligence System 🟡
    
    WAKA WAKA! Navigate the maze of code with semantic intelligence!
    
    Use --help on any command for details:
      codedoc repo --help
      codedoc graph --help  
      codedoc export --help
    """
    # Store context for subcommands
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    if version:
        console.print("🟡 CodeDoc v1.0 - WAKA WAKA Edition! 🎮")
        console.print("   Semantic Code Intelligence with PAC-MAN Power!")
        return
    
    if ctx.invoked_subcommand is None:
        # No subcommand - launch TUI
        console.print("🟡 WAKA WAKA! Launching interactive mode...")
        try:
            from codedoc.tui.app import CodeDocTUI
            app = CodeDocTUI()
            app.run()
        except ImportError:
            console.print("👻 TUI not available - showing CLI help instead")
            console.print(ctx.get_help())

# ============================================================================
# 📚 REPOSITORY COMMANDS - File Operations
# ============================================================================

@cli.group()
def repo():
    """📚 Repository file operations (clone, update, remove)"""
    pass

@repo.command("add")
@click.argument("org_repo")
@click.option('--branch', default='main', help='Git branch to track')
@handle_errors
def repo_add(org_repo: str, branch: str):
    """
    📥 Add (clone) a repository and discover releases
    
    Examples:
      codedoc repo add pixeltable/pixeltable
      codedoc repo add microsoft/typescript --branch master
    """
    validate_org_repo(org_repo)
    
    async def _add_repo():
        console.print(f"🟡 CHOMP CHOMP! Adding repository [bold blue]{org_repo}[/bold blue]...")
        
        core = CodeDocManager()
        await core.initialize()  # 🟡 PAC-MAN startup sequence!
        progress_callback = create_cli_progress_callback()
        
        result = await core.repo_add(org_repo, progress_callback=progress_callback)
        
        # Show success with next steps
        releases_text = f"Found {len(result.releases)} releases" if result.releases else "No releases found"
        latest_release = result.releases[0] if result.releases else None
        
        suggestions = []
        if latest_release:
            suggestions.append(f"Parse latest release: codedoc graph add {org_repo} {latest_release}")
        suggestions.extend([
            f"View repository details: codedoc repo show {org_repo}",
            f"List all repositories: codedoc repo list"
        ])
        
        show_success_panel(
            "Repository Added",
            f"Successfully added {org_repo}\n{releases_text}",
            suggestions
        )
    
    asyncio.run(_add_repo())

@repo.command("remove")
@click.argument("org_repo")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@handle_errors
def repo_remove(org_repo: str, force: bool):
    """
    🗑️ Remove repository and ALL associated data
    
    ⚠️  WARNING: This removes repository files, graphs, and exports!
    
    Examples:
      codedoc repo remove pixeltable/pixeltable
      codedoc repo remove old/repo --force
    """
    validate_org_repo(org_repo)
    
    async def _remove_repo():
        core = CodeDocManager()
        
        if not force:
            console.print("👻 [bold red]DANGER ZONE![/bold red] This will permanently delete:")
            console.print(f"   📁 Repository files for {org_repo}")
            console.print(f"   🧠 ALL semantic graphs")
            console.print(f"   📦 ALL export files")
            console.print(f"   💀 This cannot be undone!")
            
            if not click.confirm(f"\n🟡 Really chomp {org_repo} and all data?"):
                console.print("🟡 WAKA! Cancelled - repository safe!")
                return
        
        progress = PacManProgress(f"Removing {org_repo}")
        
        result = await core.repo_remove(org_repo, force=True)
        
        if result:
            progress.complete(f"Successfully removed {org_repo}")
            show_success_panel(
                "Repository Removed",
                f"Chomped {org_repo} and all associated data",
                ["List remaining repositories: codedoc repo list"]
            )
        else:
            show_error_panel(
                "Repository Not Found",
                f"Repository {org_repo} was not tracked",
                [
                    "Check available repositories: codedoc repo list",
                    "Verify the org/repo format is correct"
                ]
            )
    
    asyncio.run(_remove_repo())

@repo.command("list")
@handle_errors
def repo_list():
    """
    📋 List all tracked repositories with status
    
    Shows repository status, releases, and graph counts
    """
    async def _list_repos():
        core = CodeDocManager()
        await core.initialize()  # 🟡 PAC-MAN startup sequence!
        repos = await core.repo_list()
        
        if not repos:
            show_info_panel(
                "No Repositories",
                "No repositories tracked yet\n\nAdd your first repository with: codedoc repo add org/repo"
            )
            return
        
        # Create a table with PAC-MAN styling
        table = Table(title=f"🟡 Tracked Repositories ({len(repos)})")
        table.add_column("Status", style="yellow", width=6)
        table.add_column("Repository", style="bold blue")
        table.add_column("Releases", style="green") 
        table.add_column("Graphs", style="cyan")
        table.add_column("Last Updated", style="dim")
        
        for repo in repos:
            # Status icon based on repository state
            if repo.status == "ready":
                status_icon = "🟡"
            elif repo.status == "processing":
                status_icon = "👻"
            elif repo.status == "error":
                status_icon = "💀"
            else:
                status_icon = "⚪"
            
            releases_count = str(len(repo.releases)) if repo.releases else "0"
            graphs_count = str(getattr(repo, 'graphs_count', 0))
            last_updated_raw = getattr(repo, 'last_updated', None)
            if last_updated_raw and hasattr(last_updated_raw, 'strftime'):
                last_updated = last_updated_raw.strftime('%Y-%m-%d %H:%M')
            else:
                last_updated = 'Never'
            
            table.add_row(
                status_icon,
                repo.org_repo,
                releases_count,
                graphs_count,
                last_updated
            )
        
        console.print(table)
        
        # Show helpful next steps
        show_info_panel(
            "Legend",
            "🟡 Ready  👻 Processing  💀 Error  ⚪ Unknown\n\n" +
            "Next steps:\n" +
            "• View details: codedoc repo show <org/repo>\n" +
            "• Parse repository: codedoc graph add <org/repo>"
        )
    
    asyncio.run(_list_repos())

@repo.command("show")
@click.argument("org_repo")
@handle_errors
def repo_show(org_repo: str):
    """
    🔍 Show detailed repository information
    
    Displays releases, processing status, and storage info
    
    Examples:
      codedoc repo show pixeltable/pixeltable
    """
    validate_org_repo(org_repo)
    
    async def _show_repo():
        core = CodeDocManager()
        details = await core.repo_show(org_repo)
        
        # Create detailed information display
        info_text = Text()
        info_text.append("🟡 Repository: ", style="bold yellow")
        info_text.append(f"{org_repo}\n", style="bold blue")
        info_text.append(f"📁 Storage: {details.storage_path}\n")
        last_updated_str = details.last_updated.strftime('%Y-%m-%d %H:%M') if hasattr(details.last_updated, 'strftime') else str(details.last_updated)
        info_text.append(f"⏰ Updated: {last_updated_str}\n")
        info_text.append(f"📦 Releases: {len(details.releases)}\n")
        
        if hasattr(details, 'total_functions'):
            info_text.append(f"🔧 Functions: {details.total_functions}\n")
        
        if details.releases:
            info_text.append(f"\n📋 Available Releases:\n", style="bold")
            
            # Show releases in a nice format
            for i, release in enumerate(details.releases[:15]):  # Show first 15
                graph_status = "🧠" if getattr(release, 'has_graphs', False) else "⚪"
                date_raw = getattr(release, 'date', None)
                if date_raw and hasattr(date_raw, 'strftime'):
                    date_str = date_raw.strftime('%Y-%m-%d')
                else:
                    date_str = 'Unknown date'
                info_text.append(f"  {graph_status} {release.tag} ({date_str})\n")
            
            if len(details.releases) > 15:
                info_text.append(f"  ... and {len(details.releases) - 15} more releases\n")
        
        console.print(Panel(
            info_text, 
            title=f"🔍 Repository Details",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Show helpful next steps
        latest_release = details.releases[0].tag if details.releases else None
        suggestions = []
        if latest_release:
            suggestions.extend([
                f"Parse latest release: codedoc graph add {org_repo} {latest_release}",
                f"View all graphs: codedoc graph list {org_repo}"
            ])
        suggestions.append(f"Update repository: codedoc repo update {org_repo}")
        
        show_info_panel("Next Steps", "\n".join(f"• {s}" for s in suggestions))
    
    asyncio.run(_show_repo())

@repo.command("update")
@click.argument("org_repo")
@handle_errors
def repo_update(org_repo: str):
    """
    🔄 Update repository (git pull + discover new releases)
    
    Updates the local repository and discovers new releases/tags
    
    Examples:
      codedoc repo update pixeltable/pixeltable
    """
    validate_org_repo(org_repo)
    
    async def _update_repo():
        console.print(f"🔄 Updating repository [bold blue]{org_repo}[/bold blue]...")
        
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        result = await core.repo_update(org_repo, progress_callback=progress_callback)
        
        # Show update results
        if result.new_releases:
            show_success_panel(
                "Repository Updated",
                f"Found {len(result.new_releases)} new releases:\n" + 
                "\n".join(f"  🆕 {r}" for r in result.new_releases),
                [f"Parse new release: codedoc graph add {org_repo} {result.new_releases[0]}"] if result.new_releases else []
            )
        else:
            show_info_panel(
                "Repository Up to Date",
                f"{org_repo} is already up to date\nNo new releases found"
            )
    
    asyncio.run(_update_repo())

# ============================================================================
# 🧠 GRAPH COMMANDS - Semantic Analysis Operations  
# ============================================================================

@cli.group()
def graph():
    """🧠 Semantic analysis operations (parse, rebuild, remove graphs)"""
    pass

@graph.command("add")
@click.argument("org_repo")
@click.argument("release", required=False)
@click.option('--force', is_flag=True, help='Force reprocessing if graphs exist')
@handle_errors
def graph_add(org_repo: str, release: Optional[str] = None, force: bool = False):
    """
    🧠 Parse repository to semantic graphs
    
    Performs complete semantic analysis and generates all 19 graph types.
    Uses latest release if none specified.
    
    Examples:
      codedoc graph add pixeltable/pixeltable
      codedoc graph add pixeltable/pixeltable v0.4.14
      codedoc graph add old/repo --force
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    async def _add_graph():
        release_text = f" {release}" if release else " (latest)"
        console.print(f"🧠 CHOMP CHOMP! Processing semantic analysis for [bold blue]{org_repo}{release_text}[/bold blue]...")
        
        core = CodeDocManager()
        await core.initialize()  # 🟡 PAC-MAN startup sequence!
        progress_callback = create_cli_progress_callback()
        
        result = await core.graph_add(org_repo, release, progress_callback=progress_callback)
        
        # Show detailed success information
        actual_release = result.actual_release or release or "latest"
        
        show_success_panel(
            "Semantic Analysis Complete",
            f"Successfully processed {org_repo} {actual_release}\n" +
            f"📊 Generated {result.graphs_created} graphs\n" +
            f"🔍 Analyzed {result.functions_found} functions\n" +
            f"⚡ Processing time: {result.processing_time:.1f}s",
            [
                f"Export OPML: codedoc export opml {org_repo} {actual_release}",
                f"Export msgpack: codedoc export msgpack {org_repo} {actual_release}",
                f"Search functions: codedoc query functions <search-term> --repo {org_repo}"
            ]
        )
    
    asyncio.run(_add_graph())

@graph.command("remove")
@click.argument("org_repo")
@click.argument("release", required=False)
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@handle_errors
def graph_remove(org_repo: str, release: Optional[str] = None, force: bool = False):
    """
    🗑️ Remove semantic graphs from database
    
    If release specified: removes only that release's graphs
    If no release: removes ALL graphs for repository (files preserved)
    
    Examples:
      codedoc graph remove pixeltable/pixeltable v0.4.14
      codedoc graph remove pixeltable/pixeltable --force
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    async def _remove_graph():
        core = CodeDocManager()
        
        if not force:
            if release:
                message = f"Remove graphs for {org_repo} {release}?"
                warning = "This will remove semantic analysis for this specific release."
            else:
                message = f"Remove ALL graphs for {org_repo}?"
                warning = "⚠️  This will remove ALL semantic graphs (repository files preserved)."
            
            console.print(f"👻 {warning}")
            if not click.confirm(f"\n🟡 {message}"):
                console.print("🟡 WAKA! Cancelled - graphs safe!")
                return
        
        progress = PacManProgress(f"Removing graphs for {org_repo}")
        
        result = await core.graph_remove(org_repo, release, force=True)
        
        if result:
            if release:
                progress.complete(f"Removed graphs for {org_repo} {release}")
                show_success_panel(
                    "Graphs Removed",
                    f"Chomped semantic graphs for {org_repo} {release}",
                    [f"Reprocess anytime: codedoc graph add {org_repo} {release}"]
                )
            else:
                progress.complete(f"Removed all graphs for {org_repo}")
                show_success_panel(
                    "All Graphs Removed",
                    f"Chomped all semantic graphs for {org_repo}\nRepository files preserved",
                    [f"Reprocess latest: codedoc graph add {org_repo}"]
                )
        else:
            show_error_panel(
                "Graphs Not Found",
                f"No graphs found for {org_repo}{' ' + release if release else ''}",
                [
                    "Check available graphs: codedoc graph list",
                    f"Process repository first: codedoc graph add {org_repo}"
                ]
            )
    
    asyncio.run(_remove_graph())

@graph.command("list")
@click.argument("org_repo", required=False)
@handle_errors
def graph_list(org_repo: Optional[str] = None):
    """
    📋 List semantic graphs in database
    
    Shows all graphs, or filter by specific repository
    
    Examples:
      codedoc graph list
      codedoc graph list pixeltable/pixeltable
    """
    if org_repo:
        validate_org_repo(org_repo)
    
    async def _list_graphs():
        core = CodeDocManager()
        graphs = await core.graph_list(org_repo)
        
        if not graphs:
            if org_repo:
                show_info_panel(
                    "No Graphs",
                    f"No graphs found for {org_repo}\n\nProcess repository: codedoc graph add {org_repo}"
                )
            else:
                show_info_panel(
                    "No Graphs",
                    "No semantic graphs in database\n\nAdd a repository: codedoc repo add org/repo\nThen process it: codedoc graph add org/repo"
                )
            return
        
        # Create graphs table with PAC-MAN styling
        table = Table(title=f"🧠 Semantic Graphs ({len(graphs)})")
        table.add_column("Repository", style="bold blue")
        table.add_column("Release", style="green")
        table.add_column("Graphs", style="yellow")
        table.add_column("Functions", style="cyan")
        table.add_column("Size", style="dim")
        
        for graph in graphs:
            repo_name = getattr(graph, 'repository', 'Unknown')
            release = getattr(graph, 'release', 'Unknown')
            graph_count = str(getattr(graph, 'graph_count', 0))
            function_count = str(getattr(graph, 'function_count', 0))
            size = getattr(graph, 'size_mb', 0)
            size_str = f"{size:.1f}MB" if size > 0 else "Unknown"
            
            table.add_row(repo_name, release, graph_count, function_count, size_str)
        
        console.print(table)
        
        # Show helpful next steps
        show_info_panel(
            "Next Steps",
            "• View details: codedoc graph show <org/repo>\n" +
            "• Export data: codedoc export opml <org/repo> <release>\n" +
            "• Search functions: codedoc query functions <term>"
        )
    
    asyncio.run(_list_graphs())

@graph.command("show")
@click.argument("org_repo")
@click.argument("release", required=False)
@handle_errors
def graph_show(org_repo: str, release: Optional[str] = None):
    """
    🔍 Show detailed graph information and statistics
    
    Examples:
      codedoc graph show pixeltable/pixeltable
      codedoc graph show pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    async def _show_graph():
        core = CodeDocManager()
        details = await core.graph_show(org_repo, release)
        
        # Create detailed graph information display
        info_text = Text()
        info_text.append("🧠 Semantic Graphs: ", style="bold yellow")
        info_text.append(f"{org_repo}", style="bold blue")
        if release:
            info_text.append(f" {release}", style="green")
        info_text.append("\n")
        
        # Show graph statistics
        if hasattr(details, 'graph_count'):
            info_text.append(f"📊 Total Graphs: {details.graph_count}\n")
        if hasattr(details, 'function_count'):
            info_text.append(f"🔧 Functions: {details.function_count}\n")
        if hasattr(details, 'triple_count'):
            info_text.append(f"🔗 RDF Triples: {details.triple_count:,}\n")
        if hasattr(details, 'size_mb'):
            info_text.append(f"💾 Database Size: {details.size_mb:.1f}MB\n")
        if hasattr(details, 'processing_time'):
            info_text.append(f"⚡ Processing Time: {details.processing_time:.1f}s\n")
        
        # Show graph breakdown if available
        if hasattr(details, 'graph_breakdown'):
            info_text.append(f"\n📋 Graph Breakdown:\n", style="bold")
            for graph_type, count in details.graph_breakdown.items():
                info_text.append(f"  🔸 {graph_type}: {count}\n")
        
        console.print(Panel(
            info_text,
            title=f"🔍 Graph Details",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Show export options
        actual_release = release or "latest"
        suggestions = [
            f"Export OPML: codedoc export opml {org_repo} {actual_release}",
            f"Export msgpack: codedoc export msgpack {org_repo} {actual_release}",
            f"Rebuild graphs: codedoc graph update {org_repo} {actual_release}"
        ]
        
        show_info_panel("Export Options", "\n".join(f"• {s}" for s in suggestions))
    
    asyncio.run(_show_graph())

@graph.command("update")
@click.argument("org_repo")
@click.argument("release", required=False)
@handle_errors
def graph_update(org_repo: str, release: Optional[str] = None):
    """
    🔄 Nuclear rebuild of semantic graphs
    
    Completely reprocesses and rebuilds graphs (safe operation).
    Cross-graph references are preserved.
    
    Examples:
      codedoc graph update pixeltable/pixeltable
      codedoc graph update pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    async def _update_graph():
        release_text = f" {release}" if release else " (latest)"
        console.print(f"🔄 Nuclear rebuild for [bold blue]{org_repo}{release_text}[/bold blue]...")
        console.print("💡 Safe operation - cross-graph references preserved")
        
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        result = await core.graph_update(org_repo, release, progress_callback=progress_callback)
        
        # Show rebuild results
        actual_release = result.actual_release or release or "latest"
        
        show_success_panel(
            "Nuclear Rebuild Complete",
            f"Successfully rebuilt {org_repo} {actual_release}\n" +
            f"📊 Regenerated {result.graphs_created} graphs\n" +
            f"🔍 Reanalyzed {result.functions_found} functions\n" +
            f"⚡ Rebuild time: {result.processing_time:.1f}s",
            [
                f"Verify results: codedoc graph show {org_repo} {actual_release}",
                f"Export updated data: codedoc export opml {org_repo} {actual_release}"
            ]
        )
    
    asyncio.run(_update_graph())

# ============================================================================
# 📤 EXPORT COMMANDS - Generate Output Files
# ============================================================================

@cli.group()
def export():
    """📤 Generate output files (OPML, msgpack, documentation)"""
    pass

@export.command("opml")
@click.argument("org_repo")
@click.argument("release")
@click.option("--output", type=click.Path(), help="Custom output path")
@handle_errors
def export_opml(org_repo: str, release: str, output: Optional[str] = None):
    """
    🌳 Export as OPML for human browsing
    
    Examples:
      codedoc export opml pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    async def _export_opml():
        console.print(f"🌳 CHOMP! Exporting OPML for [bold blue]{org_repo} {release}[/bold blue]...")
        
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        output_path = Path(output) if output else None
        result_path = await core.export_opml(org_repo, release, output_path, progress_callback=progress_callback)
        
        show_success_panel(
            "OPML Export Complete",
            f"Successfully exported {org_repo} {release}\nLocation: {result_path}",
            [f"Open file: open {result_path}"]
        )
    
    asyncio.run(_export_opml())

@export.command("msgpack")
@click.argument("org_repo")
@click.argument("release")
@click.option("--output", type=click.Path(), help="Custom output path")
@handle_errors
def export_msgpack(org_repo: str, release: str, output: Optional[str] = None):
    """
    📦 Export as compact semantic package for LLM consumption
    
    Examples:
      codedoc export msgpack pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    async def _export_msgpack():
        console.print(f"📦 CHOMP! Creating semantic package for [bold blue]{org_repo} {release}[/bold blue]...")
        
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        output_path = Path(output) if output else None
        result_path = await core.export_msgpack(org_repo, release, output_path, progress_callback=progress_callback)
        
        show_success_panel(
            "Semantic Package Complete",
            f"Successfully packaged {org_repo} {release}\nLocation: {result_path}",
            ["Use in AI prompts for perfect API knowledge"]
        )
    
    asyncio.run(_export_msgpack())

@export.command("docs")
@click.argument("org_repo")
@click.argument("release")
@click.option("--format", type=click.Choice(["mdx", "html", "markdown"]), required=True, help="Documentation format")
@click.option("--output", type=click.Path(exists=False), required=True, help="Output directory")
@click.option("--template", help="Template name for styling (optional)")
@handle_errors
def export_docs(org_repo: str, release: str, format: str, output: str, template: Optional[str] = None):
    """
    📝 Export as documentation in specified format
    
    Examples:
      codedoc export docs pixeltable/pixeltable v0.4.14 --format mdx --output ./docs/api/
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    async def _export_docs():
        console.print(f"📝 CHOMP! Generating {format.upper()} documentation for [bold blue]{org_repo} {release}[/bold blue]...")
        
        core = CodeDocManager()
        progress_callback = create_cli_progress_callback()
        
        output_path = Path(output)
        result_path = await core.export_docs(
            org_repo, release, format, output_path, template, progress_callback=progress_callback
        )
        
        show_success_panel(
            "Documentation Generated",
            f"Successfully generated {format.upper()} docs\nLocation: {result_path}",
            [f"Open directory: open {result_path}"]
        )
    
    asyncio.run(_export_docs())

# ============================================================================
# 🔍 QUERY COMMANDS - Search and Query Operations
# ============================================================================

@cli.group()
def query():
    """🔍 Search and query operations (SPARQL, function search)"""
    pass

@query.command("sparql")
@click.argument("sparql_query")
@click.option("--format", type=click.Choice(["table", "json", "turtle", "csv"]), default="table", help="Output format")
@click.option("--output", type=click.Path(), help="Save results to file")
@handle_errors
def query_sparql(sparql_query: str, format: str, output: Optional[str] = None):
    """
    ⚡ Execute SPARQL query against semantic database
    
    Examples:
      codedoc query sparql "SELECT ?name WHERE { ?f woc:hasName ?name }"
    """
    
    async def _query_sparql():
        console.print(f"⚡ CHOMP! Executing SPARQL query...")
        
        core = CodeDocManager()
        result = await core.query_sparql(sparql_query, format, Path(output) if output else None)
        
        if output:
            show_success_panel(
                "SPARQL Query Complete",
                f"Results saved: {output}\nRows: {result.row_count}",
                [f"View results: open {output}"]
            )
        else:
            if result.formatted_output:
                console.print(f"\n📊 Results:")
                console.print(result.formatted_output)
            else:
                show_info_panel("No Results", "Query returned no results")
    
    asyncio.run(_query_sparql())

@query.command("functions")
@click.argument("search_term")
@click.option("--repo", help="Limit search to specific repository")
@click.option("--release", help="Limit search to specific release")
@click.option("--limit", type=int, default=20, help="Maximum results to show")
@handle_errors
def query_functions(search_term: str, repo: Optional[str], release: Optional[str], limit: int):
    """
    🔍 Search functions using natural language
    
    Examples:
      codedoc query functions "create table"
    """
    if repo:
        validate_org_repo(repo)
    if release:
        validate_release_tag(release)
    
    async def _query_functions():
        console.print(f"🔍 CHOMP! Searching for functions: [bold blue]{search_term}[/bold blue]")
        
        core = CodeDocManager()
        results = await core.query_functions(search_term, repo, release)
        
        if not results:
            show_info_panel(
                "No Functions Found",
                f"No functions found matching: {search_term}"
            )
            return
        
        # Show results in a table
        table = Table(title=f"🔍 Found {len(results)} functions")
        table.add_column("Function", style="bold blue")
        table.add_column("Repository", style="green")
        
        for func in results[:limit]:
            table.add_row(
                func.name,
                getattr(func, 'repository', 'Unknown')
            )
        
        console.print(table)
    
    asyncio.run(_query_functions())

# ============================================================================
# 🔧 SYSTEM COMMANDS - Configuration and Status
# ============================================================================

@cli.command("show")
@click.argument("resource", type=click.Choice(["config", "status"]))
@handle_errors
def show(resource: str):
    """
    📊 Show system information
    
    Examples:
      codedoc show config
      codedoc show status
    """
    async def _show():
        core = CodeDocManager()
        await core.initialize()  # 🟡 PAC-MAN startup sequence!
        
        if resource == "config":
            config = await core.show_config()
            
            info_text = Text()
            info_text.append("🔧 System Configuration:\n", style="bold blue")
            
            for key, value in config.items():
                info_text.append(f"  {key}: {value}\n")
            
            console.print(Panel(info_text, title="🔧 Configuration", border_style="blue"))
            
        elif resource == "status":
            status = await core.show_status()
            
            status_text = Text()
            status_text.append("🟡 WAKA WAKA! System Status:\n", style="bold yellow")
            status_text.append(f"Repositories: {getattr(status, 'repository_count', 0)}\n")
            status_text.append(f"Graphs: {getattr(status, 'graph_count', 0)}\n")
            status_text.append(f"Storage: {getattr(status, 'storage_path', 'Unknown')}\n")
            
            console.print(Panel(status_text, title="📊 System Status", border_style="green"))
    
    asyncio.run(_show())

@cli.command("update")
@click.argument("resource", type=click.Choice(["config"]))
@click.argument("key")
@click.argument("value")
@handle_errors
def update(resource: str, key: str, value: str):
    """
    🔧 Update system settings
    
    Examples:
      codedoc update config github-token ghp_xxxxxxxxxxxx
    """
    async def _update():
        core = CodeDocManager()
        
        if resource == "config":
            console.print(f"🔧 CHOMP! Updating {key} = {value}")
            
            result = await core.update_config(key, value)
            
            if result:
                show_success_panel(
                    "Configuration Updated",
                    f"Successfully updated {key} = {value}",
                    ["View settings: codedoc show config"]
                )
    
    asyncio.run(_update())

if __name__ == "__main__":
    cli()
