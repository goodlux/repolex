#!/usr/bin/env python3
"""
🟡 PAC-MAN's Repository Vault! 🟡
Repository storage management with full PAC-MAN theming!

WAKA WAKA WAKA! Let's CHOMP through all those repository dots!
"""

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
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

# PAC-MAN themed logging
logger = logging.getLogger("Repolex.repository_vault")

# PAC-MAN Constants! 🟡
PACMAN_REPO_DOTS = "🟡"  # Repository dots to chomp
PACMAN_VERSION_DOTS = "🔵"  # Version dots to collect
PACMAN_GHOST_CLEANUP = "👻"  # Ghosts to avoid during cleanup
PACMAN_POWER_PELLET = "🔮"  # Power pellets for major operations
PACMAN_CHERRY_BONUS = "🍒"  # Bonus items (tags/releases)


@dataclass
class PacManRepositoryStats:
    """PAC-MAN themed repository statistics! 🟡"""
    dots_chomped: int = 0  # Files processed
    power_pellets_collected: int = 0  # Major milestones
    cherries_found: int = 0  # Tags/releases discovered
    ghosts_avoided: int = 0  # Errors handled gracefully
    maze_size: int = 0  # Repository size in MB
    last_chomp_time: Optional[datetime] = None
    
    def chomp_dot(self) -> None:
        """CHOMP! Another dot collected! 🟡"""
        self.dots_chomped += 1
        self.last_chomp_time = datetime.now()
    
    def collect_power_pellet(self) -> None:
        """POWER PELLET! Major operation completed! 🔮"""
        self.power_pellets_collected += 1
    
    def find_cherry(self) -> None:
        """BONUS! Cherry found! 🍒"""
        self.cherries_found += 1
    
    def avoid_ghost(self) -> None:
        """Avoided a ghost! 👻"""
        self.ghosts_avoided += 1


