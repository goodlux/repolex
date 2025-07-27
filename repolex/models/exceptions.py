"""
Exception hierarchy for Repolex operations.

Custom exception hierarchy with helpful suggestions and clear error messages.
Each error provides actionable guidance to help users resolve issues.
"""

from typing import List, Optional


class RepolexError(Exception):
    """
    Base exception for all Repolex errors.
    
    Every error comes with helpful suggestions to guide users toward resolution.
    """
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.suggestions = suggestions or []
        
    def __str__(self) -> str:
        error_msg = self.message
        if self.suggestions:
            suggestions_text = "\n".join(f"  • {suggestion}" for suggestion in self.suggestions)
            error_msg += f"\n\nSuggestions:\n{suggestions_text}"
        return error_msg


class GitError(RepolexError):
    """Git operations failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check that the repository URL is correct",
            "Verify you have internet connection", 
            "Make sure you have git installed",
            "Try cloning manually first: git clone <repo-url>"
        ]
        super().__init__(
            f"Git operation failed: {message}",
            suggestions or default_suggestions
        )


class ProcessingError(RepolexError):
    """AST parsing or semantic analysis failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check that the repository contains valid Python code",
            "Verify the repository structure is standard",
            "Try processing a smaller subset first",
            "Check the logs for more detailed error information"
        ]
        super().__init__(
            f"Processing failed: {message}",
            suggestions or default_suggestions
        )


class StorageError(RepolexError):
    """Database operations failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check available disk space",
            "Verify write permissions to ~/.Repolex/",
            "Try clearing the database: rlex db clear",
            "Restart with a fresh database"
        ]
        super().__init__(
            f"Storage operation failed: {message}",
            suggestions or default_suggestions
        )


class ValidationError(RepolexError):
    """Input validation failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check the command format: rlex --help",
            "Verify your input follows the expected pattern",
            "Try the examples in the documentation"
        ]
        super().__init__(
            f"Validation failed: {message}",
            suggestions or default_suggestions
        )


class SecurityError(RepolexError):
    """Security validation failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Avoid path traversal characters (.. / \\)",
            "Use only trusted repository sources",
            "Check file paths are within allowed directories",
            "Review security guidelines in documentation"
        ]
        super().__init__(
            f"Security check failed: {message}",
            suggestions or default_suggestions
        )


class ExportError(RepolexError):
    """Export generation failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check available disk space for exports",
            "Verify write permissions to output directory",
            "Make sure the semantic graphs exist first",
            "Try a different export format"
        ]
        super().__init__(
            f"Export failed: {message}",
            suggestions or default_suggestions
        )


class NetworkError(RepolexError):
    """Network operations failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check your internet connection",
            "Verify the repository URL is accessible", 
            "Check if GitHub is experiencing issues",
            "Verify you have access to the repository"
        ]
        super().__init__(
            f"Network operation failed: {message}",
            suggestions or default_suggestions
        )


class ConfigurationError(RepolexError):
    """Configuration failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check configuration file syntax",
            "Reset to defaults: rlex config reset",
            "Verify all required settings are present",
            "Check file permissions for config directory"
        ]
        super().__init__(
            f"Configuration error: {message}",
            suggestions or default_suggestions
        )


class RepositoryNotFoundError(RepolexError):
    """Repository not found"""
    
    def __init__(self, repo_name: str):
        super().__init__(
            f"Repository '{repo_name}' not found",
            [
                f"Add the repository first: rlex repo add {repo_name}",
                "Check the repository name spelling",
                "Use 'rlex repo list' to see available repositories",
                "Verify the repository exists and is accessible"
            ]
        )


class GraphNotFoundError(RepolexError):
    """Semantic graphs not found"""
    
    def __init__(self, repo_name: str, version: Optional[str] = None):
        version_text = f" version {version}" if version else ""
        super().__init__(
            f"Semantic graphs for '{repo_name}{version_text}' not found",
            [
                f"Process the repository first: rlex graph add {repo_name}{' ' + version if version else ''}",
                "Check that the version exists: rlex repo show " + repo_name,
                "Use 'rlex graph list' to see available graphs",
                "Try processing the latest version if version not specified"
            ]
        )


class VersionNotFoundError(RepolexError):
    """Version not found"""
    
    def __init__(self, repo_name: str, version: str):
        super().__init__(
            f"Version '{version}' not found in repository '{repo_name}'",
            [
                f"Check available versions: rlex repo show {repo_name}",
                "Verify the version tag exists in the git repository",
                "Try using 'latest' to get the most recent version",
                "Update the repository: rlex repo update " + repo_name
            ]
        )


# Specific error types for common scenarios
class DatabaseCorruptedError(StorageError):
    """Database corruption detected"""
    
    def __init__(self):
        super().__init__(
            "Database appears to be corrupted",
            [
                "Clear and recreate database: rlex db clear",
                "Try reprocessing repositories from scratch",
                "Check disk health and available space",
                "Backup important exports before clearing database"
            ]
        )


class TooManyPrivateFunctionsError(ProcessingError):
    """Too many private functions detected"""
    
    def __init__(self, private_count: int, total_count: int):
        super().__init__(
            f"Repository has {private_count} private functions out of {total_count} total",
            [
                "This is normal for large codebases",
                "Private functions are tracked but not exported by default",
                "Use --include-private flag to process all functions",
                "Focus on public API for documentation purposes"
            ]
        )


class SPARQLError(RepolexError):
    """SPARQL query execution failed"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check SPARQL query syntax",
            "Verify referenced graphs exist", 
            "Ensure required prefixes are defined",
            "Try a simpler query to test connection"
        ]
        super().__init__(
            f"SPARQL query failed: {message}",
            suggestions or default_suggestions
        )


class ExportTooLargeError(ExportError):
    """Export file too large"""
    
    def __init__(self, size_mb: float):
        super().__init__(
            f"Export file would be {size_mb:.1f}MB, exceeding recommended size",
            [
                "Try exporting specific versions instead of all versions",
                "Use --public-only flag to exclude private functions", 
                "Split large repositories into smaller exports",
                "Consider using streaming export for very large datasets"
            ]
        )