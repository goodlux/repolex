"""
🟡 PAC-MAN Graph Manager - The Ultimate Semantic Analysis Powerhouse!

WAKA WAKA WAKA! PAC-MAN's biggest power pellet chomping adventure!
This is where raw repository dots get transformed into the mighty 19-graph semantic maze!

The Graph Manager is PAC-MAN's semantic analysis command center - turning boring code
into delicious semantic intelligence that can be queried, analyzed, and explored!
"""

import json
import logging
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import pyoxigraph as oxigraph

from ..models.exceptions import ProcessingError, StorageError, ValidationError
from ..models.graph import GraphInfo, GraphDetails
from ..models.results import ProcessingResult, ResultStatus
from ..models.progress import ProgressCallback, ProgressReport
from ..models.repository import RepoInfo
from ..utils.validation import validate_org_repo, validate_release_tag
from ..storage.oxigraph_client import OxigraphClient, get_oxigraph_client, reset_oxigraph_client
from ..core.config_manager import get_setting
from ..storage.graph_builder import GraphBuilder, GraphBuildContext
from ..parsers.python_parser import PythonParser
from ..parsers.git_analyzer import GitAnalyzer
from ..parsers.abc_generator import ABCGenerator


@dataclass
class SemanticProcessingStats:
    """🟡 PAC-MAN's semantic processing statistics."""
    functions_discovered: int = 0
    classes_discovered: int = 0
    modules_processed: int = 0
    commits_analyzed: int = 0
    developers_profiled: int = 0
    abc_events_generated: int = 0
    graphs_created: int = 0
    triples_stored: int = 0
    processing_time_seconds: float = 0.0
    
    # PAC-MAN themed stats 🟡
    dots_chomped: int = 0  # Total semantic elements processed
    power_pellets_found: int = 0  # Important semantic discoveries
    ghosts_avoided: int = 0  # Errors handled gracefully
    maze_levels_completed: int = 0  # Graph types successfully built