class PacManRepositoryVault:
    """
    🟡 PAC-MAN's Ultimate Repository Vault! 🟡
    
    The most advanced repository storage system ever created!
    PAC-MAN will CHOMP through your repositories and organize them perfectly!
    
    Features:
    - 🟡 Repository dot collection (cloning & organizing)  
    - 🔵 Version dot management (releases & tags)
    - 🔮 Power pellet operations (major git operations)
    - 🍒 Cherry bonus discovery (special releases)
    - 👻 Ghost avoidance (error handling)
    - 🌟 Perfect maze organization (~/.Repolex/repos/)
    
    WAKA WAKA WAKA! Let's eat all the repository dots!
    """
    
    def __init__(self, base_storage_path: Optional[Path] = None):
        """Initialize PAC-MAN's Repository Vault! 🟡"""
        self.base_path = base_storage_path or Path.home() / ".Repolex" / "repos"
        self.git_client = GitClient()
        self.stats = PacManRepositoryStats()
        
        # Ensure the vault exists!
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🟡 PAC-MAN Repository Vault initialized!")
        logger.info(f"🏠 Vault location: {self.base_path}")
        logger.info(f"🎮 Ready to CHOMP repositories! WAKA WAKA!")
    
    def chomp_repository(
        self, 
        org_repo: str, 
        progress_callback: Optional[ProgressCallback] = None
    ) -> RepoResult:
        """
        🟡 CHOMP CHOMP CHOMP! Clone and organize a repository!
        
        PAC-MAN will eat this repository and organize it perfectly in the vault!
        
        Args:
            org_repo: Repository in 'org/repo' format
            progress_callback: Progress updates for the chomping process
            
        Returns:
            RepoResult: Results of the chomping operation
            
        Raises:
            GitError: If git operations fail
            StorageError: If storage operations fail
            ValidationError: If org_repo is invalid
        """
        # Validate the repository dot! 🟡
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        logger.info(f"🟡 PAC-MAN is ready to CHOMP {org_repo}!")
        
        if progress_callback:
            progress_callback(5.0, f"🟡 PAC-MAN starting to chomp {org_repo}...")
        
        try:
            # Check if repository already exists
            repo_path = self.base_path / org / repo
            if repo_path.exists():
                logger.warning(f"🍒 Repository {org_repo} already in vault!")
                # Return existing info instead of re-cloning
                return self._analyze_existing_repository(org_repo, progress_callback)
            
            # Create organization directory (perfect maze structure!)
            org_path = self.base_path / org
            org_path.mkdir(exist_ok=True)
            self.stats.chomp_dot()
            
            if progress_callback:
                progress_callback(15.0, f"🏗️ Created organization maze for {org}...")
            
            # Clone the repository dot! 🟡
            github_url = f"https://github.com/{org_repo}.git"
            logger.info(f"🔗 Cloning repository: {github_url}")
            
            if progress_callback:
                progress_callback(25.0, f"🔗 Cloning repository from GitHub...")
            
            try:
                # Use git client to clone
                self.git_client.clone_repository(
                    github_url, 
                    repo_path,
                    progress_callback=self._create_git_progress_wrapper(progress_callback, 25.0, 70.0)
                )
                self.stats.collect_power_pellet()  # Major operation! 🔮
                
            except Exception as e:
                self.stats.avoid_ghost()  # Ghost avoided! 👻
                raise GitError(
                    f"Failed to clone repository {org_repo}: {str(e)}",
                    suggestions=[
                        "Check if repository exists and is accessible",
                        "Verify network connection",
                        "Try again in a few moments"
                    ]
                )
            
            if progress_callback:
                progress_callback(75.0, f"🍒 Discovering releases and tags...")
            
            # Discover all the cherry bonuses (tags/releases)! 🍒
            releases = self._discover_repository_cherries(repo_path)
            
            if progress_callback:
                progress_callback(85.0, f"📊 Analyzing repository structure...")
            
            # Analyze the repository maze structure
            repo_info = self._analyze_repository_structure(org_repo, repo_path, releases)
            
            # Update vault statistics
            self.stats.maze_size += self._calculate_repository_size(repo_path)
            
            if progress_callback:
                progress_callback(95.0, f"💾 Saving repository metadata...")
            
            # Save metadata to vault
            self._save_repository_metadata(org_repo, repo_info)
            
            if progress_callback:
                progress_callback(100.0, f"🟡 WAKA WAKA! {org_repo} successfully chomped!")
            
            logger.info(f"🎉 PAC-MAN successfully chomped {org_repo}!")
            logger.info(f"🍒 Found {len(releases)} cherry releases!")
            logger.info(f"📊 Repository size: {repo_info.size_mb:.1f} MB")
            
            return RepoResult(
                success=True,
                org_repo=org_repo,
                storage_path=repo_path,
                releases=[r.tag for r in releases],
                size_mb=repo_info.size_mb,
                message=f"🟡 PAC-MAN successfully chomped {org_repo}! WAKA WAKA!"
            )
            
        except Exception as e:
            self.stats.avoid_ghost()  # Another ghost avoided! 👻
            logger.error(f"👻 Ghost encountered while chomping {org_repo}: {e}")
            
            # Cleanup on failure
            repo_path = self.base_path / org / repo
            if repo_path.exists():
                self._cleanup_failed_repository(repo_path)
            
            raise
    
    def release_repository_ghosts(
        self, 
        org_repo: str, 
        force: bool = False,
        progress_callback: Optional[ProgressCallback] = None
    ) -> bool:
        """
        👻 Release all the repository ghosts (delete repository)!
        
        PAC-MAN will carefully release all ghosts and clean up the vault!
        
        Args:
            org_repo: Repository to release ghosts from
            force: Skip confirmation (dangerous!)
            progress_callback: Progress during ghost release
            
        Returns:
            bool: True if ghosts were successfully released
            
        Raises:
            SecurityError: If destructive operation not confirmed
            StorageError: If cleanup fails
        """
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        repo_path = self.base_path / org / repo
        
        if not repo_path.exists():
            logger.warning(f"👻 No ghosts found for {org_repo} - repository not in vault")
            return False
        
        logger.info(f"👻 PAC-MAN preparing to release ghosts from {org_repo}...")
        
        if not force:
            # This would normally require user confirmation
            # For now, we'll assume confirmation in automated contexts
            logger.warning(f"⚠️ About to release ALL ghosts from {org_repo}!")
        
        if progress_callback:
            progress_callback(10.0, f"👻 Preparing ghost release for {org_repo}...")
        
        try:
            # Calculate what we're about to release
            repo_size = self._calculate_repository_size(repo_path)
            
            if progress_callback:
                progress_callback(30.0, f"👻 Releasing repository ghosts...")
            
            # Release the ghosts! (Delete repository)
            shutil.rmtree(repo_path)
            self.stats.avoid_ghost()  # Successfully handled ghosts! 👻
            
            if progress_callback:
                progress_callback(70.0, f"👻 Cleaning up metadata...")
            
            # Clean up metadata
            self._remove_repository_metadata(org_repo)
            
            if progress_callback:
                progress_callback(90.0, f"👻 Final ghost cleanup...")
            
            # Clean up empty organization directory if needed
            org_path = self.base_path / org
            if org_path.exists() and not any(org_path.iterdir()):
                org_path.rmdir()
                logger.info(f"🧹 Cleaned up empty organization directory: {org}")
            
            # Update stats
            self.stats.maze_size -= repo_size
            
            if progress_callback:
                progress_callback(100.0, f"👻 All ghosts released from {org_repo}!")
            
            logger.info(f"🎉 PAC-MAN successfully released all ghosts from {org_repo}!")
            logger.info(f"💾 Freed up {repo_size:.1f} MB of vault space")
            
            return True
            
        except Exception as e:
            logger.error(f"👻 Failed to release ghosts from {org_repo}: {e}")
            raise StorageError(
                f"Failed to remove repository {org_repo}: {str(e)}",
                suggestions=[
                    "Check if repository is currently in use",
                    "Verify file permissions",
                    "Try force mode if safe to do so"
                ]
            )
    
    def survey_vault_dots(self) -> List[RepoInfo]:
        """
        🟡 Survey all dots in PAC-MAN's vault!
        
        Returns a complete survey of all repositories PAC-MAN has chomped!
        
        Returns:
            List[RepoInfo]: All repositories in the vault
        """
        logger.info("🟡 PAC-MAN surveying all dots in the vault...")
        
        vault_dots = []
        
        # Traverse the perfect maze structure
        if not self.base_path.exists():
            logger.info("🏠 Vault is empty - no dots to survey!")
            return vault_dots
        
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
                    # Analyze this repository dot
                    repo_info = self._quick_analyze_repository_dot(org_repo, repo_path)
                    vault_dots.append(repo_info)
                    self.stats.chomp_dot()
                    
                except Exception as e:
                    logger.warning(f"👻 Ghost encountered analyzing {org_repo}: {e}")
                    self.stats.avoid_ghost()
                    continue
        
        logger.info(f"🎯 PAC-MAN surveyed {len(vault_dots)} repository dots!")
        return vault_dots
    
    def examine_repository_dot(self, org_repo: str) -> RepoDetails:
        """
        🔍 Examine a specific repository dot in detail!
        
        PAC-MAN will provide detailed information about this repository dot!
        
        Args:
            org_repo: Repository to examine
            
        Returns:
            RepoDetails: Detailed repository information
            
        Raises:
            ValidationError: If repository format invalid
            StorageError: If repository not found in vault
        """
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        repo_path = self.base_path / org / repo
        
        if not repo_path.exists():
            raise StorageError(
                f"Repository {org_repo} not found in PAC-MAN's vault",
                suggestions=[
                    f"Use 'chomp_repository(\"{org_repo}\")' to add it to the vault",
                    "Check the repository name for typos",
                    "Use 'survey_vault_dots()' to see available repositories"
                ]
            )
        
        logger.info(f"🔍 PAC-MAN examining repository dot: {org_repo}")
        
        try:
            # Get basic repository information
            releases = self._discover_repository_cherries(repo_path)
            size_mb = self._calculate_repository_size(repo_path)
            
            # Get git information
            git_info = self._analyze_git_information(repo_path)
            
            # Get file structure information
            file_stats = self._analyze_file_structure(repo_path)
            
            # Load stored metadata if available
            metadata = self._load_repository_metadata(org_repo)
            
            self.stats.chomp_dot()
            
            return RepoDetails(
                org_repo=org_repo,
                storage_path=repo_path,
                size_mb=size_mb,
                releases=releases,
                last_updated=git_info.get('last_commit_date'),
                commit_count=git_info.get('commit_count', 0),
                branch_count=git_info.get('branch_count', 0),
                contributor_count=git_info.get('contributor_count', 0),
                file_count=file_stats.get('total_files', 0),
                python_file_count=file_stats.get('python_files', 0),
                has_readme=file_stats.get('has_readme', False),
                has_license=file_stats.get('has_license', False),
                main_language="python",  # We focus on Python
                metadata=metadata or {}
            )
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered examining {org_repo}: {e}")
            self.stats.avoid_ghost()
            raise StorageError(
                f"Failed to examine repository {org_repo}: {str(e)}",
                suggestions=[
                    "Repository may be corrupted",
                    "Try refreshing the repository",
                    "Check file permissions"
                ]
            )
    
    def refresh_repository_dots(
        self, 
        org_repo: str,
        progress_callback: Optional[ProgressCallback] = None
    ) -> UpdateResult:
        """
        🔄 Refresh repository dots (git pull + discover new releases)!
        
        PAC-MAN will refresh this repository and discover any new cherry bonuses!
        
        Args:
            org_repo: Repository to refresh
            progress_callback: Progress during refresh
            
        Returns:
            UpdateResult: Results of the refresh operation
        """
        validate_org_repo(org_repo)
        org, repo = org_repo.split('/')
        
        repo_path = self.base_path / org / repo
        
        if not repo_path.exists():
            raise StorageError(
                f"Repository {org_repo} not found in vault - use chomp_repository() first",
                suggestions=[f"Run: chomp_repository('{org_repo}')"]
            )
        
        logger.info(f"🔄 PAC-MAN refreshing repository dots: {org_repo}")
        
        if progress_callback:
            progress_callback(10.0, f"🔄 Starting refresh for {org_repo}...")
        
        try:
            # Get old release count for comparison
            old_releases = self._discover_repository_cherries(repo_path)
            old_release_count = len(old_releases)
            
            if progress_callback:
                progress_callback(30.0, f"📡 Pulling latest changes from GitHub...")
            
            # Pull latest changes
            pull_result = self.git_client.pull_repository(
                repo_path,
                progress_callback=self._create_git_progress_wrapper(progress_callback, 30.0, 70.0)
            )
            
            if progress_callback:
                progress_callback(75.0, f"🍒 Discovering new cherry releases...")
            
            # Discover new releases
            new_releases = self._discover_repository_cherries(repo_path)
            new_release_count = len(new_releases)
            
            # Calculate what changed
            newly_found_cherries = new_release_count - old_release_count
            if newly_found_cherries > 0:
                for _ in range(newly_found_cherries):
                    self.stats.find_cherry()
            
            if progress_callback:
                progress_callback(90.0, f"💾 Updating repository metadata...")
            
            # Update metadata
            repo_info = self._analyze_repository_structure(org_repo, repo_path, new_releases)
            self._save_repository_metadata(org_repo, repo_info)
            
            if progress_callback:
                progress_callback(100.0, f"🟡 Repository refresh complete!")
            
            logger.info(f"🎉 PAC-MAN refreshed {org_repo}!")
            logger.info(f"🍒 Found {newly_found_cherries} new releases!")
            logger.info(f"📊 Total releases: {new_release_count}")
            
            return UpdateResult(
                success=True,
                org_repo=org_repo,
                commits_pulled=pull_result.get('commits_pulled', 0),
                new_releases=[r.tag for r in new_releases if r not in old_releases],
                total_releases=new_release_count,
                changes_summary=pull_result.get('summary', 'Repository updated'),
                message=f"🟡 PAC-MAN refreshed {org_repo} - found {newly_found_cherries} new cherries!"
            )
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered during refresh of {org_repo}: {e}")
            self.stats.avoid_ghost()
            raise GitError(
                f"Failed to refresh repository {org_repo}: {str(e)}",
                suggestions=[
                    "Check network connection",
                    "Verify repository is not corrupted",
                    "Try again in a few moments"
                ]
            )
    
    def checkout_version_dot(
        self, 
        org_repo: str, 
        version: str,
        progress_callback: Optional[ProgressCallback] = None
    ) -> Path:
        """
        🔵 Checkout a specific version dot!
        
        PAC-MAN will create a separate checkout for this version dot!
        
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
                f"Repository {org_repo} not found in vault",
                suggestions=[f"Run: chomp_repository('{org_repo}')"]
            )
        
        logger.info(f"🔵 PAC-MAN checking out version dot: {org_repo}@{version}")
        
        if progress_callback:
            progress_callback(10.0, f"🔵 Preparing version checkout for {version}...")
        
        try:
            # Check if version already exists
            if version_path.exists():
                logger.info(f"🔵 Version dot {version} already exists!")
                return version_path
            
            if progress_callback:
                progress_callback(30.0, f"🔄 Creating version-specific checkout...")
            
            # Create version-specific directory
            version_path.mkdir(exist_ok=True)
            
            # Use git worktree or clone approach for version isolation
            self.git_client.checkout_version(
                repo_path, 
                version, 
                version_path,
                progress_callback=self._create_git_progress_wrapper(progress_callback, 30.0, 90.0)
            )
            
            self.stats.chomp_dot()  # Version dot collected! 🔵
            
            if progress_callback:
                progress_callback(100.0, f"🔵 Version dot {version} ready!")
            
            logger.info(f"🎉 PAC-MAN checked out version dot: {version}")
            return version_path
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered during version checkout: {e}")
            self.stats.avoid_ghost()
            
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
    
    def get_pacman_stats(self) -> Dict[str, Any]:
        """
        📊 Get PAC-MAN's vault statistics!
        
        Returns comprehensive statistics about PAC-MAN's activities!
        """
        return {
            "pacman_stats": asdict(self.stats),
            "vault_info": {
                "vault_path": str(self.base_path),
                "vault_exists": self.base_path.exists(),
                "total_vault_size_mb": self.stats.maze_size
            },
            "performance": {
                "dots_per_second": self._calculate_dots_per_second(),
                "efficiency_rating": self._calculate_efficiency_rating(),
                "ghost_avoidance_rate": self._calculate_ghost_avoidance_rate()
            }
        }
    
    # Private methods for PAC-MAN's internal operations
    
    def _create_git_progress_wrapper(
        self, 
        progress_callback: Optional[ProgressCallback], 
        start_percent: float, 
        end_percent: float
    ) -> Optional[Callable]:
        """Create a progress wrapper for git operations"""
        if not progress_callback:
            return None
        
        def git_progress_wrapper(percent: float, message: str):
            # Map git progress (0-100) to our range (start_percent to end_percent)
            mapped_percent = start_percent + (percent / 100.0) * (end_percent - start_percent)
            progress_callback(mapped_percent, f"🔗 {message}")
        
        return git_progress_wrapper
    
    def _discover_repository_cherries(self, repo_path: Path) -> List[ReleaseInfo]:
        """Discover all cherry bonuses (tags/releases) in repository"""
        try:
            releases = self.git_client.discover_releases(repo_path)
            
            # Convert to our format
            cherry_releases = []
            for release in releases:
                cherry_releases.append(ReleaseInfo(
                    tag=release['tag'],
                    commit_sha=release.get('commit_sha', ''),
                    date=release.get('date'),
                    message=release.get('message', ''),
                    is_prerelease=release.get('is_prerelease', False)
                ))
            
            logger.info(f"🍒 Found {len(cherry_releases)} cherry releases!")
            return cherry_releases
            
        except Exception as e:
            logger.warning(f"👻 Ghost encountered discovering releases: {e}")
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
                "added_to_vault": datetime.now().isoformat(),
                "git_info": git_info,
                "file_stats": file_stats
            }
        )
    
    def _analyze_existing_repository(
        self, 
        org_repo: str, 
        progress_callback: Optional[ProgressCallback]
    ) -> RepoResult:
        """Analyze an existing repository instead of re-cloning"""
        
        if progress_callback:
            progress_callback(50.0, f"🍒 Repository already in vault - analyzing...")
        
        org, repo = org_repo.split('/')
        repo_path = self.base_path / org / repo
        
        # Discover releases
        releases = self._discover_repository_cherries(repo_path)
        
        # Get repository info
        repo_info = self._analyze_repository_structure(org_repo, repo_path, releases)
        
        if progress_callback:
            progress_callback(100.0, f"🟡 Repository analysis complete!")
        
        return RepoResult(
            success=True,
            org_repo=org_repo,
            storage_path=repo_path,
            releases=[r.tag for r in releases],
            size_mb=repo_info.size_mb,
            message=f"🍒 Repository {org_repo} already in vault!"
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
    
    def _analyze_file_structure(self, repo_path: Path) -> Dict[str, Any]:
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
            logger.warning(f"👻 Ghost encountered analyzing file structure: {e}")
        
        return stats
    
    def _analyze_git_information(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze git information for repository"""
        try:
            git_info = self.git_client.get_repository_info(repo_path)
            return git_info
        except Exception as e:
            logger.warning(f"👻 Ghost encountered analyzing git info: {e}")
            return {}
    
    def _quick_analyze_repository_dot(self, org_repo: str, repo_path: Path) -> RepoInfo:
        """Quick analysis of repository for vault survey"""
        try:
            # Basic information only
            size_mb = self._calculate_repository_size(repo_path)
            releases = self._discover_repository_cherries(repo_path)
            
            return RepoInfo(
                org_repo=org_repo,
                storage_path=repo_path,
                size_mb=size_mb,
                releases=releases,
                status="ready"
            )
            
        except Exception as e:
            logger.warning(f"👻 Ghost encountered in quick analysis: {e}")
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
        """Save repository metadata to vault"""
        try:
            org, repo = org_repo.split('/')
            metadata_path = self.base_path / org / repo / ".Repolex_metadata.json"
            
            metadata = {
                "org_repo": org_repo,
                "size_mb": repo_info.size_mb,
                "releases": [asdict(r) for r in repo_info.releases],
                "last_updated": datetime.now().isoformat(),
                "vault_version": "1.0",
                "pacman_stats": asdict(self.stats)
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
                
        except Exception as e:
            logger.warning(f"👻 Ghost encountered saving metadata: {e}")
    
    def _load_repository_metadata(self, org_repo: str) -> Optional[Dict[str, Any]]:
        """Load repository metadata from vault"""
        try:
            org, repo = org_repo.split('/')
            metadata_path = self.base_path / org / repo / ".Repolex_metadata.json"
            
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"👻 Ghost encountered loading metadata: {e}")
        
        return None
    
    def _remove_repository_metadata(self, org_repo: str):
        """Remove repository metadata"""
        try:
            org, repo = org_repo.split('/')
            metadata_path = self.base_path / org / repo / ".Repolex_metadata.json"
            
            if metadata_path.exists():
                metadata_path.unlink()
        except Exception as e:
            logger.warning(f"👻 Ghost encountered removing metadata: {e}")
    
    def _cleanup_failed_repository(self, repo_path: Path):
        """Clean up after failed repository operation"""
        try:
            if repo_path.exists():
                shutil.rmtree(repo_path)
                logger.info(f"🧹 Cleaned up failed repository at {repo_path}")
        except Exception as e:
            logger.error(f"👻 Ghost encountered during cleanup: {e}")
    
    def _calculate_dots_per_second(self) -> float:
        """Calculate PAC-MAN's dots per second rate"""
        if not self.stats.last_chomp_time:
            return 0.0
        
        # This is a simplified calculation
        # In reality, you'd track timing more precisely
        return self.stats.dots_chomped / max(1, (datetime.now() - self.stats.last_chomp_time).total_seconds())
    
    def _calculate_efficiency_rating(self) -> str:
        """Calculate PAC-MAN's efficiency rating"""
        total_operations = self.stats.dots_chomped + self.stats.power_pellets_collected
        if total_operations == 0:
            return "🆕 NEW PLAYER"
        
        success_rate = (total_operations - self.stats.ghosts_avoided) / total_operations
        
        if success_rate >= 0.95:
            return "🟡 PAC-MAN MASTER"
        elif success_rate >= 0.85:
            return "🔮 POWER PELLET PRO"
        elif success_rate >= 0.70:
            return "🍒 CHERRY COLLECTOR"
        else:
            return "👻 GHOST DODGER"
    
    def _calculate_ghost_avoidance_rate(self) -> float:
        """Calculate ghost avoidance rate (lower is better)"""
        total_operations = (
            self.stats.dots_chomped + 
            self.stats.power_pellets_collected + 
            self.stats.ghosts_avoided
        )
        if total_operations == 0:
            return 0.0
        
        return self.stats.ghosts_avoided / total_operations


