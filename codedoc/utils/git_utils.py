"""🟡 PAC-MAN Git Operations Powerhouse

The ultimate Git client wrapper with PAC-MAN-level reliability, security, and ghost-busting power!
PAC-MAN chomps through Git repositories, releases, and branches with supernatural precision!
"""

import os
import subprocess
import re
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple, Union
from urllib.parse import urlparse
import tempfile
from contextlib import contextmanager

from codedoc.models.exceptions import GitError, SecurityError, ValidationError, CodeDocError
from codedoc.utils.validation import validate_org_repo
from codedoc.utils.path_utils import resolve_path_safely, ensure_path_within_bounds


class GitOperationError(GitError):
    """🟡 PAC-MAN Git operation error."""
    pass


class GitAuthenticationError(GitError):
    """🟡 PAC-MAN Git authentication error."""
    pass


class GitRepositoryError(GitError):
    """🟡 PAC-MAN Git repository error."""
    pass


def check_git_available() -> bool:
    """
    🟡 Check if Git is available - PAC-MAN's Git detector!
    
    Returns:
        bool: True if Git is available
    """
    try:
        result = subprocess.run(
            ['git', '--version'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def get_git_version() -> Optional[str]:
    """
    🟡 Get Git version - PAC-MAN's version scanner!
    
    Returns:
        Optional[str]: Git version string or None if Git not available
    """
    try:
        result = subprocess.run(
            ['git', '--version'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            # Extract version from "git version 2.x.x"
            match = re.search(r'git version (\d+\.\d+\.\d+)', result.stdout)
            return match.group(1) if match else result.stdout.strip()
        return None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def validate_git_url(url: str) -> str:
    """
    🟡 Validate and normalize Git URL - PAC-MAN's URL validator!
    
    Args:
        url: Git repository URL
        
    Returns:
        str: Validated and normalized URL
        
    Raises:
        ValidationError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValidationError(
            "Git URL must be a non-empty string",
            suggestions=["Provide a valid Git repository URL"]
        )
    
    url = url.strip()
    
    # Handle GitHub shorthand (org/repo)
    if re.match(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$', url):
        validate_org_repo(url)
        return f"https://github.com/{url}.git"
    
    # Validate URL format
    parsed = urlparse(url)
    
    # Check scheme
    if parsed.scheme not in ('http', 'https', 'git', 'ssh'):
        raise ValidationError(
            f"Unsupported Git URL scheme: {parsed.scheme}",
            suggestions=[
                "Use http://, https://, git://, or ssh:// schemes",
                "Or use GitHub shorthand: org/repo"
            ]
        )
    
    # Security checks
    if parsed.hostname:
        # Block localhost and private IPs for security
        if parsed.hostname.lower() in ('localhost', '127.0.0.1', '::1'):
            raise SecurityError(
                "🟡 PAC-MAN blocked localhost Git URL for security",
                suggestions=["Use public repository URLs only"]
            )
    
    return url


def run_git_command(args: List[str], cwd: Optional[Path] = None, 
                   timeout: int = 300, env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess:
    """
    🟡 Run Git command with PAC-MAN reliability!
    
    Args:
        args: Git command arguments (without 'git')
        cwd: Working directory for command
        timeout: Command timeout in seconds
        env: Environment variables
        
    Returns:
        subprocess.CompletedProcess: Command result
        
    Raises:
        GitOperationError: If command fails
    """
    if not check_git_available():
        raise GitOperationError(
            "🟡 Git not available - PAC-MAN needs Git to navigate the version control maze!",
            suggestions=[
                "Install Git on your system",
                "Ensure Git is in your PATH"
            ]
        )
    
    # Prepare command
    cmd = ['git'] + args
    
    # Prepare environment
    git_env = os.environ.copy()
    if env:
        git_env.update(env)
    
    # Security: Disable Git hooks for safety
    git_env['GIT_HOOKS_PATH'] = '/dev/null'
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=git_env
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip()
            raise GitOperationError(
                f"🟡 PAC-MAN Git command failed: {' '.join(cmd)}",
                suggestions=[
                    f"Git error: {error_msg}",
                    "Check repository URL and permissions",
                    "Ensure Git credentials are configured"
                ]
            )
        
        return result
        
    except subprocess.TimeoutExpired as e:
        raise GitOperationError(
            f"🟡 PAC-MAN Git command timed out: {' '.join(cmd)}",
            suggestions=[
                f"Command exceeded {timeout} seconds",
                "Check network connectivity",
                "Try with a longer timeout"
            ]
        ) from e
    except subprocess.SubprocessError as e:
        raise GitOperationError(
            f"🟡 PAC-MAN Git command error: {' '.join(cmd)}",
            suggestions=[
                "Check Git is properly installed",
                "Verify command arguments",
                f"Original error: {e}"
            ]
        ) from e


def clone_repository(url: str, destination: Path, branch: Optional[str] = None,
                    depth: Optional[int] = None, single_branch: bool = False) -> Path:
    """
    🟡 Clone Git repository - PAC-MAN's repo chomper!
    
    Args:
        url: Repository URL
        destination: Destination directory
        branch: Specific branch to clone
        depth: Shallow clone depth
        single_branch: Clone only the specified branch
        
    Returns:
        Path: Path to cloned repository
        
    Raises:
        GitOperationError: If cloning fails
    """
    # Validate inputs
    url = validate_git_url(url)
    destination = resolve_path_safely(destination)
    
    # Prepare clone arguments
    clone_args = ['clone']
    
    if depth:
        clone_args.extend(['--depth', str(depth)])
    
    if single_branch:
        clone_args.append('--single-branch')
    
    if branch:
        clone_args.extend(['--branch', branch])
    
    clone_args.extend([url, str(destination)])
    
    try:
        # Ensure parent directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove destination if it exists
        if destination.exists():
            shutil.rmtree(destination)
        
        # Clone repository
        run_git_command(clone_args, timeout=600)  # 10 minute timeout for clones
        
        if not destination.exists():
            raise GitOperationError(
                "🟡 Repository clone completed but directory not found",
                suggestions=["Check disk space and permissions"]
            )
        
        return destination
        
    except Exception as e:
        # Cleanup on failure
        if destination.exists():
            try:
                shutil.rmtree(destination)
            except OSError:
                pass
        
        if isinstance(e, GitOperationError):
            raise
        else:
            raise GitOperationError(
                f"🟡 PAC-MAN couldn't clone repository: {url}",
                suggestions=[
                    "Check repository URL is valid",
                    "Verify network connectivity",
                    "Check disk space and permissions",
                    f"Original error: {e}"
                ]
            ) from e


def fetch_repository(repo_path: Path, remote: str = 'origin') -> None:
    """
    🟡 Fetch repository updates - PAC-MAN's update chomper!
    
    Args:
        repo_path: Path to Git repository
        remote: Remote name to fetch from
        
    Raises:
        GitRepositoryError: If fetch fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        run_git_command(['fetch', remote, '--tags'], cwd=repo_path)
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't fetch from remote: {remote}",
            suggestions=[
                "Check network connectivity",
                "Verify remote exists",
                "Check authentication credentials"
            ]
        ) from e


def pull_repository(repo_path: Path, remote: str = 'origin', branch: Optional[str] = None) -> None:
    """
    🟡 Pull repository changes - PAC-MAN's sync chomper!
    
    Args:
        repo_path: Path to Git repository
        remote: Remote name to pull from
        branch: Branch to pull (current branch if None)
        
    Raises:
        GitRepositoryError: If pull fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        if branch:
            run_git_command(['pull', remote, branch], cwd=repo_path)
        else:
            run_git_command(['pull'], cwd=repo_path)
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't pull from remote: {remote}",
            suggestions=[
                "Check network connectivity",
                "Resolve any merge conflicts",
                "Check authentication credentials"
            ]
        ) from e


def checkout_branch_or_tag(repo_path: Path, ref: str, create_branch: bool = False) -> None:
    """
    🟡 Checkout branch or tag - PAC-MAN's branch navigator!
    
    Args:
        repo_path: Path to Git repository
        ref: Branch name or tag to checkout
        create_branch: Create new branch if it doesn't exist
        
    Raises:
        GitRepositoryError: If checkout fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        checkout_args = ['checkout']
        if create_branch:
            checkout_args.append('-b')
        checkout_args.append(ref)
        
        run_git_command(checkout_args, cwd=repo_path)
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't checkout: {ref}",
            suggestions=[
                f"Check branch/tag exists: {ref}",
                "Fetch latest changes first",
                "Resolve any uncommitted changes"
            ]
        ) from e


def get_current_branch(repo_path: Path) -> Optional[str]:
    """
    🟡 Get current branch name - PAC-MAN's branch detector!
    
    Args:
        repo_path: Path to Git repository
        
    Returns:
        Optional[str]: Current branch name or None if detached HEAD
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        result = run_git_command(['branch', '--show-current'], cwd=repo_path)
        branch_name = result.stdout.strip()
        return branch_name if branch_name else None
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't get current branch",
            suggestions=["Check repository is valid"]
        ) from e


def get_current_commit(repo_path: Path) -> str:
    """
    🟡 Get current commit hash - PAC-MAN's commit tracker!
    
    Args:
        repo_path: Path to Git repository
        
    Returns:
        str: Current commit hash
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        result = run_git_command(['rev-parse', 'HEAD'], cwd=repo_path)
        return result.stdout.strip()
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't get current commit",
            suggestions=["Check repository has commits"]
        ) from e


def list_branches(repo_path: Path, remote: bool = False) -> List[str]:
    """
    🟡 List repository branches - PAC-MAN's branch explorer!
    
    Args:
        repo_path: Path to Git repository
        remote: List remote branches instead of local
        
    Returns:
        List[str]: List of branch names
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        args = ['branch']
        if remote:
            args.append('-r')
        
        result = run_git_command(args, cwd=repo_path)
        
        branches = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if line and not line.startswith('*'):
                # Remove remote prefix and clean up
                branch = re.sub(r'^origin/', '', line)
                branch = re.sub(r'^\*\s*', '', branch)
                if branch and branch not in branches:
                    branches.append(branch)
            elif line.startswith('*'):
                # Current branch
                branch = line[1:].strip()
                if branch and branch not in branches:
                    branches.append(branch)
        
        return sorted(branches)
        
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't list branches",
            suggestions=["Check repository is valid"]
        ) from e


def list_tags(repo_path: Path, pattern: Optional[str] = None) -> List[str]:
    """
    🟡 List repository tags - PAC-MAN's tag collector!
    
    Args:
        repo_path: Path to Git repository
        pattern: Tag pattern filter (e.g., 'v*')
        
    Returns:
        List[str]: List of tag names sorted by version
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        args = ['tag', '--sort=-version:refname']  # Sort by version, newest first
        if pattern:
            args.extend(['-l', pattern])
        
        result = run_git_command(args, cwd=repo_path)
        
        tags = []
        for line in result.stdout.splitlines():
            tag = line.strip()
            if tag:
                tags.append(tag)
        
        return tags
        
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't list tags",
            suggestions=["Check repository is valid", "Fetch tags first"]
        ) from e


