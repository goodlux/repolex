"""🟡 PAC-MAN File System Operations

Comprehensive file system utilities with PAC-MAN-level reliability and security.
PAC-MAN chomps through files and directories with precision and safety!
"""

import os
import shutil
import hashlib
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any, Generator, Union
from contextlib import contextmanager
import json
import stat
import time

from codedoc.models.exceptions import CodeDocError, SecurityError, ValidationError
from codedoc.utils.validation import validate_file_path, validate_export_path


class FileOperationError(CodeDocError):
    """🟡 PAC-MAN file operation error."""
    pass


def ensure_directory(path: Path, parents: bool = True, exist_ok: bool = True) -> Path:
    """
    🟡 Ensure directory exists - PAC-MAN creates safe directories!
    
    Args:
        path: Directory path to create
        parents: Create parent directories if needed
        exist_ok: Don't error if directory already exists
        
    Returns:
        Path: The created/existing directory path
        
    Raises:
        FileOperationError: If directory creation fails
    """
    try:
        path = Path(path)
        path.mkdir(parents=parents, exist_ok=exist_ok)
        return path
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't create directory: {path}",
            suggestions=[
                "Check directory permissions",
                "Ensure parent directories exist",
                f"Original error: {e}"
            ]
        ) from e


def safe_remove_file(path: Path, missing_ok: bool = True) -> bool:
    """
    🟡 Safely remove a file - PAC-MAN's careful file deletion!
    
    Args:
        path: File path to remove
        missing_ok: Don't error if file doesn't exist
        
    Returns:
        bool: True if file was removed, False if it didn't exist
        
    Raises:
        FileOperationError: If file removal fails
    """
    try:
        path = Path(path)
        if not path.exists():
            if missing_ok:
                return False
            raise FileNotFoundError(f"File not found: {path}")
        
        if path.is_file():
            path.unlink()
            return True
        else:
            raise FileOperationError(
                f"🟡 Path is not a file: {path}",
                suggestions=["Use safe_remove_directory for directories"]
            )
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't remove file: {path}",
            suggestions=[
                "Check file permissions",
                "Ensure file is not in use",
                f"Original error: {e}"
            ]
        ) from e


def safe_remove_directory(path: Path, missing_ok: bool = True) -> bool:
    """
    🟡 Safely remove directory and contents - PAC-MAN's power pellet cleanup!
    
    Args:
        path: Directory path to remove
        missing_ok: Don't error if directory doesn't exist
        
    Returns:
        bool: True if directory was removed, False if it didn't exist
        
    Raises:
        FileOperationError: If directory removal fails
    """
    try:
        path = Path(path)
        if not path.exists():
            if missing_ok:
                return False
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if path.is_dir():
            shutil.rmtree(path)
            return True
        else:
            raise FileOperationError(
                f"🟡 Path is not a directory: {path}",
                suggestions=["Use safe_remove_file for files"]
            )
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't remove directory: {path}",
            suggestions=[
                "Check directory permissions",
                "Ensure no files are in use",
                f"Original error: {e}"
            ]
        ) from e


def copy_file(src: Path, dst: Path, preserve_metadata: bool = True) -> Path:
    """
    🟡 Copy file with PAC-MAN reliability!
    
    Args:
        src: Source file path
        dst: Destination file path
        preserve_metadata: Preserve file timestamps and permissions
        
    Returns:
        Path: Destination path
        
    Raises:
        FileOperationError: If copy operation fails
    """
    try:
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
        
        if not src.is_file():
            raise FileOperationError(
                f"🟡 Source is not a file: {src}",
                suggestions=["Use copy_directory for directories"]
            )
        
        # Ensure destination directory exists
        ensure_directory(dst.parent)
        
        if preserve_metadata:
            shutil.copy2(src, dst)
        else:
            shutil.copy(src, dst)
            
        return dst
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't copy file: {src} -> {dst}",
            suggestions=[
                "Check source file permissions",
                "Ensure destination directory is writable",
                f"Original error: {e}"
            ]
        ) from e


