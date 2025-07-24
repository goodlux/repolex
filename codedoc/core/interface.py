"""
🎮 PAC-MAN's Control System - Abstract CodeDoc Interface 🎮

The master interface that defines how PAC-MAN navigates the semantic maze!
Every move PAC-MAN makes follows these rules - no exceptions!

WAKA WAKA! 🟡
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, AsyncIterator
from pathlib import Path

from ..models.repository import RepoInfo, RepoDetails, RepoResult, UpdateResult
from ..models.graph import GraphInfo, GraphDetails
from ..models.results import (
    ProcessingResult,
    QueryResult, 
    ExportResult, 
    SystemStatus,
    ProgressCallback
)
from ..models.function import FunctionInfo


class CodeDocCore(ABC):
    """
    🎮 PAC-MAN's Abstract Control Interface 🎮
    
    This is the master rulebook for how PAC-MAN moves through the semantic maze!
    Every operation follows these rules - whether PAC-MAN is chomping dots (parsing),
    avoiding ghosts (handling errors), or finding power pellets (exporting data).
    
    🟡 WAKA WAKA! No implementation details here - just the sacred contract! 🟡
    """
    
    # ═══════════════════════════════════════════════════════════════
    # 🎮 MAZE EXPLORATION - Repository Operations (File Management)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    async def repo_add(
        self, 
        org_repo: str, 
        progress_callback: Optional[ProgressCallback] = None
    ) -> RepoResult:
        """
        🎮 Discover a new maze level! 🎮
        
        PAC-MAN enters a new repository maze and maps out all the available
        levels (releases). This is like finding a new arcade cabinet!
        
        Args:
            org_repo: The maze identifier (e.g., 'pixeltable/pixeltable')
            progress_callback: Watch PAC-MAN's exploration progress
            
        Returns:
            RepoResult: All the levels PAC-MAN found and their dot counts
            
        Raises:
            ValidationError: If maze coordinates are invalid
            SecurityError: If maze contains ghosts (dangerous paths)
            GitError: If the arcade cabinet is broken
        """
        pass
    
    @abstractmethod
    async def repo_remove(
        self, 
        org_repo: str, 
        force: bool = False,
        progress_callback: Optional[ProgressCallback] = None
    ) -> bool:
        """
        🎮 Destroy an entire maze! (Careful - this is like unplugging the arcade!) 🎮
        
        PAC-MAN completely removes a maze and ALL the high scores (semantic data).
        This is the nuclear option - like yanking the power cord!
        
        Args:
            org_repo: Which maze to destroy
            force: Skip the "Are you sure?" confirmation
            progress_callback: Watch the destruction progress
            
        Returns:
            bool: True if the maze was successfully destroyed
            
        Raises:
            ValidationError: If maze identifier is invalid
            SecurityError: If trying to destroy without permission
        """
        pass
    
    @abstractmethod
    async def repo_list(self) -> List[RepoInfo]:
        """
        🎮 Show PAC-MAN's arcade catalog! 🎮
        
        List all the mazes PAC-MAN knows about - like browsing the
        available games in the arcade!
        
        Returns:
            List[RepoInfo]: All mazes in PAC-MAN's arcade
        """
        pass
    
    @abstractmethod
    async def repo_show(self, org_repo: str) -> RepoDetails:
        """
        🎮 Examine a specific maze in detail! 🎮
        
        PAC-MAN gets the full details about a maze - how many levels,
        when it was last played, what high scores exist, etc.
        
        Args:
            org_repo: Which maze to examine
            
        Returns:
            RepoDetails: Complete maze information and statistics
            
        Raises:
            ValidationError: If maze identifier is invalid
            NotFoundError: If PAC-MAN doesn't know about this maze
        """
        pass
    
    @abstractmethod
    async def repo_update(
        self, 
        org_repo: str,
        progress_callback: Optional[ProgressCallback] = None
    ) -> UpdateResult:
        """
        🎮 Check for new maze levels! 🎮
        
        PAC-MAN checks if the arcade owner added new levels to a maze.
        Like checking for DLC or game updates!
        
        Args:
            org_repo: Which maze to check for updates
            progress_callback: Watch the update check progress
            
        Returns:
            UpdateResult: What new levels were found (if any)
            
        Raises:
            ValidationError: If maze identifier is invalid
            GitError: If can't connect to the arcade's update server
        """
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # 🟡 DOT CHOMPING - Graph Operations (Semantic Analysis)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    async def graph_add(
        self, 
        org_repo: str, 
        release: Optional[str] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> ProcessingResult:
        """
        🎮 PAC-MAN CHOMPS ALL THE DOTS! 🎮
        
        This is the main event! PAC-MAN enters a maze level and chomps
        every single dot, creating perfect semantic knowledge of the entire
        maze layout. WAKA WAKA WAKA! 
        
        Args:
            org_repo: Which maze to enter
            release: Specific level (uses latest if None)
            progress_callback: Watch PAC-MAN chomp in real-time!
            
        Returns:
            ProcessingResult: How many dots chomped, ghosts avoided, power pellets found
            
        Raises:
            ValidationError: If maze coordinates are wrong  
            NotFoundError: If maze or level doesn't exist
            ProcessingError: If PAC-MAN gets caught by a ghost during chomping
            StorageError: If the arcade's memory is full
        """
        pass
    
    @abstractmethod
    async def graph_remove(
        self, 
        org_repo: str, 
        release: Optional[str] = None,
        force: bool = False
    ) -> bool:
        """
        🎮 Clear PAC-MAN's high scores! 🎮
        
        Remove all the dots PAC-MAN chomped from a specific level.
        If no level specified, clears ALL high scores for that maze!
        
        Args:
            org_repo: Which maze to clear scores from
            release: Specific level (clears all levels if None)  
            force: Skip the "Really clear high scores?" prompt
            
        Returns:
            bool: True if scores were successfully cleared
            
        Raises:
            ValidationError: If maze coordinates are invalid
            SecurityError: If trying to clear without permission
            StorageError: If arcade's memory system fails
        """
        pass
    
    @abstractmethod
    async def graph_list(self, org_repo: Optional[str] = None) -> List[GraphInfo]:
        """
        🎮 Show PAC-MAN's high score tables! 🎮
        
        List all the semantic mazes PAC-MAN has conquered, with stats
        about how many dots were chomped in each!
        
        Args:
            org_repo: Show scores for specific maze (shows all if None)
            
        Returns:
            List[GraphInfo]: High score table with dot counts and maze info
            
        Raises:
            ValidationError: If maze identifier is invalid
            StorageError: If arcade's scoreboard is broken
        """
        pass
    
    @abstractmethod
    async def graph_show(
        self, 
        org_repo: str, 
        release: Optional[str] = None
    ) -> GraphDetails:
        """
        🎮 Examine PAC-MAN's detailed performance! 🎮
        
        Show detailed statistics about how PAC-MAN performed in a specific
        maze level - dots chomped, power pellets eaten, ghosts avoided!
        
        Args:
            org_repo: Which maze to examine
            release: Specific level (shows all levels if None)
            
        Returns:
            GraphDetails: Detailed performance statistics and maze analysis
            
        Raises:
            ValidationError: If maze coordinates are invalid
            NotFoundError: If PAC-MAN never played this maze/level
            StorageError: If arcade's statistics system fails
        """
        pass
    
    @abstractmethod
    async def graph_update(
        self, 
        org_repo: str, 
        release: Optional[str] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> ProcessingResult:
        """
        🎮 PAC-MAN REPLAYS A LEVEL PERFECTLY! 🎮
        
        Nuclear rebuild! PAC-MAN plays through a level again from scratch,
        chomping every dot with perfect technique. The ultimate do-over!
        
        Args:
            org_repo: Which maze to replay
            release: Specific level (replays latest if None)
            progress_callback: Watch the perfect replay
            
        Returns:
            ProcessingResult: Results of the perfect replay
            
        Raises:
            ValidationError: If maze coordinates are invalid
            NotFoundError: If maze or level doesn't exist
            ProcessingError: If something goes wrong during replay
            StorageError: If arcade can't save the new high score
        """
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # 🍒 BONUS FRUITS - Export Operations (Generate Outputs)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    async def export_opml(
        self, 
        org_repo: str, 
        release: str,
        output: Optional[Path] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Path:
        """
        🎮 Create a beautiful maze map for humans! 🎮
        
        PAC-MAN creates a gorgeous hierarchical map of the maze that
        humans can explore and understand. Like making a strategy guide!
        
        Args:
            org_repo: Which maze to map
            release: Which level to map
            output: Where to save the map (uses default if None)
            progress_callback: Watch map creation progress
            
        Returns:
            Path: Location of the beautiful maze map file
            
        Raises:
            ValidationError: If maze coordinates are invalid
            NotFoundError: If PAC-MAN never chomped this maze/level
            ExportError: If map creation fails
            SecurityError: If trying to save outside allowed areas
        """
        pass
    
    @abstractmethod
    async def export_msgpack(
        self, 
        org_repo: str, 
        release: str,
        output: Optional[Path] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Path:
        """
        🎮 Create a super-compressed AI training package! 🎮
        
        PAC-MAN compresses all his maze knowledge into a tiny package
        that AI systems can digest instantly. 125x compression magic!
        
        Args:
            org_repo: Which maze to compress
            release: Which level to compress
            output: Where to save the package (uses default if None)
            progress_callback: Watch compression progress
            
        Returns:
            Path: Location of the ultra-compressed semantic package
            
        Raises:
            ValidationError: If maze coordinates are invalid
            NotFoundError: If PAC-MAN never chomped this maze/level
            ExportError: If compression fails
            SecurityError: If trying to save outside allowed areas
        """
        pass
    
    @abstractmethod
    async def export_docs(
        self, 
        org_repo: str, 
        release: str,
        format: str,
        output: Path,
        template: Optional[str] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Path:
        """
        🎮 Generate comprehensive documentation! 🎮
        
        PAC-MAN creates complete documentation from his maze knowledge.
        Like writing the ultimate strategy guide with every secret!
        
        Args:
            org_repo: Which maze to document
            release: Which level to document  
            format: Documentation format ('mdx', 'html', 'markdown')
            output: Output directory for documentation
            template: Template for styling (optional)
            progress_callback: Watch documentation generation
            
        Returns:
            Path: Output directory with generated documentation
            
        Raises:
            ValidationError: If parameters are invalid
            NotFoundError: If PAC-MAN never chomped this maze/level
            ExportError: If documentation generation fails
            SecurityError: If trying to save outside allowed areas
        """
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # 🔍 MAZE NAVIGATION - Query Operations (Find Things)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    async def query_sparql(
        self, 
        query: str, 
        format: str = "table",
        output: Optional[Path] = None
    ) -> QueryResult:
        """
        🎮 Advanced maze navigation queries! 🎮
        
        PAC-MAN uses advanced SPARQL magic to navigate the semantic maze
        and find exactly what you're looking for. Expert-level play!
        
        Args:
            query: The SPARQL navigation command
            format: How to display results ('table', 'json', 'turtle', 'csv')
            output: Save results to file (optional)
            
        Returns:
            QueryResult: What PAC-MAN found in the maze
            
        Raises:
            ValidationError: If query format is invalid
            SPARQLError: If navigation command is malformed
            SecurityError: If query tries dangerous maze modifications
        """
        pass
    
    @abstractmethod
    async def query_functions(
        self, 
        search_term: str,
        repo: Optional[str] = None, 
        release: Optional[str] = None
    ) -> List[FunctionInfo]:
        """
        🎮 Smart dot finding! 🎮
        
        PAC-MAN searches for specific types of dots (functions) using
        natural language. Like asking "where are all the power pellets?"
        
        Args:
            search_term: What kind of dots to find (natural language)
            repo: Limit search to specific maze (optional)
            release: Limit search to specific level (optional)
            
        Returns:
            List[FunctionInfo]: All matching dots with relevance scores
            
        Raises:
            ValidationError: If search parameters are invalid
            StorageError: If maze search system fails
        """
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # ⚙️ ARCADE MANAGEMENT - System Operations (Configuration)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    async def show_config(self) -> Dict[str, Any]:
        """
        🎮 Show arcade machine settings! 🎮
        
        Display all of PAC-MAN's current configuration settings -
        like checking the arcade machine's DIP switches!
        
        Returns:
            Dict[str, Any]: All configuration settings and values
        """
        pass
    
    @abstractmethod
    async def update_config(self, key: str, value: str) -> bool:
        """
        🎮 Adjust arcade machine settings! 🎮
        
        Change PAC-MAN's configuration settings with validation.
        Like adjusting difficulty, sound volume, or player controls!
        
        Args:
            key: Which setting to change
            value: New value for the setting
            
        Returns:
            bool: True if setting was updated successfully
            
        Raises:
            ValidationError: If setting name is invalid or value is wrong format
        """
        pass
    
    @abstractmethod
    async def show_status(self) -> SystemStatus:
        """
        🎮 Arcade machine health check! 🎮
        
        Show complete status of PAC-MAN's arcade system - memory usage,
        number of mazes, recent errors, performance metrics, etc.
        
        Returns:
            SystemStatus: Complete system health and statistics
        """
        pass
    
    @abstractmethod
    async def remove_everything(self, confirm: bool = False) -> bool:
        """
        🎮 ULTIMATE ARCADE RESET! (DANGER!) 🎮
        
        Nuclear option: Remove ALL mazes, scores, and data. This is like
        factory resetting the entire arcade machine! 
        
        ⚠️  USE WITH EXTREME CAUTION! ⚠️  
        
        Args:
            confirm: Must be True to actually nuke everything
            
        Returns:
            bool: True if everything was successfully destroyed
            
        Raises:
            SecurityError: If confirm is False (safety mechanism)
        """
        pass


# ═══════════════════════════════════════════════════════════════
# 🎮 PAC-MAN'S HELPER TYPES 🎮
# ═══════════════════════════════════════════════════════════════

class ProgressCallback:
    """
    🎮 Watch PAC-MAN's progress in real-time! 🎮
    
    Callback interface for tracking PAC-MAN's maze navigation progress.
    Perfect for showing progress bars and WAKA-WAKA animations!
    """
    
    def __call__(
        self, 
        current: int, 
        total: int, 
        message: str = "",
        stage: str = "processing"
    ) -> None:
        """
        Update progress tracking.
        
        Args:
            current: How many dots PAC-MAN has chomped so far
            total: Total dots in the maze  
            message: Current activity description
            stage: Which stage of maze exploration we're in
        """
        pass


# ═══════════════════════════════════════════════════════════════
# 🎮 END OF PAC-MAN'S CONTROL INTERFACE 🎮
# ═══════════════════════════════════════════════════════════════

"""
🟡 WAKA WAKA! 🟡

This interface defines every move PAC-MAN can make in the semantic maze!
No implementation details here - just the pure contract that all
PAC-MAN implementations must follow.

The real PAC-MAN implementation lives in manager.py - that's where
the WAKA-WAKA magic actually happens! This is just the rulebook.

Ready to chomp some dots? Let's implement this interface! 🎮
"""