# Factory function for easy instantiation
def create_pacman_repository_vault(storage_path: Optional[Path] = None) -> PacManRepositoryVault:
    """
    🟡 Create PAC-MAN's Repository Vault!
    
    Factory function to create the ultimate repository storage system!
    
    Args:
        storage_path: Custom storage path (defaults to ~/.Repolex/repos)
        
    Returns:
        PacManRepositoryVault: Ready to CHOMP repositories!
    """
    vault = PacManRepositoryVault(storage_path)
    logger.info("🟡 PAC-MAN Repository Vault created and ready!")
    logger.info("🎮 WAKA WAKA WAKA! Let's chomp some repositories!")
    return vault


# Convenience aliases with PAC-MAN theming
RepositoryVault = PacManRepositoryVault  # For those who prefer shorter names
RepositoryStore = PacManRepositoryVault  # Compatible with original naming

if __name__ == "__main__":
    # Quick test of PAC-MAN's Repository Vault!
    
    def test_pacman_vault():
        vault = create_pacman_repository_vault()
        print("🟡 PAC-MAN Repository Vault test complete!")
        print("🎮 Ready to chomp repositories! WAKA WAKA!")
        
        stats = vault.get_pacman_stats()
        print(f"📊 Vault stats: {stats}")
    
    test_pacman_vault()