def copy_directory(src: Path, dst: Path, preserve_metadata: bool = True) -> Path:
    """
    🟡 Copy directory tree with PAC-MAN thoroughness!
    
    Args:
        src: Source directory path
        dst: Destination directory path
        preserve_metadata: Preserve file timestamps and permissions
        
    Returns:
        Path: Destination path
        
    Raises:
        FileOperationError: If copy operation fails
    """
    try:
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"Source directory not found: {src}")
        
        if not src.is_dir():
            raise FileOperationError(
                f"🟡 Source is not a directory: {src}",
                suggestions=["Use copy_file for files"]
            )
        
        if preserve_metadata:
            shutil.copytree(src, dst, dirs_exist_ok=False)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=False, copy_function=shutil.copy)
            
        return dst
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't copy directory: {src} -> {dst}",
            suggestions=[
                "Check source directory permissions",
                "Ensure destination parent directory exists",
                "Check for conflicting destination directory",
                f"Original error: {e}"
            ]
        ) from e


def move_file_or_directory(src: Path, dst: Path) -> Path:
    """
    🟡 Move file or directory - PAC-MAN's relocator!
    
    Args:
        src: Source path
        dst: Destination path
        
    Returns:
        Path: Destination path
        
    Raises:
        FileOperationError: If move operation fails
    """
    try:
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"Source not found: {src}")
        
        # Ensure destination parent directory exists
        ensure_directory(dst.parent)
        
        shutil.move(str(src), str(dst))
        return dst
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't move: {src} -> {dst}",
            suggestions=[
                "Check source permissions",
                "Ensure destination parent directory exists",
                "Check for conflicting destination",
                f"Original error: {e}"
            ]
        ) from e


def get_file_size(path: Path) -> int:
    """
    🟡 Get file size in bytes - PAC-MAN measures the dots!
    
    Args:
        path: File path
        
    Returns:
        int: File size in bytes
        
    Raises:
        FileOperationError: If file doesn't exist or can't be accessed
    """
    try:
        path = Path(path)
        return path.stat().st_size
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't get file size: {path}",
            suggestions=[
                "Check file exists",
                "Check file permissions",
                f"Original error: {e}"
            ]
        ) from e


def get_directory_size(path: Path) -> int:
    """
    🟡 Get total directory size - PAC-MAN counts all the maze dots!
    
    Args:
        path: Directory path
        
    Returns:
        int: Total directory size in bytes
        
    Raises:
        FileOperationError: If directory doesn't exist or can't be accessed
    """
    try:
        path = Path(path)
        total_size = 0
        
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                try:
                    total_size += file_path.stat().st_size
                except OSError:
                    # Skip files we can't access
                    continue
                    
        return total_size
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't calculate directory size: {path}",
            suggestions=[
                "Check directory exists",
                "Check directory permissions",
                f"Original error: {e}"
            ]
        ) from e


def calculate_file_hash(path: Path, algorithm: str = 'sha256') -> str:
    """
    🟡 Calculate file hash - PAC-MAN's file fingerprinting!
    
    Args:
        path: File path
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)
        
    Returns:
        str: Hexadecimal hash string
        
    Raises:
        FileOperationError: If file can't be hashed
    """
    try:
        path = Path(path)
        hasher = hashlib.new(algorithm)
        
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
                
        return hasher.hexdigest()
        
    except (OSError, ValueError) as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't hash file: {path}",
            suggestions=[
                "Check file exists and is readable",
                f"Check algorithm is supported: {algorithm}",
                f"Original error: {e}"
            ]
        ) from e


def find_files(directory: Path, pattern: str = "*", recursive: bool = True) -> List[Path]:
    """
    🟡 Find files matching pattern - PAC-MAN's file hunter!
    
    Args:
        directory: Directory to search
        pattern: Glob pattern to match
        recursive: Search subdirectories
        
    Returns:
        List[Path]: List of matching file paths
        
    Raises:
        FileOperationError: If directory search fails
    """
    try:
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not directory.is_dir():
            raise FileOperationError(
                f"🟡 Path is not a directory: {directory}",
                suggestions=["Provide a valid directory path"]
            )
        
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
            
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't search directory: {directory}",
            suggestions=[
                "Check directory permissions",
                "Check pattern syntax",
                f"Original error: {e}"
            ]
        ) from e


