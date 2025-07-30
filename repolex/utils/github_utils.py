"""🟡 PAC-MAN GitHub Integration Powerhouse

The ultimate GitHub integration system with PAC-MAN-level intelligence and ghost-busting power!
PAC-MAN navigates GitHub repositories, generates perfect links, and handles authentication like a pro!
"""

import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union
from urllib.parse import quote, urljoin
import json
from datetime import datetime, timedelta

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from repolex.models.exceptions import GitError, SecurityError, ValidationError, NetworkError, RepolexError
from repolex.utils.validation import validate_org_repo


class GitHubError(RepolexError):
    """🟡 PAC-MAN GitHub operation error."""
    pass


class GitHubRateLimitError(GitHubError):
    """🟡 PAC-MAN GitHub rate limit error."""
    pass


class GitHubAuthenticationError(GitHubError):
    """🟡 PAC-MAN GitHub authentication error."""
    pass


class GitHubLinkGenerator:
    """🟡 PAC-MAN's GitHub Link Generation Powerhouse!"""
    
    def __init__(self, org: str, repo: str, base_url: str = "https://github.com"):
        """
        Initialize GitHub link generator.
        
        Args:
            org: Organization/username
            repo: Repository name
            base_url: Base GitHub URL (for GitHub Enterprise)
        """
        self.org = self._sanitize_component(org)
        self.repo = self._sanitize_component(repo)
        self.base_url = base_url.rstrip('/')
        
        # Validate org/repo format
        validate_org_repo(f"{self.org}/{self.repo}")
    
    def _sanitize_component(self, component: str) -> str:
        """Sanitize GitHub org/repo component."""
        if not component or not isinstance(component, str):
            raise ValidationError(
                "GitHub org/repo component must be non-empty string",
                suggestions=["Provide valid org and repo names"]
            )
        
        # GitHub allows alphanumeric, hyphens, dots, underscores
        if not re.match(r'^[a-zA-Z0-9._-]+$', component):
            raise ValidationError(
                f"Invalid GitHub component: {component}",
                suggestions=["Use alphanumeric characters, hyphens, dots, underscores only"]
            )
        
        return component
    
    def repository_url(self) -> str:
        """🟡 Generate repository main page URL."""
        return f"{self.base_url}/{self.org}/{self.repo}"
    
    def file_url(self, file_path: str, ref: str = "main", line: Optional[int] = None, 
                end_line: Optional[int] = None) -> str:
        """
        🟡 Generate file URL with optional line highlighting - PAC-MAN's file linker!
        
        Args:
            file_path: Path to file within repository
            ref: Branch, tag, or commit hash
            line: Start line number for highlighting
            end_line: End line number for range highlighting
            
        Returns:
            str: GitHub file URL
        """
        # Sanitize file path
        file_path = file_path.lstrip('/')
        if not file_path:
            raise ValidationError(
                "File path cannot be empty",
                suggestions=["Provide a valid file path"]
            )
        
        # URL encode path components
        path_parts = [quote(part, safe='') for part in file_path.split('/')]
        encoded_path = '/'.join(path_parts)
        
        # Build URL
        url = f"{self.base_url}/{self.org}/{self.repo}/blob/{quote(ref, safe='')}/{encoded_path}"
        
        # Add line highlighting
        if line is not None:
            if end_line is not None and end_line > line:
                url += f"#L{line}-L{end_line}"
            else:
                url += f"#L{line}"
        
        return url
    
    def function_url(self, file_path: str, function_name: str, ref: str = "main", 
                    line: Optional[int] = None) -> str:
        """
        🟡 Generate function URL - PAC-MAN's function navigator!
        
        Args:
            file_path: Path to file containing function
            function_name: Name of the function
            ref: Branch, tag, or commit hash
            line: Line number where function is defined
            
        Returns:
            str: GitHub function URL with line highlighting
        """
        return self.file_url(file_path, ref, line)
    
    def commit_url(self, commit_hash: str) -> str:
        """🟡 Generate commit URL - PAC-MAN's commit tracker!"""
        return f"{self.base_url}/{self.org}/{self.repo}/commit/{commit_hash}"
    
    def tree_url(self, ref: str = "main", path: str = "") -> str:
        """🟡 Generate tree/directory URL - PAC-MAN's directory explorer!"""
        url = f"{self.base_url}/{self.org}/{self.repo}/tree/{quote(ref, safe='')}"
        if path:
            path = path.lstrip('/')
            path_parts = [quote(part, safe='') for part in path.split('/')]
            encoded_path = '/'.join(path_parts)
            url += f"/{encoded_path}"
        return url
    
    def releases_url(self) -> str:
        """🟡 Generate releases page URL - PAC-MAN's release tracker!"""
        return f"{self.base_url}/{self.org}/{self.repo}/releases"
    
    def release_url(self, tag: str) -> str:
        """🟡 Generate specific release URL - PAC-MAN's version navigator!"""
        return f"{self.base_url}/{self.org}/{self.repo}/releases/tag/{quote(tag, safe='')}"
    
    def issues_url(self) -> str:
        """🟡 Generate issues page URL."""
        return f"{self.base_url}/{self.org}/{self.repo}/issues"
    
    def pull_requests_url(self) -> str:
        """🟡 Generate pull requests page URL."""
        return f"{self.base_url}/{self.org}/{self.repo}/pulls"
    
    def archive_url(self, ref: str, format: str = "zip") -> str:
        """
        🟡 Generate archive download URL - PAC-MAN's archive chomper!
        
        Args:
            ref: Branch, tag, or commit hash
            format: Archive format ('zip' or 'tar.gz')
        """
        if format not in ('zip', 'tar.gz'):
            raise ValidationError(
                f"Unsupported archive format: {format}",
                suggestions=["Use 'zip' or 'tar.gz'"]
            )
        
        if format == 'tar.gz':
            format = 'tarball'
        else:
            format = 'zipball'
        
        return f"{self.base_url}/{self.org}/{self.repo}/archive/{format}/{quote(ref, safe='')}"
    
    def raw_file_url(self, file_path: str, ref: str = "main") -> str:
        """
        🟡 Generate raw file URL - PAC-MAN's raw content getter!
        
        Args:
            file_path: Path to file within repository
            ref: Branch, tag, or commit hash
            
        Returns:
            str: GitHub raw file URL
        """
        # Use raw.githubusercontent.com for raw files
        file_path = file_path.lstrip('/')
        path_parts = [quote(part, safe='') for part in file_path.split('/')]
        encoded_path = '/'.join(path_parts)
        
        return f"https://raw.githubusercontent.com/{self.org}/{self.repo}/{quote(ref, safe='')}/{encoded_path}"
    
    def api_url(self, endpoint: str = "") -> str:
        """🟡 Generate GitHub API URL - PAC-MAN's API navigator!"""
        base_api = "https://api.github.com"
        repo_path = f"repos/{self.org}/{self.repo}"
        
        if endpoint:
            endpoint = endpoint.lstrip('/')
            return f"{base_api}/{repo_path}/{endpoint}"
        else:
            return f"{base_api}/{repo_path}"
    
    def clone_url(self, use_ssh: bool = False) -> str:
        """🟡 Generate clone URL - PAC-MAN's clone helper!"""
        if use_ssh:
            return f"git@github.com:{self.org}/{self.repo}.git"
        else:
            return f"https://github.com/{self.org}/{self.repo}.git"


