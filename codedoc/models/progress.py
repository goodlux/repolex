"""
Progress tracking models for CodeDoc operations.

PAC-MAN themed progress tracking - because who doesn't want to see PAC-MAN
chomping through your repositories? 🟡
"""

from typing import Optional, Dict, Any, Callable, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ProgressStage(str, Enum):
    """Stages of processing - PAC-MAN style! 🟡"""
    
    # Repository operations
    CLONING = "cloning"           # 🟡 PAC-MAN entering the maze
    DISCOVERING = "discovering"   # 👻 Looking for dots (releases)
    UPDATING = "updating"         # 🟡 Moving through the maze
    
    # Parsing operations  
    PARSING = "parsing"           # 🟡 Chomping through files
    ANALYZING = "analyzing"       # 🧠 Understanding the code
    BUILDING = "building"         # 🏗️ Constructing graphs
    
    # Export operations
    EXPORTING = "exporting"       # 📦 Creating outputs
    COMPRESSING = "compressing"   # 🗜️ Making it tiny
    GENERATING = "generating"     # ✨ Final creation
    
    # System operations
    CLEANING = "cleaning"         # 🧹 Cleaning up the maze
    VALIDATING = "validating"     # ✅ Checking everything works

class ProgressLevel(str, Enum):
    """Progress levels with PAC-MAN emojis"""
    
    TRACE = "trace"       # 🔍 Detailed debugging
    DEBUG = "debug"       # 🐛 Development info
    INFO = "info"         # 🟡 Normal progress 
    WARNING = "warning"   # ⚠️ Something to watch
    ERROR = "error"       # 💥 Problems encountered
    SUCCESS = "success"   # ✅ Victory!

class ProgressReport(BaseModel):
    """Simple progress report for callback functions - PAC-MAN style! 🟡"""
    
    current: int = Field(..., description="Current progress value")
    total: int = Field(..., description="Total progress value") 
    message: str = Field(..., description="Progress message with PAC-MAN theming")
    stage: str = Field(..., description="Current stage name")
    
    @property
    def progress_percent(self) -> float:
        """Calculate progress percentage"""
        return (self.current / self.total) * 100 if self.total > 0 else 0.0
    
    def __str__(self) -> str:
        """String representation - PAC-MAN style"""
        return f"{self.message} ({self.progress_percent:.1f}%)"

class ProgressEvent(BaseModel):
    """Individual progress event - a PAC-MAN movement! 🟡"""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    stage: ProgressStage
    level: ProgressLevel = ProgressLevel.INFO
    message: str
    progress_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    
    # Detailed progress info
    current_item: Optional[str] = None      # What we're processing now
    total_items: Optional[int] = None       # Total items to process
    items_completed: Optional[int] = None   # Items completed so far
    
    # PAC-MAN theming
    emoji: Optional[str] = None             # Custom emoji for this event
    animation_frame: Optional[int] = None   # For animated progress
    
    # Additional context
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def __str__(self) -> str:
        """String representation with PAC-MAN flair"""
        emoji = self.emoji or self._get_default_emoji()
        progress_str = f" ({self.progress_percent:.1f}%)" if self.progress_percent else ""
        return f"{emoji} {self.message}{progress_str}"
    
    def _get_default_emoji(self) -> str:
        """Get default emoji based on stage and level"""
        
        # Level-based emojis (errors override stage)
        if self.level == ProgressLevel.ERROR:
            return "💥"
        elif self.level == ProgressLevel.WARNING:
            return "⚠️"
        elif self.level == ProgressLevel.SUCCESS:
            return "✅"
        
        # Stage-based emojis
        stage_emojis = {
            ProgressStage.CLONING: "🟡",      # PAC-MAN starting
            ProgressStage.DISCOVERING: "👻",  # Ghost looking for dots
            ProgressStage.UPDATING: "🟡",     # PAC-MAN moving
            ProgressStage.PARSING: "🟡",      # Chomping files
            ProgressStage.ANALYZING: "🧠",    # Thinking
            ProgressStage.BUILDING: "🏗️",     # Building graphs
            ProgressStage.EXPORTING: "📦",    # Creating outputs
            ProgressStage.COMPRESSING: "🗜️",  # Squishing data
            ProgressStage.GENERATING: "✨",   # Magic happening
            ProgressStage.CLEANING: "🧹",     # Cleaning maze
            ProgressStage.VALIDATING: "✅",   # Final check
        }
        
        return stage_emojis.get(self.stage, "🟡")

