"""
👻 PAC-MAN's Ghost Movement Pattern Analyzer 👻

This is where PAC-MAN tracks the mysterious movements of the ghosts (developers)!
Each commit is a ghost movement, each developer is a unique ghost with patterns!

WAKA WAKA! Understanding how the ghosts move through our code maze!
"""

import subprocess
from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass
import logging
import re

from ..models.git import GitIntelligence, CommitInfo, DeveloperInfo, ChangePatterns
from ..models.exceptions import GitError, ProcessingError
from ..models.progress import ProgressCallback
from ..utils.validation import validate_file_path

logger = logging.getLogger(__name__)


@dataclass
class GhostMovementStats:
    """👻 PAC-MAN's ghost tracking statistics!"""
    ghosts_tracked: int = 0  # Unique developers found
    movements_analyzed: int = 0  # Commits processed
    maze_changes_detected: int = 0  # Files changed
    power_pellet_encounters: int = 0  # Major changes
    bonus_patterns_found: int = 0  # Co-change patterns discovered


@dataclass
class GhostProfile:
    """👻 Individual ghost (developer) profile!"""
    name: str
    email: str
    total_commits: int
    files_touched: Set[str]
    favorite_maze_areas: List[str]  # Most common directories
    ghost_type: str  # "speed_demon", "maze_master", "power_pellet_collector"
    activity_pattern: str  # "morning_ghost", "night_owl", "weekend_warrior"
    first_seen: datetime
    last_seen: datetime


