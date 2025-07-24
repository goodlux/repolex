"""
PAC-MAN themed error handling with rich output.

When PAC-MAN encounters ghosts (errors), we make it beautiful and helpful! 👻🟡
"""

import functools
import traceback
from typing import Any, Callable, Optional, List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich.table import Table
from rich import box
import click

from codedoc.models.exceptions import (
    CodeDocError, 
    GitError, 
    ProcessingError, 
    StorageError,
    ValidationError, 
    SecurityError, 
    ExportError,
    NetworkError,
    ConfigurationError
)

# PAC-MAN themed console
console = Console()

# Ghost colors for different error types! 👻
ERROR_COLORS = {
    GitError: "red",
    ProcessingError: "yellow", 
    StorageError: "blue",
    ValidationError: "magenta",
    SecurityError: "bright_red",
    ExportError: "cyan",
    NetworkError: "orange3",
    ConfigurationError: "green",
    CodeDocError: "white",  # Generic ghost
    Exception: "bright_white"  # Unknown ghost!
}

# PAC-MAN death animations! 💥
PACMAN_DEATH_FRAMES = [
    "🟡",  # Normal PAC-MAN
    "😵",  # Dizzy PAC-MAN
    "💥",  # Explosion
    "👻"   # Ghost wins
]

# Error-specific ghost emojis
ERROR_GHOSTS = {
    GitError: "👻",           # Blinky (red ghost) - git problems
    ProcessingError: "👹",    # Processing demon
    StorageError: "🛢️",      # Storage ghost  
    ValidationError: "⚠️",   # Warning ghost
    SecurityError: "🔐",     # Security ghost
    ExportError: "📦",       # Export ghost
    NetworkError: "🌐",      # Network ghost
    ConfigurationError: "⚙️", # Config ghost
}

def get_error_ghost(error_type: type) -> str:
    """Get the appropriate ghost emoji for error type"""
    return ERROR_GHOSTS.get(error_type, "👻")

def get_error_color(error_type: type) -> str:
    """Get the appropriate color for error type"""
    return ERROR_COLORS.get(error_type, "white")

def create_pacman_death_animation() -> str:
    """Create PAC-MAN death animation text"""
    frames = " → ".join(PACMAN_DEATH_FRAMES)
    return f"[bold yellow]{frames}[/bold yellow]"

def format_error_suggestions(suggestions: List[str]) -> Table:
    """Format error suggestions as a nice table"""
    if not suggestions:
        return None
    
    table = Table(
        title="🟡 PAC-MAN Recovery Tips",
        box=box.ROUNDED,
        show_header=False,
        padding=(0, 1)
    )
    table.add_column("Tip", style="bright_blue")
    
    for i, suggestion in enumerate(suggestions, 1):
        table.add_row(f"{i}. {suggestion}")
    
    return table

def create_error_panel(error: Exception, operation: str = "operation") -> Panel:
    """Create a beautiful PAC-MAN themed error panel"""
    
    error_type = type(error)
    ghost = get_error_ghost(error_type)
    color = get_error_color(error_type)
    
    # Create main error content
    content = Text()
    
    # PAC-MAN death animation
    content.append(f"{create_pacman_death_animation()}\n\n", style="bold")
    
    # Error title
    content.append(f"{ghost} ", style=f"bold {color}")
    content.append(f"{error_type.__name__}", style=f"bold {color}")
    content.append(" caught PAC-MAN!\n\n", style="bold")
    
    # Error message
    content.append("💬 Error Details:\n", style="bold bright_white")
    content.append(f"   {str(error)}\n\n", style=color)
    
    # Add context if available
    if hasattr(error, 'operation_context'):
        content.append("🎯 What PAC-MAN was trying to do:\n", style="bold bright_white")
        content.append(f"   {error.operation_context}\n\n", style="dim")
    
    # Create panel
    panel = Panel(
        content,
        title=f"[bold {color}]{ghost} Game Over - {operation.title()} Failed {ghost}[/bold {color}]",
        border_style=color,
        padding=(1, 2)
    )
    
    return panel

