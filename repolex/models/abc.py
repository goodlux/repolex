"""
⏰ PAC-MAN's ABC Event Models ⏰

ABC = "Abstract, Birth, Change" - temporal change tracking events!
These are PAC-MAN's time pellets that track how the code maze evolves over time!

Each event captures a moment when something in the maze changed - functions appearing,
disappearing, or transforming. It's like PAC-MAN's temporal radar!

WAKA WAKA! Tracking the space-time continuum of code evolution!
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum


class ChangeType(str, Enum):
    """⏰ Types of changes PAC-MAN can detect in the time stream!"""
    ADDED = "added"           # 🟢 New function/class appeared
    MODIFIED = "modified"     # 🟡 Existing code changed
    DELETED = "deleted"       # 🔴 Code disappeared
    MOVED = "moved"          # 🔄 Code relocated 
    RENAMED = "renamed"       # 📝 Identifier changed


class ChangeScope(str, Enum):
    """⏰ What level of the maze was affected!"""
    FUNCTION = "function"     # Individual function changed
    CLASS = "class"          # Class definition changed
    MODULE = "module"        # Entire file changed
    PACKAGE = "package"      # Directory structure changed
    REPOSITORY = "repository" # Top-level repo changes


class ABCEvent(BaseModel):
    """⏰ Base ABC event - PAC-MAN's temporal change detection!"""
    
    # Event identification
    event_id: str = Field(..., description="Unique event identifier")
    event_type: ChangeType = Field(..., description="What kind of change occurred")
    scope: ChangeScope = Field(..., description="What level was affected")
    
    # Temporal context
    timestamp: datetime = Field(..., description="When the change was detected")
    release_from: Optional[str] = Field(None, description="Previous version")
    release_to: str = Field(..., description="Current version")
    
    # Change details
    entity_name: str = Field(..., description="Name of changed entity")
    entity_path: str = Field(..., description="File path of entity")
    
    # Metadata
    confidence_score: float = Field(1.0, description="How certain we are (0.0-1.0)")
    detection_method: str = Field("ast_diff", description="How change was detected")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class FunctionChangeEvent(ABCEvent):
    """⏰ Function-specific change event - when a function dot changes!"""
    
    scope: ChangeScope = Field(ChangeScope.FUNCTION, description="Always function scope")
    
    # Function-specific details
    function_signature_before: Optional[str] = Field(None, description="Previous signature")
    function_signature_after: Optional[str] = Field(None, description="New signature")
    
    # Parameters
    parameters_added: List[str] = Field(default_factory=list, description="New parameters")
    parameters_removed: List[str] = Field(default_factory=list, description="Removed parameters")
    parameters_modified: List[Dict[str, str]] = Field(default_factory=list, description="Changed parameters")
    
    # Docstring changes
    docstring_changed: bool = Field(False, description="Whether docstring was modified")
    docstring_before: Optional[str] = Field(None, description="Previous docstring")
    docstring_after: Optional[str] = Field(None, description="New docstring")
    
    # Code complexity
    complexity_before: Optional[int] = Field(None, description="Previous cyclomatic complexity")
    complexity_after: Optional[int] = Field(None, description="New cyclomatic complexity")
    
    # Line numbers
    line_start_before: Optional[int] = Field(None, description="Previous start line")
    line_start_after: Optional[int] = Field(None, description="New start line")
    line_end_before: Optional[int] = Field(None, description="Previous end line")
    line_end_after: Optional[int] = Field(None, description="New end line")


class ClassChangeEvent(ABCEvent):
    """⏰ Class-specific change event - when a class structure changes!"""
    
    scope: ChangeScope = Field(ChangeScope.CLASS, description="Always class scope")
    
    # Class-specific details
    methods_added: List[str] = Field(default_factory=list, description="New methods")
    methods_removed: List[str] = Field(default_factory=list, description="Removed methods")
    methods_modified: List[str] = Field(default_factory=list, description="Changed methods")
    
    # Inheritance changes
    base_classes_before: List[str] = Field(default_factory=list, description="Previous base classes")
    base_classes_after: List[str] = Field(default_factory=list, description="New base classes")
    
    # Attributes
    attributes_added: List[str] = Field(default_factory=list, description="New attributes")
    attributes_removed: List[str] = Field(default_factory=list, description="Removed attributes")


class ModuleChangeEvent(ABCEvent):
    """⏰ Module-specific change event - when an entire file changes!"""
    
    scope: ChangeScope = Field(ChangeScope.MODULE, description="Always module scope")
    
    # Module-specific details
    imports_added: List[str] = Field(default_factory=list, description="New imports")
    imports_removed: List[str] = Field(default_factory=list, description="Removed imports")
    
    # File-level metrics
    total_lines_before: Optional[int] = Field(None, description="Previous line count")
    total_lines_after: Optional[int] = Field(None, description="New line count")
    
    # Structure changes
    functions_added: int = Field(0, description="Number of functions added")
    functions_removed: int = Field(0, description="Number of functions removed")
    classes_added: int = Field(0, description="Number of classes added")
    classes_removed: int = Field(0, description="Number of classes removed")


class RepositoryChangeEvent(ABCEvent):
    """⏰ Repository-wide change event - major maze restructuring!"""
    
    scope: ChangeScope = Field(ChangeScope.REPOSITORY, description="Always repository scope")
    
    # Repository-specific details
    files_added: List[str] = Field(default_factory=list, description="New files")
    files_removed: List[str] = Field(default_factory=list, description="Removed files")
    files_moved: List[Dict[str, str]] = Field(default_factory=list, description="Moved files (from->to)")
    
    # Directory structure
    directories_added: List[str] = Field(default_factory=list, description="New directories")
    directories_removed: List[str] = Field(default_factory=list, description="Removed directories")
    
    # High-level metrics
    total_functions_delta: int = Field(0, description="Net change in function count")
    total_classes_delta: int = Field(0, description="Net change in class count")
    total_lines_delta: int = Field(0, description="Net change in line count")


class ABCEventSummary(BaseModel):
    """⏰ Summary of ABC events for a release - PAC-MAN's temporal report!"""
    
    release_from: Optional[str] = Field(None, description="Previous version")
    release_to: str = Field(..., description="Current version")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="When analysis was done")
    
    # Event counts by type
    events_by_type: Dict[ChangeType, int] = Field(default_factory=dict, description="Count of each change type")
    events_by_scope: Dict[ChangeScope, int] = Field(default_factory=dict, description="Count of each scope")
    
    # All events
    events: List[ABCEvent] = Field(default_factory=list, description="All detected events")
    
    # High-level insights
    major_changes: List[str] = Field(default_factory=list, description="Significant changes detected")
    stability_score: float = Field(1.0, description="How stable the release is (0.0-1.0)")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def get_function_events(self) -> List[FunctionChangeEvent]:
        """Get all function change events"""
        return [event for event in self.events if isinstance(event, FunctionChangeEvent)]
    
    def get_class_events(self) -> List[ClassChangeEvent]:
        """Get all class change events"""
        return [event for event in self.events if isinstance(event, ClassChangeEvent)]
    
    def get_events_by_file(self, file_path: str) -> List[ABCEvent]:
        """Get all events for a specific file"""
        return [event for event in self.events if event.entity_path == file_path]


# Type aliases for convenience
ChangeEvent = Union[FunctionChangeEvent, ClassChangeEvent, ModuleChangeEvent, RepositoryChangeEvent]