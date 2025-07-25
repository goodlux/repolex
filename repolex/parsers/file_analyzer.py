"""
🍎 PAC-MAN's Bonus File Mapper 🍎

This is where PAC-MAN discovers bonus items (special files) throughout the maze!
Every file becomes a mapped location with GitHub treasure coordinates!

WAKA WAKA! Finding bonus treasures in the file system maze!
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass
import mimetypes
import hashlib
import logging

from ..models.files import FileInfo, FileGraph, DirectoryInfo
from ..models.results import ParsedRepository
from ..models.graph import GraphTriple, BuiltGraph
from ..models.exceptions import ProcessingError
from ..storage.graph_schemas import GraphSchemas

logger = logging.getLogger(__name__)


@dataclass
class BonusItemStats:
    """🍎 PAC-MAN's bonus item collection statistics!"""
    bonus_files_found: int = 0  # Total files discovered
    treasure_maps_created: int = 0  # File graphs generated
    github_coordinates_mapped: int = 0  # GitHub links generated
    directory_mazes_explored: int = 0  # Directories analyzed
    special_items_detected: int = 0  # Config files, docs, etc.
    binary_treasures_skipped: int = 0  # Binary files ignored


class FileSystemExplorer:
    """
    🍎 PAC-MAN's Bonus File Explorer! 🍎
    
    Maps out the entire file system maze and discovers all the bonus treasures!
    Every file gets GitHub coordinates for instant teleportation!
    """

    def __init__(self, repo_path: Path, org: str, repo: str, release: str):
        self.repo_path = repo_path
        self.org = org
        self.repo = repo
        self.release = release
        self.stats = BonusItemStats()
        self.logger = logging.getLogger(__name__)
        
        # File type classifications
        self.code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp', '.rs', '.go'}
        self.doc_extensions = {'.md', '.rst', '.txt', '.doc', '.docx', '.pdf'}
        self.config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'}
        self.data_extensions = {'.csv', '.xml', '.sql', '.db', '.sqlite'}
        
        logger.info(f"🍎 PAC-MAN starting file exploration: {org}/{repo} {release}")

    def explore_all_bonus_items(self) -> List[FileInfo]:
        """
        🍎 EXPLORE ALL BONUS ITEMS! 🍎
        
        Comprehensive file system exploration to find all treasures!
        """
        try:
            self.logger.info("🍎 Beginning bonus item exploration...")
            
            bonus_items = []
            
            # Recursively explore the repository
            for file_path in self.repo_path.rglob("*"):
                if file_path.is_file():
                    try:
                        file_info = self._analyze_bonus_item(file_path)
                        if file_info:
                            bonus_items.append(file_info)
                            self.stats.bonus_files_found += 1
                    except Exception as e:
                        self.logger.warning(f"🍎 Could not analyze {file_path}: {e}")
                        continue
            
            self.logger.info(f"🍎 Exploration complete! Found {len(bonus_items)} bonus items")
            return bonus_items
            
        except Exception as e:
            raise ProcessingError(f"Failed to explore file system: {e}")

    def _analyze_bonus_item(self, file_path: Path) -> Optional[FileInfo]:
        """🍎 Analyze a single bonus item file!"""
        
        # Skip hidden files and directories
        if any(part.startswith('.') for part in file_path.parts):
            if not file_path.name in ['.gitignore', '.env', '.dockerignore']:
                return None
        
        # Skip common uninteresting directories
        skip_dirs = {'__pycache__', '.pytest_cache', 'node_modules', '.git', '.vscode', '.idea'}
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return None
        
        try:
            # Get relative path from repository root
            relative_path = file_path.relative_to(self.repo_path)
            
            # Get file stats
            stat = file_path.stat()
            
            # Determine file type and category
            file_type = self._classify_file_type(file_path)
            category = self._classify_file_category(file_path)
            
            # Generate GitHub URL
            github_url = self._generate_github_url(relative_path)
            
            # Get file content preview (for text files)
            content_preview = self._get_content_preview(file_path, file_type)
            
            # Calculate file hash for change detection
            file_hash = self._calculate_file_hash(file_path)
            
            # Detect if this is a special bonus item
            is_special = self._is_special_bonus_item(file_path)
            if is_special:
                self.stats.special_items_detected += 1
            
            file_info = FileInfo(
                path=relative_path,
                absolute_path=file_path,
                name=file_path.name,
                extension=file_path.suffix,
                size_bytes=stat.st_size,
                file_type=file_type,
                category=category,
                github_url=github_url,
                content_preview=content_preview,
                file_hash=file_hash,
                is_special_item=is_special,
                line_count=self._count_lines(file_path, file_type),
                encoding=self._detect_encoding(file_path)
            )
            
            self.stats.github_coordinates_mapped += 1
            return file_info
            
        except Exception as e:
            self.logger.warning(f"🍎 Failed to analyze {file_path}: {e}")
            return None

    def _classify_file_type(self, file_path: Path) -> str:
        """🔍 Classify the type of bonus item"""
        
        extension = file_path.suffix.lower()
        
        if extension in self.code_extensions:
            return "source_code"
        elif extension in self.doc_extensions:
            return "documentation"
        elif extension in self.config_extensions:
            return "configuration"
        elif extension in self.data_extensions:
            return "data"
        elif extension in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'}:
            return "image"
        elif extension in {'.mp4', '.avi', '.mov', '.mkv'}:
            return "video"
        elif extension in {'.mp3', '.wav', '.flac', '.ogg'}:
            return "audio"
        elif extension in {'.zip', '.tar', '.gz', '.bz2', '.7z'}:
            return "archive"
        elif extension in {'.exe', '.dll', '.so', '.dylib', '.bin'}:
            self.stats.binary_treasures_skipped += 1
            return "binary"
        else:
            # Try to detect using mimetypes
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type:
                if mime_type.startswith('text/'):
                    return "text"
                elif mime_type.startswith('image/'):
                    return "image"
                elif mime_type.startswith('application/'):
                    return "application"
            
            return "unknown"

    def _classify_file_category(self, file_path: Path) -> str:
        """🏷️ Classify the bonus item category"""
        
        path_str = str(file_path).lower()
        name = file_path.name.lower()
        
        # Special files
        if name in {'readme.md', 'readme.txt', 'readme.rst', 'readme'}:
            return "readme"
        elif name in {'license', 'license.txt', 'license.md', 'copying'}:
            return "license"
        elif name in {'changelog.md', 'changelog.txt', 'changes.md', 'history.md'}:
            return "changelog"
        elif name in {'requirements.txt', 'pyproject.toml', 'setup.py', 'package.json', 'cargo.toml'}:
            return "dependencies"
        elif name in {'.gitignore', '.dockerignore', '.env', '.env.example'}:
            return "project_config"
        elif name.startswith('dockerfile'):
            return "docker"
        elif 'test' in path_str and file_path.suffix == '.py':
            return "test"
        elif 'doc' in path_str or 'docs' in path_str:
            return "documentation"
        elif 'example' in path_str or 'sample' in path_str:
            return "examples"
        elif 'script' in path_str:
            return "scripts"
        elif 'config' in path_str or 'setting' in path_str:
            return "configuration"
        else:
            return "general"

    def _generate_github_url(self, relative_path: Path) -> str:
        """🔗 Generate GitHub treasure coordinates!"""
        return f"https://github.com/{self.org}/{self.repo}/blob/{self.release}/{relative_path}"

    def _get_content_preview(self, file_path: Path, file_type: str) -> Optional[str]:
        """👀 Get a preview of the file content"""
        
        if file_type in ["binary", "image", "video", "audio", "archive"]:
            return None
        
        try:
            # Only preview text-based files and limit size
            if file_path.stat().st_size > 1024 * 1024:  # 1MB limit
                return "File too large for preview"
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(500)  # First 500 characters
                if len(content) == 500:
                    content += "..."
                return content
                
        except Exception:
            return "Binary or unreadable content"

    def _calculate_file_hash(self, file_path: Path) -> str:
        """🔐 Calculate file hash for change detection"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                # Read in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "unknown"

    def _is_special_bonus_item(self, file_path: Path) -> bool:
        """⭐ Detect if this is a special bonus item"""
        name = file_path.name.lower()
        
        special_files = {
            'readme.md', 'license', 'changelog.md', 'contributing.md',
            'pyproject.toml', 'setup.py', 'requirements.txt', 'package.json',
            'dockerfile', '.gitignore', 'makefile', 'cargo.toml'
        }
        
        return name in special_files or name.startswith('dockerfile')

    def _count_lines(self, file_path: Path, file_type: str) -> Optional[int]:
        """📏 Count lines in text files"""
        if file_type in ["binary", "image", "video", "audio", "archive"]:
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return None

    def _detect_encoding(self, file_path: Path) -> str:
        """🔤 Detect file encoding"""
        try:
            # Simple encoding detection
            with open(file_path, 'rb') as f:
                raw_data = f.read(1024)
                
            # Try UTF-8 first
            try:
                raw_data.decode('utf-8')
                return 'utf-8'
            except UnicodeDecodeError:
                pass
            
            # Try other common encodings
            for encoding in ['latin-1', 'cp1252', 'ascii']:
                try:
                    raw_data.decode(encoding)
                    return encoding
                except UnicodeDecodeError:
                    continue
            
            return 'binary'
            
        except Exception:
            return 'unknown'

    def generate_directory_structure(self) -> List[DirectoryInfo]:
        """📁 Generate directory structure information"""
        directories = {}
        
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_dir():
                relative_path = file_path.relative_to(self.repo_path)
                
                # Skip hidden and uninteresting directories
                if any(part.startswith('.') for part in relative_path.parts):
                    continue
                
                # Count files in directory
                file_count = len([f for f in file_path.iterdir() if f.is_file()])
                subdir_count = len([d for d in file_path.iterdir() if d.is_dir()])
                
                directories[str(relative_path)] = DirectoryInfo(
                    path=relative_path,
                    name=file_path.name,
                    file_count=file_count,
                    subdirectory_count=subdir_count,
                    github_url=f"https://github.com/{self.org}/{self.repo}/tree/{self.release}/{relative_path}"
                )
                
                self.stats.directory_mazes_explored += 1
        
        return list(directories.values())


class FileAnalyzer:
    """
    🍎 PAC-MAN's Main File Analysis System! 🍎
    
    The master coordinator for all file system exploration and mapping!
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_repository_files(self, repo_path: Path, org: str, 
                                     repo: str, release: str) -> FileGraph:
        """
        🍎 ANALYZE ALL REPOSITORY FILES! 🍎
        
        Complete file system analysis and mapping!
        """
        try:
            self.logger.info(f"🍎 Starting file analysis: {org}/{repo} {release}")
            
            # Create explorer
            explorer = FileSystemExplorer(repo_path, org, repo, release)
            
            # Explore all files
            files = explorer.explore_all_bonus_items()
            
            # Generate directory structure
            directories = explorer.generate_directory_structure()
            
            # Create file graph
            file_graph = FileGraph(
                repository=f"{org}/{repo}",
                release=release,
                files=files,
                directories=directories,
                total_files=len(files),
                total_directories=len(directories),
                analysis_stats=explorer.stats
            )
            
            self.logger.info(f"🍎 File analysis complete! {len(files)} files, {len(directories)} directories")
            return file_graph
            
        except Exception as e:
            raise ProcessingError(f"Failed to analyze repository files: {e}")

    def generate_file_graphs_with_github_links(self, parsed_repo: ParsedRepository,
                                                   org: str, repo: str, release: str) -> BuiltGraph:
        """Generate file graphs with GitHub links"""
        
        # Analyze files if not already done
        file_analysis = self.analyze_repository_files(
            Path(parsed_repo.name), org, repo, release
        )
        
        # Build graph triples
        graph_uri = GraphSchemas.get_files_uri(org, repo, release)
        triples = []
        
        for file_info in file_analysis.files:
            file_uri = f"file:{org}/{repo}/{release}/{self._sanitize_uri(str(file_info.path))}"
            
            triples.extend([
                GraphTriple(
                    subject=file_uri,
                    predicate="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                    object="http://rdf.webofcode.org/woc/File"
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate="http://rdf.webofcode.org/woc/path",
                    object=f'"{file_info.path}"'
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate="http://rdf.webofcode.org/woc/githubUrl",
                    object=f'"{file_info.github_url}"'
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate="http://rdf.webofcode.org/woc/fileType",
                    object=f'"{file_info.file_type}"'
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate="http://rdf.webofcode.org/woc/category",
                    object=f'"{file_info.category}"'
                )
            ])
            
            if file_info.line_count:
                triples.append(GraphTriple(
                    subject=file_uri,
                    predicate="http://rdf.webofcode.org/woc/lineCount",
                    object=f'"{file_info.line_count}"'
                ))
        
        return BuiltGraph(
            uri=graph_uri,
            triples=triples,
            description=f"File structure for {org}/{repo} {release}"
        )

    def track_line_numbers_for_function_locations(self, files: List[FileInfo]) -> Dict[str, Dict[str, int]]:
        """Track line numbers for function locations"""
        function_locations = {}
        
        for file_info in files:
            if file_info.file_type == "source_code" and file_info.extension == ".py":
                # This would integrate with the Python parser to track function locations
                # For now, return empty dict - this would be enhanced with actual line tracking
                function_locations[str(file_info.path)] = {}
        
        return function_locations

    def handle_multiple_file_types(self, files: List[FileInfo]) -> Dict[str, List[FileInfo]]:
        """📂 Group files by type for specialized handling"""
        grouped_files = {}
        
        for file_info in files:
            file_type = file_info.file_type
            if file_type not in grouped_files:
                grouped_files[file_type] = []
            grouped_files[file_type].append(file_info)
        
        return grouped_files

    def _sanitize_uri(self, value: str) -> str:
        """Sanitize string for use in URI"""
        return value.replace('/', '_').replace(' ', '_').replace('.', '_')


# 🍎 PAC-MAN says: "WAKA WAKA! Found all the bonus treasures!" 🍎
def create_file_analyzer() -> FileAnalyzer:
    """Factory function to create PAC-MAN's file analyzer!"""
    return FileAnalyzer()