def read_text_file(path: Path, encoding: str = 'utf-8', errors: str = 'strict') -> str:
    """
    🟡 Read text file with PAC-MAN encoding handling!
    
    Args:
        path: File path to read
        encoding: Text encoding (default: utf-8)
        errors: Error handling strategy
        
    Returns:
        str: File contents
        
    Raises:
        FileOperationError: If file reading fails
    """
    try:
        path = Path(path)
        return path.read_text(encoding=encoding, errors=errors)
    except (OSError, UnicodeError) as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't read text file: {path}",
            suggestions=[
                "Check file exists and is readable",
                f"Try different encoding (current: {encoding})",
                f"Original error: {e}"
            ]
        ) from e


def write_text_file(path: Path, content: str, encoding: str = 'utf-8', 
                   create_parents: bool = True) -> Path:
    """
    🟡 Write text file with PAC-MAN reliability!
    
    Args:
        path: File path to write
        content: Text content to write
        encoding: Text encoding (default: utf-8)
        create_parents: Create parent directories if needed
        
    Returns:
        Path: Written file path
        
    Raises:
        FileOperationError: If file writing fails
    """
    try:
        path = Path(path)
        
        if create_parents:
            ensure_directory(path.parent)
        
        path.write_text(content, encoding=encoding)
        return path
        
    except (OSError, UnicodeError) as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't write text file: {path}",
            suggestions=[
                "Check directory permissions",
                "Check disk space",
                f"Check encoding compatibility: {encoding}",
                f"Original error: {e}"
            ]
        ) from e