def create_suggestions_panel(suggestions: List[str]) -> Optional[Panel]:
    """Create suggestions panel"""
    if not suggestions:
        return None
    
    content = Text()
    content.append("🟡 PAC-MAN can try again with these power-ups:\n\n", style="bold bright_yellow")
    
    for i, suggestion in enumerate(suggestions, 1):
        content.append(f"   💊 {suggestion}\n", style="bright_blue")
    
    return Panel(
        content,
        title="[bold bright_yellow]🟡 Power-Ups Available[/bold bright_yellow]",
        border_style="bright_yellow",
        padding=(1, 2)
    )

def create_debug_panel(error: Exception, show_traceback: bool = False) -> Optional[Panel]:
    """Create debug information panel"""
    if not show_traceback:
        return None
    
    tb_text = traceback.format_exc()
    
    content = Text()
    content.append("🔍 Debug Info (for PAC-MAN developers):\n\n", style="bold dim")
    content.append(tb_text, style="dim")
    
    return Panel(
        content,
        title="[dim]🐛 Debug Information[/dim]",
        border_style="dim",
        padding=(1, 2)
    )

def handle_error(
    error: Exception, 
    operation: str = "operation",
    show_suggestions: bool = True,
    show_debug: bool = False,
    exit_on_error: bool = True
) -> None:
    """Handle error with beautiful PAC-MAN themed output"""
    
    # Create error panel
    error_panel = create_error_panel(error, operation)
    console.print(error_panel)
    
    # Show suggestions if available
    if show_suggestions and hasattr(error, 'suggestions') and error.suggestions:
        suggestions_panel = create_suggestions_panel(error.suggestions)
        if suggestions_panel:
            console.print(suggestions_panel)
    
    # Show debug info if requested
    if show_debug:
        debug_panel = create_debug_panel(error, show_traceback=True)
        if debug_panel:
            console.print(debug_panel)
    
    # PAC-MAN game over message
    console.print()
    console.print(
        Align.center(
            Text("🎮 Insert coin to continue 🎮", style="bold bright_cyan")
        )
    )
    console.print()
    
    if exit_on_error:
        raise click.Abort()

