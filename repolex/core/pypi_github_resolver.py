"""
🔍 Production PyPI to GitHub Repository Resolver

Self-contained resolver using PyPI's JSON API to map packages to GitHub repos.
Uses subprocess + curl for maximum compatibility in the wild.
"""
import json
import re
import subprocess
from typing import Optional, Tuple, Dict
from urllib.parse import urlparse
from loguru import logger


class PyPIGitHubResolver:
    """Resolves PyPI packages to GitHub repositories using PyPI's JSON API"""
    
    API_BASE_URL = "https://pypi.org/pypi"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._cache: Dict[str, Optional[Tuple[str, str]]] = {}
    
    def resolve_package(self, package_name: str) -> Optional[Tuple[str, str]]:
        """
        Resolve a PyPI package to its GitHub org/repo
        
        Args:
            package_name: Name of PyPI package (e.g., 'pandas', 'requests')
            
        Returns:
            Tuple of (org, repo) if found, None otherwise
        """
        # Check cache first
        if package_name in self._cache:
            return self._cache[package_name]
        
        try:
            # Fetch package metadata using curl (most reliable)
            url = f"{self.API_BASE_URL}/{package_name}/json"
            
            result = subprocess.run([
                'curl', '-s', '--max-time', str(self.timeout), 
                '--user-agent', 'repolex-dependency-resolver/1.0',
                url
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.debug(f"⚠️  Failed to fetch {package_name} from PyPI")
                self._cache[package_name] = None
                return None
            
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                logger.debug(f"⚠️  Invalid JSON response for {package_name}")
                self._cache[package_name] = None
                return None
            
            info = data.get('info', {})
            
            # Try multiple sources for GitHub URL
            github_url = self._extract_github_url(info)
            
            if github_url:
                org, repo = self._parse_github_url(github_url)
                if org and repo:
                    result = (org, repo)
                    logger.debug(f"✅ Resolved {package_name} -> {org}/{repo}")
                    self._cache[package_name] = result
                    return result
            
            logger.debug(f"❌ No GitHub repository found for {package_name}")
            self._cache[package_name] = None
            return None
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to resolve {package_name}: {e}")
            self._cache[package_name] = None
            return None
    
    def _extract_github_url(self, info: dict) -> Optional[str]:
        """Extract GitHub URL from PyPI package info"""
        
        # Check project_urls first (most reliable)
        project_urls = info.get('project_urls') or {}
        
        # Common keys used for source repositories (ordered by priority)
        repo_keys = [
            'Repository', 'Source', 'Source Code', 'GitHub', 'Git',
            'repository', 'source', 'github', 'code', 'Homepage', 'Home'
        ]
        
        for key in repo_keys:
            url = project_urls.get(key)
            if url and self._is_github_url(url):
                return url
        
        # Fallback to home_page
        home_page = info.get('home_page', '')
        if home_page and self._is_github_url(home_page):
            return home_page
        
        return None
    
    def _is_github_url(self, url: str) -> bool:
        """Check if URL is a GitHub repository URL"""
        if not url:
            return False
        return 'github.com' in url.lower() and not url.lower().endswith('.github.io')
    
    def _parse_github_url(self, github_url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse GitHub URL to extract org and repo names
        
        Examples:
            https://github.com/pandas-dev/pandas -> ('pandas-dev', 'pandas')
            https://github.com/pallets/click.git -> ('pallets', 'click')
        """
        try:
            # Clean up the URL
            url = github_url.strip().rstrip('/')
            
            # Remove .git suffix if present
            if url.endswith('.git'):
                url = url[:-4]
            
            # Parse URL
            parsed = urlparse(url)
            
            if parsed.netloc.lower() != 'github.com':
                return None, None
            
            # Extract path components
            path_parts = [p for p in parsed.path.split('/') if p]
            
            if len(path_parts) >= 2:
                org = path_parts[0]
                repo = path_parts[1]
                return org, repo
            
            return None, None
            
        except Exception as e:
            logger.debug(f"⚠️  Failed to parse GitHub URL {github_url}: {e}")
            return None, None
    
    def batch_resolve(self, package_names: list[str]) -> dict[str, Tuple[str, str]]:
        """
        Resolve multiple packages in batch
        
        Returns:
            Dict mapping package_name -> (org, repo) for successful resolutions
        """
        results = {}
        
        for package_name in package_names:
            result = self.resolve_package(package_name)
            if result:
                results[package_name] = result
        
        return results
    
    def get_resolution_stats(self, package_names: list[str]) -> dict:
        """Get statistics on resolution success"""
        resolved = {}
        failed = []
        
        for package_name in package_names:
            result = self.resolve_package(package_name)
            if result:
                resolved[package_name] = result
            else:
                failed.append(package_name)
        
        return {
            'resolved': resolved,
            'failed': failed,
            'success_rate': len(resolved) / len(package_names) if package_names else 0,
            'total': len(package_names)
        }


def resolve_pypi_package(package_name: str) -> Optional[Tuple[str, str]]:
    """Convenience function to resolve a single package"""
    resolver = PyPIGitHubResolver()
    return resolver.resolve_package(package_name)


if __name__ == "__main__":
    # Test the resolver
    resolver = PyPIGitHubResolver()
    
    test_packages = [
        'pandas', 'requests', 'click', 'flask', 'numpy', 'django',
        'pydantic', 'loguru', 'msgpack', 'lxml', 'psutil'
    ]
    
    print('🔍 Testing PyPI → GitHub resolver:')
    stats = resolver.get_resolution_stats(test_packages)
    
    for pkg, (org, repo) in stats['resolved'].items():
        print(f'  ✅ {pkg} -> {org}/{repo}')
    
    for pkg in stats['failed']:
        print(f'  ❌ {pkg} -> Not found')
    
    print(f'\n📊 Success rate: {stats["success_rate"]:.1%} ({len(stats["resolved"])}/{stats["total"]})')