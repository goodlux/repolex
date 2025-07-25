"""
Simple error handling with clean output.
Unix-style error reporting and handling.
"""

import functools
import traceback
import sys
from typing import Any, Callable, Optional, List, Dict
import click

from repolex.models.exceptions import (
    RepolexError, 
    GitError, 
    ProcessingError, 
    StorageError,
    ValidationError, 
    SecurityError, 
    ExportError,
    NetworkError,
    ConfigurationError
)

def handle_error(
    error: Exception, 
    operation: str = "operation",
    show_suggestions: bool = True,
    show_debug: bool = False,
    exit_on_error: bool = True
) -> None:
    """Handle error with simple output"""
    
    # Print error to stderr
    print(f"✗ Error in {operation}: {str(error)}", file=sys.stderr)
    
    # Show suggestions if available
    if show_suggestions and hasattr(error, 'suggestions') and error.suggestions:
        print("  Try:", file=sys.stderr)
        for suggestion in error.suggestions:
            print(f"    • {suggestion}", file=sys.stderr)
        print(file=sys.stderr)
    
    # Show debug info if requested
    if show_debug:
        print("Debug information:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print(file=sys.stderr)
    
    if exit_on_error:
        raise click.Abort()

def error_handler(
    operation: str = "operation",
    show_suggestions: bool = True,
    show_debug: bool = False,
    exit_on_error: bool = True
):
    """
    Decorator for simple error handling.
    
    Usage:
        @error_handler("repository cloning")
        def clone_repository(url: str):
            # Your code here
            pass
    """
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RepolexError as e:
                # Our custom errors with suggestions
                handle_error(
                    e, 
                    operation=operation,
                    show_suggestions=show_suggestions,
                    show_debug=show_debug,
                    exit_on_error=exit_on_error
                )
            except Exception as e:
                # Unexpected errors - make them RepolexError with suggestions
                suggestions = [
                    "Check if all dependencies are installed",
                    "Verify your internet connection",
                    "Try running with --debug for more information",
                    "Check GitHub repository permissions",
                    "Clear cache with 'rlex clean'"
                ]
                
                wrapped_error = RepolexError(
                    f"Unexpected error during {operation}: {str(e)}",
                    suggestions=suggestions
                )
                
                handle_error(
                    wrapped_error,
                    operation=operation,
                    show_suggestions=show_suggestions,
                    show_debug=True,  # Always show debug for unexpected errors
                    exit_on_error=exit_on_error
                )
        
        return wrapper
    return decorator

# Special error handlers for specific operations
def git_error_handler(operation: str = "git operation"):
    """Specialized error handler for git operations"""
    return error_handler(
        operation=operation,
        show_suggestions=True,
        show_debug=False
    )

def parsing_error_handler(operation: str = "parsing operation"):
    """Specialized error handler for parsing operations"""
    return error_handler(
        operation=operation,
        show_suggestions=True,
        show_debug=True  # Parsing errors often need debug info
    )

def storage_error_handler(operation: str = "storage operation"):
    """Specialized error handler for storage operations"""
    return error_handler(
        operation=operation,
        show_suggestions=True,
        show_debug=False
    )

# Context manager for error handling
class ErrorContext:
    """Context manager for error handling"""
    
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

# Utility functions for creating specific error types
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

# Success messages
def show_success(message: str, operation: str = "operation") -> None:
    """Show success message"""
    print(f"✓ {operation}: {message}")

# Progress integration
def show_progress_error(tracker, error: Exception) -> None:
    """Show error within progress context"""
    from repolex.models.progress import ProgressLevel
    
    # Add error to progress tracker
    if hasattr(tracker, 'add_event'):
        tracker.add_event(
            stage=tracker.current_stage,
            level=ProgressLevel.ERROR,
            message=f"Error: {str(error)}",
            emoji="✗"
        )
    
    # Show full error display
    handle_error(error, exit_on_error=False)