class GitGhostTracker:
    """
    👻 PAC-MAN's Git Ghost Tracking System! 👻
    
    Tracks all the mysterious ghost movements through our code maze!
    Each ghost (developer) has unique patterns and behaviors!
    """

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.stats = GhostMovementStats()
        self.ghost_profiles: Dict[str, GhostProfile] = {}
        self.logger = logging.getLogger(__name__)
        
        # Ensure we're in a git repository
        if not (repo_path / ".git").exists():
            raise GitError(f"Not a git repository: {repo_path}")
        
        logger.info(f"👻 PAC-MAN starting ghost tracking in: {repo_path}")

    def track_all_ghost_movements(self) -> GitIntelligence:
        """
        👻 TRACK ALL THE GHOSTS! 👻
        
        Complete analysis of all ghost movements in the maze!
        """
        try:
            self.logger.info("👻 Beginning complete ghost movement analysis...")
            
            # Extract all commit movements
            commits = self._extract_all_commits()
            
            # Analyze individual ghost profiles
            developers = self._analyze_ghost_profiles(commits)
            
            # Detect movement patterns
            patterns = self._detect_movement_patterns(commits)
            
            # Analyze branch behaviors
            branches = self._analyze_branch_patterns()
            
            # Find tag/release patterns
            tags = self._analyze_tag_patterns()
            
            self.logger.info(f"👻 Ghost analysis complete! {len(developers)} ghosts, {len(commits)} movements")
            
            return GitIntelligence(
                repository_path=self.repo_path,
                commits=commits,
                total_commits=len(commits),
                developers=developers,
                change_patterns=patterns,
                first_commit_date=min(c.commit_date for c in commits) if commits else None,
                last_commit_date=max(c.commit_date for c in commits) if commits else None
            )
            
        except Exception as e:
            raise GitError(f"Failed to track ghost movements: {e}")

    def _extract_all_commits(self) -> List[CommitInfo]:
        """👻 Extract all commit movements from the maze!"""
        try:
            # Get comprehensive commit log with detailed info
            cmd = [
                "git", "log", 
                "--all",  # All branches
                "--pretty=format:%H|%an|%ae|%at|%s|%P",  # Custom format
                "--name-status"  # Show file changes
            ]
            
            result = subprocess.run(
                cmd, 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            commits = []
            current_commit = None
            
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue
                
                if '|' in line and not line.startswith(('A\t', 'M\t', 'D\t', 'R\t')):
                    # This is a commit header line
                    if current_commit:
                        commits.append(current_commit)
                    
                    parts = line.split('|')
                    if len(parts) >= 6:
                        sha, author, email, timestamp, message, parents = parts[:6]
                        
                        # Determine ghost type based on commit patterns
                        ghost_type = self._classify_ghost_movement(message, author)
                        
                        current_commit = CommitInfo(
                            commit_hash=sha,
                            author_name=author.strip(),
                            author_email=email.strip(),
                            commit_date=datetime.fromtimestamp(int(timestamp), tz=timezone.utc),
                            message=message.strip(),
                            parents=parents.split() if parents.strip() else [],
                            files_added=[],
                            files_modified=[],
                            files_deleted=[],
                            ghost_type=ghost_type
                        )
                        
                        self.stats.movements_analyzed += 1
                        
                elif current_commit and line.startswith(('A\t', 'M\t', 'D\t', 'R\t')):
                    # This is a file change line
                    change_type = line[0]
                    file_path = line[2:].strip()
                    
                    # Add to appropriate list based on change type
                    if change_type == 'A':
                        current_commit.files_added.append(file_path)
                    elif change_type == 'M':
                        current_commit.files_modified.append(file_path)
                    elif change_type == 'D':
                        current_commit.files_deleted.append(file_path)
                    elif change_type == 'R':  # Renamed files - treat as modified
                        current_commit.files_modified.append(file_path)
                    
                    self.stats.maze_changes_detected += 1
            
            # Don't forget the last commit!
            if current_commit:
                commits.append(current_commit)
            
            self.logger.info(f"👻 Extracted {len(commits)} ghost movements")
            return commits
            
        except subprocess.CalledProcessError as e:
            raise GitError(f"Git command failed: {e}")

    def _analyze_ghost_profiles(self, commits: List[CommitInfo]) -> List[DeveloperInfo]:
        """👻 Analyze individual ghost behavior patterns!"""
        ghost_data: Dict[str, Dict] = {}
        
        for commit in commits:
            ghost_key = f"{commit.author_name}<{commit.author_email}>"
            
            if ghost_key not in ghost_data:
                ghost_data[ghost_key] = {
                    'name': commit.author_name,
                    'email': commit.author_email,
                    'commits': [],
                    'files_touched': set(),
                    'directories': set(),
                    'commit_hours': [],
                    'commit_days': [],
                    'first_commit': commit.commit_date,
                    'last_commit': commit.commit_date
                }
            
            ghost_info = ghost_data[ghost_key]
            ghost_info['commits'].append(commit)
            
            # Track file and directory patterns
            all_changed_files = commit.files_added + commit.files_modified + commit.files_deleted
            for file_path in all_changed_files:
                ghost_info['files_touched'].add(file_path)
                
                # Extract directory
                if '/' in file_path:
                    directory = '/'.join(file_path.split('/')[:-1])
                    ghost_info['directories'].add(directory)
            
            # Track temporal patterns
            ghost_info['commit_hours'].append(commit.commit_date.hour)
            ghost_info['commit_days'].append(commit.commit_date.weekday())
            
            # Update time range
            if commit.commit_date < ghost_info['first_commit']:
                ghost_info['first_commit'] = commit.commit_date
            if commit.commit_date > ghost_info['last_commit']:
                ghost_info['last_commit'] = commit.commit_date
        
        # Convert to DeveloperInfo objects
        developers = []
        for ghost_key, data in ghost_data.items():
            # Classify ghost type based on behavior
            ghost_type = self._classify_ghost_type(data)
            activity_pattern = self._classify_activity_pattern(data)
            
            developer = DeveloperInfo(
                name=data['name'],
                email=data['email'],
                total_commits=len(data['commits']),
                files_touched=data['files_touched'],  # Pass the set, not its length
                favorite_directories=list(data['directories'])[:5],  # Top 5
                ghost_type=ghost_type,
                activity_pattern=activity_pattern,
                first_commit=data['first_commit'],
                last_commit=data['last_commit'],
                commit_frequency=self._calculate_commit_frequency(data['commits']),
                expertise_areas=self._identify_expertise_areas(data['files_touched'])
            )
            
            developers.append(developer)
            self.stats.ghosts_tracked += 1
        
        return developers

    def _detect_movement_patterns(self, commits: List[CommitInfo]) -> ChangePatterns:
        """👻 Detect co-change patterns - which maze areas change together!"""
        
        # Track files that change together
        co_change_pairs: Dict[Tuple[str, str], int] = {}
        file_change_frequency: Dict[str, int] = {}
        
        for commit in commits:
            changed_files = commit.files_added + commit.files_modified + commit.files_deleted
            
            # Count individual file changes
            for file_path in changed_files:
                file_change_frequency[file_path] = file_change_frequency.get(file_path, 0) + 1
            
            # Count co-changes (files that change together)
            for i, file1 in enumerate(changed_files):
                for file2 in changed_files[i+1:]:
                    pair = tuple(sorted([file1, file2]))
                    co_change_pairs[pair] = co_change_pairs.get(pair, 0) + 1
        
        # Find significant co-change patterns
        significant_patterns = []
        for (file1, file2), count in co_change_pairs.items():
            if count >= 3:  # Changed together at least 3 times
                significance = count / min(
                    file_change_frequency[file1], 
                    file_change_frequency[file2]
                )
                
                if significance > 0.3:  # 30% of changes are together
                    significant_patterns.append({
                        'files': [file1, file2],
                        'co_change_count': count,
                        'significance': significance
                    })
                    self.stats.bonus_patterns_found += 1
        
        # Sort by significance
        significant_patterns.sort(key=lambda x: x['significance'], reverse=True)
        
        return ChangePatterns(
            co_change_pairs=significant_patterns[:20],  # Top 20 patterns
            file_change_frequency=dict(sorted(
                file_change_frequency.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:50]),  # Top 50 most changed files
            temporal_patterns=self._analyze_temporal_patterns(commits)
        )

    def _analyze_branch_patterns(self) -> List[Dict[str, Any]]:
        """👻 Analyze ghost movements across different maze levels (branches)!"""
        try:
            # Get all branches
            result = subprocess.run(
                ["git", "branch", "-a"], 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            branches = []
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('  ->'):
                    branch_name = line.strip().lstrip('* ').replace('remotes/origin/', '')
                    if branch_name not in ['HEAD', '']:
                        branches.append({
                            'name': branch_name,
                            'is_current': line.startswith('*'),
                            'is_remote': 'remotes/' in line
                        })
            
            return branches
            
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"👻 Could not analyze branches: {e}")
            return []

    def _analyze_tag_patterns(self) -> List[Dict[str, Any]]:
        """👻 Analyze ghost checkpoint patterns (tags/releases)!"""
        try:
            # Get all tags with dates
            result = subprocess.run(
                ["git", "tag", "-l", "--sort=-version:refname"], 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            tags = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    tag_name = line.strip()
                    
                    # Get tag date
                    try:
                        date_result = subprocess.run(
                            ["git", "log", "-1", "--format=%at", tag_name],
                            cwd=self.repo_path,
                            capture_output=True,
                            text=True,
                            check=True
                        )
                        
                        timestamp = int(date_result.stdout.strip())
                        tag_date = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                        
                        tags.append({
                            'name': tag_name,
                            'date': tag_date,
                            'is_release': self._is_release_tag(tag_name)
                        })
                        
                    except (subprocess.CalledProcessError, ValueError):
                        # If we can't get the date, still include the tag
                        tags.append({
                            'name': tag_name,
                            'date': None,
                            'is_release': self._is_release_tag(tag_name)
                        })
            
            return tags
            
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"👻 Could not analyze tags: {e}")
            return []

    def _classify_ghost_movement(self, commit_message: str, author: str) -> str:
        """👻 Classify the type of ghost movement based on commit!"""
        message_lower = commit_message.lower()
        
        if any(word in message_lower for word in ['fix', 'bug', 'error', 'issue']):
            return "bug_hunter"  # 🐛 Bug hunting ghost
        elif any(word in message_lower for word in ['add', 'new', 'create', 'implement']):
            return "builder"  # 🏗️ Building ghost
        elif any(word in message_lower for word in ['refactor', 'clean', 'improve', 'optimize']):
            return "optimizer"  # ⚡ Optimizing ghost
        elif any(word in message_lower for word in ['test', 'spec', 'coverage']):
            return "tester"  # 🧪 Testing ghost
        elif any(word in message_lower for word in ['doc', 'readme', 'comment']):
            return "documenter"  # 📚 Documentation ghost
        else:
            return "wanderer"  # 👻 General wandering ghost

    def _classify_ghost_type(self, ghost_data: Dict) -> str:
        """👻 Classify overall ghost behavior pattern!"""
        commit_count = len(ghost_data['commits'])
        files_touched = len(ghost_data['files_touched'])
        
        if commit_count > 100:
            return "speed_demon"  # Very active ghost
        elif files_touched > 50:
            return "maze_master"  # Touches many files
        elif commit_count > 20:
            return "power_pellet_collector"  # Regular contributor
        else:
            return "cautious_ghost"  # Occasional contributor (changed from casual_ghost)

    def _classify_activity_pattern(self, ghost_data: Dict) -> str:
        """👻 Classify when this ghost is most active!"""
        hours = ghost_data['commit_hours']
        days = ghost_data['commit_days']
        
        if not hours:
            return "workday_ghost"  # Default for unknown patterns
        
        # Analyze hour patterns
        morning_commits = sum(1 for h in hours if 6 <= h < 12)
        afternoon_commits = sum(1 for h in hours if 12 <= h < 18)
        evening_commits = sum(1 for h in hours if 18 <= h < 24)
        night_commits = sum(1 for h in hours if h < 6)
        
        max_time = max(morning_commits, afternoon_commits, evening_commits, night_commits)
        
        if max_time == morning_commits:
            return "morning_ghost"
        elif max_time == afternoon_commits:
            return "afternoon_spirit"  # Fixed enum value
        elif max_time == evening_commits:
            return "night_owl"  # Evening becomes night_owl
        else:
            return "midnight_hacker"  # Night commits become midnight_hacker

    def _calculate_commit_frequency(self, commits: List) -> float:
        """📊 Calculate commits per day for this ghost"""
        if len(commits) < 2:
            return 0.0
        
        first_commit = min(c.commit_date for c in commits)
        last_commit = max(c.commit_date for c in commits)
        days_active = (last_commit - first_commit).days + 1
        
        return len(commits) / days_active if days_active > 0 else 0.0

    def _identify_expertise_areas(self, files_touched: Set[str]) -> List[str]:
        """🎯 Identify ghost's areas of expertise based on files touched"""
        expertise = []
        
        # Count file types
        extensions = {}
        for file_path in files_touched:
            if '.' in file_path:
                ext = file_path.split('.')[-1].lower()
                extensions[ext] = extensions.get(ext, 0) + 1
        
        # Find primary languages/types
        sorted_exts = sorted(extensions.items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_exts[:3]:  # Top 3 extensions
            if ext == 'py':
                expertise.append('Python')
            elif ext == 'js':
                expertise.append('JavaScript')
            elif ext == 'ts':
                expertise.append('TypeScript')
            elif ext in ['md', 'rst', 'txt']:
                expertise.append('Documentation')
            elif ext in ['yml', 'yaml', 'json']:
                expertise.append('Configuration')
            else:
                expertise.append(ext.upper())
        
        return expertise

    def _analyze_temporal_patterns(self, commits: List[CommitInfo]) -> Dict[str, Any]:
        """⏰ Analyze when ghosts are most active in the maze"""
        if not commits:
            return {}
        
        # Group commits by hour and day
        hour_counts = {}
        day_counts = {}
        month_counts = {}
        
        for commit in commits:
            hour = commit.commit_date.hour
            day = commit.commit_date.weekday()  # 0=Monday
            month = commit.commit_date.month
            
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
            day_counts[day] = day_counts.get(day, 0) + 1
            month_counts[month] = month_counts.get(month, 0) + 1
        
        # Find peak times
        peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else 12
        peak_day = max(day_counts, key=day_counts.get) if day_counts else 0
        peak_month = max(month_counts, key=month_counts.get) if month_counts else 1
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        return {
            'peak_hour': peak_hour,
            'peak_day': day_names[peak_day],
            'peak_month': month_names[peak_month],
            'hourly_distribution': hour_counts,
            'daily_distribution': day_counts,
            'monthly_distribution': month_counts
        }

    def _is_release_tag(self, tag_name: str) -> bool:
        """Check if a tag looks like a release"""
        # Common release tag patterns
        release_patterns = [
            r'v?\d+\.\d+\.\d+',  # v1.2.3 or 1.2.3
            r'release-\d+',       # release-1
            r'r\d+\.\d+',        # r1.2
        ]
        
        for pattern in release_patterns:
            if re.match(pattern, tag_name.lower()):
                return True
        
        return False


class GitAnalyzer:
    """
    👻 PAC-MAN's Main Git Intelligence System! 👻
    
    The master ghost tracker that coordinates all ghost movement analysis!
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def analyze_repository(self, repo_path: Path, progress_callback: Optional[ProgressCallback] = None) -> GitIntelligence:
        """
        👻 ANALYZE ALL GHOST MOVEMENTS! 👻
        
        Complete git intelligence extraction for the repository!
        """
        try:
            validate_file_path(repo_path, repo_path.parent)
            
            self.logger.info(f"👻 Starting ghost intelligence analysis: {repo_path}")
            
            # Create ghost tracker
            tracker = GitGhostTracker(repo_path)
            
            # Track all movements
            intelligence = tracker.track_all_ghost_movements()
            
            self.logger.info(f"👻 Ghost intelligence complete! Found {len(intelligence.developers)} ghosts")
            
            return intelligence
            
        except Exception as e:
            raise GitError(f"Failed to analyze repository git intelligence: {e}")

    async def extract_commit_history(self, repo_path: Path) -> List[CommitInfo]:
        """Extract commit history with metadata"""
        tracker = GitGhostTracker(repo_path)
        return tracker._extract_all_commits()

    async def extract_developer_profiles(self, repo_path: Path) -> List[DeveloperInfo]:
        """Build developer profiles from commit history"""
        intelligence = await self.analyze_repository(repo_path)
        return intelligence.developers

    async def analyze_change_patterns(self, repo_path: Path) -> ChangePatterns:
        """Analyze which files/functions change together"""
        intelligence = await self.analyze_repository(repo_path)
        return intelligence.change_patterns


# 👻 PAC-MAN says: "WAKA WAKA! Let's track those ghosts!" 👻
def create_git_analyzer() -> GitAnalyzer:
    """Factory function to create PAC-MAN's git analyzer!"""
    return GitAnalyzer()
