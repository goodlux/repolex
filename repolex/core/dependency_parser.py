"""
🔍 Dependency Discovery Engine
Parses Python project files to extract dependencies with versions
"""
import re
import tomllib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from loguru import logger


@dataclass
class Dependency:
    """Represents a project dependency"""
    name: str
    version: Optional[str] = None
    org: Optional[str] = None
    repo: Optional[str] = None
    source: str = "pypi"  # pypi, github, etc.
    
    @property
    def org_repo(self) -> Optional[str]:
        """Get org/repo format for GitHub dependencies"""
        if self.org and self.repo:
            return f"{self.org}/{self.repo}"
        return None
    
    @property
    def semantic_name(self) -> str:
        """Get name for semantic DNA files"""
        if self.org_repo:
            return self.org_repo.replace("/", "~")
        return self.name.replace("-", "~")


class DependencyParser:
    """Parses various Python dependency files"""
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        
    def discover_dependencies(self) -> List[Dependency]:
        """🔍 Main discovery method - tries all known formats"""
        dependencies = []
        
        # Try pyproject.toml first (modern standard)
        pyproject_deps = self._parse_pyproject_toml()
        if pyproject_deps:
            logger.info(f"📦 Found {len(pyproject_deps)} dependencies in pyproject.toml")
            dependencies.extend(pyproject_deps)
            
        # Fallback to requirements.txt
        if not dependencies:
            requirements_deps = self._parse_requirements_txt()
            if requirements_deps:
                logger.info(f"📦 Found {len(requirements_deps)} dependencies in requirements.txt")
                dependencies.extend(requirements_deps)
        
        # Try setup.py as last resort
        if not dependencies:
            setup_deps = self._parse_setup_py()
            if setup_deps:
                logger.info(f"📦 Found {len(setup_deps)} dependencies in setup.py")
                dependencies.extend(setup_deps)
        
        # Deduplicate and resolve GitHub mappings
        return self._resolve_dependencies(dependencies)
    
    def _parse_pyproject_toml(self) -> List[Dependency]:
        """Parse pyproject.toml for dependencies"""
        pyproject_path = self.project_path / "pyproject.toml"
        if not pyproject_path.exists():
            return []
            
        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
            
            dependencies = []
            
            # Poetry format
            if "tool" in data and "poetry" in data["tool"]:
                poetry_deps = data["tool"]["poetry"].get("dependencies", {})
                for name, version_spec in poetry_deps.items():
                    if name == "python":  # Skip Python version
                        continue
                    dependencies.append(self._create_dependency(name, version_spec))
            
            # PEP 621 format (setuptools, etc.)
            if "project" in data:
                project_deps = data["project"].get("dependencies", [])
                for dep_str in project_deps:
                    dep = self._parse_requirement_string(dep_str)
                    if dep:
                        dependencies.append(dep)
            
            return dependencies
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to parse pyproject.toml: {e}")
            return []
    
    def _parse_requirements_txt(self) -> List[Dependency]:
        """Parse requirements.txt file"""
        req_path = self.project_path / "requirements.txt"
        if not req_path.exists():
            return []
            
        try:
            dependencies = []
            with open(req_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        dep = self._parse_requirement_string(line)
                        if dep:
                            dependencies.append(dep)
            return dependencies
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to parse requirements.txt: {e}")
            return []
    
    def _parse_setup_py(self) -> List[Dependency]:
        """Basic setup.py parsing (limited, best effort)"""
        setup_path = self.project_path / "setup.py"
        if not setup_path.exists():
            return []
            
        try:
            # Very basic regex parsing - not perfect but better than nothing
            with open(setup_path, "r") as f:
                content = f.read()
            
            # Look for install_requires list
            install_requires_match = re.search(
                r'install_requires\s*=\s*\[(.*?)\]', 
                content, 
                re.DOTALL
            )
            
            if not install_requires_match:
                return []
            
            dependencies = []
            requires_str = install_requires_match.group(1)
            
            # Extract quoted strings
            for match in re.finditer(r'["\']([^"\']+)["\']', requires_str):
                dep_str = match.group(1)
                dep = self._parse_requirement_string(dep_str)
                if dep:
                    dependencies.append(dep)
            
            return dependencies
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to parse setup.py: {e}")
            return []
    
    def _parse_requirement_string(self, req_str: str) -> Optional[Dependency]:
        """Parse a requirement string like 'pandas>=1.0.0'"""
        req_str = req_str.strip()
        if not req_str or req_str.startswith("-"):
            return None
        
        # Handle git URLs
        if req_str.startswith("git+"):
            return self._parse_git_dependency(req_str)
        
        # Standard PyPI dependency
        # Match: name[extras]>=version
        match = re.match(r'^([a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]?)(?:\[.*?\])?\s*([><=!~]*)\s*([0-9][0-9a-zA-Z._-]*)?', req_str)
        if match:
            name = match.group(1)
            operator = match.group(2) or ""
            version = match.group(3)
            
            # For now, just take the version without the operator
            clean_version = version if version else None
            
            return Dependency(name=name, version=clean_version, source="pypi")
        
        return None
    
    def _parse_git_dependency(self, git_url: str) -> Optional[Dependency]:
        """Parse git+https://github.com/org/repo.git dependencies"""
        # Extract GitHub org/repo from git URL
        github_match = re.search(r'github\.com/([^/]+)/([^/.]+)', git_url)
        if github_match:
            org = github_match.group(1)
            repo = github_match.group(2)
            
            # Extract version/tag if present
            version = None
            if "@" in git_url:
                version = git_url.split("@")[-1]
            
            return Dependency(
                name=repo,
                version=version,
                org=org,
                repo=repo,
                source="github"
            )
        
        return None
    
    def _create_dependency(self, name: str, version_spec) -> Dependency:
        """Create dependency from name and version spec (handles poetry format)"""
        if isinstance(version_spec, str):
            # Simple version string
            version = version_spec.lstrip("^~>=<!")
            return Dependency(name=name, version=version, source="pypi")
        elif isinstance(version_spec, dict):
            # Complex dependency (poetry format)
            version = version_spec.get("version", "").lstrip("^~>=<!")
            git_url = version_spec.get("git")
            
            if git_url:
                return self._parse_git_dependency(git_url) or Dependency(name=name)
            else:
                return Dependency(name=name, version=version, source="pypi")
        
        return Dependency(name=name)
    
    def _resolve_dependencies(self, dependencies: List[Dependency]) -> List[Dependency]:
        """Resolve PyPI names to GitHub repos where possible"""
        # Import the PyPI resolver
        try:
            from .pypi_github_resolver import PyPIGitHubResolver
            resolver = PyPIGitHubResolver()
            use_api_resolver = True
        except Exception as e:
            logger.warning(f"⚠️  PyPI API resolver unavailable, using fallback mappings: {e}")
            use_api_resolver = False
        
        # Fallback hardcoded mappings for when API is unavailable
        PYPI_TO_GITHUB = {
            # Data & Analytics
            "pandas": ("pandas-dev", "pandas"),
            "numpy": ("numpy", "numpy"),
            "scipy": ("scipy", "scipy"),
            "matplotlib": ("matplotlib", "matplotlib"),
            "scikit-learn": ("scikit-learn", "scikit-learn"),
            "seaborn": ("mwaskom", "seaborn"),
            "plotly": ("plotly", "plotly.py"),
            
            # Web Frameworks
            "requests": ("psf", "requests"),
            "flask": ("pallets", "flask"),
            "django": ("django", "django"),
            "fastapi": ("tiangolo", "fastapi"),
            "tornado": ("tornadoweb", "tornado"),
            "aiohttp": ("aio-libs", "aiohttp"),
            
            # CLI & Utilities
            "click": ("pallets", "click"),
            "rich": ("Textualize", "rich"),
            "typer": ("tiangolo", "typer"),
            "pydantic": ("pydantic", "pydantic"),
            "loguru": ("Delgan", "loguru"),
            
            # Development Tools
            "pytest": ("pytest-dev", "pytest"),
            "black": ("psf", "black"),
            "flake8": ("PyCQA", "flake8"),
            "mypy": ("python", "mypy"),
            "pre-commit": ("pre-commit", "pre-commit"),
            
            # Database & ORM
            "sqlalchemy": ("sqlalchemy", "sqlalchemy"),
            "alembic": ("sqlalchemy", "alembic"),
            "django-rest-framework": ("encode", "django-rest-framework"),
            
            # Async & Concurrency
            "asyncio": ("python", "cpython"),  # Part of stdlib but sometimes listed
            "celery": ("celery", "celery"),
            "redis": ("redis", "redis-py"),
            
            # ML & AI
            "transformers": ("huggingface", "transformers"),
            "torch": ("pytorch", "pytorch"),
            "tensorflow": ("tensorflow", "tensorflow"),
            "openai": ("openai", "openai-python"),
            
            # File Processing
            "lxml": ("lxml", "lxml"),
            "beautifulsoup4": ("waylan", "beautifulsoup"),
            "pillow": ("python-pillow", "Pillow"),
            "openpyxl": ("openpyxl", "openpyxl"),
            
            # System & Process
            "psutil": ("giampaolo", "psutil"),
            "docker": ("docker", "docker-py"),
            "kubernetes": ("kubernetes-client", "python"),
            
            # Git & Version Control
            "gitpython": ("gitpython-developers", "GitPython"),
            "GitPython": ("gitpython-developers", "GitPython"),  # Handle case variations
            
            # Serialization & Data
            "msgpack": ("msgpack", "msgpack-python"),
            "pyyaml": ("yaml", "pyyaml"),
            "toml": ("uiri", "toml"),
            "jsonschema": ("python-jsonschema", "jsonschema"),
            
            # RDF & Semantic
            "pyoxigraph": ("oxigraph", "oxigraph"),
            
            # NLP & ML
            "gliner": ("urchade", "GLiNER"),
            
            # Network & HTTP
            "urllib3": ("urllib3", "urllib3"),
            "httpx": ("encode", "httpx"),
            "websockets": ("python-websockets", "websockets"),
            
            # Date & Time
            "arrow": ("arrow-py", "arrow"),
            "pendulum": ("sdispater", "pendulum"),
            "python-dateutil": ("dateutil", "dateutil"),
            
            # Configuration & Environment
            "python-dotenv": ("theskumar", "python-dotenv"),
            "configparser": ("python", "cpython"),  # stdlib
            
            # Testing & Mocking
            "mock": ("testing-cabal", "mock"),
            "faker": ("joke2k", "faker"),
            "factory-boy": ("FactoryBoy", "factory_boy"),
            
            # Caching & Performance
            "redis": ("redis", "redis-py"),
            "memcached": ("linsomniac", "python-memcached"),
            
            # Crypto & Security
            "cryptography": ("pyca", "cryptography"),
            "bcrypt": ("pyca", "bcrypt"),
            "passlib": ("assylias", "passlib"),
        }
        
        resolved = []
        seen = set()
        
        for dep in dependencies:
            # Skip duplicates
            key = (dep.name, dep.version)
            if key in seen:
                continue
            seen.add(key)
            
            # Try to resolve PyPI packages to GitHub
            if dep.source == "pypi":
                org, repo = None, None
                
                # First try API resolver if available
                if use_api_resolver:
                    try:
                        result = resolver.resolve_package(dep.name)
                        if result:
                            org, repo = result
                            logger.debug(f"🔍 API resolved {dep.name} -> {org}/{repo}")
                    except Exception as e:
                        logger.debug(f"⚠️  API resolution failed for {dep.name}: {e}")
                
                # Fallback to hardcoded mappings
                if not org and not repo and dep.name in PYPI_TO_GITHUB:
                    org, repo = PYPI_TO_GITHUB[dep.name]
                    logger.debug(f"📋 Fallback resolved {dep.name} -> {org}/{repo}")
                
                # Update dependency if resolved
                if org and repo:
                    dep.org = org
                    dep.repo = repo
                    dep.source = "github"
            
            resolved.append(dep)
        
        return resolved


def discover_project_dependencies(project_path: str = ".") -> List[Dependency]:
    """🔍 Convenience function to discover dependencies"""
    parser = DependencyParser(Path(project_path))
    return parser.discover_dependencies()