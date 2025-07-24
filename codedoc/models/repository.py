"""🟡 PAC-MAN Repository Data Models

Data models for repositories, releases, and PAC-MAN's chomping activities.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum


class RepoStatus(str, Enum):
    """🟡 PAC-MAN repository status enum."""
    UNKNOWN = "unknown"          # 🤔 PAC-MAN hasn't seen this yet
    CLONING = "cloning"          # 🔄 PAC-MAN is downloading
    READY = "ready"              # ✅ Ready for semantic chomping
    PROCESSING = "processing"    # 🟡 PAC-MAN is actively chomping
    PROCESSED = "processed"      # 🎯 Semantic digestion complete
    ERROR = "error"              # ❌ Something went wrong
    CORRUPTED = "corrupted"      # 💥 Repository or data is corrupted


class ProcessingStatus(str, Enum):
    """🧠 Semantic processing status enum."""
    PENDING = "pending"          # ⏳ Waiting in PAC-MAN's queue
    PARSING = "parsing"          # 📝 Reading the source code
    ANALYZING = "analyzing"      # 🧠 Building semantic graphs
    LINKING = "linking"          # 🔗 Creating relationships
    STORING = "storing"          # 💾 Saving to Oxigraph
    COMPLETE = "complete"        # ✅ Semantic feast complete
    FAILED = "failed"            # ❌ PAC-MAN couldn't digest


class ReleaseInfo(BaseModel):
    """🏷️ Information about a git release/tag."""
    
    tag: str = Field(description="Git tag name")
    commit_sha: str = Field(description="Git commit SHA")
    date: datetime = Field(description="Release date")
    message: Optional[str] = Field(default=None, description="Release message")
    
    # Processing status
    has_graphs: bool = Field(default=False, description="🧠 Semantic graphs exist")
    processing_status: ProcessingStatus = Field(default=ProcessingStatus.PENDING)
    last_processed: Optional[datetime] = Field(default=None, description="Last processing time")
    
    # Statistics
    functions_count: Optional[int] = Field(default=None, description="Number of functions found")
    files_count: Optional[int] = Field(default=None, description="Number of files processed") 
    size_mb: Optional[float] = Field(default=None, description="Repository size in MB")
    
    class Config:
        schema_extra = {
            "example": {
                "tag": "v0.4.14",
                "commit_sha": "abc123def456",
                "date": "2024-12-15T10:30:00Z",
                "has_graphs": True,
                "processing_status": "complete",
                "functions_count": 127,
                "files_count": 45
            }
        }


class RepoInfo(BaseModel):
    """📚 Basic repository information for listings."""
    
    org_repo: str = Field(description="Organization/repository identifier")
    display_name: str = Field(description="Human-readable name")
    status: RepoStatus = Field(description="Current repository status")
    
    # Storage info
    storage_path: Path = Field(description="Local storage path")
    last_updated: datetime = Field(description="Last update time")
    
    # Release info
    releases: List[ReleaseInfo] = Field(default_factory=list, description="Available releases")
    latest_release: Optional[str] = Field(default=None, description="Latest release tag")
    
    # Statistics
    total_size_mb: float = Field(default=0.0, description="Total storage size")
    graphs_count: int = Field(default=0, description="Number of semantic graphs")
    
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "org_repo": "pixeltable/pixeltable",
                "display_name": "Pixeltable",
                "status": "processed",
                "releases": ["v0.2.30", "v0.3.15", "v0.4.14"],
                "latest_release": "v0.4.14", 
                "graphs_count": 152
            }
        }


class RepoDetails(BaseModel):
    """🔍 Detailed repository information."""
    
    # Basic info (inherit from RepoInfo)
    org_repo: str = Field(description="Organization/repository identifier")
    display_name: str = Field(description="Human-readable name")
    status: RepoStatus = Field(description="Current repository status")
    
    # Git information
    git_url: str = Field(description="Git repository URL")
    default_branch: str = Field(default="main", description="Default git branch")
    clone_time: datetime = Field(description="When PAC-MAN first cloned this")
    
    # Storage details
    storage_path: Path = Field(description="Local storage path")
    total_size_mb: float = Field(description="Total storage size in MB")
    
    # Processing history
    releases: List[ReleaseInfo] = Field(default_factory=list, description="All releases")
    processing_history: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="History of PAC-MAN processing attempts"
    )
    
    # Semantic statistics
    total_functions: int = Field(default=0, description="Total functions across all versions")
    total_classes: int = Field(default=0, description="Total classes across all versions") 
    total_files: int = Field(default=0, description="Total files processed")
    graphs_count: int = Field(default=0, description="Number of semantic graphs")
    
    # Metadata
    description: Optional[str] = Field(default=None, description="Repository description")
    topics: List[str] = Field(default_factory=list, description="Repository topics/tags")
    language: Optional[str] = Field(default=None, description="Primary programming language")
    
    class Config:
        arbitrary_types_allowed = True


class RepoResult(BaseModel):
    """🎯 Result of repository operations."""
    
    success: bool = Field(description="Operation succeeded")
    message: str = Field(description="Human-readable result message")
    
    # Repository info
    org_repo: str = Field(description="Repository identifier")
    operation: str = Field(description="Operation performed")
    
    # Results
    releases: List[str] = Field(default_factory=list, description="Found releases")
    storage_path: Optional[Path] = Field(default=None, description="Storage location")
    
    # Statistics
    processing_time: float = Field(default=0.0, description="Operation time in seconds")
    size_mb: float = Field(default=0.0, description="Data size in MB")
    
    # Error info (if applicable)
    error_code: Optional[str] = Field(default=None, description="Error code if failed")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for fixing errors")
    
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "success": True,
                "message": "🟡 PAC-MAN successfully chomped repository!",
                "org_repo": "pixeltable/pixeltable",
                "operation": "clone",
                "releases": ["v0.2.30", "v0.3.15", "v0.4.14"],
                "processing_time": 12.5
            }
        }


class UpdateResult(BaseModel):
    """🔄 Result of repository update operations."""
    
    success: bool = Field(description="Update succeeded")
    message: str = Field(description="Human-readable result message")
    
    # Update details
    org_repo: str = Field(description="Repository identifier")
    previous_commit: str = Field(description="Previous HEAD commit")
    new_commit: str = Field(description="New HEAD commit")
    
    # Changes found
    new_releases: List[str] = Field(default_factory=list, description="New releases discovered")
    files_changed: int = Field(default=0, description="Number of files changed")
    commits_added: int = Field(default=0, description="Number of new commits")
    
    # Statistics
    update_time: float = Field(default=0.0, description="Update time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "🔄 PAC-MAN found new semantic treats!",
                "org_repo": "pixeltable/pixeltable",
                "new_releases": ["v0.4.15"],
                "files_changed": 12,
                "commits_added": 8
            }
        }


class PAC_MAN_Stats(BaseModel):
    """🟡 PAC-MAN's chomping statistics."""
    
    # Chomping activity
    repositories_chomped: int = Field(default=0, description="Repositories processed")
    functions_eaten: int = Field(default=0, description="Functions digested")
    dots_collected: int = Field(default=0, description="Semantic dots (triples) collected")
    power_pills_created: int = Field(default=0, description="Export files created")
    
    # Time tracking
    total_chomp_time: float = Field(default=0.0, description="Total processing time")
    average_repo_time: float = Field(default=0.0, description="Average time per repository")
    
    # Storage efficiency
    raw_data_mb: float = Field(default=0.0, description="Raw data processed (MB)")
    compressed_mb: float = Field(default=0.0, description="Compressed storage (MB)")
    compression_ratio: float = Field(default=0.0, description="Compression ratio achieved")
    
    # Quality metrics
    success_rate: float = Field(default=0.0, description="Processing success rate")
    error_count: int = Field(default=0, description="Total errors encountered")
    
    # PAC-MAN specific
    ghosts_avoided: int = Field(default=0, description="Private functions skipped")
    mazes_completed: int = Field(default=0, description="Repositories fully processed")
    
    class Config:
        schema_extra = {
            "example": {
                "repositories_chomped": 15,
                "functions_eaten": 2847,
                "dots_collected": 125000,
                "power_pills_created": 45,
                "compression_ratio": 125.0,
                "success_rate": 0.94,
                "mazes_completed": 12
            }
        }
