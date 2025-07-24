"""🟡 PAC-MAN Error Handling System

Custom exception hierarchy for CodeDoc with helpful suggestions and PAC-MAN themed messages.
Each error provides actionable guidance to help users get back on track!
"""

from typing import List, Optional


class CodeDocError(Exception):
    """
    🟡 Base PAC-MAN exception for all CodeDoc errors.
    
    Every error comes with helpful suggestions because PAC-MAN always finds a way around obstacles!
    """
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.suggestions = suggestions or []
        
    def __str__(self) -> str:
        error_msg = f"🟡 {self.message}"
        if self.suggestions:
            suggestions_text = "\n".join(f"💡 {suggestion}" for suggestion in self.suggestions)
            error_msg += f"\n\n{suggestions_text}"
        return error_msg


class GitError(CodeDocError):
    """🔄 Git operations failed - maybe the ghost got in the way!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check that the repository URL is correct",
            "Verify you have internet connection", 
            "Make sure you have git installed",
            "Try cloning manually first: git clone <repo-url>"
        ]
        super().__init__(
            f"Git chomping failed: {message}",
            suggestions or default_suggestions
        )


class ProcessingError(CodeDocError):
    """🧠 AST parsing or semantic analysis failed - PAC-MAN couldn't digest this!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check that the repository contains valid Python code",
            "Verify the repository structure is standard",
            "Try processing a smaller subset first",
            "Check the logs for more detailed error information"
        ]
        super().__init__(
            f"Semantic digestion failed: {message}",
            suggestions or default_suggestions
        )


class StorageError(CodeDocError):
    """💾 Oxigraph operations failed - the semantic maze is blocked!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check available disk space",
            "Verify write permissions to ~/.codedoc/",
            "Try clearing the database: codedoc db clear",
            "Restart with a fresh database"
        ]
        super().__init__(
            f"Semantic storage failed: {message}",
            suggestions or default_suggestions
        )


class ValidationError(CodeDocError):
    """⚠️ Input validation failed - PAC-MAN needs proper directions!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check the command format: codedoc --help",
            "Verify your input follows the expected pattern",
            "Try the examples in the documentation"
        ]
        super().__init__(
            f"Input validation failed: {message}",
            suggestions or default_suggestions
        )


class SecurityError(CodeDocError):
    """🛡️ Security validation failed - PAC-MAN detected danger!"""
    
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


class ExportError(CodeDocError):
    """📦 Export generation failed - PAC-MAN couldn't package the power pills!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check available disk space for exports",
            "Verify write permissions to output directory",
            "Make sure the semantic graphs exist first",
            "Try a different export format"
        ]
        super().__init__(
            f"Export generation failed: {message}",
            suggestions or default_suggestions
        )


class NetworkError(CodeDocError):
    """🌐 Network operations failed - the internet ghosts are interfering!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check your internet connection",
            "Verify the repository URL is accessible",
            "Try again in a few minutes",
            "Check if GitHub is experiencing issues"
        ]
        super().__init__(
            f"Network operation failed: {message}",
            suggestions or default_suggestions
        )


class ConfigurationError(CodeDocError):
    """⚙️ Configuration failed - PAC-MAN needs proper settings!"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None):
        default_suggestions = [
            "Check configuration file syntax",
            "Reset to defaults: codedoc config reset",
            "Verify all required settings are present",
            "Check file permissions for config directory"
        ]
        super().__init__(
            f"Configuration error: {message}",
            suggestions or default_suggestions
        )


class RepositoryNotFoundError(CodeDocError):
    """📁 Repository not found - PAC-MAN can't find that maze!"""
    
    def __init__(self, repo_name: str):
        super().__init__(
            f"Repository '{repo_name}' not found",
            [
                f"Add the repository first: codedoc repo add {repo_name}",
                "Check the repository name spelling",
                "Use 'codedoc repo list' to see available repositories",
                "Verify the repository exists and is accessible"
            ]
        )


class GraphNotFoundError(CodeDocError):
    """🧠 Semantic graphs not found - PAC-MAN hasn't digested this yet!"""
    
    def __init__(self, repo_name: str, version: Optional[str] = None):
        version_text = f" version {version}" if version else ""
        super().__init__(
            f"Semantic graphs for '{repo_name}{version_text}' not found",
            [
                f"Process the repository first: codedoc graph add {repo_name}{' ' + version if version else ''}",
                "Check that the version exists: codedoc repo show " + repo_name,
                "Use 'codedoc graph list' to see available graphs",
                "Try processing the latest version if version not specified"
            ]
        )


class VersionNotFoundError(CodeDocError):
    """🏷️ Version not found - PAC-MAN can't find that level!"""
    
    def __init__(self, repo_name: str, version: str):
        super().__init__(
            f"Version '{version}' not found in repository '{repo_name}'",
            [
                f"Check available versions: codedoc repo show {repo_name}",
                "Verify the version tag exists in the git repository",
                "Try using 'latest' to get the most recent version",
                "Update the repository: codedoc repo update " + repo_name
            ]
        )


# PAC-MAN themed error messages for specific scenarios
class DatabaseCorruptedError(StorageError):
    """💥 Database corruption detected - PAC-MAN's maze is broken!"""
    
    def __init__(self):
        super().__init__(
            "Semantic database appears to be corrupted",
            [
                "🟡 Nuclear option: codedoc db clear (removes all data)",
                "Try reprocessing repositories from scratch",
                "Check disk health and available space",
                "Backup important exports before clearing database"
            ]
        )


class TooManyGhostsError(ProcessingError):
    """👻 Too many private functions detected - ghosts everywhere!"""
    
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


class PowerPillTooLargeError(ExportError):
    """💊 Power pill too large - PAC-MAN can't swallow this!"""
    
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
