"""
🔍 Simple PyPI to GitHub Repository Resolver (stdlib only)

Uses only Python standard library to resolve PyPI packages to GitHub repos.
No external dependencies required - perfect for the wild!
"""
import json
import re
from typing import Optional, Tuple
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from loguru import logger


class SimplePyPIResolver:
    """Resolves PyPI packages to GitHub repositories using only stdlib"""
    
    API_BASE_URL = "https://pypi.org/pypi"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def resolve_package(self, package_name: str) -> Optional[Tuple[str, str]]:
        """
        Resolve a PyPI package to its GitHub org/repo
        
        Args:
            package_name: Name of PyPI package (e.g., 'pandas', 'requests')
            
        Returns:
            Tuple of (org, repo) if found, None otherwise
        """
        try:
            # Fetch package metadata from PyPI JSON API
            url = f"{self.API_BASE_URL}/{package_name}/json"
            
            req = Request(url)
            req.add_header('User-Agent', 'repolex-dependency-resolver/1.0')
            
            with urlopen(req, timeout=self.timeout) as response:
                if response.status != 200:
                    logger.debug(f"⚠️  Package {package_name} not found on PyPI (status: {response.status})")
                    return None
                
                data = json.loads(response.read().decode('utf-8'))
            
            info = data.get('info', {})
            
            # Try multiple sources for GitHub URL
            github_url = self._extract_github_url(info)
            
            if github_url:
                org, repo = self._parse_github_url(github_url)
                if org and repo:
                    logger.debug(f"✅ Resolved {package_name} -> {org}/{repo}")
                    return (org, repo)
            
            logger.debug(f"❌ No GitHub repository found for {package_name}")
            return None
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to resolve {package_name}: {e}")
            return None
    
    def _extract_github_url(self, info: dict) -> Optional[str]:
        """Extract GitHub URL from PyPI package info"""
        
        # Check project_urls first (most reliable)
        project_urls = info.get('project_urls') or {}
        
        # Common keys used for source repositories
        repo_keys = [
            'Repository', 'Source', 'Source Code', 'GitHub', 'Git',
            'Homepage', 'Home', 'repository', 'source', 'github'
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
        return url and 'github.com' in url.lower()
    
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


def resolve_pypi_package(package_name: str) -> Optional[Tuple[str, str]]:
    """Convenience function to resolve a single package"""
    resolver = SimplePyPIResolver()
    return resolver.resolve_package(package_name)


if __name__ == "__main__":
    # Test the resolver
    resolver = SimplePyPIResolver()
    
    test_packages = ['pandas', 'requests', 'click', 'flask', 'numpy', 'django']
    
    print('🔍 Testing PyPI JSON API resolver (stdlib only):')
    for pkg in test_packages:
        result = resolver.resolve_package(pkg) 
        if result:
            org, repo = result
            print(f'  ✅ {pkg} -> {org}/{repo}')
        else:
            print(f'  ❌ {pkg} -> Not found')