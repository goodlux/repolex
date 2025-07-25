"""
🟡 Repolex CLI - Export, Query, and System Commands 🟡
Continuation of the main CLI with remaining command groups.
"""

# This goes at the end of main.py before "if __name__ == '__main__':"

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
    
    Generates hierarchical OPML suitable for outline tools like WorkFlowy.
    Perfect for exploring the semantic structure of a codebase.
    
    Examples:
      Repolex export opml pixeltable/pixeltable v0.4.14
      Repolex export opml myorg/repo v1.0.0 --output ./my-opml.opml
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    def _export_opml():
        console.print(f"🌳 CHOMP! Exporting OPML for [bold blue]{org_repo} {release}[/bold blue]...")
        
        core = RepolexManager()
        progress_callback = create_cli_progress_callback()
        
        output_path = Path(output) if output else None
        result_path = core.export_opml(org_repo, release, output_path, progress_callback=progress_callback)
        
        # Get file size for display
        file_size = result_path.stat().st_size
        size_kb = file_size / 1024
        
        show_success_panel(
            "OPML Export Complete",
            f"Successfully exported {org_repo} {release}\\n" +
            f"📁 Location: {result_path}\\n" +
            f"📊 Size: {size_kb:.1f}KB\\n" +
            f"🌳 Ready for outline tools (WorkFlowy, OmniOutliner, etc.)",
            [
                f"Open file: open {result_path}",
                f"Export msgpack too: Repolex export msgpack {org_repo} {release}",
                "Import into WorkFlowy or your favorite outline tool"
            ]
        )
    
    _export_opml()

