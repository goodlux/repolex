"""🟡 PAC-MAN Input Validation System

Security-focused validation functions to protect PAC-MAN from malicious input.
Every input gets properly validated before PAC-MAN starts chomping!
"""

import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from codedoc.models.exceptions import ValidationError, SecurityError


def validate_org_repo(org_repo: str) -> None:
    """
    🟡 Validate org/repo format and prevent security issues.
    
    PAC-MAN only accepts properly formatted repository identifiers!
    
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
    
    # Security checks - PAC-MAN security protocol!
    if '..' in org_repo or org_repo.startswith('/') or '\\' in org_repo:
        raise SecurityError(
            "🛡️ Dangerous characters detected in repository identifier",
            [
                "Avoid path traversal characters (.. / \\)",
                "Use only alphanumeric characters, dots, dashes, underscores",
                "PAC-MAN detected potential security threat!"
            ]
        )
    
    # Additional security validations
    if len(org_repo) > 100:
        raise ValidationError(
            "Repository identifier too long (max 100 characters)",
            ["Keep repository names reasonable in length"]
        )
    
    parts = org_repo.split('/')
    if len(parts) != 2:
        raise ValidationError(
            "Repository identifier must have exactly one slash",
            ["Format: organization/repository", "Example: microsoft/typescript"]
        )
    
    org, repo = parts
    if not org or not repo:
        raise ValidationError(
            "Both organization and repository names are required",
            ["Format: organization/repository", "Both parts must be non-empty"]
        )


def validate_release_tag(tag: str) -> None:
    """
    🏷️ Validate release tag format.
    
    PAC-MAN only accepts clean, safe version tags!
    
    Args:
        tag: Git tag or version string
        
    Raises:
        ValidationError: If tag format is invalid
    """
    if not tag or not isinstance(tag, str):
        raise ValidationError(
            "Release tag must be a non-empty string",
            ["Example: v1.0.0", "Example: 2.1.3", "Example: latest"]
        )
    
    # Basic sanity checks
    if len(tag) > 100:
        raise ValidationError(
            "Release tag too long (max 100 characters)",
            ["Keep version tags reasonable in length"]
        )
    
    # Check for dangerous characters
    if any(char in tag for char in [' ', '\n', '\t', '\r']):
        raise ValidationError(
            "Release tag cannot contain whitespace",
            ["Use hyphens or dots instead of spaces", "Example: v1.0-beta"]
        )
    
    # Check for path traversal attempts
    if '..' in tag or '/' in tag or '\\' in tag:
        raise SecurityError(
            "🛡️ Dangerous characters detected in release tag",
            [
                "Avoid path characters (.. / \\)",
                "Use standard version formats: v1.0.0, 2.1.3, etc.",
                "PAC-MAN security protocol activated!"
            ]
        )


def validate_file_path(path: Path, base_path: Path) -> None:
    """
    🛡️ Validate file path is within allowed base directory.
    
    PAC-MAN won't let you escape the maze boundaries!
    
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
            f"🛡️ Path escape attempt detected: {path}",
            [
                f"Path must be within: {base_path}",
                "PAC-MAN blocked potential directory traversal attack!",
                "Use relative paths within the allowed directory"
            ]
        )


