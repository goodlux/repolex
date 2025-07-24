"""🟡 CodeDoc v2.0 - The Semantic PAC-MAN

PAC-MAN for your codebase! Advanced semantic code analysis that chomps through 
complexity and spits out perfect documentation.

This package provides both CLI and TUI interfaces for semantic code intelligence.
"""

__version__ = "2.0.0"
__title__ = "CodeDoc"
__description__ = "🟡 PAC-MAN for your codebase! Semantic code intelligence system."
__author__ = "Rob"
__license__ = "MIT"

# PAC-MAN themed exports
from codedoc.models.exceptions import (
    CodeDocError,
    GitError, 
    ProcessingError,
    StorageError,
    ValidationError,
    SecurityError,
    ExportError,
    NetworkError,
    ConfigurationError,
)

__all__ = [
    "__version__",
    "__title__", 
    "__description__",
    "__author__",
    "__license__",
    "CodeDocError",
    "GitError",
    "ProcessingError", 
    "StorageError",
    "ValidationError",
    "SecurityError",
    "ExportError",
    "NetworkError",
    "ConfigurationError",
]
