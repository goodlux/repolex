"""
Input Validation System

Security-focused validation functions to protect against malicious input.
All inputs are validated before processing begins.
"""

import re
from pathlib import Path
from urllib.parse import urlparse

from repolex.models.exceptions import ValidationError, SecurityError


def validate_org_repo(org_repo: str) -> None:
    """
    Validate org/repo format and prevent security issues.
    
    Args:
        org_repo: Repository identifier in 'org/repo' format
        
    Raises:
        ValidationError: If format is invalid
        SecurityError: If contains dangerous characters
    """
    if not org_repo or not isinstance(org_repo, str):
        raise ValidationError(
            "Repository identifier must be a non-empty string",
            ["Use format: organization/repository", "Example: pixeltable/pixeltable"]
        )
    
    # Check basic format
    if not re.match(r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$', org_repo):
        raise ValidationError(
            f"Invalid org/repo format: {org_repo}",
            [
                "Use format: organization/repository",
                "Only alphanumeric, dots, dashes, underscores allowed",
                "Example: goodlux/pixeltable"
            ]
        )
    
    # Security checks - prevent path traversal
    if '..' in org_repo or org_repo.startswith('/') or '\\' in org_repo:
        raise SecurityError(
            "Dangerous characters detected in repository identifier",
            [
                "Avoid path traversal characters (.. / \\)",
                "Use only alphanumeric characters, dots, dashes, underscores"
            ]
        )
    
    # Length validation
    if len(org_repo) > 100:
        raise ValidationError(
            "Repository identifier too long (max 100 characters)"
        )
    
    parts = org_repo.split('/')
    if len(parts) != 2:
        raise ValidationError(
            "Repository identifier must have exactly one slash",
            ["Format: organization/repository"]
        )
    
    org, repo = parts
    if not org or not repo:
        raise ValidationError(
            "Both organization and repository names are required"
        )


def validate_release_tag(tag: str) -> None:
    """
    Validate release tag format.
    
    Args:
        tag: Git tag or version string
        
    Raises:
        ValidationError: If tag format is invalid
        SecurityError: If contains dangerous characters
    """
    if not tag or not isinstance(tag, str):
        raise ValidationError(
            "Release tag must be a non-empty string",
            ["Example: v1.0.0", "Example: 2.1.3"]
        )
    
    # Length check
    if len(tag) > 100:
        raise ValidationError("Release tag too long (max 100 characters)")
    
    # Check for dangerous characters
    if any(char in tag for char in [' ', '\n', '\t', '\r']):
        raise ValidationError(
            "Release tag cannot contain whitespace",
            ["Use hyphens or dots instead of spaces"]
        )
    
    # Security check for path traversal
    if '..' in tag or '/' in tag or '\\' in tag:
        raise SecurityError(
            "Dangerous characters detected in release tag",
            ["Avoid path characters (.. / \\)", "Use standard version formats"]
        )


def validate_file_path(path: Path, base_path: Path) -> None:
    """
    Validate file path is within allowed base directory.
    
    Args:
        path: File path to validate
        base_path: Base directory that must contain the path
        
    Raises:
        SecurityError: If path is outside allowed directory
    """
    try:
        resolved_path = path.resolve()
        resolved_base = base_path.resolve()
        
        # Check if path is within base directory
        resolved_path.relative_to(resolved_base)
        
    except ValueError:
        raise SecurityError(
            f"Path escape attempt detected: {path}",
            [
                f"Path must be within: {base_path}",
                "Use relative paths within the allowed directory"
            ]
        )


def validate_sparql_query(query: str) -> None:
    """
    Validate SPARQL query for security issues.
    
    Args:
        query: SPARQL query string
        
    Raises:
        SecurityError: If query contains dangerous operations
        ValidationError: If query format is invalid
    """
    if not query or not isinstance(query, str):
        raise ValidationError(
            "SPARQL query must be a non-empty string",
            ["Example: SELECT ?name WHERE { ?f woc:hasName ?name }"]
        )
    
    if len(query) > 10000:  # Reasonable limit
        raise ValidationError(
            "SPARQL query too long (max 10,000 characters)",
            ["Break complex queries into smaller parts"]
        )
    
    # Security checks for dangerous SPARQL operations
    dangerous_keywords = [
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 'CLEAR', 
        'CREATE', 'LOAD', 'COPY', 'MOVE', 'ADD'
    ]
    
    query_upper = query.upper()
    found_dangerous = [keyword for keyword in dangerous_keywords if keyword in query_upper]
    
    if found_dangerous:
        raise SecurityError(
            f"Dangerous SPARQL operations detected: {', '.join(found_dangerous)}",
            [
                "Only SELECT and ASK queries are allowed",
                "Modification operations are blocked for security"
            ]
        )


def validate_repository_url(url: str) -> None:
    """
    Validate repository URL format and security.
    
    Args:
        url: Repository URL to validate
        
    Raises:
        ValidationError: If URL format is invalid
        SecurityError: If URL is potentially dangerous
    """
    if not url or not isinstance(url, str):
        raise ValidationError(
            "Repository URL must be a non-empty string",
            ["Example: https://github.com/org/repo"]
        )
    
    try:
        parsed = urlparse(url)
    except Exception:
        raise ValidationError(
            "Invalid URL format",
            ["Use a valid git URL"]
        )
    
    # Check for allowed schemes
    allowed_schemes = ['https', 'http', 'git', 'ssh']
    if parsed.scheme and parsed.scheme not in allowed_schemes:
        raise SecurityError(
            f"Unsupported URL scheme: {parsed.scheme}",
            ["Only HTTPS, HTTP, Git, and SSH schemes allowed"]
        )
    
    # Check for localhost and private IPs (basic protection)
    if parsed.hostname:
        if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
            raise SecurityError(
                "Local URLs not allowed for security",
                ["Use public repository URLs only"]
            )


def validate_export_path(path: Path) -> None:
    """
    Validate export path for safety.
    
    Args:
        path: Export path to validate
        
    Raises:
        ValidationError: If path is invalid
        SecurityError: If path is potentially dangerous
    """
    if not path:
        raise ValidationError(
            "Export path cannot be empty",
            ["Specify a valid output path"]
        )
    
    # Convert to Path object if string
    if isinstance(path, str):
        path = Path(path)
    
    # Check for dangerous path components
    parts = path.parts
    for part in parts:
        if part in ['..', '.', '']:
            continue  # These are ok in some contexts
        if any(char in part for char in ['<', '>', ':', '"', '|', '?', '*']):
            raise SecurityError(
                f"Dangerous characters in path component: {part}",
                ["Avoid special characters in file names"]
            )
    
    # Check total path length (OS dependent, but be conservative)
    if len(str(path)) > 260:  # Windows MAX_PATH limit
        raise ValidationError(
            "Export path too long (max 260 characters)",
            ["Use a shorter path"]
        )


def validate_config_key(key: str) -> None:
    """
    Validate configuration key format.
    
    Args:
        key: Configuration key to validate
        
    Raises:
        ValidationError: If key format is invalid
    """
    if not key or not isinstance(key, str):
        raise ValidationError(
            "Configuration key must be a non-empty string",
            ["Example: github-token", "Example: storage-path"]
        )
    
    # Check format (alphanumeric + hyphens/underscores)
    if not re.match(r'^[a-zA-Z0-9_.-]+$', key):
        raise ValidationError(
            f"Invalid configuration key format: {key}",
            ["Use only alphanumeric characters, hyphens, underscores, and dots"]
        )
    
    if len(key) > 50:
        raise ValidationError("Configuration key too long (max 50 characters)")


def validate_graph_uri(uri: str) -> None:
    """
    Validate graph URIs are properly formatted.
    
    Args:
        uri: Graph URI to validate
        
    Raises:
        ValidationError: If URI format is invalid
    """
    if not uri or not isinstance(uri, str):
        raise ValidationError(
            "Graph URI must be a non-empty string",
            ["Provide a valid URI string"]
        )
    
    if not uri.startswith(('http://', 'https://', 'urn:')):
        raise ValidationError(
            f"Invalid graph URI format: {uri}",
            ["Graph URIs must start with http://, https://, or urn:"]
        )


# Simple utility functions
def sanitize_filename(text: str) -> str:
    """Sanitize text for safe filename usage."""
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"\\|?*]', '_', text)
    sanitized = re.sub(r'\.\.', '_', sanitized)
    return sanitized[:100]  # Limit length


def is_valid_identifier(name: str) -> bool:
    """Check if name is a valid identifier."""
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name))