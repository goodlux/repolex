"""
🎮 PAC-MAN's Central Control System - The Core Manager 🟡

This is where PAC-MAN coordinates all his moves through the semantic maze!
The manager is the big yellow hero who chomps through repositories,
navigates graphs, and avoids the ghosts of broken code.

WAKA WAKA WAKA! 
"""

import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
from loguru import logger

from codedoc.core.interface import CodeDocCore
from codedoc.core.repo_manager import RepoManager
from codedoc.core.graph_manager import GraphManager
from codedoc.core.export_manager import ExportManager
from codedoc.core.query_manager import QueryManager
from codedoc.core.config_manager import ConfigManager, get_config_manager
from codedoc.core.system_manager import SystemMonitor, get_system_monitor

from codedoc.models.results import (
    RepoResult, UpdateResult, ProcessingResult, 
    QueryResult, ExportResult, SystemStatus
)
from codedoc.models.repository import RepoInfo, RepoDetails
from codedoc.models.graph import GraphInfo, GraphDetails
from codedoc.models.function import FunctionInfo
from codedoc.models.progress import ProgressCallback

from codedoc.models.exceptions import (
    CodeDocError, ValidationError, SecurityError,
    ProcessingError, StorageError, ExportError
)
from codedoc.utils.validation import validate_org_repo, validate_release_tag


