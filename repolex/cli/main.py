"""
Repolex CLI - Main Command Structure
Click-based command-line interface for semantic code intelligence.
"""

import click
from pathlib import Path
from typing import Optional

from repolex.core.manager import RepolexManager
from repolex.models.exceptions import RepolexError, ValidationError, SecurityError
from repolex.utils.validation import validate_org_repo, validate_release_tag


def handle_errors(func):
    """Decorator to handle errors with clean feedback."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            click.echo(f"Error: {e}", err=True)
            if hasattr(e, 'suggestions') and e.suggestions:
                for suggestion in e.suggestions:
                    click.echo(f"  • {suggestion}", err=True)
            raise click.Abort()
        except SecurityError as e:
            click.echo(f"Security Error: {e}", err=True)
            if hasattr(e, 'suggestions') and e.suggestions:
                for suggestion in e.suggestions:
                    click.echo(f"  • {suggestion}", err=True)
            raise click.Abort()
        except RepolexError as e:
            click.echo(f"Error: {e}", err=True)
            if hasattr(e, 'suggestions') and e.suggestions:
                for suggestion in e.suggestions:
                    click.echo(f"  • {suggestion}", err=True)
            raise click.Abort()
        except Exception as e:
            click.echo(f"Unexpected error: {e}", err=True)
            raise click.Abort()
    return wrapper


@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, verbose, version):
    """
    rlex - Semantic Code Intelligence System
    
    Use --help on any command for details:
      rlex repo --help
      rlex graph --help  
      rlex export --help
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    
    if version:
        click.echo("Repolex v1.0 - Semantic Code Intelligence")
        return
    
    if ctx.invoked_subcommand is None:
        # No subcommand - show interactive menu
        from repolex.cli.interactive import show_interactive_menu
        show_interactive_menu()


# ============================================================================
# REPOSITORY COMMANDS - File Operations
# ============================================================================

@cli.group()
def repo():
    """Repository file operations (clone, update, remove)"""
    pass


@repo.command("add")
@click.argument("org_repo")
@click.option('--branch', default='main', help='Git branch to track')
@handle_errors
def repo_add(org_repo: str, branch: str):
    """
    Add (clone) a repository and discover releases
    
    Examples:
      rlex repo add pixeltable/pixeltable
      rlex repo add microsoft/typescript --branch master
    """
    validate_org_repo(org_repo)
    
    click.echo(f"Adding repository {org_repo}...")
    
    core = RepolexManager()
    core.initialize()
    
    result = core.repo_add(org_repo)
    
    releases_text = f"Found {len(result.releases)} releases" if result.releases else "No releases found"
    click.echo(f"Successfully added {org_repo}")
    click.echo(releases_text)
    
    if result.releases:
        latest_release = result.releases[0]
        click.echo(f"Next: rlex graph add {org_repo} {latest_release}")


@repo.command("remove")
@click.argument("org_repo")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@handle_errors
def repo_remove(org_repo: str, force: bool):
    """
    Remove repository and ALL associated data
    
    WARNING: This removes repository files, graphs, and exports!
    
    Examples:
      rlex repo remove pixeltable/pixeltable
      rlex repo remove old/repo --force
    """
    validate_org_repo(org_repo)
    
    core = RepolexManager()
    
    if not force:
        click.echo("WARNING: This will permanently delete:")
        click.echo(f"  • Repository files for {org_repo}")
        click.echo(f"  • ALL semantic graphs")
        click.echo(f"  • ALL export files")
        click.echo(f"  • This cannot be undone!")
        
        if not click.confirm(f"Really remove {org_repo} and all data?"):
            click.echo("Cancelled")
            return
    
    result = core.repo_remove(org_repo, force=True)
    
    if result:
        click.echo(f"Successfully removed {org_repo}")
    else:
        click.echo(f"Repository {org_repo} not found")


