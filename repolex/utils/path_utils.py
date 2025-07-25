"""🟡 PAC-MAN Path Manipulation Utilities

Advanced path manipulation and resolution with PAC-MAN-level safety and intelligence.
PAC-MAN navigates even the most complex semantic mazes with perfect path precision!
"""

import os
import sys
from pathlib import Path, PurePath
from typing import List, Optional, Union, Tuple, Set
from urllib.parse import urlparse, quote, unquote
import re

from repolex.models.exceptions import ValidationError, SecurityError, RepolexError
from repolex.utils.validation import validate_file_path


class PathError(RepolexError):
    """🟡 PAC-MAN path operation error."""
    pass


def get_Repolex_home() -> Path:
    """
    🟡 Get Repolex home directory - PAC-MAN's main base!
    
    Returns ~/.Repolex/ by default, or uses Repolex_HOME environment variable.
    
    Returns:
        Path: Repolex home directory
    """
    home_env = os.environ.get('Repolex_HOME')
    if home_env:
        return Path(home_env).expanduser().resolve()
    else:
        return Path.home() / '.Repolex'


def get_repos_directory() -> Path:
    """
    🟡 Get repositories storage directory - PAC-MAN's repository vault!
    
    Returns:
        Path: Repository storage directory (~/.Repolex/repos/)
    """
    return get_Repolex_home() / 'repos'


def get_config_directory() -> Path:
    """
    🟡 Get configuration directory - PAC-MAN's control center!
    
    Returns:
        Path: Configuration directory (~/.Repolex/config/)
    """
    return get_Repolex_home() / 'config'


def get_cache_directory() -> Path:
    """
    🟡 Get cache directory - PAC-MAN's temporary storage!
    
    Returns:
        Path: Cache directory (~/.Repolex/cache/)
    """
    return get_Repolex_home() / 'cache'


def get_logs_directory() -> Path:
    """
    🟡 Get logs directory - PAC-MAN's activity tracker!
    
    Returns:
        Path: Logs directory (~/.Repolex/logs/)
    """
    return get_Repolex_home() / 'logs'


def get_exports_directory() -> Path:
    """
    🟡 Get exports directory - PAC-MAN's output depot!
    
    Returns:
        Path: Exports directory (~/.Repolex/exports/)
    """
    return get_Repolex_home() / 'exports'


def get_repository_path(org: str, repo: str) -> Path:
    """
    🟡 Get path for a specific repository - PAC-MAN's repo navigator!
    
    Args:
        org: Organization name
        repo: Repository name
        
    Returns:
        Path: Repository base path (~/.Repolex/repos/org/repo/)
    """
    # Sanitize org and repo names for safe filesystem use
    safe_org = sanitize_path_component(org)
    safe_repo = sanitize_path_component(repo)
    
    return get_repos_directory() / safe_org / safe_repo


def get_repository_version_path(org: str, repo: str, version: str) -> Path:
    """
    🟡 Get path for a specific repository version - PAC-MAN's version vault!
    
    Args:
        org: Organization name
        repo: Repository name
        version: Version/tag/branch name
        
    Returns:
        Path: Repository version path (~/.Repolex/repos/org/repo/version/)
    """
    safe_version = sanitize_path_component(version)
    return get_repository_path(org, repo) / safe_version


def get_oxigraph_database_path() -> Path:
    """
    🟡 Get Oxigraph database path - PAC-MAN's semantic database!
    
    Returns:
        Path: Oxigraph database directory (~/.Repolex/oxigraph/)
    """
    return get_Repolex_home() / 'oxigraph'


def get_config_file_path() -> Path:
    """
    🟡 Get main configuration file path - PAC-MAN's settings file!
    
    Returns:
        Path: Configuration file path (~/.Repolex/config/config.json)
    """
    return get_config_directory() / 'config.json'


def sanitize_path_component(component: str) -> str:
    """
    🟡 Sanitize path component for safe filesystem use - PAC-MAN's security filter!
    
    Args:
        component: Path component to sanitize
        
    Returns:
        str: Sanitized path component
        
    Raises:
        ValidationError: If component is invalid
    """
    if not component or not isinstance(component, str):
        raise ValidationError(
            "Path component must be a non-empty string",
            suggestions=["Provide a valid path component"]
        )
    
    # Remove/replace dangerous characters
    sanitized = re.sub(r'[<>:"|?*\\]', '_', component)
    sanitized = re.sub(r'\.\.', '_', sanitized)
    sanitized = sanitized.strip('. ')
    
    # Handle reserved names on Windows
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    if sanitized.upper() in reserved_names:
        sanitized = f"_{sanitized}"
    
    # Ensure reasonable length
    if len(sanitized) > 100:
        sanitized = sanitized[:95] + "_trunc"
    
    if not sanitized:
        raise ValidationError(
            "Path component cannot be empty after sanitization",
            suggestions=["Use a valid name with alphanumeric characters"]
        )
    
    return sanitized


