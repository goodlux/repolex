# 🟡 PAC-MAN CodeDoc Results Data Models 🟡
# waka waka waka - chomping through operation results!

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum


class ResultStatus(str, Enum):
    """PAC-MAN themed result statuses - nom nom nom!"""
    SUCCESS = "success"  # 🟡 Successfully chomped through the task!
    PARTIAL = "partial"  # 🟠 Some pellets missed, but still good!
    FAILED = "failed"    # 💥 Hit a ghost - operation failed!
    CANCELLED = "cancelled"  # 🚫 Player quit mid-game


class ProcessingPhase(str, Enum):
    """Different phases of semantic processing - like PAC-MAN levels!"""
    CLONING = "cloning"          # 🌀 Getting the maze ready
    PARSING = "parsing"          # 🟡 Chomping through the AST
    ANALYZING = "analyzing"      # 🧠 Finding the semantic patterns
    STORING = "storing"          # 💾 Saving all those delicious pellets
    INDEXING = "indexing"        # 📚 Organizing the power pellets
    EXPORTING = "exporting"      # 📤 Sharing the high score
    COMPLETE = "complete"        # 🏆 Level cleared!


class ProgressUpdate(BaseModel):
    """Real-time progress updates - like PAC-MAN score counter!"""
    phase: ProcessingPhase
    progress_percent: float = Field(ge=0, le=100)
    current_item: Optional[str] = None
    items_completed: int = 0
    items_total: int = 0
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

    def __str__(self) -> str:
        """PAC-MAN style progress display"""
        dots = "🟡" * int(self.progress_percent / 10)
        spaces = "⚫" * (10 - int(self.progress_percent / 10))
        return f"[{dots}{spaces}] {self.progress_percent:.1f}% - {self.message}"


class BaseResult(BaseModel):
    """Base result class - every PAC-MAN operation gets scored!"""
    status: ResultStatus
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    execution_time_seconds: Optional[float] = None
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    class Config:
        use_enum_values = True

    def add_warning(self, warning: str) -> None:
        """Add a warning - like eating a power pellet near a ghost! 🟠"""
        self.warnings.append(warning)

    def add_error(self, error: str) -> None:
        """Add an error - ouch, hit a ghost! 💥"""
        self.errors.append(error)
        if self.status == ResultStatus.SUCCESS:
            self.status = ResultStatus.PARTIAL

    def is_success(self) -> bool:
        """Did PAC-MAN clear the level? 🟡"""
        return self.status in [ResultStatus.SUCCESS, ResultStatus.PARTIAL]


# 📚 Repository Operation Results - Managing the PAC-MAN mazes!

class RepoResult(BaseResult):
    """Result from repository operations - found a new maze!"""
    org_repo: str
    repository_path: Optional[Path] = None
    releases: List[str] = Field(default_factory=list)
    latest_release: Optional[str] = None
    total_files: Optional[int] = None
    python_files: Optional[int] = None
    storage_size_mb: Optional[float] = None

    def get_pellet_count(self) -> int:
        """How many delicious code pellets did we find? 🟡"""
        return self.python_files or 0


class UpdateResult(BaseResult):
    """Result from repository updates - new pellets discovered!"""
    org_repo: str
    new_releases: List[str] = Field(default_factory=list)
    updated_files: List[str] = Field(default_factory=list)
    changes_detected: bool = False
    git_commits_behind: Optional[int] = None

    def has_new_pellets(self) -> bool:
        """Any new delicious code to chomp? 🟡"""
        return bool(self.new_releases or self.updated_files)


# 🧠 Graph Processing Results - Semantic PAC-MAN level completion!