@repo.command("list")
@handle_errors
def repo_list():
    """
    List all tracked repositories with status
    """
    core = RepolexManager()
    core.initialize()
    repos = core.repo_list()
    
    if not repos:
        click.echo("No repositories tracked yet")
        click.echo("Add your first repository: rlex repo add org/repo")
        return
    
    click.echo(f"Tracked Repositories ({len(repos)}):")
    click.echo("-" * 40)
    
    for repo in repos:
        status = "●" if repo.status == "ready" else "○"
        releases_count = len(repo.releases) if repo.releases else 0
        click.echo(f"{status} {repo.org_repo} - {releases_count} releases")


@repo.command("show")
@click.argument("org_repo")
@handle_errors
def repo_show(org_repo: str):
    """
    Show detailed repository information
    
    Examples:
      rlex repo show pixeltable/pixeltable
    """
    validate_org_repo(org_repo)
    
    core = RepolexManager()
    details = core.repo_show(org_repo)
    
    click.echo(f"Repository: {org_repo}")
    click.echo(f"Storage: {details.storage_path}")
    click.echo(f"Last Updated: {details.last_updated}")
    click.echo(f"Releases: {len(details.releases)}")
    
    if details.releases:
        click.echo("\nAvailable Releases:")
        for release in details.releases[:10]:  # Show first 10
            graph_status = "●" if getattr(release, 'has_graphs', False) else "○"
            click.echo(f"  {graph_status} {release.tag}")
        
        if len(details.releases) > 10:
            click.echo(f"  ... and {len(details.releases) - 10} more")


@repo.command("update")
@click.argument("org_repo")
@handle_errors
def repo_update(org_repo: str):
    """
    Update repository (git pull + discover new releases)
    
    Examples:
      rlex repo update pixeltable/pixeltable
    """
    validate_org_repo(org_repo)
    
    click.echo(f"Updating repository {org_repo}...")
    
    core = RepolexManager()
    result = core.repo_update(org_repo)
    
    if result.new_releases:
        click.echo(f"Found {len(result.new_releases)} new releases:")
        for release in result.new_releases:
            click.echo(f"  • {release}")
    else:
        click.echo("Repository is up to date")


# ============================================================================
# GRAPH COMMANDS - Semantic Analysis Operations  
# ============================================================================

@cli.group()
def graph():
    """Semantic analysis operations (parse, rebuild, remove graphs)"""
    pass


@graph.command("add")
@click.argument("org_repo")
@click.argument("release", required=False)
@click.option('--force', is_flag=True, help='Force reprocessing if graphs exist')
@handle_errors
def graph_add(org_repo: str, release: Optional[str] = None, force: bool = False):
    """
    Parse repository to semantic graphs
    
    Examples:
      rlex graph add pixeltable/pixeltable
      rlex graph add pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    release_text = f" {release}" if release else " (latest)"
    click.echo(f"Processing semantic analysis for {org_repo}{release_text}...")
    
    core = RepolexManager()
    core.initialize()
    
    result = core.graph_add(org_repo, release)
    
    actual_release = result.actual_release or release or "latest"
    
    click.echo(f"Successfully processed {org_repo} {actual_release}")
    click.echo(f"Generated {result.graphs_created} graphs")
    click.echo(f"Analyzed {result.functions_found} functions")
    click.echo(f"Processing time: {result.processing_time:.1f}s")


@graph.command("remove")
@click.argument("org_repo")
@click.argument("release", required=False)
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@handle_errors
def graph_remove(org_repo: str, release: Optional[str] = None, force: bool = False):
    """
    Remove semantic graphs from database
    
    Examples:
      rlex graph remove pixeltable/pixeltable v0.4.14
      rlex graph remove pixeltable/pixeltable --force
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    core = RepolexManager()
    
    if not force:
        if release:
            message = f"Remove graphs for {org_repo} {release}?"
        else:
            message = f"Remove ALL graphs for {org_repo}? (repository files preserved)"
        
        if not click.confirm(message):
            click.echo("Cancelled")
            return
    
    result = core.graph_remove(org_repo, release, force=True)
    
    if result:
        if release:
            click.echo(f"Removed graphs for {org_repo} {release}")
        else:
            click.echo(f"Removed all graphs for {org_repo}")
    else:
        click.echo(f"No graphs found for {org_repo}")


