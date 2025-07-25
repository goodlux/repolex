"""
🟡 PAC-MAN Repository Manager - File Operations

WAKA WAKA WAKA! PAC-MAN chomps through repositories like dots in the maze!
Handles repository file operations - cloning, updating, release discovery.
Does NOT handle semantic analysis (that's GraphManager's job).
"""

import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable
from urllib.parse import urlparse

from ..models.exceptions import GitError, ValidationError, SecurityError
from ..models.repository import RepoInfo, RepoDetails, RepoResult, UpdateResult, RepoStatus, ReleaseInfo
from ..models.progress import ProgressCallback, ProgressReport
from ..utils.validation import validate_org_repo, validate_release_tag


@dataclass
class GitRepositoryInfo:
    """🟡 PAC-MAN parsed Git repository information."""
    url: str
    org: str
    repo_name: str
    org_repo: str  # "org/repo" format for consistency
    host: str  # github.com, gitlab.com, etc.
    is_github: bool
    is_public: bool = True  # Assume public unless proven otherwise


@dataclass
class CloneResult:
    """🟡 PAC-MAN clone operation result."""
    local_path: str
    success: bool
    actual_branch: str
    commit_sha: str
    remote_url: str
    clone_timestamp: datetime
    releases: List[str]
    error_message: Optional[str] = None