class ProcessingResult(BaseResult):
    """Result from semantic analysis - how much of the maze did we chomp?"""
    org_repo: str
    release: str
    
    # Parsing stats - pellet counting!
    functions_found: int = 0
    classes_found: int = 0
    modules_found: int = 0
    files_processed: int = 0
    
    # Graph generation stats - power pellet creation!
    graphs_created: int = 0
    triples_generated: int = 0
    stable_identities_created: int = 0
    
    # Performance stats - PAC-MAN speed metrics!
    parsing_time_seconds: Optional[float] = None
    graph_build_time_seconds: Optional[float] = None
    storage_time_seconds: Optional[float] = None
    
    # Quality metrics - how clean was our chomp?
    parse_errors: int = 0
    docstring_coverage_percent: Optional[float] = None
    public_function_percent: Optional[float] = None

    def get_total_semantic_pellets(self) -> int:
        """Total semantic pellets chomped! 🟡"""
        return self.functions_found + self.classes_found + self.modules_found

    def get_performance_score(self) -> str:
        """PAC-MAN style performance rating! 🏆"""
        if not self.execution_time_seconds:
            return "⏱️ Unknown"
        
        pellets_per_second = self.get_total_semantic_pellets() / self.execution_time_seconds
        
        if pellets_per_second > 100:
            return "🟡 SUPER PAC-MAN! Lightning fast!"
        elif pellets_per_second > 50:
            return "🟠 Speedy! Nice chomping!"
        elif pellets_per_second > 20:
            return "🟢 Good pace, keep it up!"
        else:
            return "🔵 Steady chomping, but could be faster..."


# 📤 Export Results - Sharing the high scores!

class ExportResult(BaseResult):
    """Result from export operations - level completion rewards!"""
    org_repo: str
    release: str
    export_format: str
    output_path: Path
    file_size_bytes: Optional[int] = None
    compression_ratio: Optional[float] = None
    
    # Format-specific stats
    items_exported: int = 0
    export_time_seconds: Optional[float] = None

    def get_file_size_mb(self) -> float:
        """How big is our pellet package? 📦"""
        if self.file_size_bytes:
            return self.file_size_bytes / (1024 * 1024)
        return 0.0

    def get_compression_description(self) -> str:
        """How well did we compress our pellets? 🗜️"""
        if not self.compression_ratio:
            return "📦 No compression info"
        
        if self.compression_ratio > 100:
            return f"🟡 SUPER COMPRESSION! {self.compression_ratio:.0f}x smaller!"
        elif self.compression_ratio > 50:
            return f"🟠 Great compression: {self.compression_ratio:.0f}x"
        elif self.compression_ratio > 10:
            return f"🟢 Good compression: {self.compression_ratio:.0f}x"
        else:
            return f"🔵 Light compression: {self.compression_ratio:.1f}x"


# 🔍 Query Results - Finding the right pellets!

class QueryResult(BaseResult):
    """Result from SPARQL or semantic queries - pellet hunting results!"""
    query: str
    query_type: str = "sparql"  # "sparql", "function_search", "semantic"
    
    # Results data
    results: List[Dict[str, Any]] = Field(default_factory=list)
    result_count: int = 0
    
    # Performance
    query_time_seconds: Optional[float] = None
    graphs_searched: List[str] = Field(default_factory=list)
    
    # Formatting
    formatted_output: Optional[str] = None
    output_format: str = "table"  # "table", "json", "turtle", "csv"

    def get_pellet_hunt_success(self) -> str:
        """How successful was our pellet hunt? 🔍"""
        if self.result_count == 0:
            return "🚫 No pellets found - try a different maze!"
        elif self.result_count == 1:
            return "🟡 Found the perfect pellet!"
        elif self.result_count <= 10:
            return f"🟠 Found {self.result_count} tasty pellets!"
        elif self.result_count <= 100:
            return f"🟢 Pellet bonanza! {self.result_count} results!"
        else:
            return f"🔥 PELLET EXPLOSION! {self.result_count} results!"


class FunctionSearchResult(BaseModel):
    """Individual function found in search - a specific pellet! 🟡"""
    function_name: str
    signature: str
    repository: str
    release: Optional[str] = None
    description: Optional[str] = None
    relevance_score: float = Field(ge=0, le=1)
    module_path: Optional[str] = None
    github_link: Optional[str] = None

    def get_relevance_emoji(self) -> str:
        """How relevant is this pellet? 🎯"""
        if self.relevance_score >= 0.9:
            return "🟡 Perfect match!"
        elif self.relevance_score >= 0.7:
            return "🟠 Great match!"
        elif self.relevance_score >= 0.5:
            return "🟢 Good match"
        elif self.relevance_score >= 0.3:
            return "🔵 Okay match"
        else:
            return "⚪ Weak match"


