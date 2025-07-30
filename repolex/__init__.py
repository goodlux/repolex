"""
repolex - Semantic Code Intelligence System

Advanced semantic code analysis for repository documentation and intelligence.
Provides both CLI and programmatic interfaces for semantic analysis.
"""

__version__ = "2.0.0"
__title__ = "Repolex"
__description__ = "Semantic code intelligence system for repository analysis"
__author__ = "Rob"
__license__ = "MIT"

# Core exception exports
from repolex.models.exceptions import (
    RepolexError,
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
    "RepolexError",
    "GitError",
    "ProcessingError", 
    "StorageError",
    "ValidationError",
    "SecurityError",
    "ExportError",
    "NetworkError",
    "ConfigurationError",
]