class RepoManager:
    """
    🟡 PAC-MAN Repository Manager
    
    Handles repository file operations like chomping through dots in the maze!
    Clones repositories, discovers releases, manages local storage.
    
    WAKA WAKA WAKA! 
    """
    
    def __init__(self, config_manager_or_storage_root = None):
        """Initialize PAC-MAN's repository maze navigation system."""
        # Handle both config_manager and direct storage_root for backward compatibility
        if hasattr(config_manager_or_storage_root, 'get_setting'):
            # It's a config manager
            config_manager = config_manager_or_storage_root
            storage_path = config_manager.get_setting('database.storage_path', '~/.Repolex/graph')
            self.storage_root = Path(storage_path).expanduser().parent / "repos"
        elif config_manager_or_storage_root is not None:
            # It's a direct path
            self.storage_root = Path(config_manager_or_storage_root)
        else:
            # Default fallback
            self.storage_root = Path.home() / ".Repolex" / "repos"
        
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self.temp_clone_prefix = "Repolex_pacman_clone_"
        
        # PAC-MAN stats tracking 🟡
        self.dots_chomped = 0  # Repositories processed
        self.power_pellets_found = 0  # Releases discovered
        self.ghosts_avoided = 0  # Errors handled gracefully
    
    def add_repository(self, org_repo: str, progress_callback: Optional[ProgressCallback] = None) -> RepoResult:
        """
        🟡 PAC-MAN chomps a new repository dot!
        
        Clone repository and discover available releases.
        Does NOT perform semantic analysis - use graph_add() for that.
        """
        validate_org_repo(org_repo)
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=0, total=100, 
                message=f"🟡 PAC-MAN entering repository maze: {org_repo}",
                stage="initializing"
            ))
        
        try:
            # Check if already exists
            repo_path = self._get_repo_path(org_repo)
            if repo_path.exists():
                raise ValidationError(
                    f"Repository {org_repo} already exists!",
                    suggestions=[
                        f"Use 'Repolex repo update {org_repo}' to update existing repository",
                        f"Use 'Repolex repo remove {org_repo}' to remove and re-add"
                    ]
                )
            
            # Parse and validate repository URL
            git_url = self._org_repo_to_url(org_repo)
            repo_info = self._parse_git_url(git_url)
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=10, total=100,
                    message=f"🟡 PAC-MAN analyzing repository: {repo_info.host}",
                    stage="parsing"
                ))
            
            # Clone the repository
            clone_result = self._clone_repository(git_url, progress_callback)
            if not clone_result.success:
                raise GitError(
                    f"Failed to clone repository: {clone_result.error_message}",
                    suggestions=[
                        "Check if the repository URL is correct",
                        "Ensure you have access to the repository",
                        "Check your internet connection"
                    ]
                )
            
            # Move to permanent storage
            final_path = self._setup_permanent_storage(org_repo, clone_result, progress_callback)
            
            # Discover releases
            releases = self._discover_releases(final_path, progress_callback)
            
            # Cache repository metadata
            self._cache_repository_metadata(org_repo, repo_info, clone_result, releases)
            
            # Update PAC-MAN stats 🟡
            self.dots_chomped += 1
            self.power_pellets_found += len(releases)
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=100, total=100,
                    message=f"🟡 PAC-MAN successfully chomped repository! Found {len(releases)} release dots!",
                    stage="complete"
                ))
            
            return RepoResult(
                org_repo=org_repo,
                success=True,
                message=f"Successfully cloned repository {org_repo} and found {len(releases)} releases",
                operation="add_repository",
                releases=releases,
                storage_path=final_path,
                processing_time=(datetime.now() - clone_result.clone_timestamp).total_seconds(),
                size_mb=self._calculate_directory_size(final_path) / (1024 * 1024)
            )
            
        except Exception as e:
            self.ghosts_avoided += 1  # Error handled gracefully
            
            if isinstance(e, (ValidationError, GitError, SecurityError)):
                raise
            else:
                raise GitError(
                    f"Unexpected error adding repository {org_repo}: {str(e)}",
                    suggestions=[
                        "Check if the repository exists and is accessible",
                        "Try again in a few minutes"
                    ]
                )
    
    def remove_repository(self, org_repo: str, force: bool = False, progress_callback: Optional[ProgressCallback] = None) -> bool:
        """
        🟡 PAC-MAN devours a repository dot (removes everything)!
        
        Remove repository files and ALL associated semantic data.
        This operation cannot be undone - like a power pellet clearing ghosts!
        """
        validate_org_repo(org_repo)
        
        repo_path = self._get_repo_path(org_repo)
        if not repo_path.exists():
            return False  # Repository not found
        
        if not force:
            # This should be handled by CLI/TUI confirmation
            raise SecurityError(
                f"Destructive operation requires confirmation",
                suggestions=["Use --force flag or confirm in interactive mode"]
            )
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=0, total=100,
                message=f"🟡 PAC-MAN power pellet activated! Removing {org_repo}...",
                stage="removing"
            ))
        
        try:
            # Remove repository directory entirely
            shutil.rmtree(repo_path)
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=100, total=100,
                    message=f"🟡 PAC-MAN cleared the maze! Repository {org_repo} removed!",
                    stage="complete"
                ))
            
            return True
            
        except Exception as e:
            raise GitError(
                f"Failed to remove repository {org_repo}: {str(e)}",
                suggestions=["Check file permissions", "Try again"]
            )
    
    def list_repositories(self) -> List[RepoInfo]:
        """🟡 PAC-MAN surveys the maze - list all tracked repositories."""
        
        repos = []
        
        for org_dir in self.storage_root.iterdir():
            if not org_dir.is_dir() or org_dir.name.startswith('.'):
                continue
                
            for repo_dir in org_dir.iterdir():
                if not repo_dir.is_dir() or repo_dir.name.startswith('.'):
                    continue
                
                org_repo = f"{org_dir.name}/{repo_dir.name}"
                
                try:
                    # Read cached metadata
                    metadata_file = repo_dir / ".Repolex" / "repo_metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        
                        releases = metadata.get('releases', [])
                        
                        repos.append(RepoInfo(
                            org_repo=org_repo,
                            display_name=org_repo.split('/')[-1],  # Use repo name as display name
                            storage_path=repo_dir,
                            releases=[],  # ReleaseInfo objects would be populated by GraphManager
                            last_updated=datetime.fromisoformat(metadata.get('last_updated', datetime.now().isoformat())),
                            status=RepoStatus.READY,  # We'll determine this properly later
                            latest_release=releases[0] if releases else None,
                            total_size_mb=self._calculate_directory_size(repo_dir) / (1024 * 1024),
                            graphs_count=0  # This would be calculated by GraphManager
                        ))
                        
                except Exception as e:
                    # Handle repositories without metadata gracefully
                    repos.append(RepoInfo(
                        org_repo=org_repo,
                        display_name=org_repo.split('/')[-1],  # Use repo name as display name
                        storage_path=repo_dir,
                        releases=[],
                        last_updated=datetime.now(),
                        status=RepoStatus.ERROR,
                        latest_release=None,
                        total_size_mb=self._calculate_directory_size(repo_dir) / (1024 * 1024),
                        graphs_count=0
                    ))
        
        return sorted(repos, key=lambda r: r.org_repo)
    
    def show_repository(self, org_repo: str) -> RepoDetails:
        """Repository examines a specific repository in detail."""
        validate_org_repo(org_repo)
        
        repo_path = self._get_repo_path(org_repo)
        if not repo_path.exists():
            raise ValidationError(
                f"Repository {org_repo} not found",
                suggestions=[f"Use 'rlex repo add {org_repo}' to add the repository"]
            )
        
        # Read metadata
        metadata_file = repo_path / ".Repolex" / "repo_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        # Discover current releases
        releases_list = self._discover_releases(repo_path)
        
        # Create ReleaseInfo objects from strings
        releases = []
        for tag in releases_list:
            releases.append(ReleaseInfo(
                tag=tag,
                commit_sha=metadata.get('current_commit', 'unknown'),
                date=datetime.fromisoformat(metadata.get('last_updated', datetime.now().isoformat()))
            ))
        
        return RepoDetails(
            org_repo=org_repo,
            display_name=org_repo.split('/')[-1],
            status=RepoStatus.READY,
            git_url=metadata.get('remote_url', ''),
            default_branch=metadata.get('current_branch', 'main'),
            clone_time=datetime.fromisoformat(metadata.get('last_updated', datetime.now().isoformat())),
            storage_path=repo_path,
            total_size_mb=self._calculate_directory_size(repo_path) / (1024 * 1024),
            releases=releases,
            total_functions=0,  # Would be calculated by graph manager
            total_classes=0,   # Would be calculated by graph manager
            total_files=0,     # Would be calculated by graph manager
            graphs_count=0     # Would be calculated by graph manager
        )
    
    def update_repository(self, org_repo: str, progress_callback: Optional[ProgressCallback] = None) -> UpdateResult:
        """🟡 PAC-MAN refreshes a repository dot - git pull and discover new releases."""
        validate_org_repo(org_repo)
        
        repo_path = self._get_repo_path(org_repo)
        if not repo_path.exists():
            raise ValidationError(
                f"Repository {org_repo} not found",
                suggestions=[f"Use 'Repolex repo add {org_repo}' to add the repository"]
            )
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=0, total=100,
                message=f"🟡 PAC-MAN refreshing repository: {org_repo}",
                stage="updating"
            ))
        
        try:
            # Get old releases for comparison
            old_releases = self._discover_releases(repo_path)
            
            # Git pull
            result = subprocess.run(
                ["git", "-C", str(repo_path), "pull"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                raise GitError(
                    f"Git pull failed: {result.stderr.strip()}",
                    suggestions=[
                        "Check your internet connection",
                        "Ensure repository is not in a conflicted state"
                    ]
                )
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=50, total=100,
                    message="🟡 PAC-MAN discovering new release dots...",
                    stage="discovering"
                ))
            
            # Discover new releases
            new_releases = self._discover_releases(repo_path)
            new_releases_found = set(new_releases) - set(old_releases)
            
            # Update metadata
            self._update_repository_metadata(org_repo, new_releases)
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=100, total=100,
                    message=f"🟡 PAC-MAN found {len(new_releases_found)} new release dots!",
                    stage="complete"
                ))
            
            return UpdateResult(
                org_repo=org_repo,
                success=True,
                message=f"Repository updated, found {len(new_releases_found)} new releases",
                previous_commit=metadata.get('current_commit', 'unknown'),
                new_commit=self._get_current_commit_sha(str(repo_path)),
                new_releases=list(new_releases_found),
                files_changed=0,  # Would need git diff parsing to determine
                commits_added=0,  # Would need git log parsing to determine
                update_time=0.0   # Would need timing measurement
            )
            
        except subprocess.TimeoutExpired:
            raise GitError(
                f"Git pull timeout after 5 minutes for {org_repo}",
                suggestions=["Try again later", "Check repository size"]
            )
        except Exception as e:
            if isinstance(e, GitError):
                raise
            else:
                raise GitError(
                    f"Unexpected error updating repository {org_repo}: {str(e)}",
                    suggestions=["Try again in a few minutes"]
                )
    
    # Private methods (PAC-MAN's internal maze navigation) 🟡
    
    def _get_repo_path(self, org_repo: str) -> Path:
        """Get local path for repository storage."""
        org, repo = org_repo.split('/', 1)
        return self.storage_root / org / repo
    
    def _org_repo_to_url(self, org_repo: str) -> str:
        """Convert org/repo format to GitHub URL."""
        return f"https://github.com/{org_repo}.git"
    
    def _parse_git_url(self, git_url: str) -> GitRepositoryInfo:
        """Parse Git repository URL to extract org, repo, and other metadata."""
        
        # Normalize URL
        git_url = git_url.strip()
        
        # Handle SSH format: git@github.com:user/repo.git
        ssh_match = re.match(r'git@([^:]+):([^/]+)/(.+?)(?:\.git)?$', git_url)
        if ssh_match:
            host, org, repo = ssh_match.groups()
            normalized_url = f"https://{host}/{org}/{repo}"
        else:
            normalized_url = git_url
            
        # Parse normalized URL
        try:
            parsed = urlparse(normalized_url)
            host = parsed.netloc
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                raise ValidationError(f"Invalid Git URL format: {git_url}")
                
            org = path_parts[0]
            repo_name = path_parts[1]
            
            # Remove .git suffix if present
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
                
        except Exception as e:
            raise ValidationError(f"Failed to parse Git URL '{git_url}': {e}")
        
        return GitRepositoryInfo(
            url=normalized_url,
            org=org,
            repo_name=repo_name,
            org_repo=f"{org}/{repo_name}",
            host=host,
            is_github=host.lower() in ['github.com', 'www.github.com'],
            is_public=True
        )
    
    def _clone_repository(self, git_url: str, progress_callback: Optional[ProgressCallback] = None) -> CloneResult:
        """Clone repository to temporary location."""
        
        # Create temporary directory for clone
        clone_dir = tempfile.mkdtemp(prefix=self.temp_clone_prefix)
        clone_timestamp = datetime.now()
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=20, total=100,
                message="🟡 PAC-MAN chomping through git data...",
                stage="cloning"
            ))
        
        try:
            # Build git clone command
            cmd = ["git", "clone", git_url, clone_dir]
            
            # Execute clone with timeout
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                return CloneResult(
                    local_path="",
                    success=False,
                    actual_branch="",
                    commit_sha="",
                    remote_url=git_url,
                    clone_timestamp=clone_timestamp,
                    releases=[],
                    error_message=f"Git clone failed: {result.stderr.strip()}"
                )
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=60, total=100,
                    message="🟡 PAC-MAN discovering release dots...",
                    stage="discovering"
                ))
            
            # Get current branch and commit info
            actual_branch = self._get_current_branch(clone_dir)
            commit_sha = self._get_current_commit_sha(clone_dir)
            
            # Discover releases immediately
            releases = self._discover_releases(Path(clone_dir))
            
            return CloneResult(
                local_path=clone_dir,
                success=True,
                actual_branch=actual_branch,
                commit_sha=commit_sha,
                remote_url=git_url,
                clone_timestamp=clone_timestamp,
                releases=releases
            )
            
        except subprocess.TimeoutExpired:
            return CloneResult(
                local_path="",
                success=False,
                actual_branch="",
                commit_sha="",
                remote_url=git_url,
                clone_timestamp=clone_timestamp,
                releases=[],
                error_message=f"Git clone timeout after 5 minutes"
            )
        except Exception as e:
            return CloneResult(
                local_path="",
                success=False,
                actual_branch="",
                commit_sha="",
                remote_url=git_url,
                clone_timestamp=clone_timestamp,
                releases=[],
                error_message=f"Unexpected error during clone: {str(e)}"
            )
    
    def _get_current_branch(self, repo_path: str) -> str:
        """Get current branch of repository."""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "unknown"
    
    def _get_current_commit_sha(self, repo_path: str) -> str:
        """Get current commit SHA of repository."""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "rev-parse", "HEAD"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "unknown"
    
    def _setup_permanent_storage(self, org_repo: str, clone_result: CloneResult, progress_callback: Optional[ProgressCallback] = None) -> Path:
        """Move cloned repository to permanent storage location."""
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=80, total=100,
                message="🟡 PAC-MAN organizing repository in the maze...",
                stage="organizing"
            ))
        
        final_path = self._get_repo_path(org_repo)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move from temporary to permanent location
        shutil.move(clone_result.local_path, str(final_path))
        
        # Create .Repolex directory for metadata
        Repolex_dir = final_path / ".Repolex"
        Repolex_dir.mkdir(exist_ok=True)
        
        return final_path
    
    def _discover_releases(self, repo_path: Path, progress_callback: Optional[ProgressCallback] = None) -> List[str]:
        """Discover git tags/releases in repository."""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "tag", "--sort=-version:refname"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                tags = [tag.strip() for tag in result.stdout.split('\n') if tag.strip()]
                return tags
            else:
                return []
                
        except Exception:
            return []
    
    def _cache_repository_metadata(self, org_repo: str, repo_info: GitRepositoryInfo, clone_result: CloneResult, releases: List[str]):  
        """Cache repository metadata for quick access."""
        
        repo_path = self._get_repo_path(org_repo)
        Repolex_dir = repo_path / ".Repolex"
        Repolex_dir.mkdir(exist_ok=True)
        
        metadata = {
            "org_repo": org_repo,
            "remote_url": repo_info.url,
            "org": repo_info.org,
            "repo_name": repo_info.repo_name,
            "host": repo_info.host,
            "is_github": repo_info.is_github,
            "current_branch": clone_result.actual_branch,
            "current_commit": clone_result.commit_sha,
            "last_updated": clone_result.clone_timestamp.isoformat(),
            "releases": releases,
            "stats": {
                "total_releases": len(releases),
                "clone_timestamp": clone_result.clone_timestamp.isoformat()
            }
        }
        
        metadata_file = Repolex_dir / "repo_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _update_repository_metadata(self, org_repo: str, releases: List[str]):
        """Update cached repository metadata."""
        
        repo_path = self._get_repo_path(org_repo)
        metadata_file = repo_path / ".Repolex" / "repo_metadata.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        # Update with new information
        metadata.update({
            "releases": releases,
            "last_updated": datetime.now().isoformat(),
            "stats": {
                **metadata.get("stats", {}),
                "total_releases": len(releases)
            }
        })
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _calculate_directory_size(self, path: Path) -> int:
        """Calculate total size of directory in bytes."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in path.walk():
                for filename in filenames:
                    filepath = dirpath / filename
                    if filepath.exists():
                        total_size += filepath.stat().st_size
        except:
            pass
        return total_size


# 🟡 PAC-MAN Convenience Functions 

def clone_repository_pacman_style(org_repo: str, **kwargs) -> RepoResult:
    """
    🟡 PAC-MAN convenience function to quickly chomp a repository!
    
    WAKA WAKA WAKA!
    """
    manager = RepoManager()
    return manager.add_repository(org_repo, **kwargs)