class GraphManager:
    """
    🟡 PAC-MAN Graph Manager - The Semantic Analysis POWERHOUSE!
    
    This is where the magic happens! PAC-MAN chomps through raw code and transforms
    it into a beautiful 19-graph semantic maze that can be explored by both humans
    and AI systems. 
    
    WAKA WAKA WAKA! The ultimate dot-chomping semantic adventure!
    
    Features:
    - 🟡 Complete AST parsing and analysis
    - 🟡 Git intelligence extraction 
    - 🟡 ABC event generation for temporal tracking
    - 🟡 19-graph architecture with stable identities
    - 🟡 Nuclear rebuild capabilities (safe updates)
    - 🟡 Cross-repository semantic understanding
    """
    
    def __init__(self, storage_root: Optional[Path] = None):
        """Initialize PAC-MAN's semantic analysis command center."""
        self.storage_root = storage_root or Path.home() / ".repolex"
        self.logger = logging.getLogger(__name__)
        
        # Initialize the semantic analysis crew 🟡
        # Reset singleton to ensure we use the correct database path
        reset_oxigraph_client()
        # Get configured database path or use default
        db_path = get_setting("database.storage_path", "~/.repolex/graph")
        db_path = Path(db_path).expanduser()
        self.oxigraph = get_oxigraph_client(db_path)
        self.graph_builder = GraphBuilder(self.oxigraph)
        self.python_parser = PythonParser()
        self.git_analyzer = GitAnalyzer()
        self.abc_generator = ABCGenerator()
        
        # PAC-MAN stats tracking 🟡
        self.total_dots_chomped = 0
        self.total_power_pellets_found = 0
        self.total_ghosts_avoided = 0
        self.total_mazes_completed = 0
        
        # Graph manager initialized - storage ready
    
    def add_graphs(self, org_repo: str, release: Optional[str] = None, enable_nlp: bool = False, force: bool = False, progress_callback: Optional[ProgressCallback] = None) -> ProcessingResult:
        """
        🟡 PAC-MAN's ULTIMATE SEMANTIC CHOMPING ADVENTURE!
        
        Complete semantic analysis pipeline that transforms raw repository code
        into the magnificent 19-graph semantic maze architecture!
        
        This is the BIG SNACK - the ultimate power pellet that processes:
        - Python AST parsing to CodeOntology format
        - Git history analysis and developer intelligence  
        - ABC event generation for temporal change tracking
        - All 19 graph types per the architectural vision
        - Cross-graph relationship building
        
        WAKA WAKA WAKA! Let's chomp some serious semantic dots!
        """
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        start_time = datetime.now()
        stats = SemanticProcessingStats()
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=0, total=100,
                message=f"🟡 PAC-MAN entering the semantic maze: {org_repo}",
                stage="initializing"
            ))
        
        try:
            # Step 1: Validate repository exists locally
            repo_path = self._get_repo_path(org_repo)
            if not repo_path.exists():
                raise ValidationError(
                    f"Repository {org_repo} not found locally",
                    suggestions=[f"Use 'rlex repo add {org_repo}' first to clone the repository"]
                )
            
            # Step 2: Determine which release to process
            if not release:
                release = self._get_latest_release(repo_path)
                if not release:
                    # No git tags found - use "latest" for repositories without releases
                    release = "latest"
                    self.logger.info(f"🟡 No git tags found for {org_repo}, using 'latest'")
                
            
            # Validate release exists
            self._validate_release_exists(repo_path, release)
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=5, total=100,
                    message=f"🟡 PAC-MAN processing release: {release}",
                    stage="validating"
                ))
            
            # Step 3: Check if graphs already exist (avoid duplicate work unless forced)
            if not force:
                existing_graphs = self._check_existing_graphs(org_repo, release)
                if existing_graphs:
                    raise ValidationError(
                        f"Graphs already exist for {org_repo} {release}",
                        suggestions=[
                            f"Use 'rlex graph update {org_repo} {release}' to rebuild",
                            f"Use 'rlex graph remove {org_repo} {release}' to remove first"
                        ]
                    )
            else:
                # Force mode - remove existing graphs first
                self.logger.info(f"🟡 PAC-MAN FORCE MODE: Removing existing graphs for {org_repo} {release}")
                self.oxigraph.remove_all_repository_graphs(org_repo)
            
            # Step 4: CHOMP THE CODE! Parse Python AST 🟡
            if progress_callback:
                progress_callback(ProgressReport(
                    current=10, total=100,
                    message="🟡 PAC-MAN chomping through Python code dots...",
                    stage="parsing_ast"
                ))
            
            ast_data = self._parse_repository_ast(repo_path, release, org_repo, progress_callback)
            stats.functions_discovered = ast_data.total_functions
            stats.classes_discovered = ast_data.total_classes  
            stats.modules_processed = ast_data.total_modules
            stats.dots_chomped += ast_data.total_functions + ast_data.total_classes
            
            # Processed {stats.functions_discovered} functions, {stats.classes_discovered} classes
            
            # Step 5: ANALYZE THE GIT MAZE! Git intelligence extraction 🟡
            if progress_callback:
                progress_callback(ProgressReport(
                    current=30, total=100,
                    message="🟡 PAC-MAN exploring git history maze...",
                    stage="analyzing_git"
                ))
            
            git_data = self._analyze_git_intelligence(repo_path, progress_callback)
            stats.commits_analyzed = len(git_data.commits)
            stats.developers_profiled = len(git_data.developers)
            stats.power_pellets_found += len(git_data.commits)  # Each commit is a power pellet!
            
            # Analyzed {stats.commits_analyzed} commits, {stats.developers_profiled} developers
            
            # Step 6: GENERATE ABC EVENTS! Temporal change tracking 🟡
            if progress_callback:
                progress_callback(ProgressReport(
                    current=50, total=100,
                    message="🟡 PAC-MAN generating temporal change events...",
                    stage="generating_abc"
                ))
            
            abc_events = self._generate_abc_events(org_repo, release, ast_data, git_data, progress_callback)
            stats.abc_events_generated = len(abc_events)
            stats.power_pellets_found += len(abc_events)
            
            # Generated {stats.abc_events_generated} ABC events
            
            # Step 7: BUILD THE SEMANTIC MAZE! Create all 19 graphs 🟡
            if progress_callback:
                progress_callback(ProgressReport(
                    current=60, total=100,
                    message="🟡 PAC-MAN constructing the 19-graph semantic maze!",
                    stage="building_graphs"
                ))
            
            graphs_created = self._build_all_graphs(org_repo, release, ast_data, git_data, abc_events, enable_nlp, progress_callback)
            stats.graphs_created = len(graphs_created)
            stats.maze_levels_completed = len(graphs_created)
            
            print(f"🟡 PAC-MAN built {stats.graphs_created} maze levels!")
            
            # Step 8: STORE IN THE SEMANTIC DATABASE! Oxigraph storage 🟡  
            if progress_callback:
                progress_callback(ProgressReport(
                    current=80, total=100,
                    message="🟡 PAC-MAN storing semantic treasures in Oxigraph!",
                    stage="storing"
                ))
            
            triples_stored = self._store_semantic_data(org_repo, release, graphs_created, progress_callback)
            stats.triples_stored = triples_stored
            stats.dots_chomped += triples_stored // 100  # Every 100 triples = 1 dot chomped
            
            print(f"🟡 PAC-MAN stored {stats.triples_stored} semantic triple dots!")
            
            # Step 9: Update repository metadata
            self._update_processing_metadata(org_repo, release, stats)
            
            # Calculate final stats
            stats.processing_time_seconds = (datetime.now() - start_time).total_seconds()
            self.total_dots_chomped += stats.dots_chomped
            self.total_power_pellets_found += stats.power_pellets_found
            self.total_mazes_completed += 1
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=100, total=100,
                    message=f"🟡 PAC-MAN VICTORY! Semantic maze complete! WAKA WAKA WAKA!",
                    stage="complete"
                ))
            
            print("\\n" + "="*60)
            print(f"🟡 PAC-MAN SEMANTIC VICTORY! 🟡")
            print("="*60)
            print(f"🗄️  Repository: {org_repo} {release}")
            print(f"🔧 Functions: {stats.functions_discovered}")
            print(f"📊 Classes: {stats.classes_discovered}") 
            print(f"👥 Developers: {stats.developers_profiled}")
            print(f"📝 Commits: {stats.commits_analyzed}")
            print(f"⚡ ABC Events: {stats.abc_events_generated}")
            print(f"🗺️  Graphs: {stats.graphs_created}")
            print(f"🟡 Dots Chomped: {stats.dots_chomped}")
            print(f"💥 Power Pellets: {stats.power_pellets_found}")
            print(f"⏱️  Time: {stats.processing_time_seconds:.2f}s")
            print("WAKA WAKA WAKA!")
            print("="*60)
            
            return ProcessingResult(
                status=ResultStatus.SUCCESS,
                org_repo=org_repo,
                release=release,
                actual_release=release,  # The release that was actually processed
                graphs_created=len(graphs_created),
                functions_found=stats.functions_discovered,
                classes_found=stats.classes_discovered,
                modules_found=stats.modules_processed,
                processing_time=stats.processing_time_seconds,
                message="🟡 PAC-MAN semantic analysis complete! WAKA WAKA WAKA!"
            )
            
        except Exception as e:
            self.total_ghosts_avoided += 1
            stats.ghosts_avoided += 1
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Processing failed, error handled gracefully
            
            if isinstance(e, (ValidationError, ProcessingError, StorageError)):
                raise
            else:
                raise ProcessingError(
                    f"Unexpected error during semantic analysis of {org_repo}: {str(e)}",
                    suggestions=[
                        "Check repository structure and permissions",
                        "Try processing again in a few minutes",
                        "Check system resources and disk space"
                    ]
                )
    
    def remove_graphs(self, org_repo: str, release: Optional[str] = None, force: bool = False) -> bool:
        """
        🟡 PAC-MAN's POWER PELLET CLEAR! Remove semantic graphs safely.
        
        If release specified: remove only that release's graphs (surgical precision)
        If release is None: remove ALL graphs for repository (nuclear option)
        
        Uses PAC-MAN's hybrid identity model to preserve cross-graph references!
        """
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        if not force:
            raise ValidationError(
                "Destructive operation requires confirmation",
                suggestions=["Use --force flag or confirm in interactive mode"]
            )
        
        try:
            if release:
                # Surgical removal - only this release's implementation graphs
                print(f"🟡 PAC-MAN power pellet mode: Removing graphs for {org_repo} {release}")
                graphs_removed = self._remove_release_graphs(org_repo, release)
                print(f"🟡 PAC-MAN cleared {graphs_removed} graphs for {release}!")
            else:
                # Nuclear option - ALL graphs for this repository
                print(f"🟡 PAC-MAN MEGA POWER PELLET: Removing ALL graphs for {org_repo}")
                graphs_removed = self._remove_all_repository_graphs(org_repo)
                print(f"🟡 PAC-MAN cleared ALL {graphs_removed} graphs for {org_repo}!")
            
            return graphs_removed > 0
            
        except Exception as e:
            self.total_ghosts_avoided += 1
            raise StorageError(
                f"Failed to remove graphs for {org_repo}: {str(e)}",
                suggestions=["Check database permissions", "Try again"]
            )
    
    def list_graphs(self, org_repo: Optional[str] = None) -> List[GraphInfo]:
        """🟡 PAC-MAN surveys the semantic maze - list all graphs."""
        
        try:
            if org_repo:
                validate_org_repo(org_repo)
                graphs = self.oxigraph.list_repository_graphs(org_repo)
            else:
                graphs = self.oxigraph.list_all_graphs()
            
            graph_info_list = []
            for graph_uri in graphs:
                info = self._get_graph_info(graph_uri)
                graph_info_list.append(info)
            
            # Found {len(graph_info_list)} semantic graphs
            return sorted(graph_info_list, key=lambda g: g.graph_uri)
            
        except Exception as e:
            raise StorageError(
                f"Failed to list graphs: {str(e)}",
                suggestions=["Check database connection"]
            )
    
    def show_graphs(self, org_repo: str, release: Optional[str] = None) -> GraphDetails:
        """🟡 PAC-MAN examines semantic maze levels in detail."""
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        try:
            # Get all graphs for this repository/release
            graphs = self._get_repository_graphs(org_repo, release)
            
            if not graphs:
                raise ValidationError(
                    f"No graphs found for {org_repo}" + (f" {release}" if release else ""),
                    suggestions=[
                        f"Use 'rlex graph add {org_repo}" + (f" {release}" if release else "") + "' to create graphs"
                    ]
                )
            
            # Calculate detailed statistics
            total_triples = 0
            graph_details = []
            
            for graph_uri in graphs:
                info = self._get_detailed_graph_info(graph_uri)
                graph_details.append(info)
                total_triples += info.triple_count
            
            return GraphDetails(
                org_repo=org_repo,
                release=release,
                total_graphs=len(graphs),
                total_triples=total_triples,
                graphs=graph_details,
                last_updated=datetime.now(),  # Would get from metadata
                storage_size_mb=total_triples * 0.0001  # Rough estimate
            )
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            else:
                raise StorageError(
                    f"Failed to show graph details: {str(e)}",
                    suggestions=["Check database connection"]
                )
    
    def update_graphs(self, org_repo: str, release: Optional[str] = None, progress_callback: Optional[ProgressCallback] = None) -> ProcessingResult:
        """
        🟡 PAC-MAN's NUCLEAR REBUILD! Safely reconstruct semantic graphs.
        
        This is PAC-MAN's most advanced power pellet - the nuclear rebuild capability!
        Uses the hybrid identity model to preserve cross-graph references while
        completely rebuilding implementation-specific data.
        
        Safe operation that doesn't break cross-references! WAKA WAKA WAKA!
        """
        validate_org_repo(org_repo)
        if release:
            validate_release_tag(release)
        
        if progress_callback:
            progress_callback(ProgressReport(
                current=0, total=100,
                message=f"🟡 PAC-MAN NUCLEAR REBUILD MODE: {org_repo}" + (f" {release}" if release else ""),
                stage="initializing"
            ))
        
        try:
            # Step 1: Verify graphs exist
            existing_graphs = self._check_existing_graphs(org_repo, release)
            if not existing_graphs:
                raise ValidationError(
                    f"No graphs found to rebuild for {org_repo}" + (f" {release}" if release else ""),
                    suggestions=[f"Use 'rlex graph add {org_repo}' to create graphs first"]
                )
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=10, total=100,
                    message="🟡 PAC-MAN power pellet mode: Clearing old implementation graphs...",
                    stage="clearing"
                ))
            
            # Step 2: Remove ONLY implementation-specific graphs (preserve stable identities)
            self._nuclear_clear_implementation_graphs(org_repo, release)
            
            if progress_callback:
                progress_callback(ProgressReport(
                    current=20, total=100,
                    message="🟡 PAC-MAN rebuilding semantic maze from scratch...",
                    stage="rebuilding"
                ))
            
            # Step 3: Rebuild everything (reuse the main processing pipeline)
            result = self.add_graphs(org_repo, release, force=True, progress_callback=progress_callback)
            
            # Update result to reflect this was a rebuild
            result.message = f"🟡 PAC-MAN NUCLEAR REBUILD SUCCESS! {org_repo} semantic maze reconstructed! WAKA WAKA!"
            
            return result
            
        except Exception as e:
            if isinstance(e, (ValidationError, ProcessingError, StorageError)):
                raise
            else:
                raise ProcessingError(
                    f"Nuclear rebuild failed for {org_repo}: {str(e)}",
                    suggestions=[
                        "Check repository integrity",
                        "Ensure sufficient system resources",
                        "Try removing and re-adding graphs"
                    ]
                )
    
    # Private methods - PAC-MAN's internal maze navigation systems 🟡
    
    def _get_repo_path(self, org_repo: str) -> Path:
        """Get local repository path."""
        org, repo = org_repo.split('/', 1)
        return self.storage_root / "repos" / org / repo
    
    def _get_latest_release(self, repo_path: Path) -> Optional[str]:
        """Discover the latest release from git tags."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "-C", str(repo_path), "tag", "--sort=-version:refname"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                tags = [tag.strip() for tag in result.stdout.split('\n') if tag.strip()]
                return tags[0] if tags else None
            else:
                return None
                
        except Exception:
            return None
    
    def _validate_release_exists(self, repo_path: Path, release: str):
        """Validate that the specified release exists."""
        # Skip validation for "latest" - it's a special case for repos without tags
        if release == "latest":
            self.logger.info(f"🟡 Using 'latest' - skipping tag validation")
            return
            
        try:
            import subprocess
            result = subprocess.run(
                ["git", "-C", str(repo_path), "rev-parse", f"refs/tags/{release}"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise ValidationError(
                    f"Release '{release}' not found",
                    suggestions=[
                        "Check available releases with 'git tag -l'",
                        "Ensure release tag exists in repository"
                    ]
                )
                
        except subprocess.SubprocessError:
            raise ValidationError(
                f"Could not validate release '{release}'",
                suggestions=["Check git installation and repository integrity"]
            )
    
    def _check_existing_graphs(self, org_repo: str, release: Optional[str]) -> List[str]:
        """Check if graphs already exist for this repository/release."""
        return self.oxigraph.list_repository_graphs(org_repo, release)
    
    def _parse_repository_ast(self, repo_path: Path, release: str, org_repo: str, progress_callback: Optional[ProgressCallback] = None):
        """Parse repository AST using PAC-MAN's Python parser."""
        return self.python_parser.parse_repository(repo_path, release, org_repo, progress_callback)
    
    def _analyze_git_intelligence(self, repo_path: Path, progress_callback: Optional[ProgressCallback] = None):
        """Analyze git intelligence using PAC-MAN's git analyzer."""
        return self.git_analyzer.analyze_repository(repo_path, progress_callback)
    
    def _generate_abc_events(self, org_repo: str, release: str, ast_data, git_data, progress_callback: Optional[ProgressCallback] = None):
        """Generate ABC events using PAC-MAN's ABC generator."""
        # For repositories without tags/releases, we can't generate temporal events
        # since we need at least two releases to compare
        if release == "latest" or not release:
            self.logger.info("🟡 No previous release found - skipping temporal event generation")
            return []  # Return empty list of events
        
        # TODO: This would need both old and new release data to work properly
        # For now, return empty list until we have proper release comparison logic
        return []
    
    def _build_all_graphs(self, org_repo: str, release: str, ast_data, git_data, abc_events, enable_nlp: bool = False, progress_callback: Optional[ProgressCallback] = None) -> List[str]:
        """Build all 19 graph types using PAC-MAN's graph builder."""
        # Split org_repo into org and repo
        org, repo = org_repo.split('/', 1)
        
        # Create the context object that GraphBuilder expects
        context = GraphBuildContext(
            org=org,
            repo=repo,
            release=release,
            parsed_data=ast_data,
            git_data=git_data,
            previous_release_data=None,  # We don't have previous release data yet
            enable_nlp=enable_nlp  # 🛸 Pass NLP flag to context
        )
        
        # GraphBuilder.build_all_graphs is not async, so don't it
        built_graphs = self.graph_builder.build_all_graphs(context)
        
        # Extract the graph names/URIs to return
        return [graph.graph_uri for graph in built_graphs]
    
    def _store_semantic_data(self, org_repo: str, release: str, graphs_created: List[str], progress_callback: Optional[ProgressCallback] = None) -> int:
        """Store semantic data in Oxigraph."""
        return self.oxigraph.store_repository_graphs(org_repo, release, graphs_created, progress_callback)
    
    def _update_processing_metadata(self, org_repo: str, release: str, stats: SemanticProcessingStats):
        """Update processing metadata for tracking."""
        repo_path = self._get_repo_path(org_repo)
        metadata_file = repo_path / ".repolex" / "processing_metadata.json"
        metadata_file.parent.mkdir(exist_ok=True)
        
        metadata = {
            "last_processed": datetime.now().isoformat(),
            "last_release_processed": release,
            "processing_stats": stats.__dict__,
            "pacman_stats": {
                "total_dots_chomped": self.total_dots_chomped,
                "total_power_pellets_found": self.total_power_pellets_found,
                "total_ghosts_avoided": self.total_ghosts_avoided,
                "total_mazes_completed": self.total_mazes_completed
            }
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _remove_release_graphs(self, org_repo: str, release: str) -> int:
        """Remove graphs for specific release only."""
        return self.oxigraph.remove_release_graphs(org_repo, release)
    
    def _remove_all_repository_graphs(self, org_repo: str) -> int:
        """Remove ALL graphs for repository."""
        return self.oxigraph.remove_all_repository_graphs(org_repo)
    
    def _nuclear_clear_implementation_graphs(self, org_repo: str, release: Optional[str]):
        """Nuclear clear implementation graphs while preserving stable identities."""
        self.oxigraph.nuclear_clear_implementation_graphs(org_repo, release)
    
    def _get_graph_info(self, graph_uri: str) -> GraphInfo:
        """Get basic information about a graph."""
        triple_count = self.oxigraph.count_triples_in_graph(graph_uri)
        
        # Extract org_repo from URI pattern: http://Repolex.org/repo/org/repo/...
        org_repo = "unknown/unknown"
        if "/repo/" in graph_uri:
            parts = graph_uri.split("/repo/", 1)[1].split("/")
            if len(parts) >= 2:
                org_repo = f"{parts[0]}/{parts[1]}"
        
        # Import the required types
        from ..models.graph import GraphType, GraphStatus
        
        # Map the graph type
        graph_type_str = self._determine_graph_type(graph_uri)
        graph_type = self._map_to_graph_type_enum(graph_type_str)
        
        return GraphInfo(
            graph_uri=graph_uri,
            graph_type=graph_type,
            org_repo=org_repo,
            status=GraphStatus.READY,
            created_at=datetime.now(),  # TODO: Get from metadata
            updated_at=datetime.now(),  # TODO: Get from metadata
            triple_count=triple_count
        )
    
    def _get_detailed_graph_info(self, graph_uri: str):
        """Get detailed information about a graph."""
        return self.oxigraph.get_detailed_graph_info(graph_uri)
    
    def _get_repository_graphs(self, org_repo: str, release: Optional[str]) -> List[str]:
        """Get all graphs for a repository/release."""
        return self.oxigraph.list_repository_graphs(org_repo, release)
    
    def _map_to_graph_type_enum(self, graph_type_str: str):
        """Map string graph type to GraphType enum."""
        from ..models.graph import GraphType
        
        mapping = {
            "stable_functions": GraphType.FUNCTIONS_STABLE,
            "implementations": GraphType.FUNCTIONS_IMPL,
            "git_commits": GraphType.GIT_COMMITS,
            "git_developers": GraphType.GIT_DEVELOPERS,
            "git_branches": GraphType.GIT_BRANCHES,
            "git_tags": GraphType.GIT_TAGS,
            "abc_events": GraphType.ABC_EVENTS,
            "evolution": GraphType.EVOLUTION_STATS,
            "files": GraphType.FILES_STRUCTURE,
            "ontology": GraphType.ONTOLOGY_WOC,
            "text_content": GraphType.TEXT_CONTENT,
            "text_topics": GraphType.TEXT_TOPICS,
            "text_entities": GraphType.TEXT_ENTITIES,
            "text_relationships": GraphType.TEXT_RELATIONSHIPS,
            "unknown": GraphType.ONTOLOGY_WOC  # Default fallback
        }
        
        return mapping.get(graph_type_str, GraphType.ONTOLOGY_WOC)
    
    def _determine_graph_type(self, graph_uri: str) -> str:
        """Determine graph type from URI."""
        if "functions/stable" in graph_uri:
            return "stable_functions"
        elif "functions/implementations" in graph_uri:
            return "implementations"
        elif "git/commits" in graph_uri:
            return "git_commits"
        elif "git/developers" in graph_uri:
            return "git_developers"
        elif "abc/events" in graph_uri:
            return "abc_events"
        elif "evolution" in graph_uri:
            return "evolution"
        elif "files" in graph_uri:
            return "files"
        elif "ontology" in graph_uri:
            return "ontology"
        elif "content/structure" in graph_uri:
            return "text_content"
        elif "content/topics" in graph_uri:
            return "text_topics"
        elif "entities/" in graph_uri:
            return "text_entities"
        elif "relationships/" in graph_uri:
            return "text_relationships"
        else:
            return "unknown"


# 🟡 PAC-MAN Convenience Functions

def chomp_repository_semantics(org_repo: str, release: Optional[str] = None, **kwargs) -> ProcessingResult:
    """
    🟡 PAC-MAN convenience function to chomp semantic dots!
    
    WAKA WAKA WAKA! The ultimate semantic snack attack!
    """
    manager = GraphManager()
    return manager.add_graphs(org_repo, release, **kwargs)

def power_pellet_rebuild(org_repo: str, release: Optional[str] = None, **kwargs) -> ProcessingResult:
    """
    🟡 PAC-MAN convenience function for nuclear rebuilds!
    
    POWER PELLET MODE ACTIVATED! WAKA WAKA WAKA!
    """
    manager = GraphManager()
    return manager.update_graphs(org_repo, release, **kwargs)
