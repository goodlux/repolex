"""🟡 PAC-MAN Graph Data Models

Data models for semantic graphs, graph URIs, and PAC-MAN's graph intelligence.
These models represent the 19 different graph types in the semantic maze!
"""

from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum


class GraphType(str, Enum):
    """🧠 Types of semantic graphs in PAC-MAN's maze."""
    
    # Ontology graphs (4 types)
    ONTOLOGY_WOC = "ontology_woc"              # 🔬 Web of Code ontology
    ONTOLOGY_GIT = "ontology_git"              # 🔄 Git concepts ontology
    ONTOLOGY_EVOLUTION = "ontology_evolution"  # 📈 Evolution concepts
    ONTOLOGY_FILES = "ontology_files"          # 📁 File system concepts
    
    # Alternative naming (for backward compatibility)
    GIT_ONTOLOGY = "ontology_git"              # 🔄 Same as ONTOLOGY_GIT
    EVOLUTION_ONTOLOGY = "ontology_evolution"  # 📈 Same as ONTOLOGY_EVOLUTION  
    FILES_ONTOLOGY = "ontology_files"          # 📁 Same as ONTOLOGY_FILES
    
    # Function graphs (2 types)
    FUNCTIONS_STABLE = "functions_stable"      # 🟡 Stable function identities
    FUNCTIONS_IMPL = "functions_impl"          # 🔧 Version-specific implementations
    
    # File structure graphs (per version)
    FILES_STRUCTURE = "files_structure"       # 📂 File paths and line numbers
    
    # Git intelligence graphs (4 types)
    GIT_COMMITS = "git_commits"                # 📝 Commit history
    GIT_DEVELOPERS = "git_developers"          # 👥 Developer profiles
    GIT_BRANCHES = "git_branches"              # 🌿 Branch information
    GIT_TAGS = "git_tags"                      # 🏷️ Version tags and releases
    
    # ABC events graph (1 type)
    ABC_EVENTS = "abc_events"                  # ⏰ Temporal change events
    
    # Evolution analysis graphs (3 types)
    EVOLUTION_ANALYSIS = "evolution_analysis"  # 📊 Change analysis
    EVOLUTION_STATS = "evolution_stats"        # 📈 Stability metrics
    EVOLUTION_PATTERNS = "evolution_patterns"  # 🔗 Co-change patterns
    
    # Processing metadata graphs (per version)
    PROCESSING_META = "processing_meta"        # 🔧 Processing timestamps
    
    # 🛸 Text analysis graphs (10 types) - Where No LLM Has Gone Before!
    TEXT_ENTITIES = "text_entities"            # 👽 Extracted entities
    TEXT_RELATIONSHIPS = "text_relationships"  # 🔗 Entity relationships
    TEXT_CONTENT = "text_content"              # 📄 Document structure
    TEXT_TOPICS = "text_topics"                # 🎯 Content topics


class GraphStatus(str, Enum):
    """📊 Status of individual graphs."""
    EMPTY = "empty"            # 🔲 Graph exists but has no data
    BUILDING = "building"      # 🔄 Currently being built
    READY = "ready"            # ✅ Ready for queries
    UPDATING = "updating"      # 🔄 Being updated/rebuilt
    ERROR = "error"            # ❌ Error in graph
    CORRUPTED = "corrupted"    # 💥 Graph data is corrupted


class GraphInfo(BaseModel):
    """📊 Basic information about a semantic graph."""
    
    # Graph identification
    graph_uri: str = Field(description="🔗 Complete graph URI")
    graph_type: GraphType = Field(description="🧠 Type of semantic graph")
    org_repo: str = Field(description="📚 Repository identifier")
    version: Optional[str] = Field(default=None, description="🏷️ Version (if version-specific)")
    
    # Graph status
    status: GraphStatus = Field(description="📊 Current graph status")
    created_at: datetime = Field(description="⏰ When PAC-MAN created this graph")
    updated_at: datetime = Field(description="🔄 Last update time")
    
    # Statistics
    triple_count: int = Field(default=0, description="🔢 Number of RDF triples")
    size_bytes: int = Field(default=0, description="💾 Storage size in bytes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "graph_uri": "http://repolex.org/repo/pixeltable/pixeltable/functions/stable",
                "graph_type": "functions_stable",
                "org_repo": "pixeltable/pixeltable",
                "status": "ready",
                "triple_count": 1247,
                "size_bytes": 124800
            }
        }