# 📊 System Status Results - Overall PAC-MAN game state!

class SystemStatus(BaseModel):
    """Current system status - how's our PAC-MAN game going? 🎮"""
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Repository stats
    repository_count: int = 0
    total_releases: int = 0
    
    # Graph stats - our semantic maze!
    graph_count: int = 0
    total_triples: int = 0
    database_size_mb: float = 0.0
    
    # Export stats - achievements unlocked!
    export_count: int = 0
    export_size_mb: float = 0.0
    
    # Performance stats
    uptime: str = "0:00:00"
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    
    # Health indicators
    recent_errors: List[str] = Field(default_factory=list)
    storage_path: Optional[Path] = None
    last_successful_operation: Optional[datetime] = None

    def get_health_status(self) -> str:
        """Overall PAC-MAN health! 🟡"""
        error_count = len(self.recent_errors)
        
        if error_count == 0:
            return "🟡 PERFECT! All systems chomping smoothly!"
        elif error_count <= 3:
            return f"🟠 Mostly good, {error_count} minor ghost encounters"
        elif error_count <= 10:
            return f"🟢 Functional but {error_count} issues to watch"
        else:
            return f"🔴 Warning! {error_count} errors need attention!"

    def get_storage_description(self) -> str:
        """How much has PAC-MAN chomped and stored? 💾"""
        total_mb = self.database_size_mb + self.export_size_mb
        
        if total_mb < 10:
            return f"🟡 Compact: {total_mb:.1f}MB total storage"
        elif total_mb < 100:
            return f"🟠 Growing: {total_mb:.1f}MB semantic knowledge"
        elif total_mb < 1000:
            return f"🟢 Substantial: {total_mb:.1f}MB code intelligence"
        else:
            return f"🔥 MASSIVE: {total_mb:.1f}MB semantic empire!"


# 📈 Graph Detail Results - Deep maze analysis!

class GraphDetails(BaseModel):
    """Detailed information about semantic graphs - maze architecture! 🏗️"""
    org_repo: str
    release: Optional[str] = None
    
    # Graph breakdown - different maze sections!
    ontology_graphs: int = 0
    function_graphs: int = 0
    file_graphs: int = 0
    git_graphs: int = 0
    abc_graphs: int = 0
    evolution_graphs: int = 0
    metadata_graphs: int = 0
    
    # Content stats
    stable_functions: int = 0
    implementations: int = 0
    git_commits: int = 0
    abc_events: int = 0
    
    # Quality metrics
    processing_date: Optional[datetime] = None
    data_quality_score: Optional[float] = None
    completeness_percent: Optional[float] = None

    def get_graph_architecture_summary(self) -> str:
        """PAC-MAN maze layout summary! 🗺️"""
        total_graphs = (self.ontology_graphs + self.function_graphs + 
                       self.file_graphs + self.git_graphs + 
                       self.abc_graphs + self.evolution_graphs + 
                       self.metadata_graphs)
        
        return f"🏗️ {total_graphs}-graph semantic maze with {self.stable_functions} function pellets!"


class GraphInfo(BaseModel):
    """Information about a specific graph - maze section details! 📊"""
    graph_uri: str
    graph_type: str
    triple_count: int = 0
    size_mb: float = 0.0
    last_updated: Optional[datetime] = None
    status: str = "active"  # "active", "building", "error"

    def get_graph_description(self) -> str:
        """What kind of maze section is this? 🧩"""
        if self.triple_count == 0:
            return f"🚫 Empty {self.graph_type} section"
        elif self.triple_count < 1000:
            return f"🟡 Small {self.graph_type}: {self.triple_count} triples"
        elif self.triple_count < 10000:
            return f"🟠 Medium {self.graph_type}: {self.triple_count:,} triples"
        else:
            return f"🔥 Large {self.graph_type}: {self.triple_count:,} triples!"


# 🎯 Specialized Result Types for different operations