@export.command("msgpack")
@click.argument("org_repo")
@click.argument("release")
@click.option("--output", type=click.Path(), help="Custom output path")
@handle_errors
def export_msgpack(org_repo: str, release: str, output: Optional[str] = None):
    """
    📦 Export as compact semantic package for LLM consumption
    
    Generates ultra-compressed semantic intelligence package with
    125x compression ratio vs full RDF. Perfect for AI systems!
    
    Examples:
      Repolex export msgpack pixeltable/pixeltable v0.4.14
      Repolex export msgpack myorg/repo v1.0.0 --output ./ai-package.msgpack
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    def _export_msgpack():
        console.print(f"📦 CHOMP! Creating semantic package for [bold blue]{org_repo} {release}[/bold blue]...")
        
        core = RepolexManager()
        progress_callback = create_cli_progress_callback()
        
        output_path = Path(output) if output else None
        result_path = core.export_msgpack(org_repo, release, output_path, progress_callback=progress_callback)
        
        # Get file size for display
        file_size = result_path.stat().st_size
        size_mb = file_size / (1024 * 1024)
        
        show_success_panel(
            "Semantic Package Complete",
            f"Successfully packaged {org_repo} {release}\\n" +
            f"📁 Location: {result_path}\\n" +
            f"📊 Size: {size_mb:.1f}MB (125x compressed!)\\n" +
            f"🤖 Ready for AI/LLM consumption",
            [
                f"Test with jq: cat {result_path} | msgpack -d | jq '.functions[0]'",
                "Use in AI prompts for perfect API knowledge",
                f"Export OPML too: Repolex export opml {org_repo} {release}"
            ]
        )
    
    _export_msgpack()

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
    
    Generates comprehensive API documentation from semantic analysis.
    Supports multiple formats for different documentation platforms.
    
    Examples:
      Repolex export docs pixeltable/pixeltable v0.4.14 --format mdx --output ./docs/api/
      Repolex export docs myorg/repo v1.0.0 --format html --output ./website/ --template clean
    """
    validate_org_repo(org_repo)
    validate_release_tag(release)
    
    def _export_docs():
        console.print(f"📝 CHOMP! Generating {format.upper()} documentation for [bold blue]{org_repo} {release}[/bold blue]...")
        
        core = RepolexManager()
        progress_callback = create_cli_progress_callback()
        
        output_path = Path(output)
        result_path = core.export_docs(
            org_repo, release, format, output_path, template, progress_callback=progress_callback
        )
        
        # Count generated files
        doc_files = list(result_path.rglob(f"*.{format}"))
        file_count = len(doc_files)
        
        show_success_panel(
            "Documentation Generated",
            f"Successfully generated {format.upper()} docs for {org_repo} {release}\\n" +
            f"📁 Location: {result_path}\\n" +
            f"📄 Files: {file_count} {format} files\\n" +
            f"🎨 Template: {template or 'default'}",
            [
                f"Open directory: open {result_path}",
                "Deploy to your documentation platform",
                f"Export other formats: Repolex export docs {org_repo} {release} --format <format> --output <dir>"
            ]
        )
    
    _export_docs()

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
    
    Run custom SPARQL queries to explore the semantic knowledge.
    Results can be displayed in multiple formats.
    
    Examples:
      Repolex query sparql "SELECT ?name WHERE { ?f woc:hasName ?name }"
      Repolex query sparql "SELECT * WHERE { ?s ?p ?o } LIMIT 10" --format json
      Repolex query sparql "<complex-query>" --output results.csv --format csv
    """
    
    def _query_sparql():
        console.print(f"⚡ CHOMP! Executing SPARQL query...")
        console.print(f"🔍 Query: [dim]{sparql_query[:100]}{'...' if len(sparql_query) > 100 else ''}[/dim]")
        
        core = RepolexManager()
        
        result = core.query_sparql(sparql_query, format, Path(output) if output else None)
        
        if output:
            show_success_panel(
                "SPARQL Query Complete",
                f"Query executed successfully\\n" +
                f"📁 Results saved: {output}\\n" +
                f"📊 Rows: {result.row_count}\\n" +
                f"⚡ Execution time: {result.execution_time:.2f}s",
                [f"View results: open {output}"]
            )
        else:
            # Display results directly
            if result.formatted_output:
                console.print(f"\\n📊 Results ({result.row_count} rows):")
                console.print(result.formatted_output)
            else:
                show_info_panel("No Results", "Query returned no results")
            
            console.print(f"\\n⚡ Execution time: {result.execution_time:.2f}s")
    
    _query_sparql()

@query.command("functions")
@click.argument("search_term")
@click.option("--repo", help="Limit search to specific repository")
@click.option("--release", help="Limit search to specific release")
@click.option("--limit", type=int, default=20, help="Maximum results to show")
@handle_errors
def query_functions(search_term: str, repo: Optional[str], release: Optional[str], limit: int):
    """
    🔍 Search functions using natural language
    
    Find functions across your semantic database using natural language.
    Searches function names, descriptions, and semantic tags.
    
    Examples:
      Repolex query functions "create table"
      Repolex query functions "image processing" --repo pixeltable/pixeltable
      Repolex query functions "database" --repo myorg/repo --release v1.0.0 --limit 5
    """
    if repo:
        validate_org_repo(repo)
    if release:
        validate_release_tag(release)
    
    def _query_functions():
        console.print(f"🔍 CHOMP! Searching for functions: [bold blue]{search_term}[/bold blue]")
        if repo:
            console.print(f"   📁 Repository: {repo}")
        if release:
            console.print(f"   🏷️ Release: {release}")
        
        core = RepolexManager()
        results = core.query_functions(search_term, repo, release)
        
        if not results:
            show_info_panel(
                "No Functions Found",
                f"No functions found matching: {search_term}\\n\\n" +
                "Try different search terms or check:\\n" +
                "• Repolex graph list - see available repositories\\n" +
                "• Repolex repo list - see tracked repositories"
            )
            return
        
        # Show results in a nice table
        table = Table(title=f"🔍 Found {len(results)} functions matching: {search_term}")
        table.add_column("Score", style="yellow", width=8)
        table.add_column("Function", style="bold blue")
        table.add_column("Repository", style="green")
        table.add_column("Description", style="dim")
        
        # Show top results (limited by --limit)
        for func in results[:limit]:
            # Create relevance score
            score = getattr(func, 'relevance_score', 0.0)
            score_str = f"{score:.2f}"
            
            # Truncate description
            description = getattr(func, 'description', '')
            if description and len(description) > 60:
                description = description[:57] + "..."
            
            table.add_row(
                score_str,
                func.name,
                getattr(func, 'repository', 'Unknown'),
                description or "No description"
            )
        
        console.print(table)
        
        if len(results) > limit:
            console.print(f"\\n📊 Showing top {limit} of {len(results)} results")
            console.print(f"Use --limit {len(results)} to see all results")
        
        # Show helpful next steps
        show_info_panel(
            "Next Steps",
            "• View function details: Repolex graph show <org/repo>\\n" +
            "• Export for browsing: Repolex export opml <org/repo> <release>\\n" +
            "• Try different search terms for more results"
        )
    
    _query_functions()

# ============================================================================
# 🔧 SYSTEM COMMANDS - Configuration and Status
# ============================================================================

@cli.command("show")
@click.argument("resource", type=click.Choice(["config", "status"]))
@handle_errors
def show(resource: str):
    """
    📊 Show system information (config or status)
    
    Examples:
      Repolex show config
      Repolex show status
    """
    def _show():
        core = RepolexManager()
        core.initialize()  # 🟡 PAC-MAN startup sequence!
        
        if resource == "config":
            config = core.show_config()
            
            # Create config display
            info_text = Text()
            info_text.append("🔧 System Configuration:\\n", style="bold blue")
            
            for key, value in config.items():
                info_text.append(f"  {key}: ", style="bold")
                info_text.append(f"{value}\\n")
            
            console.print(Panel(
                info_text, 
                title="🔧 Configuration",
                border_style="blue",
                padding=(1, 2)
            ))
            
            show_info_panel(
                "Configuration",
                "Update settings: Repolex update config <key> <value>"
            )
            
        elif resource == "status":
            status = core.show_status()
            
            # Create status display with PAC-MAN flair
            status_text = Text()
            status_text.append("🟡 WAKA WAKA! System Status:\\n", style="bold yellow")
            status_text.append(f"📁 Repositories: {getattr(status, 'repository_count', 0)}\\n")
            status_text.append(f"🧠 Graphs: {getattr(status, 'graph_count', 0)}\\n")
            status_text.append(f"💾 Database Size: {getattr(status, 'database_size_mb', 0):.1f}MB\\n")
            status_text.append(f"📦 Export Files: {getattr(status, 'export_count', 0)}\\n")
            status_text.append(f"📁 Storage Path: {getattr(status, 'storage_path', 'Unknown')}\\n")
            status_text.append(f"⏰ Uptime: {getattr(status, 'uptime', 'Unknown')}\\n")
            
            # Show recent errors if any
            recent_errors = getattr(status, 'recent_errors', [])
            if recent_errors:
                status_text.append(f"\\n👻 Recent Errors ({len(recent_errors)}):\\n", style="bold red")
                for error in recent_errors[-3:]:  # Last 3 errors
                    status_text.append(f"  • {error}\\n", style="red")
            
            console.print(Panel(
                status_text,
                title="📊 System Status",
                border_style="green" if not recent_errors else "red",
                padding=(1, 2)
            ))
    
    _show()

@cli.command("update")
@click.argument("resource", type=click.Choice(["config"]))
@click.argument("key")
@click.argument("value")
@handle_errors
def update(resource: str, key: str, value: str):
    """
    🔧 Update system settings
    
    Examples:
      Repolex update config github-token ghp_xxxxxxxxxxxx
      Repolex update config storage-path /custom/path
    """
    def _update():
        core = RepolexManager()
        
        if resource == "config":
            console.print(f"🔧 CHOMP! Updating configuration: [bold blue]{key}[/bold blue] = [bold green]{value}[/bold green]")
            
            result = core.update_config(key, value)
            
            if result:
                show_success_panel(
                    "Configuration Updated",
                    f"Successfully updated {key} = {value}",
                    ["View all settings: Repolex show config"]
                )
            else:
                show_error_panel(
                    "Configuration Error",
                    f"Failed to update {key}",
                    [
                        "Check valid configuration keys: Repolex show config",
                        "Verify the value format is correct"
                    ]
                )
    
    _update()
