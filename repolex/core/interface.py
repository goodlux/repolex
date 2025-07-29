"""
Repolex Core Interface - Abstract API Definition

Defines the core interface for semantic code intelligence operations.
All implementations must follow this contract.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..models.repository import RepoInfo, RepoDetails, RepoResult, UpdateResult
from ..models.graph import GraphInfo, GraphDetails
from ..models.results import (
    ProcessingResult,
    QueryResult, 
    ExportResult, 
    SystemStatus
)
from ..models.function import FunctionInfo


class RepolexCore(ABC):
    """
    Abstract interface for Repolex operations.
    
    Defines all core operations for semantic code intelligence including
    repository management, graph operations, exports, and queries.
    """
    
    # ═══════════════════════════════════════════════════════════════
    # Repository Operations (File Management)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    def repo_add(self, org_repo: str) -> RepoResult:
        """
        Clone and track a repository.
        
        Args:
            org_repo: Repository identifier in 'org/repo' format
            
        Returns:
            RepoResult: Repository info and available releases
            
        Raises:
            ValidationError: If org_repo format is invalid
            SecurityError: If org_repo contains dangerous characters
            GitError: If repository cannot be cloned or accessed
        """
        pass
    
    @abstractmethod
    def repo_remove(self, org_repo: str, force: bool = False) -> bool:
        """
        Remove repository files and ALL associated semantic data.
        
        Args:
            org_repo: Repository identifier in 'org/repo' format
            force: Skip confirmation prompts (use with caution)
            
        Returns:
            bool: True if successfully removed, False if repository not found
        """
        pass
    
    @abstractmethod
    def repo_list(self) -> List[RepoInfo]:
        """List all tracked repositories."""
        pass
    
    @abstractmethod
    def repo_show(self, org_repo: str) -> RepoDetails:
        """Show detailed information about a specific repository."""
        pass
    
    @abstractmethod
    def repo_update(self, org_repo: str) -> UpdateResult:
        """Update repository with latest commits and releases."""
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # Graph Operations (Semantic Analysis)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    def graph_add(self, org_repo: str, release: Optional[str] = None, enable_nlp: bool = False, force: bool = False) -> ProcessingResult:
        """Parse repository release and add to semantic database."""
        pass
    
    @abstractmethod
    def graph_remove(self, org_repo: str, release: Optional[str] = None, force: bool = False) -> bool:
        """Remove semantic graphs from database."""
        pass
    
    @abstractmethod
    def graph_list(self, org_repo: Optional[str] = None) -> List[GraphInfo]:
        """List semantic graphs in database."""
        pass
    
    @abstractmethod
    def graph_show(self, org_repo: str, release: Optional[str] = None) -> GraphDetails:
        """Show detailed graph information and statistics."""
        pass
    
    @abstractmethod
    def graph_update(self, org_repo: str, release: Optional[str] = None) -> ProcessingResult:
        """Nuclear rebuild of semantic graphs."""
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # Export Operations (Generate Outputs)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    def export_opml(self, org_repo: str, release: str, output: Optional[Path] = None) -> Path:
        """Export as OPML for human browsing."""
        pass
    
    @abstractmethod
    def export_msgpack(self, org_repo: str, release: str, output: Optional[Path] = None) -> Path:
        """Export as compact semantic package."""
        pass
    
    @abstractmethod
    def export_docs(self, org_repo: str, release: str, format: str, output: Path, template: Optional[str] = None) -> Path:
        """Export as documentation in specified format."""
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # Query Operations (Search and Query)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    def query_sparql(self, query: str, format: str = "table", output: Optional[Path] = None) -> QueryResult:
        """Execute SPARQL query against semantic database."""
        pass
    
    @abstractmethod
    def query_functions(self, search_term: str, repo: Optional[str] = None, release: Optional[str] = None) -> List[FunctionInfo]:
        """Search functions using natural language."""
        pass
    
    # ═══════════════════════════════════════════════════════════════
    # System Operations (Configuration and Status)
    # ═══════════════════════════════════════════════════════════════
    
    @abstractmethod
    def show_config(self) -> Dict[str, Any]:
        """Show current system configuration."""
        pass
    
    @abstractmethod
    def update_config(self, key: str, value: str) -> bool:
        """Update a configuration setting with validation."""
        pass
    
    @abstractmethod
    def show_status(self) -> SystemStatus:
        """Show comprehensive system status."""
        pass
    
    @abstractmethod
    def remove_everything(self, confirm: bool = False) -> bool:
        """Nuclear option: remove all repositories, graphs, and exports."""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the core system."""
        pass