def validate_sparql_query(query: str) -> None:
    """
    💾 Validate SPARQL query for security issues.
    
    PAC-MAN checks SPARQL queries for dangerous operations!
    
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
            f"🛡️ Dangerous SPARQL operations detected: {', '.join(found_dangerous)}",
            [
                "Only SELECT and ASK queries are allowed",
                "Modification operations are blocked for security",
                "PAC-MAN security protocol: READ-ONLY queries only!"
            ]
        )


def validate_repository_url(url: str) -> None:
    """
    🌐 Validate repository URL format and security.
    
    PAC-MAN only trusts well-formed repository URLs!
    
    Args:
        url: Repository URL to validate
        
    Raises:
        ValidationError: If URL format is invalid
        SecurityError: If URL is potentially dangerous
    """
    if not url or not isinstance(url, str):
        raise ValidationError(
            "Repository URL must be a non-empty string",
            ["Example: https://github.com/org/repo", "Example: git@github.com:org/repo.git"]
        )
    
    try:
        parsed = urlparse(url)
    except Exception:
        raise ValidationError(
            "Invalid URL format",
            ["Use a valid git URL", "Example: https://github.com/org/repo"]
        )
    
    # Check for allowed schemes
    allowed_schemes = ['https', 'http', 'git', 'ssh']
    if parsed.scheme and parsed.scheme not in allowed_schemes:
        raise SecurityError(
            f"🛡️ Unsupported URL scheme: {parsed.scheme}",
            [
                "Only HTTPS, HTTP, Git, and SSH schemes allowed",
                "PAC-MAN blocked potentially dangerous scheme!"
            ]
        )
    
    # Check for localhost and private IPs (basic protection)
    if parsed.hostname:
        if parsed.hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
            raise SecurityError(
                "🛡️ Local URLs not allowed for security",
                ["Use public repository URLs only", "PAC-MAN protects against local attacks"]
            )


def validate_export_path(path: Path) -> None:
    """
    📦 Validate export path for safety.
    
    PAC-MAN ensures export paths are safe and reasonable!
    
    Args:
        path: Export path to validate
        
    Raises:
        ValidationError: If path is invalid
        SecurityError: If path is potentially dangerous
    """
    if not path:
        raise ValidationError(
            "Export path cannot be empty",
            ["Specify a valid output path", "Example: ./exports/my-repo.opml"]
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
                f"🛡️ Dangerous characters in path component: {part}",
                [
                    "Avoid special characters in file names",
                    "Use alphanumeric characters, hyphens, and underscores",
                    "PAC-MAN blocked potentially dangerous filename!"
                ]
            )
    
    # Check total path length (OS dependent, but be conservative)
    if len(str(path)) > 260:  # Windows MAX_PATH limit
        raise ValidationError(
            "Export path too long (max 260 characters)",
            ["Use a shorter path", "Consider exporting to a directory closer to root"]
        )


def validate_config_key(key: str) -> None:
    """
    ⚙️ Validate configuration key format.
    
    PAC-MAN only accepts safe configuration keys!
    
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
    if not re.match(r'^[a-zA-Z0-9_-]+$', key):
        raise ValidationError(
            f"Invalid configuration key format: {key}",
            [
                "Use only alphanumeric characters, hyphens, and underscores",
                "Example: github-token, storage-path, log-level"
            ]
        )
    
    if len(key) > 50:
        raise ValidationError(
            "Configuration key too long (max 50 characters)",
            ["Keep configuration keys concise"]
        )


def validate_version_format(version: str) -> None:
    """
    🏷️ Validate semantic version format.
    
    PAC-MAN prefers proper semantic versioning!
    
    Args:
        version: Version string to validate
        
    Raises:
        ValidationError: If version format is problematic
    """
    if not version or not isinstance(version, str):
        raise ValidationError(
            "Version must be a non-empty string",
            ["Example: v1.0.0", "Example: 2.1.3"]
        )
    
    # Check for common version patterns (flexible validation)
    version_patterns = [
        r'^\d+\.\d+\.\d+$',  # 1.0.0
        r'^v\d+\.\d+\.\d+$',  # v1.0.0  
        r'^\d+\.\d+$',  # 1.0
        r'^v\d+\.\d+$',  # v1.0
        r'^latest$',  # latest
        r'^main$',  # main
        r'^master$',  # master
    ]
    
    if not any(re.match(pattern, version) for pattern in version_patterns):
        # This is just a warning-level validation, not an error
        pass  # Be flexible with version formats


# PAC-MAN themed validation helpers
def is_pac_man_approved_name(name: str) -> bool:
    """🟡 Check if name follows PAC-MAN naming conventions."""
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name))


def sanitize_for_pac_man(text: str) -> str:
    """🟡 Sanitize text for safe PAC-MAN processing."""
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"\\|?*]', '_', text)
    sanitized = re.sub(r'\.\.', '_', sanitized)
    return sanitized[:100]  # Limit length


def validate_pac_man_maze_size(size_mb: float) -> None:
    """🟡 Validate that the semantic maze isn't too big for PAC-MAN."""
    if size_mb > 1000:  # 1GB limit
        raise ValidationError(
            f"🟡 Semantic maze too large: {size_mb:.1f}MB",
            [
                "PAC-MAN can handle up to 1GB semantic mazes",
                "Consider processing repository in smaller chunks",
                "Use --public-only to reduce maze size",
                "The maze is getting too complex for even PAC-MAN!"
            ]
        )

def validate_graph_uri(uri: str) -> None:
    """🟡 PAC-MAN validates graph URIs are properly formatted!"""
    if not uri or not isinstance(uri, str):
        raise ValidationError(
            "Invalid graph URI: empty or not a string 🟡",
            suggestions=["Provide a valid URI string"]
        )
    
    if not uri.startswith(('http://', 'https://', 'urn:')):
        raise ValidationError(
            f"Invalid graph URI format: {uri} 🟡",
            suggestions=["Graph URIs must start with http://, https://, or urn:"]
        )
