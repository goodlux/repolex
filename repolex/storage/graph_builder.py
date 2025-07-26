"""
🟡 PAC-MAN's Semantic Maze Builder 🟡
WAKA WAKA WAKA - Building all 19 graph types per repository!

This module constructs the complete semantic maze architecture:
- Ontology graphs (4): The maze walls and rules  
- Function graphs (2): The dots and power pellets (stable + implementations)
- File structure graphs (per version): The maze layout
- Git intelligence graphs (4): The ghost movement patterns
- ABC events graph (1): The game history log  
- Evolution analysis graphs (3): The strategy analytics
- Processing metadata graphs (per version): The level completion stats

Each repository becomes a complete PAC-MAN maze with semantic intelligence!
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime
import logging
from dataclasses import dataclass

from ..models.function import FunctionInfo, ParameterInfo, DocstringInfo
from ..models.graph import BuiltGraph, GraphType, GraphMetadata
from ..models.results import ParsedRepository
from ..models.git import GitIntelligence, CommitInfo, DeveloperInfo
from ..models.results import ProcessingResult
from .graph_schemas import GraphSchemas
from .oxigraph_client import OxigraphClient, get_oxigraph_client

logger = logging.getLogger(__name__)

@dataclass
class GraphBuildContext:
    """Context for building graphs - PAC-MAN's maze construction context"""
    org: str
    repo: str
    release: str
    parsed_data: ParsedRepository
    git_data: Optional[GitIntelligence] = None
    previous_release_data: Optional[ParsedRepository] = None