class ValidationResult(BaseResult):
    """Result from validation operations - making sure no ghosts in the code! 👻"""
    validated_item: str
    validation_type: str
    issues_found: List[str] = Field(default_factory=list)
    security_score: Optional[float] = None
    recommendations: List[str] = Field(default_factory=list)


class ConfigurationResult(BaseResult):
    """Result from configuration operations - setting up the PAC-MAN game! ⚙️"""
    config_key: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    config_file_path: Optional[Path] = None
    requires_restart: bool = False


# 🏆 Progress Callback Types for real-time updates!

ProgressCallback = Optional[callable]  # Function that takes ProgressUpdate

class ProgressTracker:
    """Tracks progress like PAC-MAN score keeper! 🏆"""
    
    def __init__(self, callback: ProgressCallback = None):
        self.callback = callback
        self.current_phase: Optional[ProcessingPhase] = None
        self.start_time = datetime.now()
    
    def update(self, 
               phase: ProcessingPhase,
               progress: float,
               message: str,
               current_item: Optional[str] = None,
               completed: int = 0,
               total: int = 0) -> None:
        """Update progress - PAC-MAN chomping through the maze! 🟡"""
        
        update = ProgressUpdate(
            phase=phase,
            progress_percent=progress,
            message=message,
            current_item=current_item,
            items_completed=completed,
            items_total=total
        )
        
        if self.callback:
            self.callback(update)
    
    def complete(self, message: str = "PAC-MAN level completed! 🏆") -> None:
        """Mark as complete - got all the pellets! 🟡"""
        self.update(ProcessingPhase.COMPLETE, 100.0, message)


# 🎮 Utility functions for PAC-MAN themed results!

def create_success_result(message: str, **kwargs) -> BaseResult:
    """Create a successful PAC-MAN result! 🟡"""
    return BaseResult(
        status=ResultStatus.SUCCESS,
        message=f"🟡 {message}",
        **kwargs
    )

def create_error_result(message: str, **kwargs) -> BaseResult:
    """Create a ghost-collision result! 💥"""
    return BaseResult(
        status=ResultStatus.FAILED,
        message=f"💥 {message}",
        **kwargs
    )

def format_duration(seconds: Optional[float]) -> str:
    """Format duration PAC-MAN style! ⏱️"""
    if not seconds:
        return "⏱️ Unknown time"
    
    if seconds < 1:
        return f"⚡ Lightning fast: {seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"🟡 Quick chomp: {seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"🟠 Steady pace: {minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"🔵 Marathon session: {hours}h {minutes}m"


class ParsedFile(BaseModel):
    """🟡 PAC-MAN's parsed file result - a single file worth of semantic dots!"""
    
    file_path: Path = Field(..., description="Path to the parsed file")
    functions: List[Dict[str, Any]] = Field(default_factory=list, description="Functions found")
    classes: List[Dict[str, Any]] = Field(default_factory=list, description="Classes found")
    imports: List[str] = Field(default_factory=list, description="Import statements")
    line_count: int = Field(0, description="Total lines in file")
    
    class Config:
        json_encoders = {
            Path: str
        }


class ParsedRepository(BaseModel):
    """🟡 PAC-MAN's parsed repository result - the entire semantic maze!"""
    
    org_repo: str = Field(..., description="Repository identifier")
    release: str = Field(..., description="Release/version processed")
    files: List[ParsedFile] = Field(default_factory=list, description="All parsed files")
    total_functions: int = Field(0, description="Total functions found")
    total_classes: int = Field(0, description="Total classes found")
    total_modules: int = Field(0, description="Total modules processed")
    processing_time_seconds: float = Field(0.0, description="Time taken to parse")
    
    @property
    def all_functions(self) -> List[Dict[str, Any]]:
        """Get all functions from all files"""
        functions = []
        for file in self.files:
            functions.extend(file.functions)
        return functions
    
    @property 
    def all_classes(self) -> List[Dict[str, Any]]:
        """Get all classes from all files"""
        classes = []
        for file in self.files:
            classes.extend(file.classes)
        return classes

# waka waka waka! 🟡 All the result models are ready for PAC-MAN semantic chomping! 🟡