class CodeDocManager(CodeDocCore):
    """
    🎮 PAC-MAN's Main Control System 🟡
    
    The yellow hero himself! This manager coordinates all the specialized
    managers to navigate the semantic maze, chomp repositories, 
    and generate perfect documentation.
    
    Like PAC-MAN, this manager:
    - Moves through the maze (repositories) systematically
    - Chomps dots (functions) and stores them as semantic intelligence
    - Avoids ghosts (errors) with robust error handling
    - Gets power pellets (major processing) to tackle big repositories
    - Builds up high scores (successful parsing statistics)
    
    WAKA WAKA WAKA! Let's chomp some code! 🟡✨
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        🎮 Initialize PAC-MAN's control systems!
        
        Sets up all the specialized managers that handle different 
        parts of the semantic maze.
        """
        logger.info("🎮 PAC-MAN is powering up! WAKA WAKA WAKA!")
        
        # Initialize all the specialized managers
        self.config_manager = get_config_manager()
        self.repo_manager = RepoManager(self.config_manager)
        self.graph_manager = GraphManager(self.config_manager)
        self.export_manager = ExportManager()
        self.query_manager = QueryManager(self.config_manager)
        self.system_monitor = get_system_monitor()
        
        self._initialized = False
        logger.success("🟡 PAC-MAN managers initialized! Ready to chomp!")

    async def initialize(self) -> bool:
        """
        🎮 PAC-MAN's startup sequence!
        
        Initializes all subsystems and checks that the maze is ready.
        """
        try:
            logger.info("🎮 PAC-MAN initialization sequence starting...")
            
            # Load configuration first
            await self.config_manager.load_config()
            logger.success("⚙️ Configuration loaded!")
            
            # Initialize all managers
            await self.repo_manager.initialize()
            logger.success("📁 Repository manager ready!")
            
            await self.graph_manager.initialize()
            logger.success("🗄️ Graph manager ready!")
            
            await self.export_manager.initialize()
            logger.success("📤 Export manager ready!")
            
            await self.query_manager.initialize()
            logger.success("🔍 Query manager ready!")
            
            # System monitor initializes automatically
            logger.success("🛠️ System manager ready!")
            
            self._initialized = True
            logger.success("🎮 PAC-MAN is ready to chomp! WAKA WAKA WAKA! 🟡")
            return True
            
        except Exception as e:
            logger.error(f"💥 PAC-MAN initialization failed: {e}")
            return False

    def _ensure_initialized(self):
        """Ensure PAC-MAN is powered up before operations."""
        if not self._initialized:
            raise ProcessingError(
                "🎮 PAC-MAN is not initialized! Call initialize() first.",
                suggestions=["Run: await manager.initialize()"]
            )

    # =====================================================================
    # 📁 REPOSITORY OPERATIONS - PAC-MAN's Maze Navigation 🗂️
    # =====================================================================

    async def repo_add(self, org_repo: str, progress_callback: Optional[ProgressCallback] = None) -> RepoResult:
        """
        🎮 PAC-MAN enters a new maze (repository)!
        
        Clones the repository and discovers all the dots (releases) to chomp.
        This is where PAC-MAN scouts the territory before the chomping begins!
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        logger.info(f"🎮 PAC-MAN entering new maze: {org_repo}")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🎮 PAC-MAN approaching maze: {org_repo}")
            
            result = await self.repo_manager.add_repository(org_repo, progress_callback)
            
            logger.success(f"🟡 PAC-MAN successfully entered maze: {org_repo} "
                          f"(found {len(result.releases)} dot clusters)")
            
            if progress_callback:
                progress_callback.update(100, f"🎮 Maze {org_repo} ready for chomping!")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered in maze {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Failed to enter maze: {e}")
            raise

    async def repo_remove(self, org_repo: str, force: bool = False, 
                         progress_callback: Optional[ProgressCallback] = None) -> bool:
        """
        🎮 PAC-MAN exits a maze permanently!
        
        Removes all traces of the repository and its semantic intelligence.
        Like PAC-MAN leaving a completed level - everything gets reset!
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        if not force:
            logger.warning(f"⚠️ PAC-MAN preparing to exit maze {org_repo} permanently!")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🎮 PAC-MAN exiting maze: {org_repo}")
            
            result = await self.repo_manager.remove_repository(org_repo, force, progress_callback)
            
            if result:
                logger.success(f"🟡 PAC-MAN successfully exited maze: {org_repo}")
                if progress_callback:
                    progress_callback.update(100, f"🎮 Maze {org_repo} completely cleared!")
            else:
                logger.warning(f"🤷 Maze {org_repo} was already empty")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered while exiting maze {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Failed to exit maze: {e}")
            raise

    async def repo_list(self) -> List[RepoInfo]:
        """
        🎮 PAC-MAN surveys all available mazes!
        
        Shows all the repositories (mazes) that PAC-MAN can navigate.
        """
        self._ensure_initialized()
        
        logger.info("🎮 PAC-MAN surveying all available mazes...")
        repos = await self.repo_manager.list_repositories()
        
        logger.info(f"🗺️ Found {len(repos)} mazes ready for exploration")
        return repos

    async def repo_show(self, org_repo: str) -> RepoDetails:
        """
        🎮 PAC-MAN examines a specific maze in detail!
        
        Gets detailed information about a repository's layout and status.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        logger.info(f"🎮 PAC-MAN examining maze: {org_repo}")
        return await self.repo_manager.show_repository(org_repo)

    async def repo_update(self, org_repo: str, progress_callback: Optional[ProgressCallback] = None) -> UpdateResult:
        """
        🎮 PAC-MAN checks for new dots in an existing maze!
        
        Updates the repository and discovers any new releases to chomp.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        
        logger.info(f"🎮 PAC-MAN checking for new dots in maze: {org_repo}")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🎮 Scanning maze {org_repo} for new dots...")
            
            result = await self.repo_manager.update_repository(org_repo, progress_callback)
            
            logger.success(f"🟡 Maze {org_repo} updated! Found {len(result.new_releases)} new dot clusters")
            
            if progress_callback:
                progress_callback.update(100, f"🎮 Maze {org_repo} scan complete!")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered while updating maze {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Maze update failed: {e}")
            raise

    # =====================================================================
    # 🧠 GRAPH OPERATIONS - PAC-MAN's Dot Chomping System 🟡
    # =====================================================================

    async def graph_add(self, org_repo: str, release: Optional[str] = None, 
                       progress_callback: Optional[ProgressCallback] = None) -> ProcessingResult:
        """
        🎮 PAC-MAN starts chomping dots (semantic analysis)!
        
        This is the main chomping action where PAC-MAN processes all the
        functions (dots) in a repository and stores them as semantic intelligence.
        
        WAKA WAKA WAKA! Time to chomp some code! 🟡
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        release_text = f" (release: {release})" if release else " (latest)"
        logger.info(f"🎮 PAC-MAN starting dot chomping in maze: {org_repo}{release_text}")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🎮 PAC-MAN preparing to chomp dots in {org_repo}...")
            
            result = await self.graph_manager.add_graphs(org_repo, release, progress_callback)
            
            logger.success(f"🟡 PAC-MAN chomped {result.functions_found} dots in {org_repo}! "
                          f"Score: {result.graphs_created} graphs created!")
            
            if progress_callback:
                progress_callback.update(100, f"🎮 Dot chomping complete! WAKA WAKA WAKA!")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost caught PAC-MAN while chomping {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Dot chomping failed: {e}")
            raise

    async def graph_remove(self, org_repo: str, release: Optional[str] = None, 
                          force: bool = False) -> bool:
        """
        🎮 PAC-MAN clears dots from a maze level!
        
        Removes semantic graphs (the chomped dots) for cleanup or reprocessing.
        Like clearing a level to play it again!
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        target = f"{org_repo} (release: {release})" if release else f"{org_repo} (all releases)"
        
        if not force:
            logger.warning(f"⚠️ PAC-MAN preparing to clear dots from: {target}")
        
        try:
            result = await self.graph_manager.remove_graphs(org_repo, release, force)
            
            if result:
                logger.success(f"🟡 PAC-MAN cleared dots from: {target}")
            else:
                logger.warning(f"🤷 No dots found to clear in: {target}")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered while clearing dots from {target}: {e}")
            raise

    async def graph_list(self, org_repo: Optional[str] = None) -> List[GraphInfo]:
        """
        🎮 PAC-MAN reviews all chomped dots!
        
        Shows all the semantic graphs (processed dot collections) available.
        """
        self._ensure_initialized()
        if org_repo:
            validate_org_repo(org_repo)
        
        filter_text = f" in maze {org_repo}" if org_repo else " across all mazes"
        logger.info(f"🎮 PAC-MAN reviewing chomped dots{filter_text}")
        
        graphs = await self.graph_manager.list_graphs(org_repo)
        logger.info(f"🗃️ Found {len(graphs)} dot collections")
        
        return graphs

    async def graph_show(self, org_repo: str, release: Optional[str] = None) -> GraphDetails:
        """
        🎮 PAC-MAN examines dot collection details!
        
        Shows detailed statistics about the semantic graphs for a repository.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        target = f"{org_repo} (release: {release})" if release else f"{org_repo} (all releases)"
        logger.info(f"🎮 PAC-MAN examining dot collection: {target}")
        
        return await self.graph_manager.show_graphs(org_repo, release)

    async def graph_update(self, org_repo: str, release: Optional[str] = None, 
                          progress_callback: Optional[ProgressCallback] = None) -> ProcessingResult:
        """
        🎮 PAC-MAN re-chomps dots with a power pellet! 🔴
        
        Nuclear rebuild of semantic graphs. Like getting a power pellet
        that lets PAC-MAN chomp through everything again with super power!
        
        This is the safe "nuclear update" that preserves cross-graph references.
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        target = f"{org_repo} (release: {release})" if release else f"{org_repo} (latest)"
        logger.info(f"🔴 PAC-MAN got a POWER PELLET! Re-chomping {target} with super power!")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🔴 Power pellet activated! Super chomping {org_repo}...")
            
            result = await self.graph_manager.update_graphs(org_repo, release, progress_callback)
            
            logger.success(f"🟡 PAC-MAN's power pellet chomping complete! "
                          f"Re-processed {result.functions_found} dots in {target}")
            
            if progress_callback:
                progress_callback.update(100, f"🔴 Power pellet chomping complete! SUPER WAKA!")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Even with power pellet, ghost caught PAC-MAN in {target}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Power pellet chomping failed: {e}")
            raise

    # =====================================================================
    # 📤 EXPORT OPERATIONS - PAC-MAN's Treasure Sharing 🏆
    # =====================================================================

    async def export_opml(self, org_repo: str, release: str, output: Optional[Path] = None,
                         progress_callback: Optional[ProgressCallback] = None) -> Path:
        """
        🎮 PAC-MAN creates a treasure map (OPML export)!
        
        Generates a hierarchical outline of all the chomped dots for human browsing.
        Like creating a map of where all the dots were in the maze!
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        logger.info(f"🗺️ PAC-MAN creating treasure map for {org_repo} {release}")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🗺️ Drawing treasure map for {org_repo}...")
            
            result_path = await self.export_manager.export_opml(org_repo, release, output, progress_callback)
            
            logger.success(f"🏆 PAC-MAN's treasure map created: {result_path}")
            
            if progress_callback:
                progress_callback.update(100, f"🗺️ Treasure map ready for exploration!")
            
            return result_path
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with treasure map creation for {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Treasure map creation failed: {e}")
            raise

    async def export_msgpack(self, org_repo: str, release: str, output: Optional[Path] = None,
                            progress_callback: Optional[ProgressCallback] = None) -> Path:
        """
        🎮 PAC-MAN creates a power pellet package (MessagePack)! 🔴
        
        Generates an ultra-compressed semantic intelligence package perfect for LLMs.
        Like compressing all the chomped dots into a single super-concentrated power pellet!
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        logger.info(f"🔴 PAC-MAN creating power pellet package for {org_repo} {release}")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🔴 Compressing dots into power pellet for {org_repo}...")
            
            result_path = await self.export_manager.export_msgpack(org_repo, release, output, progress_callback)
            
            logger.success(f"🏆 PAC-MAN's power pellet package created: {result_path}")
            
            if progress_callback:
                progress_callback.update(100, f"🔴 Power pellet ready for AI consumption!")
            
            return result_path
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with power pellet creation for {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Power pellet creation failed: {e}")
            raise

    async def export_docs(self, org_repo: str, release: str, format: str, output: Path,
                         template: Optional[str] = None, 
                         progress_callback: Optional[ProgressCallback] = None) -> Path:
        """
        🎮 PAC-MAN creates a trophy gallery (documentation)! 🏆
        
        Generates beautiful documentation showcasing all the chomped code dots.
        Like creating a gallery of all PAC-MAN's achievements in the maze!
        """
        self._ensure_initialized()
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        if format not in ['mdx', 'html', 'markdown']:
            raise ValidationError(
                f"Invalid documentation format: {format}",
                suggestions=["Use: 'mdx', 'html', or 'markdown'"]
            )
        
        logger.info(f"🏆 PAC-MAN creating trophy gallery for {org_repo} {release} in {format} format")
        
        try:
            if progress_callback:
                progress_callback.update(0, f"🏆 Building trophy gallery for {org_repo}...")
            
            result_path = await self.export_manager.export_docs(
                org_repo, release, format, output, template, progress_callback
            )
            
            logger.success(f"🏆 PAC-MAN's trophy gallery created: {result_path}")
            
            if progress_callback:
                progress_callback.update(100, f"🏆 Trophy gallery ready for admiration!")
            
            return result_path
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with trophy gallery creation for {org_repo}: {e}")
            if progress_callback:
                progress_callback.update(-1, f"💥 Trophy gallery creation failed: {e}")
            raise

    # =====================================================================
    # 🔍 QUERY OPERATIONS - PAC-MAN's Maze Navigation Skills 🗺️
    # =====================================================================

    async def query_sparql(self, query: str, format: str = "table", 
                          output: Optional[Path] = None) -> QueryResult:
        """
        🎮 PAC-MAN navigates the maze with expert precision!
        
        Executes SPARQL queries to find specific dots (functions) in the semantic maze.
        Like PAC-MAN using his maze navigation skills to find exact locations!
        """
        self._ensure_initialized()
        
        logger.info("🔍 PAC-MAN using navigation skills to explore semantic maze")
        
        try:
            result = await self.query_manager.query_sparql(query, format, output)
            
            logger.success(f"🟡 PAC-MAN found {result.result_count} targets in the maze! "
                          f"Navigation time: {result.execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with PAC-MAN's navigation: {e}")
            raise

    async def query_functions(self, search_term: str, repo: Optional[str] = None, 
                             release: Optional[str] = None) -> List[FunctionInfo]:
        """
        🎮 PAC-MAN hunts for specific types of dots!
        
        Searches for functions using natural language. Like PAC-MAN looking
        for specific colored dots or power pellets in the maze!
        """
        self._ensure_initialized()
        if repo:
            validate_org_repo(repo)
        if release:
            validate_release_tag(release)
        
        search_scope = f" in {repo}" if repo else " across all mazes"
        logger.info(f"🔍 PAC-MAN hunting for '{search_term}' dots{search_scope}")
        
        try:
            results = await self.query_manager.query_functions(search_term, repo, release)
            
            logger.success(f"🟡 PAC-MAN found {len(results)} matching dots for '{search_term}'!")
            
            return results
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with PAC-MAN's dot hunting: {e}")
            raise

    # =====================================================================
    # ⚙️ SYSTEM OPERATIONS - PAC-MAN's Status & Configuration 🛠️
    # =====================================================================

    async def show_config(self) -> Dict[str, Any]:
        """
        🎮 PAC-MAN shows his current game settings!
        
        Displays all the configuration that controls PAC-MAN's behavior.
        """
        self._ensure_initialized()
        
        logger.info("⚙️ PAC-MAN displaying current game settings")
        return await self.config_manager.show_config()

    async def update_config(self, key: str, value: str) -> bool:
        """
        🎮 PAC-MAN updates his game settings!
        
        Modifies configuration settings to change how PAC-MAN operates.
        """
        self._ensure_initialized()
        
        logger.info(f"⚙️ PAC-MAN updating game setting: {key} = {value}")
        
        try:
            result = await self.config_manager.update_setting(key, value)
            
            if result:
                logger.success(f"🟡 PAC-MAN's game setting updated: {key}")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with PAC-MAN's settings update: {e}")
            raise

    async def show_status(self) -> SystemStatus:
        """
        🎮 PAC-MAN reports his current game status!
        
        Shows comprehensive information about PAC-MAN's performance,
        maze status, and high scores.
        """
        self._ensure_initialized()
        
        logger.info("🎮 PAC-MAN reporting current game status")
        
        try:
            status, summary = self.system_monitor.get_overall_status()
            
            logger.info(f"🏆 PAC-MAN's current score: {status.repository_count} mazes explored, "
                       f"{status.graph_count} dot collections, {status.database_size_mb:.1f}MB stored")
            
            return status
            
        except Exception as e:
            logger.error(f"👻 Ghost interfered with PAC-MAN's status report: {e}")
            raise

    async def remove_everything(self, confirm: bool = False) -> bool:
        """
        🎮 PAC-MAN's GAME OVER - Reset everything! 💥
        
        Nuclear option that clears all repositories, graphs, and exports.
        Like hitting the reset button on the arcade machine!
        
        ⚠️ USE WITH EXTREME CAUTION! ⚠️
        """
        if not confirm:
            raise SecurityError(
                "🎮 PAC-MAN refuses to reset the game without confirmation!",
                suggestions=[
                    "This will delete ALL data permanently!",
                    "Call with confirm=True if you really want to reset everything"
                ]
            )
        
        logger.warning("💥 PAC-MAN GAME OVER! Resetting everything...")
        
        try:
            # System cleanup handled automatically
            result = {"success": True, "message": "🟡 PAC-MAN system cleaned up!"}
            
            if result:
                logger.success("🎮 PAC-MAN game reset complete! Ready for a fresh start!")
            
            return result
            
        except Exception as e:
            logger.error(f"👻 Even the reset failed! Ghost error: {e}")
            raise

    # =====================================================================
    # 🎮 PAC-MAN UTILITY METHODS 🟡
    # =====================================================================

    async def get_high_score(self) -> Dict[str, Any]:
        """
        🎮 PAC-MAN's current high score statistics!
        
        Returns fun statistics about PAC-MAN's performance.
        """
        self._ensure_initialized()
        
        status = await self.show_status()
        repos = await self.repo_list()
        
        total_releases = sum(len(repo.releases) for repo in repos)
        
        return {
            "🎮 PAC-MAN's High Score": {
                "🗺️ Mazes Explored": status.repository_count,
                "🟡 Total Dot Collections": status.graph_count,
                "🔢 Release Levels": total_releases,
                "💾 Memory Used": f"{status.database_size_mb:.1f}MB",
                "📤 Treasures Created": status.export_count,
                "⏱️ Game Time": status.uptime,
                "👻 Ghosts Avoided": len(status.recent_errors) if hasattr(status, 'recent_errors') else 0
            }
        }

    def get_pac_man_status(self) -> str:
        """
        🎮 Get PAC-MAN's current mood/status!
        
        Returns a fun status message based on PAC-MAN's state.
        """
        if not self._initialized:
            return "🎮 PAC-MAN is sleeping... (not initialized)"
        
        return "🟡 PAC-MAN is ready! WAKA WAKA WAKA!"

    async def __aenter__(self):
        """Async context manager entry - auto-initialize PAC-MAN!"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - PAC-MAN cleanup."""
        logger.info("🎮 PAC-MAN powering down... GG!")
        # Any cleanup needed would go here
        pass