def resolve_path_safely(path: Union[str, Path], base_path: Optional[Path] = None) -> Path:
    """
    🟡 Safely resolve path with security validation - PAC-MAN's secure navigator!
    
    Args:
        path: Path to resolve
        base_path: Base path for relative resolution (default: current working directory)
        
    Returns:
        Path: Safely resolved absolute path
        
    Raises:
        SecurityError: If path resolution leads outside allowed areas
        PathError: If path resolution fails
    """
    try:
        path = Path(path)
        
        if base_path is None:
            base_path = Path.cwd()
        else:
            base_path = Path(base_path)
        
        # Resolve the path
        if path.is_absolute():
            resolved = path.resolve()
        else:
            resolved = (base_path / path).resolve()
        
        # Validate against base path if provided and not absolute
        if not path.is_absolute() and base_path:
            validate_file_path(resolved, base_path)
        
        return resolved
        
    except (OSError, ValueError) as e:
        raise PathError(
            f"🟡 PAC-MAN couldn't resolve path: {path}",
            suggestions=[
                "Check path syntax is valid",
                "Ensure base path exists",
                f"Original error: {e}"
            ]
        ) from e


def make_relative_path(path: Path, base_path: Path) -> Path:
    """
    🟡 Make path relative to base - PAC-MAN's relative calculator!
    
    Args:
        path: Path to make relative
        base_path: Base path for relative calculation
        
    Returns:
        Path: Relative path
        
    Raises:
        PathError: If relative path cannot be calculated
    """
    try:
        path = Path(path).resolve()
        base_path = Path(base_path).resolve()
        
        return path.relative_to(base_path)
        
    except ValueError as e:
        # Paths are not related - find common ancestor
        try:
            common = find_common_path([path, base_path])
            path_parts = path.relative_to(common).parts
            base_parts = base_path.relative_to(common).parts
            
            # Add '..' for each level up from base to common
            up_parts = ['..'] * len(base_parts)
            
            # Combine with path down from common
            relative_parts = up_parts + list(path_parts)
            
            return Path(*relative_parts) if relative_parts else Path('.')
            
        except Exception:
            raise PathError(
                f"🟡 PAC-MAN couldn't calculate relative path: {path} from {base_path}",
                suggestions=[
                    "Ensure both paths exist",
                    "Check paths are accessible",
                    f"Original error: {e}"
                ]
            ) from e


def find_common_path(paths: List[Path]) -> Path:
    """
    🟡 Find common ancestor path - PAC-MAN's ancestry finder!
    
    Args:
        paths: List of paths to find common ancestor for
        
    Returns:
        Path: Common ancestor path
        
    Raises:
        PathError: If no common path found
    """
    if not paths:
        raise PathError(
            "🟡 Cannot find common path of empty list",
            suggestions=["Provide at least one path"]
        )
    
    if len(paths) == 1:
        return paths[0].parent if paths[0].is_file() else paths[0]
    
    try:
        # Resolve all paths
        resolved_paths = [Path(p).resolve() for p in paths]
        
        # Find common parts
        common_parts = []
        min_parts = min(len(p.parts) for p in resolved_paths)
        
        for i in range(min_parts):
            part = resolved_paths[0].parts[i]
            if all(p.parts[i] == part for p in resolved_paths):
                common_parts.append(part)
            else:
                break
        
        if not common_parts:
            # No common path found
            if sys.platform == 'win32':
                return Path('C:\\')  # Default to C: on Windows
            else:
                return Path('/')  # Default to root on Unix
        
        return Path(*common_parts)
        
    except Exception as e:
        raise PathError(
            f"🟡 PAC-MAN couldn't find common path",
            suggestions=[
                "Check all paths are valid",
                "Ensure paths are accessible",
                f"Original error: {e}"
            ]
        ) from e


