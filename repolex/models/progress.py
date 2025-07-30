"""
Progress tracking models for repolex operations.

Clean, professional progress tracking for all repository operations.
"""

from typing import Optional, Dict, Any, Callable, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ProgressStage(str, Enum):
    """Stages of processing operations"""
    
    # Repository operations
    CLONING = "cloning"
    DISCOVERING = "discovering"
    UPDATING = "updating"
    
    # Parsing operations  
    PARSING = "parsing"
    ANALYZING = "analyzing"
    BUILDING = "building"
    
    # Export operations
    EXPORTING = "exporting"
    COMPRESSING = "compressing"
    GENERATING = "generating"
    
    # System operations
    CLEANING = "cleaning"
    VALIDATING = "validating"

class ProgressLevel(str, Enum):
    """Progress levels for logging and display"""
    
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"

class ProgressReport(BaseModel):
    """Simple progress report for callback functions"""
    
    current: int = Field(..., description="Current progress value")
    total: int = Field(..., description="Total progress value") 
    message: str = Field(..., description="Progress message")
    stage: str = Field(..., description="Current stage name")
    
    @property
    def progress_percent(self) -> float:
        """Calculate progress percentage"""
        return (self.current / self.total) * 100 if self.total > 0 else 0.0
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.message} ({self.progress_percent:.1f}%)"

class ProgressEvent(BaseModel):
    """Individual progress event"""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    stage: ProgressStage
    level: ProgressLevel = ProgressLevel.INFO
    message: str
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    
    # Detailed progress info
    current_item: Optional[str] = None
    total_items: Optional[int] = None
    items_completed: Optional[int] = None
    
    # Display info
    emoji: Optional[str] = None
    
    # Additional context
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def __str__(self) -> str:
        """String representation"""
        emoji = self.emoji or self._get_default_emoji()
        progress_str = f" ({self.progress_percent:.1f}%)" if self.progress_percent else ""
        return f"{emoji} {self.message}{progress_str}"
    
    def _get_default_emoji(self) -> str:
        """Get default emoji based on stage and level"""
        
        # Level-based emojis (errors override stage)
        if self.level == ProgressLevel.ERROR:
            return "✗"
        elif self.level == ProgressLevel.WARNING:
            return "⚠"
        elif self.level == ProgressLevel.SUCCESS:
            return "✓"
        
        # Stage-based emojis
        stage_emojis = {
            ProgressStage.CLONING: "⬇",
            ProgressStage.DISCOVERING: "🔍",
            ProgressStage.UPDATING: "🔄",
            ProgressStage.PARSING: "📝",
            ProgressStage.ANALYZING: "🔬",
            ProgressStage.BUILDING: "🏗",
            ProgressStage.EXPORTING: "📤",
            ProgressStage.COMPRESSING: "🗜",
            ProgressStage.GENERATING: "⚡",
            ProgressStage.CLEANING: "🧹",
            ProgressStage.VALIDATING: "✓",
        }
        
        return stage_emojis.get(self.stage, "•")

