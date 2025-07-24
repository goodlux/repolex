"""
👻 PAC-MAN's Git Intelligence Models 👻

Models for tracking ghost movements (developer activity) and maze changes (commits)!
Each developer is a ghost with unique patterns, each commit is a ghost movement!

WAKA WAKA! Understanding the supernatural side of code evolution!
"""

from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum


class GhostType(str, Enum):
    """👻 Types of developer ghosts in the PAC-MAN code maze!"""
    SPEED_DEMON = "speed_demon"          # Fast, frequent commits
    MAZE_MASTER = "maze_master"          # Deep knowledge, complex changes
    POWER_PELLET_COLLECTOR = "power_pellet_collector"  # Big features
    CAUTIOUS_GHOST = "cautious_ghost"    # Careful, well-tested changes
    NIGHT_OWL = "night_owl"             # Late night coding
    MORNING_GHOST = "morning_ghost"      # Early bird developer


class ActivityPattern(str, Enum):
    """👻 When ghosts are most active in the maze!"""
    MORNING_GHOST = "morning_ghost"      # 6AM-12PM peak activity
    AFTERNOON_SPIRIT = "afternoon_spirit" # 12PM-6PM peak activity  
    NIGHT_OWL = "night_owl"             # 6PM-12AM peak activity
    MIDNIGHT_HACKER = "midnight_hacker"  # 12AM-6AM peak activity
    WEEKEND_WARRIOR = "weekend_warrior"  # Weekend coding sessions
    WORKDAY_GHOST = "workday_ghost"      # Monday-Friday only


class CommitInfo(BaseModel):
    """👻 A single ghost movement through the maze!"""
    
    commit_hash: str = Field(..., description="Git commit SHA")
    author_name: str = Field(..., description="Ghost name")
    author_email: str = Field(..., description="Ghost email")
    commit_date: datetime = Field(..., description="When the ghost moved")
    message: str = Field(..., description="What the ghost was thinking")
    
    # File changes
    files_added: List[str] = Field(default_factory=list, description="New maze paths")
    files_modified: List[str] = Field(default_factory=list, description="Changed maze paths")
    files_deleted: List[str] = Field(default_factory=list, description="Removed maze paths")
    
    # Statistics
    lines_added: int = Field(0, description="Lines of code added")
    lines_deleted: int = Field(0, description="Lines of code removed")
    
    # PAC-MAN theming
    is_power_pellet: bool = Field(False, description="Major feature/change")
    ghost_energy_level: int = Field(1, description="Commit impact score 1-10")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DeveloperInfo(BaseModel):
    """👻 Complete ghost profile - a developer's maze behavior!"""
    
    name: str = Field(..., description="Ghost name")
    email: str = Field(..., description="Ghost email")
    
    # Activity stats
    total_commits: int = Field(0, description="Total ghost movements")
    total_lines_added: int = Field(0, description="Total maze expansion")
    total_lines_deleted: int = Field(0, description="Total maze cleanup")
    
    # File expertise
    files_touched: Set[str] = Field(default_factory=set, description="Maze areas visited")
    favorite_directories: List[str] = Field(default_factory=list, description="Preferred maze zones")
    expertise_areas: List[str] = Field(default_factory=list, description="Ghost specializations")
    
    # Temporal patterns
    first_commit: Optional[datetime] = Field(None, description="First ghost sighting")
    last_commit: Optional[datetime] = Field(None, description="Last ghost sighting")
    most_active_hour: Optional[int] = Field(None, description="Peak haunting hour (0-23)")
    most_active_day: Optional[str] = Field(None, description="Peak haunting day")
    
    # Ghost classification
    ghost_type: GhostType = Field(GhostType.CAUTIOUS_GHOST, description="Ghost behavior type")
    activity_pattern: ActivityPattern = Field(ActivityPattern.WORKDAY_GHOST, description="When ghost is active")
    
    # Collaboration
    frequent_collaborators: List[str] = Field(default_factory=list, description="Other ghosts often seen with")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            set: list
        }


class ChangePatterns(BaseModel):
    """👻 Co-change patterns - when ghosts move together through maze areas!"""
    
    # File co-change patterns
    frequently_changed_together: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Files that change together (file -> list of co-changed files)"
    )
    
    # Developer collaboration patterns  
    collaboration_strength: Dict[str, Dict[str, int]] = Field(
        default_factory=dict,
        description="How often developers work on same files (dev1 -> dev2 -> count)"
    )
    
    # Temporal patterns
    hotspot_files: List[str] = Field(
        default_factory=list,
        description="Files that change most frequently"
    )
    
    stable_files: List[str] = Field(
        default_factory=list,
        description="Files that rarely change"
    )
    
    # Change impact patterns
    high_impact_changes: List[str] = Field(
        default_factory=list,
        description="Commits that touched many files"
    )


class GitIntelligence(BaseModel):
    """👻 Complete git intelligence - the full ghost surveillance report!"""
    
    repository_path: Path = Field(..., description="Path to the haunted repository")
    analysis_date: datetime = Field(default_factory=datetime.now, description="When we investigated")
    
    # Commit data
    commits: List[CommitInfo] = Field(default_factory=list, description="All ghost movements")
    total_commits: int = Field(0, description="Total ghost sightings")
    
    # Developer data
    developers: List[DeveloperInfo] = Field(default_factory=list, description="All ghost profiles")
    active_developers: int = Field(0, description="Ghosts seen in last 90 days")
    
    # Pattern analysis
    change_patterns: ChangePatterns = Field(default_factory=ChangePatterns, description="Ghost behavior patterns")
    
    # Repository stats
    first_commit_date: Optional[datetime] = Field(None, description="When maze was first created")
    last_commit_date: Optional[datetime] = Field(None, description="Last ghost sighting")
    total_files_tracked: int = Field(0, description="Total maze paths monitored")
    
    # PAC-MAN insights
    most_haunted_files: List[str] = Field(default_factory=list, description="Files with most ghost activity")
    ghost_activity_score: float = Field(0.0, description="Overall maze activity level")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Path: str
        }
    
    def get_developer_by_email(self, email: str) -> Optional[DeveloperInfo]:
        """Find a ghost by their email"""
        for dev in self.developers:
            if dev.email == email:
                return dev
        return None
    
    def get_commits_by_author(self, author_email: str) -> List[CommitInfo]:
        """Get all movements by a specific ghost"""
        return [commit for commit in self.commits if commit.author_email == author_email]
    
    def get_power_pellet_commits(self) -> List[CommitInfo]:
        """Get all major changes (power pellet commits)"""
        return [commit for commit in self.commits if commit.is_power_pellet]