class GraphDetails(BaseModel):
    """🔍 Detailed information about semantic graphs."""
    
    # Basic info
    org_repo: str = Field(description="📚 Repository identifier")
    version: Optional[str] = Field(default=None, description="🏷️ Version filter")
    
    # Graph breakdown
    graphs: List[GraphInfo] = Field(default_factory=list, description="📊 Individual graphs")
    total_graphs: int = Field(description="🔢 Total number of graphs")
    total_triples: int = Field(description="🔢 Total RDF triples across all graphs")
    total_size_mb: float = Field(description="💾 Total storage size in MB")
    
    # Graph type breakdown
    ontology_graphs: int = Field(default=0, description="🔬 Number of ontology graphs")
    function_graphs: int = Field(default=0, description="🟡 Number of function graphs")
    git_graphs: int = Field(default=0, description="🔄 Number of git intelligence graphs")
    evolution_graphs: int = Field(default=0, description="📈 Number of evolution graphs")
    file_graphs: int = Field(default=0, description="📁 Number of file structure graphs")
    
    # Processing info
    last_processed: Optional[datetime] = Field(default=None, description="⏰ Last processing time")
    processing_duration: Optional[float] = Field(default=None, description="⏱️ Last processing duration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "org_repo": "pixeltable/pixeltable", 
                "total_graphs": 19,
                "total_triples": 125000,
                "total_size_mb": 12.5,
                "ontology_graphs": 4,
                "function_graphs": 2,
                "git_graphs": 4
            }
        }


class GraphURISet(BaseModel):
    """🔗 Complete set of graph URIs for a repository."""
    
    # Repository info
    org: str = Field(description="📚 Organization name")
    repo: str = Field(description="📚 Repository name")
    version: Optional[str] = Field(default=None, description="🏷️ Version (for version-specific graphs)")
    
    # Ontology graph URIs (4)
    ontology_woc: str = Field(description="🔬 Web of Code ontology URI")
    ontology_git: str = Field(description="🔄 Git ontology URI")  
    ontology_evolution: str = Field(description="📈 Evolution ontology URI")
    ontology_files: str = Field(description="📁 Files ontology URI")
    
    # Function graph URIs (2)
    functions_stable: str = Field(description="🟡 Stable function identities URI")
    functions_impl: str = Field(description="🔧 Function implementations URI")
    
    # File structure URI (version-specific)
    files_structure: Optional[str] = Field(default=None, description="📂 File structure URI")
    
    # Git intelligence URIs (4)
    git_commits: str = Field(description="📝 Git commits URI")
    git_developers: str = Field(description="👥 Git developers URI")
    git_branches: str = Field(description="🌿 Git branches URI")
    git_tags: str = Field(description="🏷️ Git tags URI")
    
    # ABC events URI (1)
    abc_events: str = Field(description="⏰ ABC events URI")
    
    # Evolution analysis URIs (3)
    evolution_analysis: str = Field(description="📊 Evolution analysis URI")
    evolution_stats: str = Field(description="📈 Evolution statistics URI")
    evolution_patterns: str = Field(description="🔗 Evolution patterns URI")
    
    # Processing metadata URI (version-specific)
    processing_meta: Optional[str] = Field(default=None, description="🔧 Processing metadata URI")
    
    def get_all_uris(self) -> List[str]:
        """🔗 Get all graph URIs as a list."""
        uris = [
            self.ontology_woc,
            self.ontology_git,
            self.ontology_evolution,
            self.ontology_files,
            self.functions_stable,
            self.functions_impl,
            self.git_commits,
            self.git_developers,
            self.git_branches,
            self.git_tags,
            self.abc_events,
            self.evolution_analysis,
            self.evolution_stats,
            self.evolution_patterns,
        ]
        
        # Add version-specific URIs if they exist
        if self.files_structure:
            uris.append(self.files_structure)
        if self.processing_meta:
            uris.append(self.processing_meta)
            
        return uris
    
    def get_version_specific_uris(self) -> List[str]:
        """🏷️ Get only version-specific graph URIs."""
        uris = []
        if self.files_structure:
            uris.append(self.files_structure)
        if self.processing_meta:
            uris.append(self.processing_meta)
        return uris
    
    def get_stable_uris(self) -> List[str]:
        """🟡 Get stable (non-version-specific) graph URIs."""
        return [
            self.ontology_woc,
            self.ontology_git,
            self.ontology_evolution,
            self.ontology_files,
            self.functions_stable,
            self.git_commits,
            self.git_developers,
            self.git_branches,
            self.git_tags,
            self.abc_events,
            self.evolution_analysis,
            self.evolution_stats,
            self.evolution_patterns,
        ]