def expand_path_patterns(patterns: List[str], base_path: Optional[Path] = None) -> List[Path]:
    """
    🟡 Expand glob patterns to file paths - PAC-MAN's pattern expander!
    
    Args:
        patterns: List of glob patterns
        base_path: Base directory for relative patterns
        
    Returns:
        List[Path]: List of matching paths
        
    Raises:
        PathError: If pattern expansion fails
    """
    try:
        if base_path is None:
            base_path = Path.cwd()
        else:
            base_path = Path(base_path)
        
        all_paths = []
        
        for pattern in patterns:
            if Path(pattern).is_absolute():
                # Absolute pattern
                matches = list(Path().glob(pattern))
            else:
                # Relative pattern
                matches = list(base_path.glob(pattern))
            
            all_paths.extend(matches)
        
        # Remove duplicates and sort
        unique_paths = list(set(all_paths))
        return sorted(unique_paths)
        
    except Exception as e:
        raise PathError(
            f"🟡 PAC-MAN couldn't expand patterns: {patterns}",
            suggestions=[
                "Check pattern syntax",
                "Ensure base path exists",
                f"Original error: {e}"
            ]
        ) from e


def normalize_path_separators(path: str) -> str:
    """
    🟡 Normalize path separators for current OS - PAC-MAN's separator fixer!
    
    Args:
        path: Path string with potentially mixed separators
        
    Returns:
        str: Path with normalized separators
    """
    return os.path.normpath(path)


def path_to_uri(path: Path) -> str:
    """
    🟡 Convert path to file URI - PAC-MAN's URI converter!
    
    Args:
        path: File system path
        
    Returns:
        str: File URI
    """
    path = Path(path).resolve()
    return path.as_uri()


def uri_to_path(uri: str) -> Path:
    """
    🟡 Convert file URI to path - PAC-MAN's URI decoder!
    
    Args:
        uri: File URI string
        
    Returns:
        Path: File system path
        
    Raises:
        PathError: If URI is invalid or not a file URI
    """
    try:
        parsed = urlparse(uri)
        if parsed.scheme not in ('file', ''):
            raise PathError(
                f"🟡 Not a file URI: {uri}",
                suggestions=["Provide a file:// URI"]
            )
        
        # Decode URL-encoded path
        path_str = unquote(parsed.path)
        
        # Handle Windows paths
        if sys.platform == 'win32' and path_str.startswith('/'):
            path_str = path_str[1:]  # Remove leading slash
        
        return Path(path_str)
        
    except Exception as e:
        raise PathError(
            f"🟡 PAC-MAN couldn't convert URI to path: {uri}",
            suggestions=[
                "Check URI format is valid",
                "Use file:// scheme for file URIs",
                f"Original error: {e}"
            ]
        ) from e


def ensure_path_within_bounds(path: Path, allowed_paths: List[Path]) -> Path:
    """
    🟡 Ensure path is within allowed boundaries - PAC-MAN's boundary checker!
    
    Args:
        path: Path to check
        allowed_paths: List of allowed base paths
        
    Returns:
        Path: Validated path
        
    Raises:
        SecurityError: If path is outside allowed boundaries
    """
    path = Path(path).resolve()
    
    for allowed_path in allowed_paths:
        allowed_path = Path(allowed_path).resolve()
        try:
            path.relative_to(allowed_path)
            return path  # Path is within this allowed path
        except ValueError:
            continue
    
    # Path is not within any allowed path
    raise SecurityError(
        f"🟡 Path outside allowed boundaries: {path}",
        suggestions=[
            f"Path must be within one of: {[str(p) for p in allowed_paths]}",
            "PAC-MAN blocked path traversal attempt!"
        ]
    )


def get_path_depth(path: Path, base_path: Optional[Path] = None) -> int:
    """
    🟡 Get path depth relative to base - PAC-MAN's depth calculator!
    
    Args:
        path: Path to measure
        base_path: Base path for relative depth (default: root)
        
    Returns:
        int: Path depth (number of levels)
    """
    if base_path:
        try:
            relative_path = make_relative_path(path, base_path)
            return len(relative_path.parts)
        except PathError:
            # Paths not related, use absolute depth
            pass
    
    # Use absolute path depth
    return len(Path(path).resolve().parts)


