"""🟡 PAC-MAN Configuration Data Models

Pydantic models for Repolex configuration with PAC-MAN themed defaults.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field, validator


class RepolexConfig(BaseModel):
    """🟡 PAC-MAN Configuration Model with validation and PAC-MAN defaults."""
    
    # Storage settings - where PAC-MAN keeps his power pills
    storage_path: Path = Field(
        default_factory=lambda: Path.home() / ".Repolex",
        description="🗂️ Base directory for PAC-MAN's semantic storage"
    )
    
    # GitHub integration
    github_token: Optional[str] = Field(
        default=None,
        description="🔑 GitHub token for private repository access"
    )
    
    # Logging settings
    log_level: str = Field(
        default="INFO",
        description="📝 Logging level for PAC-MAN's activities",
        regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    
    # Processing settings
    processing_timeout: int = Field(
        default=300,
        ge=30,
        le=3600,
        description="⏱️ Timeout for semantic digestion (30s to 1h)"
    )
    
    max_file_size_mb: int = Field(
        default=10,
        ge=1,
        le=100,
        description="📄 Maximum file size for PAC-MAN to chomp (1-100MB)"
    )
    
    # Export templates
    export_templates: Dict[str, str] = Field(
        default_factory=lambda: {
            "mdx": "default",
            "html": "clean", 
            "markdown": "github"
        },
        description="📦 Templates for different export formats"
    )
    
    # Performance settings
    max_concurrent_parsers: int = Field(
        default=4,
        ge=1,
        le=16,
        description="🚀 Maximum concurrent PAC-MAN parser processes"
    )
    
    cache_size_mb: int = Field(
        default=500,
        ge=100,
        le=2000,
        description="💾 Cache size for PAC-MAN's memory (100MB-2GB)"
    )
    
    # Safety settings - PAC-MAN security protocol
    allow_large_repositories: bool = Field(
        default=False,
        description="🛡️ Allow repositories with >10k files (security setting)"
    )
    
    require_confirmation_for_destructive: bool = Field(
        default=True,
        description="⚠️ Require confirmation for destructive operations"
    )
    
    # PAC-MAN theme settings
    pac_man_mode: bool = Field(
        default=True,
        description="🟡 Enable PAC-MAN themed messages and emojis"
    )
    
    tui_animations: bool = Field(
        default=True,
        description="🎮 Enable animations in PAC-MAN dashboard"
    )
    
    @validator('storage_path')
    def validate_storage_path(cls, v):
        """Ensure storage path is valid and create if needed."""
        if isinstance(v, str):
            v = Path(v)
        
        # Create directory if it doesn't exist
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @validator('github_token')
    def validate_github_token(cls, v):
        """Validate GitHub token format."""
        if v is not None:
            if not v.startswith(('ghp_', 'github_pat_')):
                raise ValueError(
                    "GitHub token should start with 'ghp_' or 'github_pat_'"
                )
        return v
    
    class Config:
        # Allow use of Path objects
        arbitrary_types_allowed = True
        
        # JSON Schema extras
        schema_extra = {
            "example": {
                "storage_path": "~/.Repolex",
                "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx",
                "log_level": "INFO",
                "processing_timeout": 300,
                "max_file_size_mb": 10,
                "pac_man_mode": True,
                "tui_animations": True
            }
        }


class RuntimeConfig(BaseModel):
    """🎮 Runtime configuration for PAC-MAN operations."""
    
    # Current operation settings
    debug_mode: bool = Field(default=False, description="🐛 Debug mode enabled")
    quiet_mode: bool = Field(default=False, description="🤫 Quiet mode (minimal output)")
    force_mode: bool = Field(default=False, description="💪 Force operations without confirmation") 
    
    # Processing filters
    public_only: bool = Field(default=False, description="👁️ Process only public functions")
    include_tests: bool = Field(default=False, description="🧪 Include test files")
    include_docs: bool = Field(default=True, description="📚 Include documentation files")
    
    # Export settings
    compress_exports: bool = Field(default=True, description="🗜️ Compress export files")
    include_source_links: bool = Field(default=True, description="🔗 Include GitHub source links")
    
    # Performance settings
    parallel_processing: bool = Field(default=True, description="⚡ Use parallel processing")
    streaming_exports: bool = Field(default=False, description="🌊 Use streaming for large exports")
    
    class Config:
        schema_extra = {
            "example": {
                "debug_mode": False,
                "quiet_mode": False,
                "public_only": True,
                "compress_exports": True,
                "parallel_processing": True
            }
        }


class PAC_MAN_ThemeConfig(BaseModel):
    """🟡 PAC-MAN specific theme configuration."""
    
    # Emoji settings
    use_emojis: bool = Field(default=True, description="🟡 Use PAC-MAN emojis in output")
    emoji_density: str = Field(
        default="normal",
        description="🎨 Emoji density in output",
        regex="^(minimal|normal|high|maximum)$"
    )
    
    # Color scheme
    primary_color: str = Field(default="yellow", description="🟡 Primary PAC-MAN color")
    accent_color: str = Field(default="blue", description="🔵 Accent color for highlights")
    
    # Sound effects (for future TUI enhancements)
    sound_effects: bool = Field(default=False, description="🔊 Enable sound effects")
    
    # Messages
    use_pac_man_messages: bool = Field(default=True, description="💬 Use PAC-MAN themed messages")
    
    # Progress indicators
    use_pac_man_progress: bool = Field(default=True, description="🟡 Use PAC-MAN progress indicators")
    
    class Config:
        schema_extra = {
            "example": {
                "use_emojis": True,
                "emoji_density": "normal",
                "primary_color": "yellow", 
                "use_pac_man_messages": True,
                "use_pac_man_progress": True
            }
        }