def get_latest_tag(repo_path: Path, pattern: Optional[str] = None) -> Optional[str]:
    """
    🟡 Get latest tag - PAC-MAN's latest version finder!
    
    Args:
        repo_path: Path to Git repository
        pattern: Tag pattern filter
        
    Returns:
        Optional[str]: Latest tag name or None if no tags
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    tags = list_tags(repo_path, pattern)
    return tags[0] if tags else None


def get_remote_url(repo_path: Path, remote: str = 'origin') -> Optional[str]:
    """
    🟡 Get remote URL - PAC-MAN's remote detector!
    
    Args:
        repo_path: Path to Git repository
        remote: Remote name
        
    Returns:
        Optional[str]: Remote URL or None if remote doesn't exist
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        result = run_git_command(['remote', 'get-url', remote], cwd=repo_path)
        return result.stdout.strip()
    except GitOperationError:
        # Remote doesn't exist
        return None


def list_remotes(repo_path: Path) -> Dict[str, str]:
    """
    🟡 List repository remotes - PAC-MAN's remote explorer!
    
    Args:
        repo_path: Path to Git repository
        
    Returns:
        Dict[str, str]: Dictionary of remote name -> URL
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        result = run_git_command(['remote', '-v'], cwd=repo_path)
        
        remotes = {}
        for line in result.stdout.splitlines():
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    name, url = parts[0], parts[1]
                    # Only keep fetch URLs (ignore push URLs)
                    if len(parts) < 3 or parts[2] == '(fetch)':
                        remotes[name] = url
        
        return remotes
        
    except GitOperationError as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't list remotes",
            suggestions=["Check repository is valid"]
        ) from e


def is_git_repository(path: Path) -> bool:
    """
    🟡 Check if directory is a Git repository - PAC-MAN's Git detector!
    
    Args:
        path: Path to check
        
    Returns:
        bool: True if path is a Git repository
    """
    try:
        path = resolve_path_safely(path)
        git_dir = path / '.git'
        return git_dir.exists() and (git_dir.is_dir() or git_dir.is_file())
    except Exception:
        return False


def get_repository_info(repo_path: Path) -> Dict[str, Any]:
    """
    🟡 Get comprehensive repository information - PAC-MAN's repo inspector!
    
    Args:
        repo_path: Path to Git repository
        
    Returns:
        Dict[str, Any]: Repository information
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        info = {
            'path': str(repo_path),
            'current_branch': get_current_branch(repo_path),
            'current_commit': get_current_commit(repo_path),
            'remotes': list_remotes(repo_path),
            'branches': list_branches(repo_path),
            'tags': list_tags(repo_path),
            'latest_tag': get_latest_tag(repo_path),
            'git_version': get_git_version()
        }
        
        return info
        
    except Exception as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't get repository info",
            suggestions=["Check repository is valid and accessible"]
        ) from e