class ProgressTracker(BaseModel):
    """Progress tracker for operations - the PAC-MAN game state! 🎮"""
    
    operation_id: str = Field(..., description="Unique identifier for this operation")
    operation_name: str = Field(..., description="Human-readable operation name")
    started_at: datetime = Field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None
    
    current_stage: ProgressStage
    overall_progress: float = Field(0.0, ge=0.0, le=100.0)
    
    # Event history - PAC-MAN's journey through the maze
    events: List[ProgressEvent] = Field(default_factory=list)
    
    # Stage progress tracking
    stage_progress: Dict[ProgressStage, float] = Field(default_factory=dict)
    stage_weights: Dict[ProgressStage, float] = Field(default_factory=dict)
    
    # PAC-MAN animation state
    animation_frame: int = 0
    animation_direction: str = "right"  # "right", "left", "up", "down"
    
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
        """Add a progress event - PAC-MAN makes a move! 🟡"""
        
        # Update animation
        self.animation_frame = (self.animation_frame + 1) % 4
        
        # Create event
        event = ProgressEvent(
            stage=stage,
            level=level,
            message=message,
            progress_percent=progress_percent,
            animation_frame=self.animation_frame,
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
        """Mark a stage as complete - PAC-MAN cleared a level! 🟡"""
        message = message or f"Completed {stage.value}"
        return self.add_event(
            stage=stage,
            message=message,
            level=ProgressLevel.SUCCESS,
            progress_percent=100.0,
            emoji="✅"
        )
    
    def fail_stage(self, stage: ProgressStage, error: str) -> ProgressEvent:
        """Mark a stage as failed - PAC-MAN got caught! 💥"""
        return self.add_event(
            stage=stage,
            message=f"Failed: {error}",
            level=ProgressLevel.ERROR,
            emoji="💥"
        )
    
    def finish(self, success: bool = True) -> None:
        """Mark operation as finished"""
        self.finished_at = datetime.now()
        if success:
            self.overall_progress = 100.0
            self.add_event(
                stage=self.current_stage,
                message="Operation completed successfully!",
                level=ProgressLevel.SUCCESS,
                progress_percent=100.0,
                emoji="🎉"
            )
        else:
            self.add_event(
                stage=self.current_stage,
                message="Operation failed",
                level=ProgressLevel.ERROR,
                emoji="💥"
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
        """Operation duration in seconds"""
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        else:
            return (datetime.now() - self.started_at).total_seconds()
    
    @property
    def is_finished(self) -> bool:
        """Whether operation is finished"""
        return self.finished_at is not None
    
    @property
    def is_successful(self) -> bool:
        """Whether operation completed successfully"""
        return self.is_finished and self.error_count == 0
    
    def get_latest_events(self, count: int = 5) -> List[ProgressEvent]:
        """Get latest progress events"""
        return self.events[-count:] if self.events else []
    
    def get_summary(self) -> str:
        """Get operation summary - PAC-MAN's final score! 🎮"""
        duration = self.duration or 0
        status = "✅ Success" if self.is_successful else f"⚠️ {self.error_count} errors"
        
        return (
            f"🟡 {self.operation_name}\n"
            f"   Progress: {self.overall_progress:.1f}%\n"
            f"   Duration: {duration:.1f}s\n" 
            f"   Status: {status}\n"
            f"   Items: {self.items_processed}"
            f"/{self.total_items}" if self.total_items else f"{self.items_processed}"
        )

# Type alias for progress callback functions
ProgressCallback = Callable[[ProgressTracker], None]

class ProgressManager:
    """Manager for progress tracking - the PAC-MAN arcade! 🎮"""
    
    def __init__(self):
        self.active_trackers: Dict[str, ProgressTracker] = {}
        self.callbacks: List[ProgressCallback] = []
    
    def create_tracker(self, 
                      operation_id: str,
                      operation_name: str,
                      stage_weights: Optional[Dict[ProgressStage, float]] = None) -> ProgressTracker:
        """Create new progress tracker"""
        
        tracker = ProgressTracker(
            operation_id=operation_id,
            operation_name=operation_name,
            current_stage=ProgressStage.CLONING  # Default starting stage
        )
        
        # Set default stage weights for common operations
        if stage_weights:
            for stage, weight in stage_weights.items():
                tracker.set_stage_weight(stage, weight)
        else:
            # Default weights for repository processing
            default_weights = {
                ProgressStage.CLONING: 10.0,
                ProgressStage.DISCOVERING: 5.0,
                ProgressStage.PARSING: 40.0,
                ProgressStage.ANALYZING: 30.0,
                ProgressStage.BUILDING: 15.0
            }
            for stage, weight in default_weights.items():
                tracker.set_stage_weight(stage, weight)
        
        self.active_trackers[operation_id] = tracker
        return tracker
    
    def get_tracker(self, operation_id: str) -> Optional[ProgressTracker]:
        """Get existing tracker"""
        return self.active_trackers.get(operation_id)
    
    def remove_tracker(self, operation_id: str) -> None:
        """Remove finished tracker"""
        self.active_trackers.pop(operation_id, None)
    
    def add_callback(self, callback: ProgressCallback) -> None:
        """Add progress callback"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: ProgressCallback) -> None:
        """Remove progress callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def notify_callbacks(self, tracker: ProgressTracker) -> None:
        """Notify all callbacks of progress update"""
        for callback in self.callbacks:
            try:
                callback(tracker)
            except Exception as e:
                # Don't let callback errors break progress tracking
                print(f"Progress callback error: {e}")

# Default progress manager instance
progress_manager = ProgressManager()

def create_progress_tracker(operation_id: str, operation_name: str) -> ProgressTracker:
    """Convenience function to create progress tracker"""
    return progress_manager.create_tracker(operation_id, operation_name)

# PAC-MAN themed progress messages
PACMAN_MESSAGES = {
    ProgressStage.CLONING: [
        "🟡 PAC-MAN entering the repository maze...",
        "🟡 Chomping through the git history...",
        "🟡 Collecting all the code dots...",
    ],
    ProgressStage.PARSING: [
        "🟡 Munching through Python files...",
        "🟡 Eating up those function definitions...",  
        "🟡 Chomping on delicious docstrings...",
        "🟡 Gobbling up class hierarchies...",
    ],
    ProgressStage.ANALYZING: [
        "🧠 PAC-MAN thinking about semantic relationships...",
        "🧠 Understanding the code architecture...",
        "🧠 Connecting the function dots...",
    ],
    ProgressStage.BUILDING: [
        "🏗️ Building the semantic maze...",
        "🏗️ Constructing knowledge graphs...", 
        "🏗️ Creating the ontology tunnels...",
    ],
    ProgressStage.EXPORTING: [
        "📦 Packaging up the semantic goods...",
        "📦 Creating portable PAC-MAN cartridges...",
        "📦 Wrapping up the knowledge gems...",
    ]
}

def get_random_pacman_message(stage: ProgressStage) -> str:
    """Get a random PAC-MAN themed message for the stage"""
    import random
    messages = PACMAN_MESSAGES.get(stage, [f"🟡 Working on {stage.value}..."])
    return random.choice(messages)