class GraphMetadata(BaseModel):
    """🟡 PAC-MAN's graph metadata - details about each semantic maze level!"""
    
    description: str = Field(..., description="Description of what this graph contains")
    build_time: datetime = Field(..., description="When this graph was built")
    source_data_count: int = Field(..., description="Number of source items processed")
    builder_version: Optional[str] = Field(None, description="Version of builder used")
    processing_time_seconds: Optional[float] = Field(None, description="Time taken to build")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BuiltGraph(BaseModel):
    """🟡 PAC-MAN's built graph result - a completed semantic maze level!"""
    
    graph_uri: str = Field(..., description="URI of the built graph")
    graph_type: GraphType = Field(..., description="Type of graph that was built")
    triple_count: int = Field(..., description="Number of RDF triples in the graph")
    entity_count: int = Field(..., description="Number of entities in the graph")
    metadata: GraphMetadata = Field(..., description="Metadata about the graph build")
    success: bool = Field(True, description="Whether the build was successful")
    error_message: Optional[str] = Field(None, description="Error message if build failed")
    
    def __str__(self) -> str:
        return f"🟡 {self.graph_type.value}: {self.triple_count} triples, {self.entity_count} entities"


class GraphQuery(BaseModel):
    """🔍 Query information for graph operations."""
    
    # Query details
    sparql_query: str = Field(description="📝 SPARQL query string")
    graph_uris: List[str] = Field(description="🔗 Target graph URIs")
    
    # Execution details
    timeout_seconds: int = Field(default=30, description="⏰ Query timeout")
    limit: Optional[int] = Field(default=None, description="🔢 Result limit")
    
    # Results
    results: Optional[List[Dict[str, Any]]] = Field(default=None, description="📊 Query results")
    execution_time: Optional[float] = Field(default=None, description="⏱️ Execution time")
    error_message: Optional[str] = Field(default=None, description="❌ Error if query failed")


class GraphStatistics(BaseModel):
    """📈 Statistics about PAC-MAN's semantic graphs."""
    
    # Overall statistics
    total_repositories: int = Field(description="📚 Total repositories with graphs")
    total_graphs: int = Field(description="📊 Total number of graphs")
    total_triples: int = Field(description="🔢 Total RDF triples")
    total_size_mb: float = Field(description="💾 Total storage size")
    
    # Graph type breakdown
    graph_type_counts: Dict[str, int] = Field(
        default_factory=dict,
        description="📊 Count of each graph type"
    )
    
    # Performance metrics
    average_build_time: float = Field(description="⏱️ Average graph build time")
    successful_builds: int = Field(description="✅ Successful graph builds")
    failed_builds: int = Field(description="❌ Failed graph builds")
    success_rate: float = Field(description="📈 Build success rate")
    
    # Recent activity
    graphs_built_today: int = Field(default=0, description="🟡 Graphs built today")
    last_build_time: Optional[datetime] = Field(default=None, description="⏰ Last build time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_repositories": 15,
                "total_graphs": 285,
                "total_triples": 1250000,
                "total_size_mb": 125.5,
                "success_rate": 0.94,
                "graphs_built_today": 12
            }
        }