def discover_releases(repo_path: Path, tag_pattern: str = r'^v?\d+\.\d+\.\d+.*$') -> List[Dict[str, Any]]:
    """
    🟡 Discover repository releases - PAC-MAN's release hunter!
    
    Args:
        repo_path: Path to Git repository
        tag_pattern: Regex pattern for version tags
        
    Returns:
        List[Dict[str, Any]]: List of release information
        
    Raises:
        GitRepositoryError: If repository access fails
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Not a Git repository: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    try:
        tags = list_tags(repo_path)
        releases = []
        
        pattern = re.compile(tag_pattern)
        
        for tag in tags:
            if pattern.match(tag):
                # Get tag information
                try:
                    # Get commit hash for tag
                    result = run_git_command(['rev-list', '-n', '1', tag], cwd=repo_path)
                    commit_hash = result.stdout.strip()
                    
                    # Get tag date
                    result = run_git_command(['log', '-1', '--format=%ci', commit_hash], cwd=repo_path)
                    date_str = result.stdout.strip()
                    
                    releases.append({
                        'tag': tag,
                        'commit': commit_hash,
                        'date': date_str,
                        'is_release': True
                    })
                    
                except GitOperationError:
                    # Skip tags we can't process
                    continue
        
        # Sort by version (newest first)
        return releases
        
    except Exception as e:
        raise GitRepositoryError(
            f"🟡 PAC-MAN couldn't discover releases",
            suggestions=["Check repository has tags", "Fetch tags first"]
        ) from e


@contextmanager
def temporary_git_clone(url: str, branch: Optional[str] = None):
    """
    🟡 Temporary Git clone context manager - PAC-MAN's temp repo!
    
    Args:
        url: Repository URL
        branch: Branch to clone
        
    Yields:
        Path: Path to temporary repository
        
    The repository is automatically cleaned up on exit.
    """
    temp_dir = None
    try:
        temp_dir = Path(tempfile.mkdtemp(prefix="codedoc_git_", suffix="_tmp"))
        repo_path = clone_repository(url, temp_dir / "repo", branch=branch, depth=1)
        yield repo_path
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def validate_repository_access(repo_path: Path) -> None:
    """
    🟡 Validate repository access - PAC-MAN's access checker!
    
    Args:
        repo_path: Path to Git repository
        
    Raises:
        GitRepositoryError: If repository is not accessible
    """
    repo_path = resolve_path_safely(repo_path)
    
    if not repo_path.exists():
        raise GitRepositoryError(
            f"🟡 Repository path doesn't exist: {repo_path}",
            suggestions=["Clone the repository first"]
        )
    
    if not repo_path.is_dir():
        raise GitRepositoryError(
            f"🟡 Repository path is not a directory: {repo_path}",
            suggestions=["Provide a valid directory path"]
        )
    
    if not is_git_repository(repo_path):
        raise GitRepositoryError(
            f"🟡 Path is not a Git repository: {repo_path}",
            suggestions=["Initialize Git repository or clone an existing one"]
        )
    
    # Check read permissions
    if not os.access(repo_path, os.R_OK):
        raise GitRepositoryError(
            f"🟡 No read access to repository: {repo_path}",
            suggestions=["Check file permissions"]
        )


# PAC-MAN convenience functions
def pac_man_clone(url: str, destination: Path) -> Path:
    """🟡 PAC-MAN's express repository cloning!"""
    return clone_repository(url, destination, depth=1, single_branch=True)


def pac_man_get_latest_release(repo_path: Path) -> Optional[str]:
    """🟡 PAC-MAN's latest release finder!"""
    return get_latest_tag(repo_path, pattern='v*')


def pac_man_discover_versions(repo_path: Path) -> List[str]:
    """🟡 PAC-MAN's version discovery chomper!"""
    releases = discover_releases(repo_path)
    return [release['tag'] for release in releases]


def pac_man_checkout_version(repo_path: Path, version: str) -> None:
    """🟡 PAC-MAN's version navigator!"""
    checkout_branch_or_tag(repo_path, version)


def pac_man_repo_info(repo_path: Path) -> Dict[str, Any]:
    """🟡 PAC-MAN's comprehensive repo scan!"""
    return get_repository_info(repo_path)


def is_pac_man_git_ready() -> bool:
    """🟡 Check if PAC-MAN's Git powers are ready!"""
    return check_git_available()