class GraphBuilder:
    """
    🟡 PAC-MAN's Semantic Maze Constructor! 🟡
    
    Builds the complete 19-graph architecture for each repository:
    - Creates semantic mazes (ontology graphs)
    - Places dots and power pellets (function graphs)  
    - Maps the game board (file structure graphs)
    - Tracks ghost movements (git intelligence graphs)
    - Records game history (ABC events)
    - Analyzes gameplay patterns (evolution graphs)
    - Keeps score (metadata graphs)
    
    Each repository becomes a playable semantic PAC-MAN maze!
    """
    
    def __init__(self, oxigraph_client: Optional[OxigraphClient] = None):
        self.oxigraph = oxigraph_client or get_oxigraph_client()
        self.schemas = GraphSchemas()
        
        # PAC-MAN themed logging messages
        logger.info("🟡 PAC-MAN Graph Builder initialized - Ready to build semantic mazes!")
    
    def build_all_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """
        🟡 Build complete PAC-MAN semantic maze (all 19 graph types)
        
        This is the master maze constructor that creates the full semantic
        intelligence architecture for a repository release.
        
        Returns:
            List[BuiltGraph]: All 19 built graphs with metadata
        """
        logger.info(f"🟡 Building complete semantic maze for {context.org}/{context.repo} {context.release}")
        
        all_graphs = []
        
        try:
            # Phase 1: Ontology Graphs (4) - The maze walls and rules
            logger.info("🟡 Phase 1: Building maze walls (ontology graphs)...")
            ontology_graphs = self._build_ontology_graphs(context)
            all_graphs.extend(ontology_graphs)
            logger.info(f"✅ Built {len(ontology_graphs)} ontology graphs - Maze walls complete!")
            
            # Phase 2: Function Graphs (2) - The dots and power pellets  
            logger.info("🟡 Phase 2: Placing dots and power pellets (function graphs)...")
            function_graphs = self._build_function_graphs(context)
            all_graphs.extend(function_graphs)
            logger.info(f"✅ Built {len(function_graphs)} function graphs - Dots and power pellets placed!")
            
            # Phase 3: File Structure Graphs (per version) - The maze layout
            logger.info("🟡 Phase 3: Mapping the game board (file structure graphs)...")
            file_graphs = self._build_file_structure_graphs(context)
            all_graphs.extend(file_graphs)
            logger.info(f"✅ Built {len(file_graphs)} file structure graphs - Game board mapped!")
            
            # Phase 4: Git Intelligence Graphs (4) - Ghost movement patterns
            if context.git_data:
                logger.info("🟡 Phase 4: Tracking ghost movements (git intelligence graphs)...")
                git_graphs = self._build_git_intelligence_graphs(context)
                all_graphs.extend(git_graphs)
                logger.info(f"✅ Built {len(git_graphs)} git intelligence graphs - Ghost patterns recorded!")
            
            # Phase 5: ABC Events Graph (1) - Game history log
            logger.info("🟡 Phase 5: Recording game history (ABC events graph)...")
            abc_graphs = self._build_abc_events_graph(context)
            all_graphs.extend(abc_graphs)
            logger.info(f"✅ Built {len(abc_graphs)} ABC events graphs - Game history logged!")
            
            # Phase 6: Evolution Analysis Graphs (3) - Strategy analytics
            logger.info("🟡 Phase 6: Analyzing gameplay patterns (evolution graphs)...")
            evolution_graphs = self._build_evolution_analysis_graphs(context)
            all_graphs.extend(evolution_graphs)
            logger.info(f"✅ Built {len(evolution_graphs)} evolution analysis graphs - Strategy analyzed!")
            
            # Phase 7: Processing Metadata Graphs (per version) - Level completion stats
            logger.info("🟡 Phase 7: Recording level stats (metadata graphs)...")
            metadata_graphs = self._build_processing_metadata_graphs(context)
            all_graphs.extend(metadata_graphs)
            logger.info(f"✅ Built {len(metadata_graphs)} metadata graphs - Level stats recorded!")
            
            logger.info(f"🎉 PAC-MAN maze complete! Built {len(all_graphs)}/19 graphs for {context.org}/{context.repo}")
            
            # Validate we built all expected graphs
            if len(all_graphs) < 19:
                logger.warning(f"⚠️ Expected 19 graphs, but built {len(all_graphs)} - some maze sections missing!")
            
            return all_graphs
            
        except Exception as e:
            logger.error(f"Graph construction failed: {e}")
            if "Invalid IRI code point" in str(e):
                raise ProcessingError(f"Failed to build semantic maze due to invalid characters in URI. This usually means function names or other identifiers contain square brackets or other special characters: {e}") from e
            else:
                raise ProcessingError(f"Failed to build semantic maze: {e}") from e
    
    def _build_ontology_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build the 4 ontology graphs - PAC-MAN's maze walls and rules"""
        graphs = []
        
        # 1. Web of Code Ontology Graph - The fundamental maze structure
        woc_graph = self._build_woc_ontology_graph(context)
        graphs.append(woc_graph)
        
        # 2. Git Ontology Graph - Ghost behavior rules
        git_graph = self._build_git_ontology_graph(context)
        graphs.append(git_graph)
        
        # 3. Evolution Ontology Graph - Game progression rules
        evolution_graph = self._build_evolution_ontology_graph(context)
        graphs.append(evolution_graph)
        
        # 4. Files Ontology Graph - Maze layout rules
        files_graph = self._build_files_ontology_graph(context)
        graphs.append(files_graph)
        
        return graphs
    
    def _build_function_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build the 2 function graphs - PAC-MAN's dots and power pellets"""
        graphs = []
        
        # 1. Stable Function Identities Graph - The eternal dots (never disappear)
        stable_graph = self.build_stable_function_graph(
            context.org, context.repo, context.parsed_data.all_functions
        )
        graphs.append(stable_graph)
        
        # 2. Implementation Graph - Version-specific power pellets  
        impl_graph = self.build_implementation_graph(
            context.org, context.repo, context.release, context.parsed_data.all_functions
        )
        graphs.append(impl_graph)
        
        return graphs
    
    def _build_git_intelligence_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build the 4 git intelligence graphs - PAC-MAN's ghost movement patterns"""
        graphs = []
        
        # 1. Git Commits Graph - Ghost movement history
        commits_graph = self._build_commits_graph(context)
        graphs.append(commits_graph)
        
        # 2. Git Developers Graph - Ghost profiles  
        developers_graph = self._build_developers_graph(context)
        graphs.append(developers_graph)
        
        # 3. Git Branches Graph - Ghost territories
        branches_graph = self._build_branches_graph(context)
        graphs.append(branches_graph)
        
        # 4. Git Tags Graph - Level completion markers
        tags_graph = self._build_tags_graph(context)
        graphs.append(tags_graph)
        
        return graphs
    
    def build_stable_function_graph(self, org: str, repo: str, functions: List[FunctionInfo]) -> BuiltGraph:
        """
        🟡 Build stable function identities graph - The eternal dots!
        
        These are the permanent function identities that never disappear, 
        even when implementations change. Like PAC-MAN dots that always
        exist in the same maze positions, regardless of the game level.
        """
        graph_uri = self.schemas.get_stable_functions_uri(org, repo)
        logger.info(f"🟡 Building stable dots at {graph_uri}")
        
        triples = []
        stable_function_uris = set()
        
        for func in functions:
            # Create stable function identity URI - the permanent dot location
            stable_uri = self.schemas.get_stable_function_uri(org, repo, func.name)
            stable_function_uris.add(stable_uri)
            
            # Basic stable identity triples - dot properties that never change
            triples.extend([
                f"<{stable_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.webofcode.org/woc/Function> .",
                f'<{stable_uri}> <http://rdf.webofcode.org/woc/canonicalName> "{func.name}" .',
                f'<{stable_uri}> <http://rdf.webofcode.org/woc/module> "{func.location.module_name or "unknown"}" .',
                f'<{stable_uri}> <http://Repolex.org/githubUrl> "https://github.com/{org}/{repo}" .',
            ])
            
            # Track when this dot first appeared in the maze
            # TODO: These fields are not yet implemented in the new model
            # first_appeared_in and exists_in_versions need temporal tracking
            
            # Note: Stable functions don't track specific versions - that's for implementation graphs
        
        # Store the dots in the maze
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"✅ Placed {len(stable_function_uris)} eternal dots in the maze!")
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.FUNCTIONS_STABLE,
            triple_count=len(triples),
            entity_count=len(stable_function_uris),
            metadata=GraphMetadata(
                description="Stable function identities - PAC-MAN's eternal dots",
                build_time=datetime.now(),
                source_data_count=len(functions)
            )
        )
    
    def build_implementation_graph(self, org: str, repo: str, release: str, functions: List[FunctionInfo]) -> BuiltGraph:
        """
        🟡 Build implementation graph - Version-specific power pellets!
        
        These are the release-specific function implementations that can change
        between versions. Like power pellets that might move position or change
        power between PAC-MAN levels, but the dots stay in the same place.
        """
        graph_uri = self.schemas.get_function_graph_uris(org, repo)["implementations"]
        logger.info(f"🟡 Building power pellets for level {release} at {graph_uri}")
        
        triples = []
        implementation_uris = set()
        
        for func in functions:
            # Create version-specific implementation URI - the power pellet
            stable_uri = self.schemas.get_stable_function_uri(org, repo, func.name)
            impl_uri = f"{stable_uri}#{release}"
            implementation_uris.add(impl_uri)
            
            # Link implementation to stable identity - pellet connects to dot
            triples.extend([
                f"<{impl_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.webofcode.org/woc/MethodImplementation> .",
                f"<{impl_uri}> <http://rdf.webofcode.org/woc/implementsFunction> <{stable_uri}> .",
                f'<{impl_uri}> <http://rdf.webofcode.org/woc/belongsToVersion> "{release}" .',
            ])
            
            # Function signature - the power pellet's current form
            if func.signature:
                triples.append(
                    f'<{impl_uri}> <http://rdf.webofcode.org/woc/hasSignature> "{self._escape_turtle_string(func.signature)}" .'
                )
            
            # Docstring - the power pellet's description
            if func.docstring:
                triples.append(
                    f'<{impl_uri}> <http://www.w3.org/2000/01/rdf-schema#comment> "{self._escape_turtle_string(func.docstring)}" .'
                )
            
            # File location - where the power pellet is found in this level
            if func.location.file_path:
                file_uri = f"<{self.schemas.get_file_uri(org, repo, release, func.location.file_path)}>"
                triples.extend([
                    f'<{impl_uri}> <http://rdf.webofcode.org/woc/definedInFile> "{func.location.file_path}" .',
                    f'<{impl_uri}> <http://rdf.webofcode.org/woc/startLine> "{func.location.start_line or 0}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
                    f'<{impl_uri}> <http://rdf.webofcode.org/woc/endLine> "{func.location.end_line or 0}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
                ])
                
                # GitHub link - direct path to the power pellet
                github_link = f"https://github.com/{org}/{repo}/blob/{release}/{func.location.file_path}"
                if func.location.start_line and func.location.end_line:
                    github_link += f"#L{func.location.start_line}-L{func.location.end_line}"
                elif func.location.start_line:
                    github_link += f"#L{func.location.start_line}"
                
                triples.append(
                    f'<{impl_uri}> <http://rdf.webofcode.org/woc/githubLink> "{github_link}" .'
                )
            
            # Parameters - the power pellet's special abilities
            for param in func.parameters:
                param_uri = f"{impl_uri}/param_{param.name}"
                triples.extend([
                    f"<{param_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdf.webofcode.org/woc/Parameter> .",
                    f"<{impl_uri}> <http://rdf.webofcode.org/woc/hasParameter> <{param_uri}> .",
                    f'<{param_uri}> <http://rdf.webofcode.org/woc/hasName> "{param.name}" .',
                ])
                
                if param.type_annotation:
                    triples.append(
                        f'<{param_uri}> <http://rdf.webofcode.org/woc/hasType> "{param.type_annotation}" .'
                    )
                
                if param.default_value is not None:
                    triples.append(
                        f'<{param_uri}> <http://rdf.webofcode.org/woc/hasDefault> "{param.default_value}" .'
                    )
                
                triples.append(
                    f'<{param_uri}> <http://rdf.webofcode.org/woc/isRequired> "{str(param.required).lower()}"^^<http://www.w3.org/2001/XMLSchema#boolean> .'
                )
            
            # Return type - what you get when you eat this power pellet
            if func.return_type:
                triples.append(
                    f'<{impl_uri}> <http://rdf.webofcode.org/woc/hasReturnType> "{func.return_type}" .'
                )
            
            # Visibility - can PAC-MAN see this power pellet?
            visibility = "public" if not func.name.startswith("_") else "private"
            triples.append(
                f'<{impl_uri}> <http://rdf.webofcode.org/woc/hasVisibility> "{visibility}" .'
            )
        
        # Store the power pellets in the maze level
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"✅ Placed {len(implementation_uris)} power pellets in level {release}!")
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.FUNCTIONS_IMPL,
            triple_count=len(triples),
            entity_count=len(implementation_uris),
            metadata=GraphMetadata(
                description=f"Function implementations for {release} - PAC-MAN's power pellets",
                build_time=datetime.now(),
                source_data_count=len(functions),
                version=release
            )
        )
    
    def build_git_intelligence_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """
        🟡 Build git intelligence graphs - Ghost movement patterns!
        
        Tracks how the ghosts (developers) move through the maze (codebase),
        when they make changes, and their behavioral patterns.
        """
        if not context.git_data:
            logger.warning("👻 No ghost data available - skipping ghost intelligence graphs")
            return []
        
        graphs = []
        
        # 1. Commits Graph - Individual ghost movements
        commits_graph = self._build_commits_graph(context)
        graphs.append(commits_graph)
        
        # 2. Developers Graph - Ghost profiles and stats
        developers_graph = self._build_developers_graph(context)
        graphs.append(developers_graph)
        
        # 3. Branches Graph - Ghost territories
        branches_graph = self._build_branches_graph(context)
        graphs.append(branches_graph)
        
        # 4. Tags Graph - Level completion markers
        tags_graph = self._build_tags_graph(context)
        graphs.append(tags_graph)
        
        return graphs
    
    def _build_commits_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build commits graph - Individual ghost movements"""
        graph_uri = self.schemas.get_git_commits_uri(context.org, context.repo)
        logger.info(f"👻 Tracking ghost movements at {graph_uri}")
        
        triples = []
        commit_uris = set()
        
        for commit in context.git_data.commits:
            commit_uri = self.schemas.get_commit_uri(context.org, context.repo, commit.commit_hash)
            commit_uris.add(commit_uri)
            
            # Basic commit info - ghost movement record
            triples.extend([
                f"<{commit_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/git/Commit> .",
                f'<{commit_uri}> <http://Repolex.org/git/sha> "{commit.commit_hash}" .',
                f'<{commit_uri}> <http://Repolex.org/git/message> "{self._escape_turtle_string(commit.message)}" .',
                f'<{commit_uri}> <http://Repolex.org/git/date> "{commit.commit_date.isoformat()}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .',
            ])
            
            # Author - which ghost made this movement
            if commit.author_name and commit.author_email:
                author_uri = self.schemas.get_developer_uri(context.org, context.repo, commit.author_email)
                triples.extend([
                    f"<{commit_uri}> <http://Repolex.org/git/author> <{author_uri}> .",
                    f'<{commit_uri}> <http://Repolex.org/git/authorName> "{self._escape_turtle_string(commit.author_name)}" .',
                    f'<{commit_uri}> <http://Repolex.org/git/authorEmail> "{commit.author_email}" .',
                ])
            
            # Files modified - which maze sections the ghost touched
            for file_path in commit.files_modified:
                triples.append(
                    f'<{commit_uri}> <http://Repolex.org/git/modifiesFile> "{file_path}" .'
                )
            
            # Functions affected - which dots/pellets the ghost interacted with
            # TODO: Implement function-level change tracking
            # This would require parsing the commit diffs to identify which functions were changed
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"👻 Recorded {len(commit_uris)} ghost movements!")
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.GIT_COMMITS,
            triple_count=len(triples),
            entity_count=len(commit_uris),
            metadata=GraphMetadata(
                description="Git commits - Ghost movement patterns",
                build_time=datetime.now(),
                source_data_count=len(context.git_data.commits)
            )
        )
    
    def _build_developers_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build developers graph - Ghost profiles and statistics"""
        graph_uri = self.schemas.get_git_developers_uri(context.org, context.repo)
        logger.info(f"👻 Building ghost profiles at {graph_uri}")
        
        triples = []
        developer_uris = set()
        
        for developer in context.git_data.developers:
            dev_uri = self.schemas.get_developer_uri(context.org, context.repo, developer.email)
            developer_uris.add(dev_uri)
            
            # Basic ghost profile
            triples.extend([
                f"<{dev_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/git/Developer> .",
                f'<{dev_uri}> <http://Repolex.org/git/name> "{self._escape_turtle_string(developer.name)}" .',
                f'<{dev_uri}> <http://Repolex.org/git/email> "{developer.email}" .',
                f'<{dev_uri}> <http://Repolex.org/git/commitCount> "{developer.total_commits}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
                f'<{dev_uri}> <http://Repolex.org/git/firstCommit> "{developer.first_commit.isoformat()}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .',
                f'<{dev_uri}> <http://Repolex.org/git/lastCommit> "{developer.last_commit.isoformat()}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .',
            ])
            
            # Ghost specializations - which parts of the maze they prefer
            for expertise_area in developer.expertise_areas:
                triples.append(
                    f'<{dev_uri}> <http://Repolex.org/git/hasExpertiseIn> "{expertise_area}" .'
                )
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"👻 Profiled {len(developer_uris)} ghosts!")
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.GIT_DEVELOPERS,
            triple_count=len(triples),
            entity_count=len(developer_uris),
            metadata=GraphMetadata(
                description="Git developers - Ghost profiles and stats",
                build_time=datetime.now(),
                source_data_count=len(context.git_data.developers)
            )
        )
    
    def _build_file_structure_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build file structure graphs - The maze layout for this level"""
        graph_uri = self.schemas.get_file_structure_uri(context.org, context.repo, context.release)
        logger.info(f"🗺️ Mapping maze layout for level {context.release} at {graph_uri}")
        
        triples = []
        file_uris = set()
        
        for file_info in context.parsed_data.files:
            file_uri = self.schemas.get_file_uri(context.org, context.repo, context.release, file_info.file_path)
            file_uris.add(file_uri)
            
            # Basic file info - maze section properties
            triples.extend([
                f"<{file_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/files/PythonFile> .",
                f'<{file_uri}> <http://Repolex.org/files/path> "{file_info.file_path}" .',
                f'<{file_uri}> <http://Repolex.org/files/lineCount> "{file_info.line_count}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
            ])
            
            # GitHub link - direct access to this maze section
            github_url = f"https://github.com/{context.org}/{context.repo}/blob/{context.release}/{file_info.file_path}"
            triples.append(
                f'<{file_uri}> <http://Repolex.org/files/githubUrl> "{github_url}" .'
            )
            
            # Functions contained - which dots/pellets are in this maze section
            for func in file_info.functions:
                impl_uri = f"{self.schemas.get_stable_function_uri(context.org, context.repo, func.name)}#{context.release}"
                triples.append(
                    f"<{file_uri}> <http://Repolex.org/files/containsFunction> <{impl_uri}> ."
                )
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"🗺️ Mapped {len(file_uris)} maze sections for level {context.release}!")
        
        return [BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.FILES_STRUCTURE,
            triple_count=len(triples),
            entity_count=len(file_uris),
            metadata=GraphMetadata(
                description=f"File structure for {context.release} - Maze layout",
                build_time=datetime.now(),
                source_data_count=len(context.parsed_data.files),
                version=context.release
            )
        )]
    
    def _build_abc_events_graph(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build ABC events graph - Game history log"""
        graph_uri = self.schemas.get_abc_events_uri(context.org, context.repo)
        logger.info(f"📜 Recording game history at {graph_uri}")
        
        triples = []
        
        # If we have previous release data, generate change events
        if context.previous_release_data:
            change_events = self._detect_changes(context.parsed_data, context.previous_release_data)
            
            for event in change_events:
                event_uri = f"{graph_uri}#{event.event_id}"
                
                triples.extend([
                    f"<{event_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/abc/Event> .",
                    f'<{event_uri}> <http://Repolex.org/abc/eventType> "{event.event_type}" .',
                    f'<{event_uri}> <http://Repolex.org/abc/timestamp> "{event.timestamp.isoformat()}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .',
                ])
                
                # Link to affected function (stable identity)
                if event.affected_function:
                    stable_uri = self.schemas.get_stable_function_uri(context.org, context.repo, event.affected_function)
                    triples.append(
                        f"<{event_uri}> <http://Repolex.org/abc/affects> <{stable_uri}> ."
                    )
        
        # Always record the processing event for this release
        processing_event_uri = f"{graph_uri}#processing_{context.release}_{int(datetime.now().timestamp())}"
        triples.extend([
            f"<{processing_event_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/abc/Event> .",
            f'<{processing_event_uri}> <http://Repolex.org/abc/eventType> "repository_processed" .',
            f'<{processing_event_uri}> <http://Repolex.org/abc/version> "{context.release}" .',
            f'<{processing_event_uri}> <http://Repolex.org/abc/timestamp> "{datetime.now().isoformat()}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .',
            f'<{processing_event_uri}> <http://Repolex.org/abc/functionsProcessed> "{len(context.parsed_data.all_functions)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
        ])
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"📜 Recorded game history with {len(triples)} events!")
        
        return [BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.ABC_EVENTS,
            triple_count=len(triples),
            entity_count=1,  # At least the processing event
            metadata=GraphMetadata(
                description="ABC events - Game history log",
                build_time=datetime.now(),
                source_data_count=len(context.parsed_data.all_functions)
            )
        )]
    
    def _build_evolution_analysis_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build evolution analysis graphs - Strategy analytics"""
        graphs = []
        
        # 1. Analysis Graph - Pattern recognition
        analysis_graph = self._build_analysis_graph(context)
        graphs.append(analysis_graph)
        
        # 2. Statistics Graph - Score keeping
        stats_graph = self._build_statistics_graph(context)
        graphs.append(stats_graph)
        
        # 3. Patterns Graph - Gameplay insights
        patterns_graph = self._build_patterns_graph(context)
        graphs.append(patterns_graph)
        
        return graphs
    
    def _build_processing_metadata_graphs(self, context: GraphBuildContext) -> List[BuiltGraph]:
        """Build processing metadata graphs - Level completion stats"""
        graph_uri = self.schemas.get_processing_metadata_uri(context.org, context.repo, context.release)
        logger.info(f"📊 Recording level completion stats at {graph_uri}")
        
        triples = []
        
        # Processing metadata
        metadata_uri = f"{graph_uri}#metadata"
        triples.extend([
            f"<{metadata_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/meta/ProcessingMetadata> .",
            f'<{metadata_uri}> <http://Repolex.org/meta/version> "{context.release}" .',
            f'<{metadata_uri}> <http://Repolex.org/meta/processedAt> "{datetime.now().isoformat()}"^^<http://www.w3.org/2001/XMLSchema#dateTime> .',
            f'<{metadata_uri}> <http://Repolex.org/meta/functionsFound> "{len(context.parsed_data.all_functions)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
            f'<{metadata_uri}> <http://Repolex.org/meta/filesProcessed> "{len(context.parsed_data.files)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
        ])
        
        # Calculate level difficulty (PAC-MAN scoring)
        public_functions = [f for f in context.parsed_data.all_functions if not f.name.startswith('_')]
        complexity_score = len(public_functions) * 10 + len(context.parsed_data.files) * 5
        
        triples.extend([
            f'<{metadata_uri}> <http://Repolex.org/meta/publicFunctions> "{len(public_functions)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
            f'<{metadata_uri}> <http://Repolex.org/meta/complexityScore> "{complexity_score}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
        ])
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        logger.info(f"📊 Level {context.release} completed! Complexity score: {complexity_score}")
        
        return [BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.PROCESSING_META,
            triple_count=len(triples),
            entity_count=1,
            metadata=GraphMetadata(
                description=f"Processing metadata for {context.release} - Level completion stats",
                build_time=datetime.now(),
                source_data_count=len(context.parsed_data.all_functions),
                version=context.release
            )
        )]
    
    # Helper methods for the maze construction process
    
    def _build_woc_ontology_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build Web of Code ontology graph - Fundamental maze structure"""
        graph_uri = self.schemas.get_woc_ontology_uri()
        
        # Basic Web of Code ontology triples
        triples = [
            "<http://rdf.webofcode.org/woc/Function> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://rdf.webofcode.org/woc/MethodImplementation> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://rdf.webofcode.org/woc/Parameter> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://rdf.webofcode.org/woc/hasName> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#DatatypeProperty> .",
            "<http://rdf.webofcode.org/woc/hasSignature> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#DatatypeProperty> .",
            "<http://rdf.webofcode.org/woc/implementsFunction> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .",
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.ONTOLOGY_WOC,
            triple_count=len(triples),
            entity_count=6,
            metadata=GraphMetadata(
                description="Web of Code ontology - Fundamental maze structure",
                build_time=datetime.now(),
                source_data_count=6  # Number of ontology classes defined
            )
        )
    
    def _build_git_ontology_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build Git ontology graph - Ghost behavior rules"""
        graph_uri = self.schemas.get_git_ontology_uri()
        
        triples = [
            "<http://Repolex.org/git/Commit> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://Repolex.org/git/Developer> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://Repolex.org/git/author> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .",
            "<http://Repolex.org/git/sha> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#DatatypeProperty> .",
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.GIT_ONTOLOGY,
            triple_count=len(triples),
            entity_count=4,
            metadata=GraphMetadata(
                description="Git ontology - Ghost behavior rules",
                build_time=datetime.now(),
                source_data_count=5  # Number of git ontology classes defined
            )
        )
    
    def _build_evolution_ontology_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build Evolution ontology graph - Game progression rules"""
        graph_uri = self.schemas.get_evolution_ontology_uri()
        
        triples = [
            "<http://Repolex.org/evolution/FunctionChange> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://Repolex.org/evolution/AnalysisResult> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://Repolex.org/evolution/changeFrequency> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#DatatypeProperty> .",
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.EVOLUTION_ONTOLOGY,
            triple_count=len(triples),
            entity_count=3,
            metadata=GraphMetadata(
                description="Evolution ontology - Game progression rules",
                build_time=datetime.now(),
                source_data_count=4  # Number of evolution ontology classes defined
            )
        )
    
    def _build_files_ontology_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build Files ontology graph - Maze layout rules"""
        graph_uri = self.schemas.get_files_ontology_uri()
        
        triples = [
            "<http://Repolex.org/files/PythonFile> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .",
            "<http://Repolex.org/files/path> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#DatatypeProperty> .",
            "<http://Repolex.org/files/containsFunction> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .",
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.FILES_ONTOLOGY,
            triple_count=len(triples),
            entity_count=3,
            metadata=GraphMetadata(
                description="Files ontology - Maze layout rules",
                build_time=datetime.now(),
                source_data_count=3  # Number of file ontology classes defined
            )
        )
    
    def _build_branches_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build branches graph - Ghost territories"""
        graph_uri = self.schemas.get_git_branches_uri(context.org, context.repo)
        
        # Placeholder implementation - would need branch data
        triples = [
            f'<{graph_uri}#main> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/git/Branch> .',
            f'<{graph_uri}#main> <http://Repolex.org/git/name> "main" .',
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.GIT_BRANCHES,
            triple_count=len(triples),
            entity_count=1,
            metadata=GraphMetadata(
                description="Git branches - Ghost territories",
                build_time=datetime.now(),
                source_data_count=len(context.git_data.branches) if context.git_data and hasattr(context.git_data, 'branches') else 0
            )
        )
    
    def _build_tags_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build tags graph - Level completion markers"""
        graph_uri = self.schemas.get_git_tags_uri(context.org, context.repo)
        
        triples = [
            f'<{graph_uri}#{context.release}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/git/Tag> .',
            f'<{graph_uri}#{context.release}> <http://Repolex.org/git/name> "{context.release}" .',
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.GIT_TAGS,
            triple_count=len(triples),
            entity_count=1,
            metadata=GraphMetadata(
                description="Git tags - Level completion markers",
                build_time=datetime.now(),
                source_data_count=len(context.git_data.tags) if context.git_data and hasattr(context.git_data, 'tags') else 0
            )
        )
    
    def _build_analysis_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build analysis graph - Pattern recognition"""
        graph_uri = self.schemas.get_evolution_analysis_uri(context.org, context.repo)
        
        # Basic analysis placeholder
        triples = [
            f'<{graph_uri}#analysis> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/evolution/AnalysisResult> .',
            f'<{graph_uri}#analysis> <http://Repolex.org/evolution/version> "{context.release}" .',
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.EVOLUTION_ANALYSIS,
            triple_count=len(triples),
            entity_count=1,
            metadata=GraphMetadata(
                description="Evolution analysis - Pattern recognition",
                build_time=datetime.now(),
                source_data_count=len(context.parsed_data.all_functions)
            )
        )
    
    def _build_statistics_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build statistics graph - Score keeping"""
        graph_uri = self.schemas.get_evolution_statistics_uri(context.org, context.repo)
        
        # Calculate basic statistics
        public_funcs = [f for f in context.parsed_data.all_functions if not f.name.startswith('_')]
        private_funcs = [f for f in context.parsed_data.all_functions if f.name.startswith('_')]
        
        triples = [
            f'<{graph_uri}#stats> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/evolution/Statistics> .',
            f'<{graph_uri}#stats> <http://Repolex.org/evolution/publicFunctionCount> "{len(public_funcs)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
            f'<{graph_uri}#stats> <http://Repolex.org/evolution/privateFunctionCount> "{len(private_funcs)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
            f'<{graph_uri}#stats> <http://Repolex.org/evolution/totalFunctionCount> "{len(context.parsed_data.all_functions)}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
        ]
        
        self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.EVOLUTION_STATS,
            triple_count=len(triples),
            entity_count=1,
            metadata=GraphMetadata(
                description="Evolution statistics - Score keeping",
                build_time=datetime.now(),
                source_data_count=len(context.parsed_data.all_functions)
            )
        )
    
    def _build_patterns_graph(self, context: GraphBuildContext) -> BuiltGraph:
        """Build patterns graph - Gameplay insights"""
        graph_uri = self.schemas.get_evolution_patterns_uri(context.org, context.repo)
        
        # Analyze patterns in function names
        patterns = {}
        for func in context.parsed_data.all_functions:
            if '_' in func.name:
                pattern = func.name.split('_')[0]
                patterns[pattern] = patterns.get(pattern, 0) + 1
        
        triples = []
        for pattern, count in patterns.items():
            if count > 1:  # Only patterns that appear multiple times
                pattern_uri = f"{graph_uri}#pattern_{pattern}"
                triples.extend([
                    f"<{pattern_uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://Repolex.org/evolution/Pattern> .",
                    f'<{pattern_uri}> <http://Repolex.org/evolution/patternName> "{pattern}" .',
                    f'<{pattern_uri}> <http://Repolex.org/evolution/frequency> "{count}"^^<http://www.w3.org/2001/XMLSchema#integer> .',
                ])
        
        if triples:
            self.oxigraph.insert_triples(graph_uri, triples)
        
        return BuiltGraph(
            graph_uri=graph_uri,
            graph_type=GraphType.EVOLUTION_PATTERNS,
            triple_count=len(triples),
            entity_count=len(patterns),
            metadata=GraphMetadata(
                description="Evolution patterns - Gameplay insights",
                build_time=datetime.now(),
                source_data_count=len(context.parsed_data.all_functions)
            )
        )
    
    def _detect_changes(self, current_data: ParsedRepository, previous_data: ParsedRepository) -> List[Any]:
        """Detect changes between releases - PAC-MAN level transitions"""
        changes = []
        
        # Compare function lists
        current_func_names = {f.name for f in current_data.functions}
        previous_func_names = {f.name for f in previous_data.functions}
        
        # New functions (new dots appeared!)
        new_functions = current_func_names - previous_func_names
        for func_name in new_functions:
            changes.append({
                'event_id': f"function_added_{func_name}",
                'event_type': 'function_added',
                'affected_function': func_name,
                'timestamp': datetime.now()
            })
        
        # Removed functions (dots disappeared!)
        removed_functions = previous_func_names - current_func_names
        for func_name in removed_functions:
            changes.append({
                'event_id': f"function_removed_{func_name}",
                'event_type': 'function_removed',
                'affected_function': func_name,
                'timestamp': datetime.now()
            })
        
        return changes
    
    def _escape_turtle_string(self, text: str) -> str:
        """Escape string for Turtle format"""
        if not text:
            return ""
        
        # Basic escaping for Turtle format
        return (text.replace('\\', '\\\\')
                   .replace('"', '\\"')
                   .replace('\n', '\\n')
                   .replace('\r', '\\r')
                   .replace('\t', '\\t'))


# PAC-MAN themed imports for the models that need to be implemented
class ProcessingError(Exception):
    """PAC-MAN got caught by a ghost during processing!"""
    pass
