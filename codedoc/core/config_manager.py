"""
⚙️ PAC-MAN's Configuration Control Panel ⚙️

The ultimate configuration management system for CodeDoc's semantic intelligence!
PAC-MAN's preferences, maze settings, and power-up configurations all in one place!

WAKA WAKA! Configuring the perfect semantic arcade experience!
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)


class LogLevel(str, Enum):
    """🟡 PAC-MAN's logging volume control"""
    DEBUG = "debug"
    INFO = "info" 
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ThemeMode(str, Enum):
    """🎨 PAC-MAN's visual style preferences"""
    CLASSIC = "classic"          # 🟡 Original PAC-MAN yellow
    NEON = "neon"               # 💫 Bright arcade neon
    RETRO = "retro"             # 📺 Old-school CRT vibes
    GHOST = "ghost"             # 👻 Spooky ghost mode
    POWER_PELLET = "power"      # ⚡ High-energy mode


class DatabaseSettings(BaseModel):
    """🗄️ PAC-MAN's semantic database preferences"""
    engine: str = Field(default="oxigraph", description="Database engine (oxigraph)")
    storage_path: str = Field(default="~/.codedoc/graph", description="Graph storage path")
    memory_limit_mb: int = Field(default=1024, description="Memory limit in MB")
    query_timeout_sec: int = Field(default=30, description="Query timeout in seconds")
    backup_enabled: bool = Field(default=True, description="Enable automatic backups")
    backup_interval_hours: int = Field(default=24, description="Backup interval in hours")


class TUISettings(BaseModel):
    """🎮 PAC-MAN's TUI arcade settings"""
    theme: ThemeMode = Field(default=ThemeMode.CLASSIC, description="Visual theme")
    animations_enabled: bool = Field(default=True, description="Enable PAC-MAN animations")
    sound_effects: bool = Field(default=True, description="Enable WAKA WAKA sounds")
    refresh_interval_ms: int = Field(default=1000, description="Auto-refresh interval")
    max_history_items: int = Field(default=100, description="Max items in history panels")
    keyboard_shortcuts: bool = Field(default=True, description="Enable keyboard shortcuts")


class GitSettings(BaseModel):
    """👻 PAC-MAN's git intelligence settings"""
    default_branch: str = Field(default="main", description="Default branch name")
    max_commits: int = Field(default=1000, description="Max commits to analyze")
    include_merge_commits: bool = Field(default=False, description="Include merge commits")
    author_email_domains: List[str] = Field(default_factory=list, description="Trusted email domains")
    ignore_bot_commits: bool = Field(default=True, description="Ignore bot commits")


class QuerySettings(BaseModel):
    """🔍 PAC-MAN's SPARQL query preferences"""
    default_limit: int = Field(default=100, description="Default query result limit")
    timeout_seconds: int = Field(default=30, description="Query timeout")
    enable_caching: bool = Field(default=True, description="Enable query result caching")
    cache_ttl_minutes: int = Field(default=60, description="Cache TTL in minutes")
    format_queries: bool = Field(default=True, description="Auto-format SPARQL queries")


class ExportSettings(BaseModel):
    """📤 PAC-MAN's export configuration"""
    output_directory: str = Field(default="~/.codedoc/exports", description="Export output directory")
    default_format: str = Field(default="json", description="Default export format")
    include_metadata: bool = Field(default=True, description="Include metadata in exports")
    compress_exports: bool = Field(default=True, description="Compress export files")
    timestamp_filenames: bool = Field(default=True, description="Add timestamps to filenames")


class SystemSettings(BaseModel):
    """⚙️ PAC-MAN's system-wide settings"""
    max_workers: int = Field(default=4, description="Max worker threads")
    memory_limit_mb: int = Field(default=2048, description="System memory limit")
    temp_directory: str = Field(default="~/.codedoc/temp", description="Temporary files directory")
    auto_cleanup: bool = Field(default=True, description="Auto-cleanup temporary files")
    performance_monitoring: bool = Field(default=True, description="Enable performance monitoring")