def pacman_error_handler(
    operation: str = "operation",
    show_suggestions: bool = True,
    show_debug: bool = False,
    exit_on_error: bool = True
):
    """
    Decorator for PAC-MAN themed error handling.
    
    Usage:
        @pacman_error_handler("repository cloning")
        def clone_repository(url: str):
            # Your code here
            pass
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CodeDocError as e:
                # Our custom errors with suggestions
                handle_error(
                    e, 
                    operation=operation,
                    show_suggestions=show_suggestions,
                    show_debug=show_debug,
                    exit_on_error=exit_on_error
                )
            except Exception as e:
                # Unexpected errors - make them CodeDocError with suggestions
                suggestions = [
                    "Check if all dependencies are installed",
                    "Verify your internet connection",
                    "Try running with --debug for more information",
                    "Check GitHub repository permissions",
                    "Clear cache with 'codedoc clean'"
                ]
                
                wrapped_error = CodeDocError(
                    f"Unexpected error during {operation}: {str(e)}",
                    suggestions=suggestions
                )
                wrapped_error.operation_context = operation
                
                handle_error(
                    wrapped_error,
                    operation=operation,
                    show_suggestions=show_suggestions,
                    show_debug=True,  # Always show debug for unexpected errors
                    exit_on_error=exit_on_error
                )
        
        return wrapper
    return decorator

# Async version of the decorator
def async_pacman_error_handler(
    operation: str = "operation",
    show_suggestions: bool = True,
    show_debug: bool = False,
    exit_on_error: bool = True
):
    """Async version of PAC-MAN error handler"""
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except CodeDocError as e:
                handle_error(
                    e, 
                    operation=operation,
                    show_suggestions=show_suggestions,
                    show_debug=show_debug,
                    exit_on_error=exit_on_error
                )
            except Exception as e:
                suggestions = [
                    "Check if all dependencies are installed",
                    "Verify your internet connection", 
                    "Try running with --debug for more information",
                    "Check GitHub repository permissions",
                    "Clear cache with 'codedoc clean'"
                ]
                
                wrapped_error = CodeDocError(
                    f"Unexpected error during {operation}: {str(e)}",
                    suggestions=suggestions
                )
                wrapped_error.operation_context = operation
                
                handle_error(
                    wrapped_error,
                    operation=operation,
                    show_suggestions=show_suggestions,
                    show_debug=True,
                    exit_on_error=exit_on_error
                )
        
        return wrapper
    return decorator

# Special error handlers for specific operations
def git_error_handler(operation: str = "git operation"):
    """Specialized error handler for git operations"""
    return pacman_error_handler(
        operation=operation,
        show_suggestions=True,
        show_debug=False
    )

def parsing_error_handler(operation: str = "parsing operation"):
    """Specialized error handler for parsing operations"""
    return pacman_error_handler(
        operation=operation,
        show_suggestions=True,
        show_debug=True  # Parsing errors often need debug info
    )

def storage_error_handler(operation: str = "storage operation"):
    """Specialized error handler for storage operations"""
    return pacman_error_handler(
        operation=operation,
        show_suggestions=True,
        show_debug=False
    )

# Context manager for error handling
class PacmanErrorContext:
    """Context manager for PAC-MAN error handling"""
    
    def __init__(self, operation: str, show_debug: bool = False):
        self.operation = operation
        self.show_debug = show_debug
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            handle_error(
                exc_val,
                operation=self.operation,
                show_debug=self.show_debug,
                exit_on_error=False  # Don't exit in context manager
            )
            return True  # Suppress the exception
        return False

# Utility functions for creating specific error types with PAC-MAN flair
def create_git_error(message: str, suggestions: List[str] = None) -> GitError:
    """Create a git error with default suggestions"""
    default_suggestions = [
        "Check if repository URL is correct",
        "Verify git is installed and accessible",
        "Check network connection",
        "Verify GitHub authentication if accessing private repos"
    ]
    return GitError(message, suggestions or default_suggestions)

def create_validation_error(message: str, suggestions: List[str] = None) -> ValidationError:
    """Create a validation error with default suggestions"""
    default_suggestions = [
        "Check command syntax with --help",
        "Verify all required arguments are provided",
        "Check input format matches expected pattern"
    ]
    return ValidationError(message, suggestions or default_suggestions)

def create_processing_error(message: str, suggestions: List[str] = None) -> ProcessingError:
    """Create a processing error with default suggestions"""
    default_suggestions = [
        "Check if source code is valid Python",
        "Verify file permissions are correct",
        "Try with a smaller test repository first",
        "Check available disk space"
    ]
    return ProcessingError(message, suggestions or default_suggestions)

# Fun PAC-MAN error messages
PACMAN_ERROR_MESSAGES = {
    "file_not_found": "🟡 PAC-MAN couldn't find that dot (file)!",
    "permission_denied": "👻 Ghost blocked PAC-MAN's path (permission denied)!",
    "network_error": "📡 PAC-MAN lost connection to the maze server!",
    "invalid_input": "🟡 PAC-MAN doesn't understand that command!",
    "git_error": "👻 Git ghost caught PAC-MAN in the repository!",
    "parsing_error": "🟡 PAC-MAN choked on that code!",
    "storage_error": "🛢️ PAC-MAN's storage maze is full!",
}

def get_pacman_error_message(error_type: str) -> str:
    """Get a fun PAC-MAN themed error message"""
    return PACMAN_ERROR_MESSAGES.get(error_type, "🟡 PAC-MAN encountered an unknown ghost!")

# Success messages for when PAC-MAN wins!
def show_success(message: str, operation: str = "operation") -> None:
    """Show success message with PAC-MAN celebration"""
    
    success_panel = Panel(
        Text.from_markup(
            f"🟡✨ [bold bright_yellow]PAC-MAN WINS![/bold bright_yellow] ✨🟡\n\n"
            f"🎉 {message}\n\n"
            f"[dim]Operation: {operation}[/dim]"
        ),
        title="[bold bright_yellow]🏆 SUCCESS! 🏆[/bold bright_yellow]",
        border_style="bright_yellow",
        padding=(1, 2)
    )
    
    console.print(success_panel)
    
    # PAC-MAN victory dance!
    console.print(
        Align.center(
            Text("🟡 → 😊 → 🎉 → 🏆", style="bold bright_yellow")
        )
    )
    console.print()

# Progress integration
def show_progress_error(tracker, error: Exception) -> None:
    """Show error within progress context"""
    from codedoc.models.progress import ProgressLevel
    
    # Add error to progress tracker
    if hasattr(tracker, 'add_event'):
        tracker.add_event(
            stage=tracker.current_stage,
            level=ProgressLevel.ERROR,
            message=f"Error: {str(error)}",
            emoji="💥"
        )
    
    # Show full error display
    handle_error(error, exit_on_error=False)