@graph.command("list")
@click.argument("org_repo", required=False)
@handle_errors
def graph_list(org_repo: Optional[str] = None):
    """
    List semantic graphs in database
    
    Examples:
      rlex graph list
      rlex graph list pixeltable/pixeltable
    """
    if org_repo:
        validate_org_repo(org_repo)
    
    core = RepolexManager()
    core.initialize()
    graphs = core.graph_list(org_repo)
    
    if not graphs:
        if org_repo:
            click.echo(f"No graphs found for {org_repo}")
            click.echo(f"Process repository: rlex graph add {org_repo}")
        else:
            click.echo("No semantic graphs in database")
            click.echo("Add a repository: rlex repo add org/repo")
        return
    
    click.echo(f"Semantic Graphs ({len(graphs)}):")
    click.echo("-" * 50)
    
    for graph in graphs:
        repo_name = getattr(graph, 'repository', 'Unknown')
        release = getattr(graph, 'release', 'Unknown')
        function_count = getattr(graph, 'function_count', 0)
        click.echo(f"{repo_name} {release} - {function_count} functions")


@graph.command("show")
@click.argument("org_repo")
@click.argument("release", required=False)
@handle_errors
def graph_show(org_repo: str, release: Optional[str] = None):
    """
    Show detailed graph information and statistics
    
    Examples:
      rlex graph show pixeltable/pixeltable
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    core = RepolexManager()
    details = core.graph_show(org_repo, release)
    
    click.echo(f"Semantic Graphs: {org_repo}")
    if release:
        click.echo(f"Release: {release}")
    
    if hasattr(details, 'graph_count'):
        click.echo(f"Total Graphs: {details.graph_count}")
    if hasattr(details, 'function_count'):
        click.echo(f"Functions: {details.function_count}")
    if hasattr(details, 'triple_count'):
        click.echo(f"RDF Triples: {details.triple_count:,}")


@graph.command("update")
@click.argument("org_repo")
@click.argument("release", required=False)
@handle_errors
def graph_update(org_repo: str, release: Optional[str] = None):
    """
    Nuclear rebuild of semantic graphs
    
    Examples:
      rlex graph update pixeltable/pixeltable
    """
    validate_org_repo(org_repo)
    if release:
        validate_release_tag(release)
    
    release_text = f" {release}" if release else " (latest)"
    click.echo(f"Rebuilding graphs for {org_repo}{release_text}...")
    
    core = RepolexManager()
    result = core.graph_update(org_repo, release)
    
    actual_release = result.actual_release or release or "latest"
    click.echo(f"Successfully rebuilt {org_repo} {actual_release}")


# ============================================================================
# EXPORT COMMANDS - Generate Output Files
# ============================================================================

@cli.group()
def export():
    """Generate output files (OPML, msgpack, documentation)"""
    pass


@export.command("opml")
@click.argument("org_repo")
@click.argument("release")
@click.option("--output", type=click.Path(), help="Custom output path")
@handle_errors
def export_opml(org_repo: str, release: str, output: Optional[str] = None):
    """
    Export as OPML for human browsing
    
    Examples:
      rlex export opml pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    click.echo(f"Exporting OPML for {org_repo} {release}...")
    
    core = RepolexManager()
    output_path = Path(output) if output else None
    result_path = core.export_opml(org_repo, release, output_path)
    
    click.echo(f"Successfully exported to: {result_path}")