class ProgressTracker(BaseModel):
    """Progress tracker for operations"""
    
    operation_id: str = Field(..., description="Unique identifier for this operation")
    operation_name: str = Field(..., description="Human-readable operation name")
    started_at: datetime = Field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None
    
    current_stage: ProgressStage
    overall_progress: float = Field(0.0, ge=0.0, le=100.0)
    
    # Event history
    events: List[ProgressEvent] = Field(default_factory=list)
    
    # Stage progress tracking
    stage_progress: Dict[ProgressStage, float] = Field(default_factory=dict)
    stage_weights: Dict[ProgressStage, float] = Field(default_factory=dict)
    
    # Error tracking
    error_count: int = 0
    warning_count: int = 0
    
    # Performance metrics
    items_processed: int = 0
    total_items: Optional[int] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def add_event(self, 
                  stage: ProgressStage,
                  message: str,
                  level: ProgressLevel = ProgressLevel.INFO,
                  progress_percent: Optional[float] = None,
                  **kwargs) -> ProgressEvent:
        """Add a progress event"""
        
        # Create event
        event = ProgressEvent(
            stage=stage,
            level=level,
            message=message,
            progress_percent=progress_percent,
            **kwargs
        )
        
        # Update tracker state
        self.events.append(event)
        self.current_stage = stage
        
        # Update progress
        if progress_percent is not None:
            self.stage_progress[stage] = progress_percent
            self._update_overall_progress()
        
        # Update counters
        if level == ProgressLevel.ERROR:
            self.error_count += 1
        elif level == ProgressLevel.WARNING:
            self.warning_count += 1
        
        return event
    
    def set_stage_weight(self, stage: ProgressStage, weight: float) -> None:
        """Set weight for stage in overall progress calculation"""
        self.stage_weights[stage] = weight
        self._update_overall_progress()
    
    def complete_stage(self, stage: ProgressStage, message: str = None) -> ProgressEvent:
        """Mark a stage as complete"""
        message = message or f"Completed {stage.value}"
        return self.add_event(
            stage=stage,
            message=message,
            level=ProgressLevel.SUCCESS,
            progress_percent=100.0,
            emoji="✓"
        )
    
    def fail_stage(self, stage: ProgressStage, error: str) -> ProgressEvent:
        """Mark a stage as failed"""
        return self.add_event(
            stage=stage,
            message=f"Failed: {error}",
            level=ProgressLevel.ERROR,
            emoji="✗"
        )
    
    def finish(self, success: bool = True) -> None:
        """Mark operation as finished"""
        self.finished_at = datetime.now()
        if success:
            self.overall_progress = 100.0
            self.add_event(
                stage=self.current_stage,
                message="Operation completed successfully",
                level=ProgressLevel.SUCCESS,
                progress_percent=100.0,
                emoji="✓"
            )
        else:
            self.add_event(
                stage=self.current_stage,
                message="Operation failed",
                level=ProgressLevel.ERROR,
                emoji="✗"
            )
    
    def _update_overall_progress(self) -> None:
        """Update overall progress based on stage weights and progress"""
        if not self.stage_weights:
            return
        
        total_weight = sum(self.stage_weights.values())
        if total_weight == 0:
            return
        
        weighted_progress = 0.0
        for stage, weight in self.stage_weights.items():
            stage_prog = self.stage_progress.get(stage, 0.0)
            weighted_progress += (stage_prog * weight)
        
        self.overall_progress = min(100.0, weighted_progress / total_weight)
    
    @property
    def duration(self) -> Optional[float]:
        """Get operation duration in seconds"""
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return (datetime.now() - self.started_at).total_seconds()
    
    @property
    def is_finished(self) -> bool:
        """Check if operation is finished"""
        return self.finished_at is not None
    
    @property
    def is_successful(self) -> bool:
        """Check if operation completed successfully"""
        return self.is_finished and self.error_count == 0
    
    @property
    def latest_event(self) -> Optional[ProgressEvent]:
        """Get the most recent progress event"""
        return self.events[-1] if self.events else None
    
    def get_events_by_level(self, level: ProgressLevel) -> List[ProgressEvent]:
        """Get all events of a specific level"""
        return [event for event in self.events if event.level == level]
    
    def get_events_by_stage(self, stage: ProgressStage) -> List[ProgressEvent]:
        """Get all events for a specific stage"""
        return [event for event in self.events if event.stage == stage]

# Type alias for progress callback functions
ProgressCallback = Callable[[int, str, Optional[int]], None]

# Convenience function for creating simple progress trackers
def create_progress_tracker(operation_name: str, 
                          operation_id: Optional[str] = None) -> ProgressTracker:
    """Create a new progress tracker"""
    if operation_id is None:
        operation_id = f"{operation_name}_{datetime.now().isoformat()}"
    
    return ProgressTracker(
        operation_id=operation_id,
        operation_name=operation_name,
        current_stage=ProgressStage.CLONING  # Default starting stage
    )