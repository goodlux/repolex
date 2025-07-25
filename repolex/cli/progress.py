"""
Simple CLI Progress Indicators
Clean, Unix-style progress output for CLI operations.
"""

from typing import Optional, Callable, Any, Union
import time
import sys

class SimpleProgress:
    """Simple progress tracker for CLI operations."""
    
    def __init__(self, description: str = "Processing"):
        self.description = description
        self.current_step = 0
        self.total_steps = 100
        self.start_time = time.time()
        self.last_output = ""
        
    def update(self, step: int, message: str = "", total: Optional[int] = None):
        """Update progress with simple text output."""
        if total:
            self.total_steps = total
        self.current_step = step
        
        if self.total_steps > 0:
            percentage = (step / self.total_steps) * 100
            progress_text = f"{self.description}: {message} [{percentage:.1f}%]"
        else:
            progress_text = f"{self.description}: {message}"
        
        # Clear previous line and print new progress
        if self.last_output:
            print("\r" + " " * len(self.last_output), end="")
        print(f"\r{progress_text}", end="", flush=True)
        self.last_output = progress_text
    
    def complete(self, message: str = "Complete"):
        """Show completion."""
        elapsed = time.time() - self.start_time
        print(f"\r{message} ({elapsed:.1f}s)")
        self.last_output = ""

def create_cli_progress_callback() -> Callable:
    """Create a progress callback for CLI operations."""
    progress_tracker = SimpleProgress("Processing")
    
    def progress_callback(step_or_report, message: str = "", total: Optional[int] = None):
        # Handle both ProgressReport objects and individual parameters
        from ..models.progress import ProgressReport
        
        if isinstance(step_or_report, ProgressReport):
            # Called with ProgressReport object from RepoManager
            progress_tracker.update(step_or_report.current, step_or_report.message, step_or_report.total)
        else:
            # Called with individual parameters from Manager
            progress_tracker.update(step_or_report, message, total)
    
    return progress_callback

def show_success(title: str, content: str, suggestions: list = None):
    """Show a success message."""
    print(f"✓ {title}")
    print(f"  {content}")
    
    if suggestions:
        print("  Next steps:")
        for suggestion in suggestions:
            print(f"    • {suggestion}")
    print()

def show_error(title: str, error: str, suggestions: list = None):
    """Show an error message."""
    print(f"✗ {title}", file=sys.stderr)
    print(f"  {error}", file=sys.stderr)
    
    if suggestions:
        print("  Try:", file=sys.stderr)
        for suggestion in suggestions:
            print(f"    • {suggestion}", file=sys.stderr)
    print(file=sys.stderr)

def show_info(title: str, content: str):
    """Show an info message."""
    print(f"ℹ {title}")
    print(f"  {content}")
    print()

def show_repository_status(repo_info: dict):
    """Show repository status with simple text."""
    status_icon = "✓" if repo_info.get("status") == "ready" else "✗"
    releases = repo_info.get("releases", [])
    graphs = repo_info.get("graphs_count", 0)
    
    print(f"{status_icon} {repo_info.get('name', 'Unknown')}")
    print(f"   Releases: {len(releases)}")
    print(f"   Graphs: {graphs}")
    
    if releases:
        print(f"   Latest: {releases[0] if releases else 'None'}")
    print()