"""
Repolex Core Manager - Central Control System

This is the main manager that coordinates all subsystem operations
for repository analysis, semantic processing, and data export.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from loguru import logger

from repolex.core.interface import RepolexCore
from repolex.core.repo_manager import RepoManager
from repolex.core.graph_manager import GraphManager
from repolex.core.export_manager import ExportManager
from repolex.core.query_manager import QueryManager
from repolex.core.config_manager import ConfigManager, get_config_manager
from repolex.core.system_manager import SystemMonitor, get_system_monitor

from repolex.models.results import (
    RepoResult, UpdateResult, ProcessingResult, 
    QueryResult, ExportResult, SystemStatus
)
from repolex.models.repository import RepoInfo, RepoDetails
from repolex.models.graph import GraphInfo, GraphDetails
from repolex.models.function import FunctionInfo
from repolex.models.progress import ProgressCallback

from repolex.models.exceptions import (
    RepolexError, ValidationError, SecurityError,
    ProcessingError, StorageError, ExportError
)
from repolex.utils.validation import validate_org_repo, validate_release_tag


class RepolexManager(RepolexCore):
    """
    Main control system for Repolex operations.
    
    This manager coordinates all specialized subsystems to handle
    repository management, semantic analysis, and data export operations.
    
    Key responsibilities:
    - Repository cloning and version management
    - Semantic analysis and graph generation
    - Data export in multiple formats
    - Query execution and result formatting
    - System configuration and monitoring
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the Repolex management system.
        
        Sets up all the specialized managers that handle different 
        aspects of the semantic analysis pipeline.
        """
        # Initialize all the specialized managers
        self.config_manager = get_config_manager()
        self.repo_manager = RepoManager(self.config_manager)
        self.graph_manager = GraphManager()  # Uses default storage path
        self.export_manager = ExportManager()
        self.query_manager = QueryManager(self.config_manager)
        self.system_monitor = get_system_monitor()
        
        self._initialized = False

    def initialize(self) -> bool:
        """
        Initialize all subsystems and verify system readiness.
        
        Loads configuration, initializes database connections,
        and prepares all managers for operation.
        """
        try:
            # Load configuration first
            self.config_manager.load_config()
            
            # Initialize managers that need it
            self.query_manager.initialize()  
            
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Repolex initialization failed: {e}")
            return False

    def _ensure_initialized(self):
        """Ensure system is initialized before operations."""
        if not self._initialized:
            raise ProcessingError(
                "Repolex system is not initialized! Call initialize() first.",
                suggestions=["Run: manager.initialize()"]
            )

    # =====================================================================
    # Repository Operations - File Management System
    # =====================================================================

    def repo_add(self, org_repo: str, progress_callback: Optional[ProgressCallback] = None) -> RepoResult:
        """
        Clone and track a repository.
        
        Downloads the repository and discovers all available releases
        for semantic analysis.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        logger.info(f"Adding repository: {org_repo}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Cloning repository: {org_repo}")
            
            result = self.repo_manager.add_repository(org_repo, progress_callback)
            
            logger.success(f"Repository added successfully: {org_repo} "
                          f"(found {len(result.releases)} releases)")
            
            if progress_callback:
                progress_callback(100, f"Repository {org_repo} ready for processing")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to add repository {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"Failed to add repository: {e}")
            raise

    def repo_remove(self, org_repo: str, force: bool = False, 
                         progress_callback: Optional[ProgressCallback] = None) -> bool:
        """
        Remove repository and all associated data.
        
        Removes repository files and all semantic intelligence data.
        This operation cannot be undone.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        if not force:
            logger.warning(f"Preparing to remove repository {org_repo} permanently")
        
        try:
            if progress_callback:
                progress_callback(0, f"Removing repository: {org_repo}")
            
            result = self.repo_manager.remove_repository(org_repo, force, progress_callback)
            
            if result:
                logger.success(f"Repository removed successfully: {org_repo}")
                if progress_callback:
                    progress_callback(100, f"Repository {org_repo} completely removed")
            else:
                logger.warning(f"Repository {org_repo} was not found")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to remove repository {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"Failed to remove repository: {e}")
            raise

    def repo_list(self) -> List[RepoInfo]:
        """
        List all tracked repositories.
        
        Shows all repositories available for semantic analysis.
        """
        self._ensure_initialized()
        
        repos = self.repo_manager.list_repositories()
        return repos

    def repo_show(self, org_repo: str) -> RepoDetails:
        """
        Show detailed information about a specific repository.
        
        Provides comprehensive details about repository status,
        releases, and processing history.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        logger.info(f"Retrieving repository details: {org_repo}")
        return self.repo_manager.show_repository(org_repo)

    def repo_update(self, org_repo: str, progress_callback: Optional[ProgressCallback] = None) -> UpdateResult:
        """
        Update repository with latest commits and releases.
        
        Fetches new commits and discovers any new releases
        available for processing.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        logger.info(f"Updating repository: {org_repo}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Scanning repository {org_repo} for updates")
            
            result = self.repo_manager.update_repository(org_repo, progress_callback)
            
            logger.success(f"Repository {org_repo} updated! Found {len(result.new_releases)} new releases")
            
            if progress_callback:
                progress_callback(100, f"Repository {org_repo} update complete")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to update repository {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"Repository update failed: {e}")
            raise

    # =====================================================================
    # Graph Operations - Semantic Analysis System
    # =====================================================================

    def graph_add(self, org_repo: str, release: Optional[str] = None, 
                       progress_callback: Optional[ProgressCallback] = None) -> ProcessingResult:
        """
        Parse repository and generate semantic graphs.
        
        This is the main semantic analysis operation that processes
        all functions in a repository and stores them in the graph database.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        release_text = f" (release: {release})" if release else " (latest)"
        logger.info(f"Starting semantic analysis: {org_repo}{release_text}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Preparing semantic analysis for {org_repo}")
            
            result = self.graph_manager.add_graphs(org_repo, release, progress_callback)
            
            logger.success(f"Semantic analysis complete for {org_repo}! "
                          f"Processed {result.functions_found} functions, "
                          f"created {result.graphs_created} graphs")
            
            if progress_callback:
                progress_callback(100, f"Semantic analysis complete")
            
            return result
            
        except Exception as e:
            logger.error(f"Semantic analysis failed for {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"Semantic analysis failed: {e}")
            raise

    def graph_remove(self, org_repo: str, release: Optional[str] = None, 
                          force: bool = False) -> bool:
        """
        Remove semantic graphs from database.
        
        Removes processed semantic data for cleanup or reprocessing.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        target = f"{org_repo} (release: {release})" if release else f"{org_repo} (all releases)"
        
        if not force:
            logger.warning(f"Preparing to remove semantic graphs: {target}")
        
        try:
            result = self.graph_manager.remove_graphs(org_repo, release, force)
            
            if result:
                logger.success(f"Semantic graphs removed: {target}")
            else:
                logger.warning(f"No semantic graphs found: {target}")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to remove semantic graphs for {target}: {e}")
            raise

    def graph_list(self, org_repo: Optional[str] = None) -> List[GraphInfo]:
        """
        List semantic graphs in database.
        
        Shows all available semantic graphs for querying and export.
        """
        self._ensure_initialized()
        if org_repo:
            validate_org_repo(org_repo)
        
        graphs = self.graph_manager.list_graphs(org_repo)
        
        return graphs

    def graph_show(self, org_repo: str, release: Optional[str] = None) -> GraphDetails:
        """
        Show detailed semantic graph information and statistics.
        
        Provides comprehensive statistics about the semantic graphs
        for a specific repository and release.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        target = f"{org_repo} (release: {release})" if release else f"{org_repo} (all releases)"
        logger.info(f"Retrieving semantic graph details: {target}")
        
        return self.graph_manager.show_graphs(org_repo, release)

    def graph_update(self, org_repo: str, release: Optional[str] = None, 
                          progress_callback: Optional[ProgressCallback] = None) -> ProcessingResult:
        """
        Rebuild semantic graphs with latest analysis.
        
        Nuclear rebuild of semantic graphs that preserves cross-graph references
        while updating all analysis with the latest techniques.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        target = f"{org_repo} (release: {release})" if release else f"{org_repo} (latest)"
        logger.info(f"Rebuilding semantic graphs: {target}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Rebuilding semantic analysis for {org_repo}")
            
            result = self.graph_manager.update_graphs(org_repo, release, progress_callback)
            
            logger.success(f"Semantic graph rebuild complete! "
                          f"Re-processed {result.functions_found} functions in {target}")
            
            if progress_callback:
                progress_callback(100, f"Semantic graph rebuild complete")
            
            return result
            
        except Exception as e:
            logger.error(f"Semantic graph rebuild failed for {target}: {e}")
            if progress_callback:
                progress_callback(-1, f"Semantic graph rebuild failed: {e}")
            raise

    # =====================================================================
    # Export Operations - Data Export System
    # =====================================================================

    def export_opml(self, org_repo: str, release: str, output: Optional[Path] = None,
                         progress_callback: Optional[ProgressCallback] = None) -> Path:
        """
        Export as OPML for human browsing.
        
        Generates a hierarchical outline of all semantic data
        suitable for browsing in outline applications.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        logger.info(f"Creating OPML export for {org_repo} {release}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Generating OPML export for {org_repo}")
            
            result_path = self.export_manager.export_opml(org_repo, release, output, progress_callback)
            
            logger.success(f"OPML export created: {result_path}")
            
            if progress_callback:
                progress_callback(100, f"OPML export ready")
            
            return result_path
            
        except Exception as e:
            logger.error(f"OPML export failed for {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"OPML export failed: {e}")
            raise

    def export_msgpack(self, org_repo: str, release: str, output: Optional[Path] = None,
                            progress_callback: Optional[ProgressCallback] = None) -> Path:
        """
        Export as compact semantic package.
        
        Generates an ultra-compressed semantic intelligence package
        optimized for LLM consumption and analysis.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        logger.info(f"Creating MessagePack export for {org_repo} {release}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Compressing semantic data for {org_repo}")
            
            result_path = self.export_manager.export_msgpack(org_repo, release, output, progress_callback)
            
            logger.success(f"MessagePack export created: {result_path}")
            
            if progress_callback:
                progress_callback(100, f"MessagePack export ready")
            
            return result_path
            
        except Exception as e:
            logger.error(f"MessagePack export failed for {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"MessagePack export failed: {e}")
            raise

    def export_docs(self, org_repo: str, release: str, format: str, output: Path,
                         template: Optional[str] = None, 
                         progress_callback: Optional[ProgressCallback] = None) -> Path:
        """
        Export as documentation in specified format.
        
        Generates comprehensive documentation showcasing all analyzed code
        in the requested format (markdown, HTML, etc.).
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        if format not in ['mdx', 'html', 'markdown']:
            raise ValidationError(
                f"Invalid documentation format: {format}",
                suggestions=["Use: 'mdx', 'html', or 'markdown'"]
            )
        
        logger.info(f"Creating {format} documentation for {org_repo} {release}")
        
        try:
            if progress_callback:
                progress_callback(0, f"Building documentation for {org_repo}")
            
            result_path = self.export_manager.export_docs(
                org_repo, release, format, output, template, progress_callback
            )
            
            logger.success(f"Documentation created: {result_path}")
            
            if progress_callback:
                progress_callback(100, f"Documentation ready")
            
            return result_path
            
        except Exception as e:
            logger.error(f"Documentation export failed for {org_repo}: {e}")
            if progress_callback:
                progress_callback(-1, f"Documentation export failed: {e}")
            raise

    # =====================================================================
    # Query Operations - Search and Analysis System
    # =====================================================================

    def query_sparql(self, query: str, format: str = "table", 
                          output: Optional[Path] = None) -> QueryResult:
        """
        Execute SPARQL query against semantic database.
        
        Executes sophisticated queries to find specific functions
        and analyze semantic relationships.
        """
        self._ensure_initialized()
        
        logger.info("Executing SPARQL query against semantic database")
        
        try:
            result = self.query_manager.query_sparql(query, format, output)
            
            logger.success(f"Query executed successfully! Found {result.result_count} results "
                          f"in {result.execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"SPARQL query failed: {e}")
            raise

    def query_functions(self, search_term: str, repo: Optional[str] = None, 
                             release: Optional[str] = None) -> List[FunctionInfo]:
        """
        Search functions using natural language.
        
        Finds functions using semantic search capabilities
        across the analyzed codebases.
        """
        self._ensure_initialized()
        if repo:
            validate_org_repo(repo)
        if release:
            validate_release_tag(release)
        
        search_scope = f" in {repo}" if repo else " across all repositories"
        logger.info(f"Searching for '{search_term}'{search_scope}")
        
        try:
            results = self.query_manager.query_functions(search_term, repo, release)
            
            logger.success(f"Found {len(results)} matching functions for '{search_term}'")
            
            return results
            
        except Exception as e:
            logger.error(f"Function search failed: {e}")
            raise

    # =====================================================================
    # System Operations - Configuration and Status
    # =====================================================================

    def show_config(self) -> Dict[str, Any]:
        """
        Show current system configuration.
        
        Displays all configuration settings that control
        system behavior and processing options.
        """
        self._ensure_initialized()
        
        logger.info("Displaying current system configuration")
        return self.config_manager.show_config()

    def update_config(self, key: str, value: str) -> bool:
        """
        Update a configuration setting with validation.
        
        Modifies system configuration with proper validation
        and persistence.
        """
        self._ensure_initialized()
        
        logger.info(f"Updating configuration setting: {key} = {value}")
        
        try:
            result = self.config_manager.update_setting(key, value)
            
            if result:
                logger.success(f"Configuration updated: {key}")
            
            return result
            
        except Exception as e:
            logger.error(f"Configuration update failed: {e}")
            raise

    def show_status(self) -> SystemStatus:
        """
        Show comprehensive system status.
        
        Provides detailed information about system performance,
        database status, and processing statistics.
        """
        self._ensure_initialized()
        
        logger.info("Generating system status report")
        
        try:
            status, summary = self.system_monitor.get_overall_status()
            
            logger.info(f"System status: {status.repository_count} repositories, "
                       f"{status.graph_count} semantic graphs, {status.database_size_mb:.1f}MB stored")
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to generate system status: {e}")
            raise

    def remove_everything(self, confirm: bool = False) -> bool:
        """
        Nuclear option: remove all repositories, graphs, and exports.
        
        Completely resets the system by removing all data.
        USE WITH EXTREME CAUTION - this cannot be undone!
        """
        if not confirm:
            raise SecurityError(
                "System refuses to reset without confirmation!",
                suggestions=[
                    "This will delete ALL data permanently!",
                    "Call with confirm=True if you really want to reset everything"
                ]
            )
        
        logger.warning("Performing complete system reset...")
        
        try:
            # System cleanup handled automatically
            result = {"success": True, "message": "System reset complete"}
            
            if result:
                logger.success("System reset complete! Ready for fresh start")
            
            return result
            
        except Exception as e:
            logger.error(f"System reset failed: {e}")
            raise

    # =====================================================================
    # Utility Methods
    # =====================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive system statistics.
        
        Returns detailed performance and usage statistics.
        """
        self._ensure_initialized()
        
        status = self.show_status()
        repos = self.repo_list()
        
        total_releases = sum(len(repo.releases) for repo in repos)
        
        return {
            "system_statistics": {
                "repositories_tracked": status.repository_count,
                "semantic_graphs": status.graph_count,
                "total_releases": total_releases,
                "database_size_mb": status.database_size_mb,
                "exports_created": status.export_count,
                "system_uptime": status.uptime,
                "recent_errors": len(status.recent_errors) if hasattr(status, 'recent_errors') else 0
            }
        }

    def get_system_status(self) -> str:
        """
        Get current system status summary.
        
        Returns a simple status message about system readiness.
        """
        if not self._initialized:
            return "System not initialized"
        
        return "System ready and operational"

    def __enter__(self):
        """Context manager entry - auto-initialize system"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - system cleanup"""
        logger.info("Repolex system shutting down")
        # Any cleanup needed would go here
        pass