def read_json_file(path: Path, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    🟡 Read JSON file with PAC-MAN parsing!
    
    Args:
        path: JSON file path
        encoding: Text encoding
        
    Returns:
        Dict[str, Any]: Parsed JSON data
        
    Raises:
        FileOperationError: If JSON reading/parsing fails
    """
    try:
        content = read_text_file(path, encoding=encoding)
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't parse JSON file: {path}",
            suggestions=[
                "Check JSON syntax is valid",
                "Verify file contains valid JSON",
                f"JSON error: {e}"
            ]
        ) from e


def write_json_file(path: Path, data: Dict[str, Any], encoding: str = 'utf-8',
                   indent: int = 2, create_parents: bool = True) -> Path:
    """
    🟡 Write JSON file with PAC-MAN formatting!
    
    Args:
        path: JSON file path
        data: Data to serialize
        encoding: Text encoding
        indent: JSON indentation
        create_parents: Create parent directories
        
    Returns:
        Path: Written file path
        
    Raises:
        FileOperationError: If JSON writing fails
    """
    try:
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        return write_text_file(path, content, encoding=encoding, 
                             create_parents=create_parents)
    except (TypeError, ValueError) as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't serialize JSON data for: {path}",
            suggestions=[
                "Check data is JSON serializable",
                "Avoid circular references",
                f"Serialization error: {e}"
            ]
        ) from e


@contextmanager
def temporary_directory(prefix: str = "codedoc_", suffix: str = "_tmp"):
    """
    🟡 Create temporary directory - PAC-MAN's scratch space!
    
    Args:
        prefix: Directory name prefix
        suffix: Directory name suffix
        
    Yields:
        Path: Temporary directory path
        
    The directory is automatically cleaned up on exit.
    """
    temp_dir = None
    try:
        temp_dir = Path(tempfile.mkdtemp(prefix=prefix, suffix=suffix))
        yield temp_dir
    finally:
        if temp_dir and temp_dir.exists():
            safe_remove_directory(temp_dir)


@contextmanager
def temporary_file(mode: str = 'w+', suffix: str = '', prefix: str = 'codedoc_',
                  delete: bool = True, encoding: str = 'utf-8'):
    """
    🟡 Create temporary file - PAC-MAN's scratch file!
    
    Args:
        mode: File open mode
        suffix: File name suffix
        prefix: File name prefix
        delete: Auto-delete on close
        encoding: Text encoding (for text modes)
        
    Yields:
        File object or Path: Temporary file
    """
    temp_file = None
    try:
        if 'b' in mode:
            temp_file = tempfile.NamedTemporaryFile(
                mode=mode, suffix=suffix, prefix=prefix, delete=delete
            )
        else:
            temp_file = tempfile.NamedTemporaryFile(
                mode=mode, suffix=suffix, prefix=prefix, delete=delete,
                encoding=encoding
            )
        yield temp_file
    finally:
        if temp_file and not temp_file.closed:
            temp_file.close()


def is_binary_file(path: Path, chunk_size: int = 1024) -> bool:
    """
    🟡 Check if file is binary - PAC-MAN's file type detector!
    
    Args:
        path: File path to check
        chunk_size: Bytes to read for detection
        
    Returns:
        bool: True if file appears to be binary
        
    Raises:
        FileOperationError: If file can't be read
    """
    try:
        path = Path(path)
        with open(path, 'rb') as f:
            chunk = f.read(chunk_size)
            
        # Check for null bytes (common in binary files)
        return b'\x00' in chunk
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't check file type: {path}",
            suggestions=[
                "Check file exists and is readable",
                f"Original error: {e}"
            ]
        ) from e


def get_file_permissions(path: Path) -> str:
    """
    🟡 Get file permissions - PAC-MAN's security scanner!
    
    Args:
        path: File path
        
    Returns:
        str: Octal permission string (e.g., '755')
        
    Raises:
        FileOperationError: If permissions can't be read
    """
    try:
        path = Path(path)
        mode = path.stat().st_mode
        return oct(stat.S_IMODE(mode))[-3:]
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't read permissions: {path}",
            suggestions=[
                "Check file exists",
                "Check access permissions",
                f"Original error: {e}"
            ]
        ) from e


def set_file_permissions(path: Path, permissions: Union[str, int]) -> None:
    """
    🟡 Set file permissions - PAC-MAN's security setter!
    
    Args:
        path: File path
        permissions: Octal permissions (e.g., '755' or 0o755)
        
    Raises:
        FileOperationError: If permissions can't be set
    """
    try:
        path = Path(path)
        if isinstance(permissions, str):
            permissions = int(permissions, 8)
        path.chmod(permissions)
    except (OSError, ValueError) as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't set permissions: {path}",
            suggestions=[
                "Check file exists",
                "Check you have permission to modify file",
                f"Check permissions format: {permissions}",
                f"Original error: {e}"
            ]
        ) from e


def get_file_info(path: Path) -> Dict[str, Any]:
    """
    🟡 Get comprehensive file information - PAC-MAN's file inspector!
    
    Args:
        path: File path
        
    Returns:
        Dict[str, Any]: File information dictionary
        
    Raises:
        FileOperationError: If file info can't be read
    """
    try:
        path = Path(path)
        stat_info = path.stat()
        
        return {
            'path': str(path),
            'name': path.name,
            'size': stat_info.st_size,
            'size_mb': stat_info.st_size / (1024 * 1024),
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'is_symlink': path.is_symlink(),
            'permissions': oct(stat.S_IMODE(stat_info.st_mode))[-3:],
            'owner_uid': stat_info.st_uid,
            'group_gid': stat_info.st_gid,
            'created': stat_info.st_ctime,
            'modified': stat_info.st_mtime,
            'accessed': stat_info.st_atime,
            'is_binary': is_binary_file(path) if path.is_file() else False,
        }
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't get file info: {path}",
            suggestions=[
                "Check file exists",
                "Check access permissions",
                f"Original error: {e}"
            ]
        ) from e


def cleanup_empty_directories(root_path: Path, preserve_root: bool = True) -> int:
    """
    🟡 Remove empty directories - PAC-MAN's maze cleaner!
    
    Args:
        root_path: Root directory to clean
        preserve_root: Don't delete the root directory itself
        
    Returns:
        int: Number of directories removed
        
    Raises:
        FileOperationError: If cleanup fails
    """
    try:
        root_path = Path(root_path)
        removed_count = 0
        
        # Walk bottom-up to handle nested empty directories
        for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
            dir_path = Path(dirpath)
            
            # Skip root directory if preserving
            if preserve_root and dir_path == root_path:
                continue
                
            # Check if directory is empty
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    removed_count += 1
            except OSError:
                # Directory not empty or permission error
                continue
                
        return removed_count
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't cleanup directories: {root_path}",
            suggestions=[
                "Check directory permissions",
                "Ensure no files are in use",
                f"Original error: {e}"
            ]
        ) from e


def ensure_file_writable(path: Path) -> None:
    """
    🟡 Ensure file is writable - PAC-MAN's write enabler!
    
    Args:
        path: File path to check/modify
        
    Raises:
        FileOperationError: If file can't be made writable
    """
    try:
        path = Path(path)
        if path.exists() and not os.access(path, os.W_OK):
            # Try to make it writable
            current_permissions = path.stat().st_mode
            new_permissions = current_permissions | stat.S_IWUSR
            path.chmod(new_permissions)
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't make file writable: {path}",
            suggestions=[
                "Check file ownership",
                "Check parent directory permissions",
                f"Original error: {e}"
            ]
        ) from e


def list_directory_contents(path: Path, include_hidden: bool = False,
                          include_stats: bool = False) -> List[Dict[str, Any]]:
    """
    🟡 List directory contents - PAC-MAN's directory explorer!
    
    Args:
        path: Directory path
        include_hidden: Include hidden files/directories
        include_stats: Include file statistics
        
    Returns:
        List[Dict[str, Any]]: List of directory entries
        
    Raises:
        FileOperationError: If directory can't be listed
    """
    try:
        path = Path(path)
        entries = []
        
        for item in path.iterdir():
            # Skip hidden files if requested
            if not include_hidden and item.name.startswith('.'):
                continue
                
            entry = {
                'name': item.name,
                'path': str(item),
                'is_file': item.is_file(),
                'is_dir': item.is_dir(),
                'is_symlink': item.is_symlink()
            }
            
            if include_stats and (item.is_file() or item.is_dir()):
                try:
                    stat_info = item.stat()
                    entry.update({
                        'size': stat_info.st_size,
                        'modified': stat_info.st_mtime,
                        'permissions': oct(stat.S_IMODE(stat_info.st_mode))[-3:]
                    })
                except OSError:
                    # Skip stat info if can't access
                    pass
                    
            entries.append(entry)
            
        return sorted(entries, key=lambda x: (not x['is_dir'], x['name'].lower()))
        
    except OSError as e:
        raise FileOperationError(
            f"🟡 PAC-MAN couldn't list directory: {path}",
            suggestions=[
                "Check directory exists",
                "Check directory permissions",
                f"Original error: {e}"
            ]
        ) from e


# PAC-MAN convenience functions
def chomp_file(path: Path) -> bool:
    """🟡 PAC-MAN chomps (deletes) a file!"""
    return safe_remove_file(path)


def chomp_directory(path: Path) -> bool:
    """🟡 PAC-MAN chomps (deletes) an entire directory maze!"""
    return safe_remove_directory(path)


def pac_man_file_size_mb(path: Path) -> float:
    """🟡 Get file size in MB - perfect for PAC-MAN maze measurements!"""
    return get_file_size(path) / (1024 * 1024)


def is_pac_man_maze_too_big(path: Path, max_mb: float = 100.0) -> bool:
    """🟡 Check if directory is too big for PAC-MAN to handle efficiently!"""
    if Path(path).is_file():
        return pac_man_file_size_mb(path) > max_mb
    else:
        return get_directory_size(path) / (1024 * 1024) > max_mb