class CodeDocConfig(BaseModel):
    """🟡 PAC-MAN's Master Configuration - The Ultimate Control Panel!"""
    
    # Metadata
    version: str = Field(default="2.0.0", description="Configuration version")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Config creation time")
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Last update time")
    
    # Core settings
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    
    # Component settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings, description="Database settings")
    tui: TUISettings = Field(default_factory=TUISettings, description="TUI settings")
    git: GitSettings = Field(default_factory=GitSettings, description="Git settings")
    query: QuerySettings = Field(default_factory=QuerySettings, description="Query settings")
    export: ExportSettings = Field(default_factory=ExportSettings, description="Export settings")
    system: SystemSettings = Field(default_factory=SystemSettings, description="System settings")
    
    # User customizations
    custom_settings: Dict[str, Any] = Field(default_factory=dict, description="User custom settings")


class ConfigError(Exception):
    """🟡 PAC-MAN configuration error"""
    pass


class ConfigManager:
    """⚙️ PAC-MAN's Configuration Manager - The Semantic Arcade Control Center!"""
    
    def __init__(self, config_path: Optional[Path] = None):
        """⚙️ Initialize PAC-MAN's configuration system"""
        self.config_path = config_path or Path.home() / ".codedoc" / "config" / "codedoc.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._config: Optional[CodeDocConfig] = None
        self._watchers: List[callable] = []  # Config change watchers
        
        logger.info(f"🟡 PAC-MAN's config manager initialized: {self.config_path}")
    
    @property
    def config(self) -> CodeDocConfig:
        """⚙️ Get current configuration (lazy loaded)"""
        if self._config is None:
            self.load_config()
        return self._config
    
    def load_config(self) -> CodeDocConfig:
        """⚙️ Load PAC-MAN's configuration from disk"""
        try:
            if self.config_path.exists():
                logger.info(f"🟡 Loading PAC-MAN config from: {self.config_path}")
                
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Handle config migration if needed
                config_data = self._migrate_config(config_data)
                
                # Validate and create config
                self._config = CodeDocConfig(**config_data)
                logger.info("🟡 PAC-MAN configuration loaded successfully!")
                
            else:
                logger.info("🟡 No config found, creating PAC-MAN defaults!")
                self._config = CodeDocConfig()
                self.save_config()  # Save default config
            
            return self._config
            
        except ValidationError as e:
            logger.error(f"💥 PAC-MAN config validation error: {e}")
            logger.info("🔧 Using default configuration instead")
            self._config = CodeDocConfig()
            return self._config
            
        except Exception as e:
            logger.error(f"💥 Failed to load PAC-MAN config: {e}")
            logger.info("🔧 Using default configuration instead")
            self._config = CodeDocConfig()
            return self._config
    
    def save_config(self) -> bool:
        """⚙️ Save PAC-MAN's configuration to disk"""
        try:
            if self._config is None:
                raise ConfigError("🟡 No configuration to save!")
            
            # Update timestamp
            self._config.updated_at = datetime.now().isoformat()
            
            # Create backup of existing config
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.json.backup')
                backup_path.write_text(self.config_path.read_text())
                logger.debug(f"🟡 Created config backup: {backup_path}")
            
            # Save new config
            config_dict = self._config.model_dump(exclude_unset=False)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟡 PAC-MAN configuration saved: {self.config_path}")
            
            # Notify watchers
            for watcher in self._watchers:
                try:
                    watcher(self._config)
                except Exception as e:
                    logger.error(f"💥 Config watcher error: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to save PAC-MAN config: {e}")
            return False
    
    def update_setting(self, setting_path: str, value: Any) -> bool:
        """⚙️ Update a specific PAC-MAN setting using dot notation"""
        try:
            if self._config is None:
                self.load_config()
            
            # Parse setting path (e.g., "tui.theme" or "database.memory_limit_mb")
            parts = setting_path.split('.')
            
            if len(parts) == 1:
                # Top-level setting
                if hasattr(self._config, parts[0]):
                    setattr(self._config, parts[0], value)
                else:
                    raise ConfigError(f"🟡 Unknown setting: {parts[0]}")
            
            elif len(parts) == 2:
                # Nested setting (component.setting)
                component_name, setting_name = parts
                
                if hasattr(self._config, component_name):
                    component = getattr(self._config, component_name)
                    if hasattr(component, setting_name):
                        setattr(component, setting_name, value)
                    else:
                        raise ConfigError(f"🟡 Unknown setting: {setting_path}")
                else:
                    raise ConfigError(f"🟡 Unknown component: {component_name}")
            
            else:
                raise ConfigError(f"🟡 Invalid setting path: {setting_path}")
            
            logger.info(f"🟡 PAC-MAN setting updated: {setting_path} = {value}")
            return self.save_config()
            
        except Exception as e:
            logger.error(f"💥 Failed to update PAC-MAN setting {setting_path}: {e}")
            return False
    
    def get_setting(self, setting_path: str, default: Any = None) -> Any:
        """⚙️ Get a specific PAC-MAN setting using dot notation"""
        try:
            if self._config is None:
                self.load_config()
            
            parts = setting_path.split('.')
            current = self._config
            
            for part in parts:
                if hasattr(current, part):
                    current = getattr(current, part)
                else:
                    logger.warning(f"🟡 Setting not found: {setting_path}, using default: {default}")
                    return default
            
            return current
            
        except Exception as e:
            logger.error(f"💥 Failed to get PAC-MAN setting {setting_path}: {e}")
            return default
    
    def reset_to_defaults(self) -> bool:
        """⚙️ Reset PAC-MAN configuration to defaults"""
        try:
            logger.info("🟡 Resetting PAC-MAN to default configuration...")
            self._config = CodeDocConfig()
            return self.save_config()
        except Exception as e:
            logger.error(f"💥 Failed to reset PAC-MAN config: {e}")
            return False
    
    def export_config(self, export_path: Path) -> bool:
        """⚙️ Export PAC-MAN configuration to file"""
        try:
            if self._config is None:
                self.load_config()
            
            config_dict = self._config.model_dump(exclude_unset=False)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟡 PAC-MAN config exported to: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to export PAC-MAN config: {e}")
            return False
    
    def import_config(self, import_path: Path) -> bool:
        """⚙️ Import PAC-MAN configuration from file"""
        try:
            if not import_path.exists():
                raise ConfigError(f"🟡 Config file not found: {import_path}")
            
            with open(import_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate imported config
            imported_config = CodeDocConfig(**config_data)
            
            # Create backup before import
            if self.config_path.exists():
                backup_path = self.config_path.with_suffix('.json.pre-import')
                backup_path.write_text(self.config_path.read_text())
                logger.info(f"🟡 Created pre-import backup: {backup_path}")
            
            # Apply imported config
            self._config = imported_config
            success = self.save_config()
            
            if success:
                logger.info(f"🟡 PAC-MAN config imported from: {import_path}")
            
            return success
            
        except Exception as e:
            logger.error(f"💥 Failed to import PAC-MAN config: {e}")
            return False
    
    def add_watcher(self, callback: callable) -> None:
        """⚙️ Add a configuration change watcher"""
        self._watchers.append(callback)
        logger.debug(f"🟡 Added config watcher: {callback.__name__}")
    
    def remove_watcher(self, callback: callable) -> None:
        """⚙️ Remove a configuration change watcher"""
        if callback in self._watchers:
            self._watchers.remove(callback)
            logger.debug(f"🟡 Removed config watcher: {callback.__name__}")
    
    def validate_config(self) -> List[str]:
        """⚙️ Validate PAC-MAN configuration and return issues"""
        issues = []
        
        try:
            if self._config is None:
                self.load_config()
            
            # Check paths exist and are writable
            paths_to_check = [
                (self._config.database.storage_path, "Database storage"),
                (self._config.export.output_directory, "Export output"),
                (self._config.system.temp_directory, "Temporary files")
            ]
            
            for path_str, description in paths_to_check:
                try:
                    path = Path(path_str).expanduser()
                    path.mkdir(parents=True, exist_ok=True)
                    
                    # Test write access
                    test_file = path / ".codedoc_write_test"
                    test_file.write_text("test")
                    test_file.unlink()
                    
                except Exception as e:
                    issues.append(f"🟡 {description} path issue: {path_str} - {e}")
            
            # Check memory limits are reasonable
            if self._config.system.memory_limit_mb < 256:
                issues.append("🟡 System memory limit too low (< 256MB)")
            
            if self._config.database.memory_limit_mb < 128:
                issues.append("🟡 Database memory limit too low (< 128MB)")
            
            # Check timeout values
            if self._config.query.timeout_seconds < 1:
                issues.append("🟡 Query timeout too low (< 1 second)")
            
            logger.info(f"🟡 PAC-MAN config validation complete: {len(issues)} issues found")
            
        except Exception as e:
            issues.append(f"🟡 Config validation error: {e}")
        
        return issues
    
    def _migrate_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """⚙️ Migrate old PAC-MAN config formats to current version"""
        version = config_data.get('version', '1.0.0')
        
        if version < '2.0.0':
            logger.info("🟡 Migrating PAC-MAN config from v1.x to v2.0...")
            
            # Add new v2.0 fields with defaults
            if 'tui' not in config_data:
                config_data['tui'] = TUISettings().model_dump()
            
            if 'system' not in config_data:
                config_data['system'] = SystemSettings().model_dump()
            
            # Update version
            config_data['version'] = '2.0.0'
            config_data['updated_at'] = datetime.now().isoformat()
            
            logger.info("🟡 PAC-MAN config migration complete!")
        
        return config_data
    
    def get_theme_colors(self) -> Dict[str, str]:
        """🎨 Get PAC-MAN theme colors for TUI"""
        theme = self.get_setting('tui.theme', ThemeMode.CLASSIC)
        
        theme_colors = {
            ThemeMode.CLASSIC: {
                'primary': '#FFD700',      # PAC-MAN yellow
                'secondary': '#FF69B4',    # Pink (Pinky ghost)
                'accent': '#00FFFF',       # Cyan (Inky ghost)
                'background': '#000080',   # Navy blue maze
                'text': '#FFFFFF'          # White text
            },
            ThemeMode.NEON: {
                'primary': '#00FF00',      # Bright green
                'secondary': '#FF00FF',    # Magenta
                'accent': '#FFFF00',       # Bright yellow
                'background': '#000000',   # Black
                'text': '#FFFFFF'          # White
            },
            ThemeMode.RETRO: {
                'primary': '#FF8000',      # Orange
                'secondary': '#8000FF',    # Purple
                'accent': '#00FF80',       # Green
                'background': '#404040',   # Dark gray
                'text': '#C0C0C0'          # Light gray
            },
            ThemeMode.GHOST: {
                'primary': '#FF0000',      # Red (Blinky)
                'secondary': '#FFB6C1',    # Light pink
                'accent': '#87CEEB',       # Sky blue
                'background': '#2F2F2F',   # Dark gray
                'text': '#F0F8FF'          # Alice blue
            },
            ThemeMode.POWER_PELLET: {
                'primary': '#FFFF00',      # Bright yellow
                'secondary': '#FF4500',    # Orange red
                'accent': '#00BFFF',       # Deep sky blue
                'background': '#191970',   # Midnight blue
                'text': '#FFFAF0'          # Floral white
            }
        }
        
        return theme_colors.get(theme, theme_colors[ThemeMode.CLASSIC])


# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """🟡 Get the global PAC-MAN configuration manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config() -> CodeDocConfig:
    """🟡 Get PAC-MAN's current configuration"""
    return get_config_manager().config


def update_config(setting_path: str, value: Any) -> bool:
    """🟡 Update a PAC-MAN configuration setting"""
    return get_config_manager().update_setting(setting_path, value)


def get_setting(setting_path: str, default: Any = None) -> Any:
    """🟡 Get a PAC-MAN configuration setting"""
    return get_config_manager().get_setting(setting_path, default)


# Example usage and defaults for PAC-MAN's arcade!
if __name__ == "__main__":
    # 🟡 PAC-MAN Configuration Demo!
    config_manager = ConfigManager()
    
    print("🟡 Loading PAC-MAN configuration...")
    config = config_manager.load_config()
    
    print(f"🎮 Theme: {config.tui.theme}")
    print(f"🧠 Database engine: {config.database.engine}")
    print(f"🔍 Query limit: {config.query.default_limit}")
    
    print("\n🟡 Updating PAC-MAN preferences...")
    config_manager.update_setting('tui.theme', ThemeMode.NEON)
    config_manager.update_setting('tui.animations_enabled', True)
    
    print("\n🟡 Validating PAC-MAN configuration...")
    issues = config_manager.validate_config()
    if issues:
        print("⚠️  Configuration issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ PAC-MAN configuration is perfect!")
    
    print("\n🟡 WAKA WAKA! Configuration system ready!")