class GraphUpdateResult(BaseModel):
    """🔄 Result of graph update operations."""
    
    success: bool = Field(description="✅ Update succeeded")
    message: str = Field(description="💬 Human-readable result message")
    
    # Update details
    graph_uri: str = Field(description="🔗 Updated graph URI") 
    operation: str = Field(description="🔧 Operation performed")
    
    # Before/after statistics
    old_triple_count: int = Field(default=0, description="📊 Triples before update")
    new_triple_count: int = Field(default=0, description="📊 Triples after update")
    
    # Performance
    update_time: float = Field(description="⏱️ Update time in seconds")
    
    # Nuclear update safety
    cross_references_preserved: bool = Field(
        default=True,
        description="🛡️ Cross-graph references preserved"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "🟡 PAC-MAN successfully updated semantic graph!",
                "graph_uri": "http://repolex.org/repo/pixeltable/pixeltable/functions/impl",
                "operation": "nuclear_rebuild",
                "old_triple_count": 1200,
                "new_triple_count": 1247,
                "update_time": 3.2,
                "cross_references_preserved": True
            }
        }


class PAC_MAN_GraphMaze(BaseModel):
    """🟡 PAC-MAN's complete semantic maze representation."""
    
    # Maze info
    org_repo: str = Field(description="📚 Repository identifier")
    maze_name: str = Field(description="🟡 Human-readable maze name")
    
    # All graphs in the maze
    all_graphs: Dict[str, GraphInfo] = Field(
        default_factory=dict,
        description="📊 All graphs indexed by URI"
    )
    
    # Maze statistics
    total_dots_collected: int = Field(description="🔵 Total semantic dots (triples)")
    power_pills_available: int = Field(description="💊 Export files available")
    ghosts_encountered: int = Field(description="👻 Private functions found")
    maze_completion: float = Field(description="📈 Completion percentage")
    
    # PAC-MAN's path through the maze
    processing_path: List[str] = Field(
        default_factory=list,
        description="🟡 Order in which graphs were processed"
    )
    
    # Maze health
    corrupted_sections: List[str] = Field(
        default_factory=list,
        description="💥 Corrupted graph URIs"
    )
    blocked_paths: List[str] = Field(
        default_factory=list,
        description="🚧 Graphs that failed to build"
    )
    
    def get_maze_health_score(self) -> float:
        """🟡 Calculate overall maze health (0-1)."""
        if not self.all_graphs:
            return 0.0
        
        healthy_graphs = sum(
            1 for graph in self.all_graphs.values()
            if graph.status == GraphStatus.READY
        )
        
        return healthy_graphs / len(self.all_graphs)
    
    def get_waka_score(self) -> int:
        """🟡 Get PAC-MAN's waka-waka score!"""
        # Fun scoring based on semantic achievements
        score = 0
        score += self.total_dots_collected // 100  # 1 point per 100 triples
        score += self.power_pills_available * 50   # 50 points per export
        score += int(self.maze_completion * 1000)  # Up to 1000 points for completion
        return score
    
    class Config:
        json_schema_extra = {
            "example": {
                "org_repo": "pixeltable/pixeltable",
                "maze_name": "Pixeltable Semantic Maze",
                "total_dots_collected": 125000,
                "power_pills_available": 8,
                "ghosts_encountered": 45,
                "maze_completion": 0.87,
                "waka_score": 2650
            }
        }
