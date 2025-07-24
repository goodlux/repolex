"""
🟡 CLI Progress Indicators with PAC-MAN Theme 🟡
Rich progress bars and status displays for CLI operations.
"""

from typing import Optional, Callable, Any, Union
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
import time

console = Console()

# PAC-MAN themed progress characters
PACMAN_FRAMES = ["🟡", "🟠", "🟡", "🟠"]
GHOST_FRAMES = ["👻", "💀", "👻", "💀"]
DOT_FRAMES = ["⚪", "🔴", "🟠", "🟡"]

class PacManProgress:
    """PAC-MAN themed progress tracker for CLI operations."""
    
    def __init__(self, description: str = "Processing"):
        self.description = description
        self.current_step = 0
        self.total_steps = 100
        self.frame_count = 0
        self.start_time = time.time()
        
    def update(self, step: int, message: str = "", total: Optional[int] = None):
        """Update progress with PAC-MAN animation."""
        if total:
            self.total_steps = total
        self.current_step = step
        self.frame_count += 1
        
        # PAC-MAN animation
        pacman = PACMAN_FRAMES[self.frame_count % len(PACMAN_FRAMES)]
        dots = "⚪" * min(10, step // 10)
        
        progress_text = f"{pacman} {self.description}: {message}"
        if self.total_steps > 0:
            percentage = (step / self.total_steps) * 100
            progress_text += f" [{percentage:.1f}%]"
        
        console.print(f"\r{progress_text}{dots}", end="")
    
    def complete(self, message: str = "WAKA WAKA! Complete!"):
        """Show completion with celebration."""
        elapsed = time.time() - self.start_time
        console.print(f"\r🟡 {message} ⚡ ({elapsed:.1f}s)")

def create_cli_progress_callback() -> Callable:
    """Create a progress callback for CLI operations."""
    progress_tracker = PacManProgress("Processing")
    
    async def progress_callback(step_or_report, message: str = "", total: Optional[int] = None):
        # Handle both ProgressReport objects and individual parameters
        from ..models.progress import ProgressReport
        
        if isinstance(step_or_report, ProgressReport):
            # Called with ProgressReport object from RepoManager
            progress_tracker.update(step_or_report.current, step_or_report.message, step_or_report.total)
        else:
            # Called with individual parameters from Manager
            progress_tracker.update(step_or_report, message, total)
    
    return progress_callback

def create_rich_progress(description: str) -> Progress:
    """Create a rich progress bar with PAC-MAN theme."""
    return Progress(
        SpinnerColumn(spinner_style="yellow"),
        TextColumn("🟡 [bold yellow]{task.description}"),
        BarColumn(bar_width=None, style="yellow", complete_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    )

def show_success_panel(title: str, content: str, suggestions: list = None):
    """Show a success panel with PAC-MAN celebration."""
    text = Text()
    text.append("🟡 WAKA WAKA! ", style="bold yellow")
    text.append(content)
    
    if suggestions:
        text.append("\n\n💡 Next steps:\n", style="bold blue")
        for suggestion in suggestions:
            text.append(f"   • {suggestion}\n")
    
    console.print(Panel(
        text,
        title=f"🏆 {title}",
        border_style="green",
        padding=(1, 2)
    ))

def show_error_panel(title: str, error: str, suggestions: list = None):
    """Show an error panel with helpful PAC-MAN guidance."""
    text = Text()
    text.append("👻 CHOMP! ", style="bold red")
    text.append(error)
    
    if suggestions:
        text.append("\n\n🔧 Try this:\n", style="bold blue")
        for suggestion in suggestions:
            text.append(f"   • {suggestion}\n")
    
    console.print(Panel(
        text,
        title=f"💥 {title}",
        border_style="red",
        padding=(1, 2)
    ))

def show_info_panel(title: str, content: str):
    """Show an info panel with PAC-MAN style."""
    text = Text()
    text.append("⚪ ", style="bold blue")
    text.append(content)
    
    console.print(Panel(
        text,
        title=f"ℹ️  {title}",
        border_style="blue",
        padding=(1, 2)
    ))

def animate_processing(description: str, duration: float = 2.0):
    """Show a PAC-MAN processing animation."""
    frames = ["🟡", "🟠", "🔴", "🟠"]
    dots = ["⚪", "🔴", "🟠", "🟡"]
    
    with Live(console=console, refresh_per_second=4) as live:
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            frame = frames[frame_count % len(frames)]
            dot_pattern = "".join([dots[(frame_count + i) % len(dots)] for i in range(10)])
            
            text = Text()
            text.append(f"{frame} {description} ", style="bold yellow")
            text.append(dot_pattern)
            
            live.update(Panel(text, border_style="yellow"))
            time.sleep(0.25)
            frame_count += 1
    
    console.print("🟡 WAKA WAKA! Processing complete! ⚡")

def show_repository_status(repo_info: dict):
    """Show repository status with PAC-MAN visualization."""
    status_icon = "🟡" if repo_info.get("status") == "ready" else "👻"
    releases = repo_info.get("releases", [])
    graphs = repo_info.get("graphs_count", 0)
    
    text = Text()
    text.append(f"{status_icon} ", style="bold yellow")
    text.append(f"{repo_info.get('name', 'Unknown')}", style="bold")
    text.append(f"\n   📋 {len(releases)} releases")
    text.append(f"\n   🧠 {graphs} graphs")
    
    if releases:
        text.append(f"\n   📦 Latest: {releases[0] if releases else 'None'}")
    
    console.print(text)

# PAC-MAN maze visualization for TUI
MAZE_BORDER = "🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫"
MAZE_EMPTY = "   "
MAZE_DOT = " ⚪ "
MAZE_POWER = " 🔴 "

def create_status_maze(width: int = 10) -> str:
    """Create a PAC-MAN style status display."""
    top = "🟫" * width
    middle = "🟫" + "⚪" * (width - 2) + "🟫"
    bottom = "🟫" * width
    
    return f"{top}\n{middle}\n{bottom}"