class GitHubRateLimiter:
    """🟡 PAC-MAN's Rate Limit Guardian!"""
    
    def __init__(self, requests_per_hour: int = 5000):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_hour: Maximum requests per hour
        """
        self.requests_per_hour = requests_per_hour
        self.request_times: List[datetime] = []
        self.reset_time: Optional[datetime] = None
        self.remaining_requests: Optional[int] = None
    
    def can_make_request(self) -> bool:
        """Check if we can make a request without hitting rate limit."""
        now = datetime.now()
        
        # Clean old requests (older than 1 hour)
        cutoff = now - timedelta(hours=1)
        self.request_times = [t for t in self.request_times if t > cutoff]
        
        # Check if we're under the limit
        return len(self.request_times) < self.requests_per_hour
    
    def record_request(self, headers: Optional[Dict[str, str]] = None) -> None:
        """Record a request and update rate limit info from headers."""
        self.request_times.append(datetime.now())
        
        if headers:
            # Update from GitHub rate limit headers
            remaining = headers.get('X-RateLimit-Remaining')
            reset = headers.get('X-RateLimit-Reset')
            
            if remaining:
                self.remaining_requests = int(remaining)
            
            if reset:
                self.reset_time = datetime.fromtimestamp(int(reset))
    
    def time_until_reset(self) -> Optional[timedelta]:
        """Get time until rate limit reset."""
        if self.reset_time:
            now = datetime.now()
            if self.reset_time > now:
                return self.reset_time - now
        return None
    
    def wait_if_needed(self) -> None:
        """Wait if we're hitting rate limits."""
        if not self.can_make_request():
            wait_time = self.time_until_reset()
            if wait_time and wait_time.total_seconds() > 0:
                # Don't actually wait in this implementation, just raise error
                raise GitHubRateLimitError(
                    f"🟡 PAC-MAN hit GitHub rate limit!",
                    suggestions=[
                        f"Rate limit resets in {wait_time}",
                        "Wait before making more requests",
                        "Configure authentication for higher limits"
                    ]
                )