@export.command("msgpack")
@click.argument("org_repo")
@click.argument("release")
@click.option("--output", type=click.Path(), help="Custom output path")
@handle_errors
def export_msgpack(org_repo: str, release: str, output: Optional[str] = None):
    """
    Export as compact semantic package
    
    Examples:
      rlex export msgpack pixeltable/pixeltable v0.4.14
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    click.echo(f"Creating semantic package for {org_repo} {release}...")
    
    core = RepolexManager()
    output_path = Path(output) if output else None
    result_path = core.export_msgpack(org_repo, release, output_path)
    
    click.echo(f"Successfully packaged to: {result_path}")


# ============================================================================
# QUERY COMMANDS - Search and Query Operations
# ============================================================================

@cli.group()
def query():
    """Search and query operations (SPARQL, function search)"""
    pass


@query.command("sparql")
@click.argument("sparql_query")
@click.option("--format", type=click.Choice(["table", "json", "turtle", "csv"]), default="table")
@click.option("--output", type=click.Path(), help="Save results to file")
@handle_errors
def query_sparql(sparql_query: str, format: str, output: Optional[str] = None):
    """
    Execute SPARQL query against semantic database
    
    Examples:
      rlex query sparql "SELECT ?name WHERE { ?f woc:hasName ?name }"
    """
    click.echo("Executing SPARQL query...")
    
    core = RepolexManager()
    result = core.query_sparql(sparql_query, format, Path(output) if output else None)
    
    if output:
        click.echo(f"Results saved to: {output}")
    else:
        if result.formatted_output:
            click.echo("Results:")
            click.echo(result.formatted_output)
        else:
            click.echo("No results found")


@query.command("functions")
@click.argument("search_term")
@click.option("--repo", help="Limit search to specific repository")
@click.option("--release", help="Limit search to specific release")
@click.option("--limit", type=int, default=20, help="Maximum results to show")
@handle_errors
def query_functions(search_term: str, repo: Optional[str], release: Optional[str], limit: int):
    """
    Search functions using natural language
    
    Examples:
      rlex query functions "create table"
    """
    if repo:
        validate_org_repo(repo)
    if release:
        validate_release_tag(release)
    
    click.echo(f"Searching for functions: {search_term}")
    
    core = RepolexManager()
    results = core.query_functions(search_term, repo, release)
    
    if not results:
        click.echo("No functions found")
        return
    
    click.echo(f"Found {len(results)} functions:")
    for func in results[:limit]:
        repo_name = getattr(func, 'repository', 'Unknown')
        click.echo(f"  {func.name} ({repo_name})")


# ============================================================================
# SYSTEM COMMANDS - Configuration and Status
# ============================================================================

@cli.command("show")
@click.argument("resource", type=click.Choice(["config", "status"]))
@handle_errors
def show(resource: str):
    """
    Show system information
    
    Examples:
      rlex show config
      rlex show status
    """
    core = RepolexManager()
    core.initialize()
    
    if resource == "config":
        config = core.show_config()
        
        click.echo("System Configuration:")
        for key, value in config.items():
            click.echo(f"  {key}: {value}")
            
    elif resource == "status":
        status = core.show_status()
        
        click.echo("System Status:")
        click.echo(f"  Repositories: {getattr(status, 'repository_count', 0)}")
        click.echo(f"  Graphs: {getattr(status, 'graph_count', 0)}")
        click.echo(f"  Storage: {getattr(status, 'storage_path', 'Unknown')}")


@cli.command("update")
@click.argument("resource", type=click.Choice(["config"]))
@click.argument("key")
@click.argument("value")
@handle_errors
def update(resource: str, key: str, value: str):
    """
    Update system settings
    
    Examples:
      rlex update config github-token ghp_xxxxxxxxxxxx
    """
    core = RepolexManager()
    
    if resource == "config":
        click.echo(f"Updating {key} = {value}")
        
        result = core.update_config(key, value)
        
        if result:
            click.echo(f"Successfully updated {key}")


if __name__ == "__main__":
    cli()
