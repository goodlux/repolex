#!/usr/bin/env python3
"""
Repository Storage Management

Manages local repository storage, cloning, and version management.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Any
from datetime import datetime
import json
import logging
from dataclasses import dataclass, asdict
import re

from ..models.exceptions import (
    RepolexError, GitError, StorageError, ValidationError, SecurityError
)
from ..models.repository import (
    RepoInfo, RepoDetails, RepoResult, UpdateResult, ReleaseInfo
)
from ..models.progress import ProgressCallback
from ..utils.validation import validate_org_repo, validate_release_tag, validate_file_path
from ..utils.git_utils import GitClient

logger = logging.getLogger(__name__)

# Storage configuration constants
DEFAULT_BATCH_SIZE = 1000
DEFAULT_TIMEOUT_SECONDS = 30


@dataclass
class RepositoryStats:
    """Repository operation statistics."""
    files_processed: int = 0
    operations_completed: int = 0
    releases_discovered: int = 0
    errors_handled: int = 0
    total_size_mb: int = 0
    last_update_time: Optional[datetime] = None
    
    def increment_files(self) -> None:
        """Track processed file."""
        self.files_processed += 1
        self.last_update_time = datetime.now()
    
    def increment_operations(self) -> None:
        """Track completed operation."""
        self.operations_completed += 1
    
    def increment_releases(self) -> None:
        """Track discovered release."""
        self.releases_discovered += 1
    
    def increment_errors(self) -> None:
        """Track handled error."""
        self.errors_handled += 1


class RepositoryStore:
    """
    Repository storage management system.
    
    Handles local repository storage with the following features:
    - Repository cloning and organization  
    - Version and release management
    - Git operations and synchronization
    - Release discovery and tracking
    - Error handling and recovery
    - Organized storage structure (~/.repolex/repos/)
    """
    
    def __init__(self, base_storage_path: Optional[Path] = None):
        """Initialize repository storage system."""
        self.base_path = base_storage_path or Path.home() / ".repolex" / "repos"
        self.git_client = GitClient()
        self.stats = RepositoryStats()
        
        # Ensure the storage directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Repository storage initialized at {self.base_path}")
    
    def add_repository(
        self, 
        org_repo: str, 
        progress_callback: ProgressCallback = None
    ) -> RepoResult:
        """
        Clone and organize a repository.
        
        Downloads the repository and organizes it in local storage.
        
        Args:
            org_repo: Repository in 'org/repo' format
            progress_callback: Progress updates during operation
            
        Returns:
            RepoResult: Results of the operation
            
        Raises:
            GitError: If git operations fail
            StorageError: If storage operations fail
            ValidationError: If org_repo is invalid
        """
        # Validate repository format
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        logger.info(f"Cloning repository: {org_repo}")
        
        if progress_callback:
            progress_callback(5.0, f"Starting repository clone: {org_repo}")
        
        try:
            # Check if repository already exists
            repo_path = self.base_path / org / repo
            if repo_path.exists():
                logger.warning(f"Repository {org_repo} already exists in storage")
                # Return existing info instead of re-cloning
                return self._analyze_existing_repository(org_repo, progress_callback)
            
            # Create organization directory
            org_path = self.base_path / org
            org_path.mkdir(exist_ok=True)
            self.stats.increment_files()
            
            if progress_callback:
                progress_callback(15.0, f"Created organization directory for {org}")
            
            # Clone the repository
            github_url = f"https://github.com/{org_repo}.git"
            logger.info(f"Cloning repository: {github_url}")
            
            if progress_callback:
                progress_callback(25.0, f"Cloning repository from GitHub...")
            
            try:
                # Use git client to clone
                self.git_client.clone_repository(
                    github_url, 
                    repo_path,
                    progress_callback=self._create_git_progress_wrapper(progress_callback, 25.0, 70.0)
                )
                self.stats.increment_operations()  # Major operation completed
                
            except Exception as e:
                self.stats.increment_errors()  # Error handled
                raise GitError(
                    f"Failed to clone repository {org_repo}: {str(e)}",
                    suggestions=[
                        "Check if repository exists and is accessible",
                        "Verify network connection",
                        "Try again in a few moments"
                    ]
                )
            
            if progress_callback:
                progress_callback(75.0, f"Discovering releases and tags...")
            
            # Discover releases and tags
            releases = self._discover_repository_releases(repo_path)
            
            if progress_callback:
                progress_callback(85.0, f"Analyzing repository structure...")
            
            # Analyze the repository structure
            repo_info = self._analyze_repository_structure(org_repo, repo_path, releases)
            
            # Update storage statistics
            self.stats.total_size_mb += self._calculate_repository_size(repo_path)
            
            if progress_callback:
                progress_callback(95.0, f"Saving repository metadata...")
            
            # Save metadata to storage
            self._save_repository_metadata(org_repo, repo_info)
            
            if progress_callback:
                progress_callback(100.0, f"Repository {org_repo} successfully cloned!")
            
            logger.info(f"Successfully cloned {org_repo}")
            logger.info(f"Found {len(releases)} releases")
            logger.info(f"Repository size: {repo_info.size_mb:.1f} MB")
            
            return RepoResult(
                success=True,
                org_repo=org_repo,
                storage_path=repo_path,
                releases=[r.tag for r in releases],
                size_mb=repo_info.size_mb,
                message=f"Successfully cloned {org_repo}"
            )
            
        except Exception as e:
            self.stats.increment_errors()  # Error tracked
            logger.error(f"Error cloning {org_repo}: {e}")
            
            # Cleanup on failure
            repo_path = self.base_path / org / repo
            if repo_path.exists():
                self._cleanup_failed_repository(repo_path)
            
            raise
    
    def remove_repository(
        self, 
        org_repo: str, 
        force: bool = False,
        progress_callback: ProgressCallback = None
    ) -> bool:
        """
        Remove repository and all associated data.
        
        Removes repository files and all semantic intelligence data.
        This operation cannot be undone.
        """
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        repo_path = self.base_path / org / repo
        
        if not repo_path.exists():
            logger.warning(f"Repository {org_repo} not found in storage")
            return False
        
        logger.info(f"Removing repository: {org_repo}")
        
        if not force:
            logger.warning(f"Preparing to remove repository {org_repo} permanently")
        
        if progress_callback:
            progress_callback(10.0, f"Preparing removal for {org_repo}...")
        
        try:
            # Calculate what we're about to remove
            repo_size = self._calculate_repository_size(repo_path)
            
            if progress_callback:
                progress_callback(30.0, f"Removing repository files...")
            
            # Remove the repository
            shutil.rmtree(repo_path)
            self.stats.increment_errors()  # Track operation
            
            if progress_callback:
                progress_callback(70.0, f"Cleaning up metadata...")
            
            # Clean up metadata
            self._remove_repository_metadata(org_repo)
            
            if progress_callback:
                progress_callback(90.0, f"Final cleanup...")
            
            # Clean up empty organization directory if needed
            org_path = self.base_path / org
            if org_path.exists() and not any(org_path.iterdir()):
                org_path.rmdir()
                logger.info(f"Cleaned up empty organization directory: {org}")
            
            # Update stats
            self.stats.total_size_mb -= repo_size
            
            if progress_callback:
                progress_callback(100.0, f"Repository {org_repo} removed")
            
            logger.info(f"Successfully removed repository {org_repo}")
            logger.info(f"Freed up {repo_size:.1f} MB of storage space")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove repository {org_repo}: {e}")
            raise StorageError(
                f"Failed to remove repository {org_repo}: {str(e)}",
                suggestions=[
                    "Check if repository is currently in use",
                    "Verify file permissions",
                    "Try force mode if safe to do so"
                ]
            )
    
    def list_repositories(self) -> List[RepoInfo]:
        """
        List all repositories in storage.
        
        Returns a complete list of all repositories in local storage.
        
        Returns:
            List[RepoInfo]: All repositories in storage
        """
        logger.info("Listing all repositories in storage")
        
        repositories = []
        
        # Traverse the storage structure
        if not self.base_path.exists():
            logger.info("Storage is empty - no repositories found")
            return repositories
        
        for org_path in self.base_path.iterdir():
            if not org_path.is_dir() or org_path.name.startswith('.'):
                continue
                
            org_name = org_path.name
            
            for repo_path in org_path.iterdir():
                if not repo_path.is_dir() or repo_path.name.startswith('.'):
                    continue
                
                repo_name = repo_path.name
                org_repo = f"{org_name}/{repo_name}"
                
                try:
                    # Analyze this repository
                    repo_info = self._quick_analyze_repository(org_repo, repo_path)
                    repositories.append(repo_info)
                    self.stats.increment_files()
                    
                except Exception as e:
                    logger.warning(f"Error analyzing {org_repo}: {e}")
                    self.stats.increment_errors()
                    continue
        
        logger.info(f"Found {len(repositories)} repositories in storage")
        return repositories
    
    def show_repository(self, org_repo: str) -> RepoDetails:
        """
        Show detailed information about a specific repository.
        
        Provides detailed information about repository status,
        releases, and processing history.
        
        Args:
            org_repo: Repository to examine
            
        Returns:
            RepoDetails: Detailed repository information
            
        Raises:
            ValidationError: If repository format invalid
            StorageError: If repository not found in storage
        """
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        repo_path = self.base_path / org / repo
        
        if not repo_path.exists():
            raise StorageError(
                f"Repository {org_repo} not found in storage",
                suggestions=[
                    f"Use 'add_repository(\"{org_repo}\")' to add it to storage",
                    "Check the repository name for typos",
                    "Use 'list_repositories()' to see available repositories"
                ]
            )
        
        logger.info(f"Examining repository: {org_repo}")
        
        try:
            # Get basic repository information
            releases = self._discover_repository_releases(repo_path)
            size_mb = self._calculate_repository_size(repo_path)
            
            # Get git information
            git_info = self._analyze_git_information(repo_path)
            
            # Get file structure information
            file_stats = self._analyze_file_structure(repo_path)
            
            # Load stored metadata if available
            metadata = self._load_repository_metadata(org_repo)
            
            self.stats.increment_files()
            
            return RepoDetails(
                org_repo=org_repo,
                storage_path=repo_path,
                size_mb=size_mb,
                releases=releases,
                clone_time=git_info.get('last_commit_date'),
                commit_count=git_info.get('commit_count', 0),
                branch_count=git_info.get('branch_count', 0),
                contributor_count=git_info.get('contributor_count', 0),
                file_count=file_stats.get('total_files', 0),
                python_file_count=file_stats.get('python_files', 0),
                has_readme=file_stats.get('has_readme', False),
                has_license=file_stats.get('has_license', False),
                main_language="python",  # Focus on Python
                metadata=metadata or {}
            )
            
        except Exception as e:
            logger.error(f"Error examining {org_repo}: {e}")
            self.stats.increment_errors()
            raise StorageError(
                f"Failed to examine repository {org_repo}: {str(e)}",
                suggestions=[
                    "Repository may be corrupted",
                    "Try refreshing the repository",
                    "Check file permissions"
                ]
            )
    
    def update_repository(
        self, 
        org_repo: str,
        progress_callback: ProgressCallback = None
    ) -> UpdateResult:
        """
        Update repository with latest commits and releases.
        
        Fetches new commits and discovers any new releases
        available for processing.
        
        Args:
            org_repo: Repository to update
            progress_callback: Progress during update
            
        Returns:
            UpdateResult: Results of the update operation
        """
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        repo_path = self.base_path / org / repo
        
        if not repo_path.exists():
            raise StorageError(
                f"Repository {org_repo} not found in storage - use add_repository() first",
                suggestions=[f"Run: add_repository('{org_repo}')"]
            )
        
        logger.info(f"Updating repository: {org_repo}")
        
        if progress_callback:
            progress_callback(10.0, f"Starting update for {org_repo}...")
        
        try:
            # Get old release count for comparison
            old_releases = self._discover_repository_releases(repo_path)
            old_release_count = len(old_releases)
            
            if progress_callback:
                progress_callback(30.0, f"Pulling latest changes from GitHub...")
            
            # Pull latest changes
            pull_result = self.git_client.pull_repository(
                repo_path,
                progress_callback=self._create_git_progress_wrapper(progress_callback, 30.0, 70.0)
            )
            
            if progress_callback:
                progress_callback(75.0, f"Discovering new releases...")
            
            # Discover new releases
            new_releases = self._discover_repository_releases(repo_path)
            new_release_count = len(new_releases)
            
            # Calculate what changed
            newly_found_releases = new_release_count - old_release_count
            if newly_found_releases > 0:
                for _ in range(newly_found_releases):
                    self.stats.increment_releases()
            
            if progress_callback:
                progress_callback(90.0, f"Updating repository metadata...")
            
            # Update metadata
            repo_info = self._analyze_repository_structure(org_repo, repo_path, new_releases)
            self._save_repository_metadata(org_repo, repo_info)
            
            if progress_callback:
                progress_callback(100.0, f"Repository update complete")
            
            logger.info(f"Updated {org_repo}")
            logger.info(f"Found {newly_found_releases} new releases")
            logger.info(f"Total releases: {new_release_count}")
            
            return UpdateResult(
                success=True,
                org_repo=org_repo,
                commits_pulled=pull_result.get('commits_pulled', 0),
                new_releases=[r.tag for r in new_releases if r not in old_releases],
                total_releases=new_release_count,
                changes_summary=pull_result.get('summary', 'Repository updated'),
                message=f"Updated {org_repo} - found {newly_found_releases} new releases"
            )
            
        except Exception as e:
            logger.error(f"Error during update of {org_repo}: {e}")
            self.stats.increment_errors()
            raise GitError(
                f"Failed to update repository {org_repo}: {str(e)}",
                suggestions=[
                    "Check network connection",
                    "Verify repository is not corrupted",
                    "Try again in a few moments"
                ]
            )
    
    def checkout_version(
        self, 
        org_repo: str, 
        version: str,
        progress_callback: ProgressCallback = None
    ) -> Path:
        """
        Checkout a specific version.
        
        Creates a separate checkout for this version.
        
        Args:
            org_repo: Repository to checkout from
            version: Version/tag to checkout
            progress_callback: Progress during checkout
            
        Returns:
            Path: Path to the version-specific checkout
        """
        validate_org_repo(org_repo)
        validate_release_tag(version)
        
        org, repo = org_repo.split('/')
        repo_path = self.base_path / org / repo
        version_path = repo_path / version
        
        if not repo_path.exists():
            raise StorageError(
                f"Repository {org_repo} not found in storage",
                suggestions=[f"Run: add_repository('{org_repo}')"]
            )
        
        logger.info(f"Checking out version: {org_repo}@{version}")
        
        if progress_callback:
            progress_callback(10.0, f"Preparing version checkout for {version}...")
        
        try:
            # Check if version already exists
            if version_path.exists():
                logger.info(f"Version {version} already exists")
                return version_path
            
            if progress_callback:
                progress_callback(30.0, f"Creating version-specific checkout...")
            
            # Create version-specific directory
            version_path.mkdir(exist_ok=True)
            
            # Use git worktree or clone approach for version isolation
            self.git_client.checkout_version(
                repo_path, 
                version, 
                version_path,
                progress_callback=self._create_git_progress_wrapper(progress_callback, 30.0, 90.0)
            )
            
            self.stats.increment_files()  # Version checkout completed
            
            if progress_callback:
                progress_callback(100.0, f"Version {version} ready")
            
            logger.info(f"Checked out version: {version}")
            return version_path
            
        except Exception as e:
            logger.error(f"Error during version checkout: {e}")
            self.stats.increment_errors()
            
            # Cleanup on failure
            if version_path.exists():
                shutil.rmtree(version_path)
            
            raise GitError(
                f"Failed to checkout version {version} for {org_repo}: {str(e)}",
                suggestions=[
                    f"Verify version {version} exists in repository",
                    "Check if version tag is valid",
                    "Try refreshing repository first"
                ]
            )
    
    def get_stats(self) -> dict[str, Any]:
        """
        Get storage statistics.
        
        Returns comprehensive statistics about storage activities.
        """
        return {
            "storage_stats": asdict(self.stats),
            "storage_info": {
                "storage_path": str(self.base_path),
                "storage_exists": self.base_path.exists(),
                "total_storage_size_mb": self.stats.total_size_mb
            },
            "performance": {
                "files_per_second": self._calculate_files_per_second(),
                "efficiency_rating": self._calculate_efficiency_rating(),
                "error_rate": self._calculate_error_rate()
            }
        }
    
    # Private methods for internal operations
    
    def _create_git_progress_wrapper(
        self, 
        progress_callback: ProgressCallback, 
        start_percent: float, 
        end_percent: float
    ):
        """Create a progress wrapper for git operations"""
        if not progress_callback:
            return None
        
        def git_progress_wrapper(percent: float, message: str):
            # Map git progress (0-100) to our range (start_percent to end_percent)
            mapped_percent = start_percent + (percent / 100.0) * (end_percent - start_percent)
            progress_callback(mapped_percent, f"Git: {message}")
        
        return git_progress_wrapper
    
    def _discover_repository_releases(self, repo_path: Path) -> List[ReleaseInfo]:
        """Discover all releases in repository"""
        try:
            releases = self.git_client.discover_releases(repo_path)
            
            # Convert to our format
            release_list = []
            for release in releases:
                release_list.append(ReleaseInfo(
                    tag=release['tag'],
                    commit_sha=release.get('commit_sha', ''),
                    date=release.get('date'),
                    message=release.get('message', ''),
                    is_prerelease=release.get('is_prerelease', False)
                ))
            
            logger.info(f"Found {len(release_list)} releases")
            return release_list
            
        except Exception as e:
            logger.warning(f"Error discovering releases: {e}")
            return []
    
    def _analyze_repository_structure(
        self, 
        org_repo: str, 
        repo_path: Path, 
        releases: List[ReleaseInfo]
    ) -> RepoInfo:
        """Analyze repository structure and create RepoInfo"""
        
        # Calculate repository size
        size_mb = self._calculate_repository_size(repo_path)
        
        # Analyze file structure
        file_stats = self._analyze_file_structure(repo_path)
        
        # Get git information
        git_info = self._analyze_git_information(repo_path)
        
        return RepoInfo(
            org_repo=org_repo,
            storage_path=repo_path,
            size_mb=size_mb,
            releases=releases,
            last_updated=git_info.get('last_commit_date'),
            file_count=file_stats.get('total_files', 0),
            python_file_count=file_stats.get('python_files', 0),
            status="ready",
            metadata={
                "added_to_storage": datetime.now().isoformat(),
                "git_info": git_info,
                "file_stats": file_stats
            }
        )
    
    def _analyze_existing_repository(
        self, 
        org_repo: str, 
        progress_callback: ProgressCallback
    ) -> RepoResult:
        """Analyze an existing repository instead of re-cloning"""
        
        if progress_callback:
            progress_callback(50.0, f"Repository already in storage - analyzing...")
        
        org, repo = org_repo.split('/')
        repo_path = self.base_path / org / repo
        
        # Discover releases
        releases = self._discover_repository_releases(repo_path)
        
        # Get repository info
        repo_info = self._analyze_repository_structure(org_repo, repo_path, releases)
        
        if progress_callback:
            progress_callback(100.0, f"Repository analysis complete")
        
        return RepoResult(
            success=True,
            org_repo=org_repo,
            storage_path=repo_path,
            releases=[r.tag for r in releases],
            size_mb=repo_info.size_mb,
            message=f"Repository {org_repo} already in storage"
        )
    
    def _calculate_repository_size(self, repo_path: Path) -> float:
        """Calculate repository size in MB"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in repo_path.walk():
                for filename in filenames:
                    file_path = dirpath / filename
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, IOError):
                        continue
            return total_size / (1024 * 1024)  # Convert to MB
        except Exception:
            return 0.0
    
    def _analyze_file_structure(self, repo_path: Path) -> dict[str, Any]:
        """Analyze file structure of repository"""
        stats = {
            'total_files': 0,
            'python_files': 0,
            'has_readme': False,
            'has_license': False,
            'directories': 0,
            'file_types': {}
        }
        
        try:
            for path in repo_path.rglob('*'):
                if path.is_file():
                    stats['total_files'] += 1
                    
                    # Check file type
                    suffix = path.suffix.lower()
                    stats['file_types'][suffix] = stats['file_types'].get(suffix, 0) + 1
                    
                    # Special file checks
                    if suffix == '.py':
                        stats['python_files'] += 1
                    elif path.name.lower().startswith('readme'):
                        stats['has_readme'] = True
                    elif path.name.lower().startswith('license'):
                        stats['has_license'] = True
                        
                elif path.is_dir():
                    stats['directories'] += 1
                    
        except Exception as e:
            logger.warning(f"Error analyzing file structure: {e}")
        
        return stats
    
    def _analyze_git_information(self, repo_path: Path) -> dict[str, Any]:
        """Analyze git information for repository"""
        try:
            git_info = self.git_client.get_repository_info(repo_path)
            return git_info
        except Exception as e:
            logger.warning(f"Error analyzing git info: {e}")
            return {}
    
    def _quick_analyze_repository(self, org_repo: str, repo_path: Path) -> RepoInfo:
        """Quick analysis of repository for storage listing"""
        try:
            # Basic information only
            size_mb = self._calculate_repository_size(repo_path)
            releases = self._discover_repository_releases(repo_path)
            
            return RepoInfo(
                org_repo=org_repo,
                storage_path=repo_path,
                size_mb=size_mb,
                releases=releases,
                status="ready"
            )
            
        except Exception as e:
            logger.warning(f"Error in quick analysis: {e}")
            # Return minimal info on error
            return RepoInfo(
                org_repo=org_repo,
                storage_path=repo_path,
                size_mb=0.0,
                releases=[],
                status="error",
                metadata={"error": str(e)}
            )
    
    def _save_repository_metadata(self, org_repo: str, repo_info: RepoInfo):
        """Save repository metadata to storage"""
        try:
            org, repo = org_repo.split('/')
            metadata_path = self.base_path / org / repo / ".repolex_metadata.json"
            
            metadata = {
                "org_repo": org_repo,
                "size_mb": repo_info.size_mb,
                "releases": [asdict(r) for r in repo_info.releases],
                "last_updated": datetime.now().isoformat(),
                "storage_version": "1.0",
                "stats": asdict(self.stats)
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
                
        except Exception as e:
            logger.warning(f"Error saving metadata: {e}")
    
    def _load_repository_metadata(self, org_repo: str) -> dict[str, Any] | None:
        """Load repository metadata from storage"""
        try:
            org, repo = org_repo.split('/')
            metadata_path = self.base_path / org / repo / ".repolex_metadata.json"
            
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading metadata: {e}")
        
        return None
    
    def _remove_repository_metadata(self, org_repo: str):
        """Remove repository metadata"""
        try:
            org, repo = org_repo.split('/')
            metadata_path = self.base_path / org / repo / ".repolex_metadata.json"
            
            if metadata_path.exists():
                metadata_path.unlink()
        except Exception as e:
            logger.warning(f"Error removing metadata: {e}")
    
    def _cleanup_failed_repository(self, repo_path: Path):
        """Clean up after failed repository operation"""
        try:
            if repo_path.exists():
                shutil.rmtree(repo_path)
                logger.info(f"Cleaned up failed repository at {repo_path}")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def _calculate_files_per_second(self) -> float:
        """Calculate files per second rate"""
        if not self.stats.last_update_time:
            return 0.0
        
        # This is a simplified calculation
        # In reality, you'd track timing more precisely
        return self.stats.files_processed / max(1, (datetime.now() - self.stats.last_update_time).total_seconds())
    
    def _calculate_efficiency_rating(self) -> str:
        """Calculate efficiency rating"""
        total_operations = self.stats.files_processed + self.stats.operations_completed
        if total_operations == 0:
            return "NEW SYSTEM"
        
        success_rate = (total_operations - self.stats.errors_handled) / total_operations
        
        if success_rate >= 0.95:
            return "EXCELLENT"
        elif success_rate >= 0.85:
            return "GOOD"
        elif success_rate >= 0.70:
            return "FAIR"
        else:
            return "NEEDS_IMPROVEMENT"
    
    def _calculate_error_rate(self) -> float:
        """Calculate error rate (lower is better)"""
        total_operations = (
            self.stats.files_processed + 
            self.stats.operations_completed + 
            self.stats.errors_handled
        )
        if total_operations == 0:
            return 0.0
        
        return self.stats.errors_handled / total_operations


# Factory function for easy instantiation
def create_repository_store(storage_path: Optional[Path] = None) -> RepositoryStore:
    """
    Create repository storage system.
    
    Factory function to create the repository storage system.
    
    Args:
        storage_path: Custom storage path (defaults to ~/.repolex/repos)
        
    Returns:
        RepositoryStore: Ready for repository operations
    """
    store = RepositoryStore(storage_path)
    logger.info("Repository storage system created and ready")
    return store


# Convenience aliases
RepositoryVault = RepositoryStore  # For compatibility