class GitHubAPIClient:
    """🟡 PAC-MAN's GitHub API Client Powerhouse!"""
    
    def __init__(self, token: Optional[str] = None, rate_limiter: Optional[GitHubRateLimiter] = None):
        """
        Initialize GitHub API client.
        
        Args:
            token: GitHub personal access token
            rate_limiter: Rate limiter instance
        """
        if not REQUESTS_AVAILABLE:
            raise GitHubError(
                "🟡 Requests library not available",
                suggestions=["Install requests: pip install requests"]
            )
        
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.rate_limiter = rate_limiter or GitHubRateLimiter()
        self.session = requests.Session()
        
        # Set up authentication
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        
        # Set user agent
        self.session.headers.update({
            'User-Agent': 'repolex-PAC-MAN/1.0 (https://github.com/goodlux/repolex)'
        })
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make authenticated GitHub API request with rate limiting."""
        # Check rate limit
        self.rate_limiter.wait_if_needed()
        
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            
            # Record request for rate limiting
            self.rate_limiter.record_request(response.headers)
            
            # Handle rate limit
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                raise GitHubRateLimitError(
                    "🟡 PAC-MAN hit GitHub rate limit!",
                    suggestions=[
                        "Wait before making more requests",
                        "Configure authentication for higher limits",
                        f"Rate limit info: {response.headers.get('X-RateLimit-Remaining', 'unknown')} remaining"
                    ]
                )
            
            # Handle authentication errors
            elif response.status_code == 401:
                raise GitHubAuthenticationError(
                    "🟡 GitHub authentication failed!",
                    suggestions=[
                        "Check your GitHub token is valid",
                        "Set GITHUB_TOKEN environment variable",
                        "Ensure token has required permissions"
                    ]
                )
            
            # Handle other errors
            elif not response.ok:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise GitHubError(
                    f"🟡 GitHub API error: {response.status_code}",
                    suggestions=[
                        f"Error message: {error_data.get('message', 'Unknown error')}",
                        "Check repository exists and is accessible",
                        "Verify your authentication and permissions"
                    ]
                )
            
            return response
            
        except requests.RequestException as e:
            raise NetworkError(
                f"🟡 PAC-MAN couldn't connect to GitHub API",
                suggestions=[
                    "Check internet connectivity",
                    "Verify GitHub API is accessible",
                    f"Original error: {e}"
                ]
            ) from e
    
    def get_repository_info(self, org: str, repo: str) -> Dict[str, Any]:
        """Get repository information from GitHub API."""
        url = f"https://api.github.com/repos/{org}/{repo}"
        response = self._make_request('GET', url)
        return response.json()
    
    def get_releases(self, org: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository releases from GitHub API."""
        url = f"https://api.github.com/repos/{org}/{repo}/releases"
        response = self._make_request('GET', url)
        return response.json()
    
    def get_tags(self, org: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository tags from GitHub API."""
        url = f"https://api.github.com/repos/{org}/{repo}/tags"
        response = self._make_request('GET', url)
        return response.json()
    
    def get_branches(self, org: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository branches from GitHub API."""
        url = f"https://api.github.com/repos/{org}/{repo}/branches"
        response = self._make_request('GET', url)
        return response.json()
    
    def check_repository_access(self, org: str, repo: str) -> bool:
        """Check if repository is accessible."""
        try:
            self.get_repository_info(org, repo)
            return True
        except (GitHubError, NetworkError):
            return False


def create_github_link_generator(org: str, repo: str, base_url: str = "https://github.com") -> GitHubLinkGenerator:
    """🟡 Create GitHub link generator - PAC-MAN's link factory!"""
    return GitHubLinkGenerator(org, repo, base_url)


def generate_file_link(org: str, repo: str, file_path: str, ref: str = "main", 
                      line: Optional[int] = None, end_line: Optional[int] = None) -> str:
    """🟡 Quick file link generation - PAC-MAN's express linker!"""
    generator = GitHubLinkGenerator(org, repo)
    return generator.file_url(file_path, ref, line, end_line)


def generate_function_link(org: str, repo: str, file_path: str, function_name: str, 
                          ref: str = "main", line: Optional[int] = None) -> str:
    """🟡 Quick function link generation - PAC-MAN's function finder!"""
    generator = GitHubLinkGenerator(org, repo)
    return generator.function_url(file_path, function_name, ref, line)


def parse_github_url(url: str) -> Optional[Dict[str, str]]:
    """
    🟡 Parse GitHub URL into components - PAC-MAN's URL parser!
    
    Args:
        url: GitHub URL to parse
        
    Returns:
        Optional[Dict[str, str]]: Parsed components or None if not a GitHub URL
    """
    patterns = [
        # https://github.com/org/repo
        r'https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
        # https://github.com/org/repo/blob/ref/path#L123
        r'https?://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+?)(?:#L(\d+)(?:-L(\d+))?)?$',
        # https://github.com/org/repo/tree/ref/path
        r'https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)$',
        # https://github.com/org/repo/tree/ref
        r'https?://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/?$',
        # git@github.com:org/repo.git
        r'git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            groups = match.groups()
            result = {
                'org': groups[0],
                'repo': groups[1].rstrip('.git')
            }
            
            if len(groups) > 2 and groups[2]:
                result['ref'] = groups[2]
            if len(groups) > 3 and groups[3]:
                result['path'] = groups[3]
            if len(groups) > 4 and groups[4]:
                result['line'] = int(groups[4])
            if len(groups) > 5 and groups[5]:
                result['end_line'] = int(groups[5])
                
            return result
    
    return None


def extract_org_repo_from_url(url: str) -> Tuple[str, str]:
    """
    🟡 Extract org/repo from GitHub URL - PAC-MAN's extractor!
    
    Args:
        url: GitHub URL
        
    Returns:
        Tuple[str, str]: Organization and repository names
        
    Raises:
        ValidationError: If URL is not a valid GitHub URL
    """
    parsed = parse_github_url(url)
    if not parsed:
        raise ValidationError(
            f"Invalid GitHub URL: {url}",
            suggestions=["Provide a valid GitHub repository URL"]
        )
    
    return parsed['org'], parsed['repo']


def is_github_url(url: str) -> bool:
    """🟡 Check if URL is a GitHub URL - PAC-MAN's URL detector!"""
    return parse_github_url(url) is not None


def get_github_token() -> Optional[str]:
    """🟡 Get GitHub token from environment - PAC-MAN's token finder!"""
    return os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')


def validate_github_token(token: str) -> bool:
    """
    🟡 Validate GitHub token - PAC-MAN's token validator!
    
    Args:
        token: GitHub personal access token
        
    Returns:
        bool: True if token is valid
    """
    if not REQUESTS_AVAILABLE:
        return False
    
    try:
        client = GitHubAPIClient(token)
        response = client._make_request('GET', 'https://api.github.com/user')
        return response.ok
    except:
        return False


# PAC-MAN convenience functions
def pac_man_generate_link(org: str, repo: str, file_path: str, line: Optional[int] = None) -> str:
    """🟡 PAC-MAN's express link generator!"""
    return generate_file_link(org, repo, file_path, line=line)


def pac_man_parse_url(url: str) -> Optional[Dict[str, str]]:
    """🟡 PAC-MAN's URL parsing power!"""
    return parse_github_url(url)


def pac_man_create_api_client(token: Optional[str] = None) -> GitHubAPIClient:
    """🟡 PAC-MAN's API client factory!"""
    return GitHubAPIClient(token or get_github_token())


def pac_man_check_repo_access(org: str, repo: str) -> bool:
    """🟡 PAC-MAN's repository access checker!"""
    try:
        client = pac_man_create_api_client()
        return client.check_repository_access(org, repo)
    except:
        return False


def pac_man_get_clone_url(org: str, repo: str, use_ssh: bool = False) -> str:
    """🟡 PAC-MAN's clone URL generator!"""
    generator = GitHubLinkGenerator(org, repo)
    return generator.clone_url(use_ssh)


# GitHub URL templates for different contexts
GITHUB_TEMPLATES = {
    'file': 'https://github.com/{org}/{repo}/blob/{ref}/{path}#{line_anchor}',
    'function': 'https://github.com/{org}/{repo}/blob/{ref}/{path}#{line_anchor}',
    'commit': 'https://github.com/{org}/{repo}/commit/{commit}',
    'tree': 'https://github.com/{org}/{repo}/tree/{ref}/{path}',
    'releases': 'https://github.com/{org}/{repo}/releases',
    'release': 'https://github.com/{org}/{repo}/releases/tag/{tag}',
    'raw': 'https://raw.githubusercontent.com/{org}/{repo}/{ref}/{path}',
    'clone_https': 'https://github.com/{org}/{repo}.git',
    'clone_ssh': 'git@github.com:{org}/{repo}.git'
}