def find_files_by_extension(directory: Path, extensions: List[str], 
                          recursive: bool = True) -> List[Path]:
    """
    🟡 Find files by extensions - PAC-MAN's extension hunter!
    
    Args:
        directory: Directory to search
        extensions: List of file extensions (with or without dots)
        recursive: Search subdirectories
        
    Returns:
        List[Path]: List of matching files
        
    Raises:
        PathError: If directory search fails
    """
    try:
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not directory.is_dir():
            raise PathError(
                f"🟡 Path is not a directory: {directory}",
                suggestions=["Provide a valid directory path"]
            )
        
        # Normalize extensions (ensure they start with dot)
        normalized_extensions = []
        for ext in extensions:
            if not ext.startswith('.'):
                ext = '.' + ext
            normalized_extensions.append(ext.lower())
        
        matching_files = []
        
        if recursive:
            for file_path in directory.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in normalized_extensions:
                    matching_files.append(file_path)
        else:
            for file_path in directory.glob('*'):
                if file_path.is_file() and file_path.suffix.lower() in normalized_extensions:
                    matching_files.append(file_path)
        
        return sorted(matching_files)
        
    except OSError as e:
        raise PathError(
            f"🟡 PAC-MAN couldn't search for files: {directory}",
            suggestions=[
                "Check directory permissions",
                "Ensure directory exists",
                f"Original error: {e}"
            ]
        ) from e


def create_unique_path(base_path: Path, suffix: str = "") -> Path:
    """
    🟡 Create unique path by adding numbers - PAC-MAN's uniqueness generator!
    
    Args:
        base_path: Base path to make unique
        suffix: Additional suffix to add
        
    Returns:
        Path: Unique path that doesn't exist
    """
    base_path = Path(base_path)
    
    if suffix:
        base_name = base_path.stem + suffix
        extension = base_path.suffix
        parent = base_path.parent
    else:
        base_name = base_path.stem
        extension = base_path.suffix
        parent = base_path.parent
    
    # Try the original path first
    candidate = parent / (base_name + extension)
    if not candidate.exists():
        return candidate
    
    # Add numbers until we find a unique path
    counter = 1
    while True:
        candidate = parent / f"{base_name}_{counter}{extension}"
        if not candidate.exists():
            return candidate
        counter += 1


def validate_path_safe_for_extraction(path: Path, extract_to: Path) -> None:
    """
    🟡 Validate path is safe for archive extraction - PAC-MAN's extraction guard!
    
    Args:
        path: Path from archive entry
        extract_to: Target extraction directory
        
    Raises:
        SecurityError: If path is unsafe for extraction
    """
    # Resolve paths
    extract_to = Path(extract_to).resolve()
    
    # Handle relative paths
    if not path.is_absolute():
        full_path = (extract_to / path).resolve()
    else:
        full_path = path.resolve()
    
    # Check if resolved path is within extraction directory
    try:
        full_path.relative_to(extract_to)
    except ValueError:
        raise SecurityError(
            f"🟡 Archive entry tries to escape extraction directory: {path}",
            suggestions=[
                "Archive contains dangerous path traversal entries",
                "PAC-MAN blocked zip slip attack!",
                "Use a trusted archive source"
            ]
        )


def get_path_parts_list(path: Path) -> List[str]:
    """
    🟡 Get path parts as list - PAC-MAN's path parser!
    
    Args:
        path: Path to parse
        
    Returns:
        List[str]: List of path components
    """
    return list(Path(path).parts)


def join_path_parts(parts: List[str]) -> Path:
    """
    🟡 Join path parts into path - PAC-MAN's path builder!
    
    Args:
        parts: List of path components
        
    Returns:
        Path: Joined path
    """
    if not parts:
        return Path('.')
    
    return Path(*parts)


def is_path_case_sensitive() -> bool:
    """
    🟡 Check if filesystem is case sensitive - PAC-MAN's case detector!
    
    Returns:
        bool: True if filesystem is case sensitive
    """
    import tempfile
    
    with tempfile.NamedTemporaryFile(prefix='case_test_') as tmp:
        tmp_path = Path(tmp.name)
        upper_path = tmp_path.with_name(tmp_path.name.upper())
        
        # If upper case version exists when lower case exists,
        # filesystem is case insensitive
        return not upper_path.exists()


# PAC-MAN convenience functions
def pac_man_safe_path(path: Union[str, Path]) -> Path:
    """🟡 Make any path PAC-MAN safe!"""
    return resolve_path_safely(path)


def pac_man_repo_path(org: str, repo: str, version: Optional[str] = None) -> Path:
    """🟡 Get PAC-MAN repository path quickly!"""
    if version:
        return get_repository_version_path(org, repo, version)
    else:
        return get_repository_path(org, repo)


def pac_man_home() -> Path:
    """🟡 PAC-MAN's home directory!"""
    return get_Repolex_home()


def is_pac_man_territory(path: Path) -> bool:
    """🟡 Check if path is in PAC-MAN's territory (Repolex directories)!"""
    try:
        pac_home = get_Repolex_home()
        Path(path).resolve().relative_to(pac_home)
        return True
    except ValueError:
        return False