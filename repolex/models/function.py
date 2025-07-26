"""🟡 PAC-MAN Function Data Models

Data models for functions, parameters, and all the semantic dots PAC-MAN eats!
These represent the core entities in our semantic feast.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field, validator
from enum import Enum


class FunctionVisibility(str, Enum):
    """👁️ Function visibility levels (PAC-MAN vs Ghosts)."""
    PUBLIC = "public"          # 🟡 PAC-MAN can eat these!
    PRIVATE = "private"        # 👻 Ghost functions (hidden)
    PROTECTED = "protected"    # 🔒 Semi-private
    INTERNAL = "internal"      # 🔧 Internal implementation


class ParameterKind(str, Enum):
    """📋 Types of function parameters."""
    POSITIONAL = "positional"           # Standard positional arg
    KEYWORD = "keyword"                 # Keyword-only arg
    VAR_POSITIONAL = "var_positional"   # *args
    VAR_KEYWORD = "var_keyword"         # **kwargs
    POSITIONAL_ONLY = "positional_only" # / separator args


class FunctionType(str, Enum):
    """🔧 Types of callable entities."""
    FUNCTION = "function"      # Regular function
    METHOD = "method"          # Class method
    CLASSMETHOD = "classmethod" # @classmethod
    STATICMETHOD = "staticmethod" # @staticmethod
    PROPERTY = "property"      # @property
    COROUTINE = "coroutine"    # def


class ParameterInfo(BaseModel):
    """📋 Information about a function parameter."""
    
    # Basic parameter info
    name: str = Field(description="📝 Parameter name")
    type_annotation: Optional[str] = Field(default=None, description="🏷️ Type annotation")
    kind: ParameterKind = Field(description="📋 Parameter kind")
    
    # Default value
    has_default: bool = Field(default=False, description="❓ Has default value")
    default_value: Optional[str] = Field(default=None, description="🔢 Default value (as string)")
    
    # Documentation
    description: Optional[str] = Field(default=None, description="📚 Parameter description from docstring")
    
    # Validation info
    required: bool = Field(description="⚠️ Parameter is required")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "name",
                "type_annotation": "str",
                "kind": "positional",
                "required": True,
                "description": "Name of the table to create"
            }
        }


class DocstringInfo(BaseModel):
    """📚 Parsed docstring information."""
    
    # Main description
    short_description: Optional[str] = Field(default=None, description="📝 Brief description")
    long_description: Optional[str] = Field(default=None, description="📖 Detailed description")
    
    # Structured sections
    parameters: Dict[str, str] = Field(
        default_factory=dict,
        description="📋 Parameter descriptions"
    )
    returns: Optional[str] = Field(default=None, description="↩️ Return value description")
    raises: Dict[str, str] = Field(
        default_factory=dict,
        description="❌ Exception descriptions"
    )
    examples: List[str] = Field(
        default_factory=list,
        description="💡 Usage examples"
    )
    
    # Additional sections
    notes: List[str] = Field(default_factory=list, description="📝 Additional notes")
    warnings: List[str] = Field(default_factory=list, description="⚠️ Warnings")
    see_also: List[str] = Field(default_factory=list, description="🔗 Related functions")
    
    class Config:
        schema_extra = {
            "example": {
                "short_description": "Creates a new table with specified schema",
                "parameters": {
                    "name": "Name of the table to create",
                    "schema": "Table schema definition"
                },
                "returns": "Table object for the created table",
                "examples": ["pxt.create_table('users', {'id': int, 'name': str})"]
            }
        }


class FunctionLocation(BaseModel):
    """📍 Location information for a function."""
    
    # File location
    file_path: str = Field(description="📁 Relative file path")
    start_line: int = Field(description="🔢 Starting line number")
    end_line: int = Field(description="🔢 Ending line number")
    
    # Module information
    module_name: str = Field(description="📦 Python module name")
    class_name: Optional[str] = Field(default=None, description="🏛️ Class name (if method)")
    
    # GitHub integration
    github_url: Optional[str] = Field(default=None, description="🔗 GitHub source URL")
    
    def generate_github_url(self, org: str, repo: str, version: str) -> str:
        """🔗 Generate GitHub source URL on demand."""
        base = f"https://github.com/{org}/{repo}/blob/{version}/{self.file_path}"
        if self.start_line and self.end_line:
            return f"{base}#L{self.start_line}-L{self.end_line}"
        elif self.start_line:
            return f"{base}#L{self.start_line}"
        return base
    
    class Config:
        schema_extra = {
            "example": {
                "file_path": "pixeltable/core.py",
                "start_line": 142,
                "end_line": 187,
                "module_name": "pixeltable.core",
                "github_url": "https://github.com/pixeltable/pixeltable/blob/v0.4.14/pixeltable/core.py#L142-L187"
            }
        }


class FunctionInfo(BaseModel):
    """🟡 Complete information about a function (PAC-MAN's favorite snack!)."""
    
    # Basic identification
    name: str = Field(description="📝 Function name")
    canonical_name: str = Field(description="🎯 Canonical identifier (for stable identity)")
    signature: str = Field(description="✍️ Complete function signature")
    
    # Function classification
    function_type: FunctionType = Field(description="🔧 Type of callable")
    visibility: FunctionVisibility = Field(description="👁️ Visibility level")
    
    # Location information
    location: FunctionLocation = Field(description="📍 Where PAC-MAN found this function")
    
    # Type information
    return_type: Optional[str] = Field(default=None, description="↩️ Return type annotation")
    parameters: List[ParameterInfo] = Field(
        default_factory=list,
        description="📋 Function parameters"
    )
    
    # Documentation
    docstring: Optional[str] = Field(default=None, description="📚 Raw docstring")
    docstring_info: Optional[DocstringInfo] = Field(
        default=None,
        description="📖 Parsed docstring information"
    )
    
    # Semantic tags
    tags: List[str] = Field(
        default_factory=list,
        description="🏷️ Semantic tags (e.g., 'core', 'table', 'image')"
    )
    
    # Related functions
    related_functions: List[str] = Field(
        default_factory=list,
        description="🔗 Names of related functions"
    )
    
    # Quality metrics
    complexity_score: Optional[float] = Field(
        default=None,
        description="🧠 Complexity score (if calculated)"
    )
    
    # PAC-MAN specific
    dots_collected: int = Field(
        default=0,
        description="🔵 Semantic dots collected from this function"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "name": "create_table",
                "canonical_name": "pixeltable.create_table",
                "signature": "create_table(name: str, schema: Dict[str, Any] = None) -> Table",
                "function_type": "function",
                "visibility": "public",
                "return_type": "Table",
                "tags": ["core", "table", "creation"],
                "dots_collected": 125
            }
        }


class FunctionImplementation(BaseModel):
    """🔧 Version-specific implementation of a function."""
    
    # Links to stable identity
    stable_function_id: str = Field(description="🟡 Stable function identifier")
    version: str = Field(description="🏷️ Version this implementation belongs to")
    
    # Implementation details
    function_info: FunctionInfo = Field(description="🔧 Function implementation details")
    
    # Version-specific changes
    changed_from_previous: bool = Field(default=False, description="🔄 Changed from previous version")
    change_description: Optional[str] = Field(
        default=None,
        description="📝 Description of changes"
    )
    
    # Processing metadata
    processed_at: datetime = Field(description="⏰ When PAC-MAN processed this")
    processing_time: float = Field(description="⏱️ Processing time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "stable_function_id": "function:pixeltable/pixeltable/create_table",
                "version": "v0.4.14",
                "changed_from_previous": True,
                "change_description": "Added optional schema parameter",
                "processing_time": 0.05
            }
        }


class FunctionSearchResult(BaseModel):
    """🔍 Result from function search operations."""
    
    # Function identification
    function_info: FunctionInfo = Field(description="🟡 Function information")
    repository: str = Field(description="📚 Repository identifier")
    version: str = Field(description="🏷️ Version")
    
    # Search relevance
    relevance_score: float = Field(description="🎯 Search relevance (0-1)")
    match_reasons: List[str] = Field(
        default_factory=list,
        description="💡 Why this function matched the search"
    )
    
    # Context information
    usage_examples: List[str] = Field(
        default_factory=list,
        description="💡 Relevant usage examples"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "repository": "pixeltable/pixeltable",
                "version": "v0.4.14",
                "relevance_score": 0.95,
                "match_reasons": [
                    "Function name contains 'table'",
                    "Description mentions 'create'"
                ]
            }
        }


class FunctionUsagePattern(BaseModel):
    """🎯 Common usage patterns for functions."""
    
    # Pattern identification
    pattern_name: str = Field(description="🎯 Name of the usage pattern")
    function_names: List[str] = Field(description="🟡 Functions involved in pattern")
    
    # Pattern details
    template: str = Field(description="📋 Code template for pattern")
    frequency: float = Field(description="📈 How often this pattern appears")
    context: List[str] = Field(description="🏷️ Contexts where pattern is used")
    
    # Examples
    example_code: List[str] = Field(
        default_factory=list,
        description="💡 Example code snippets"
    )
    
    # Quality metrics
    success_rate: float = Field(description="✅ Pattern success rate")
    common_errors: List[str] = Field(
        default_factory=list,
        description="❌ Common errors with this pattern"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "pattern_name": "table_creation_basic",
                "function_names": ["create_table"],
                "template": "pxt.create_table('{name}', {schema})",
                "frequency": 0.8,
                "context": ["beginner", "tutorial"],
                "success_rate": 0.95
            }
        }


class FunctionEvolution(BaseModel):
    """📈 How a function evolved across versions."""
    
    # Function identity
    canonical_name: str = Field(description="🎯 Stable function identifier")
    repository: str = Field(description="📚 Repository")
    
    # Evolution history
    first_version: str = Field(description="🐣 First version this function appeared")
    versions: List[str] = Field(description="🏷️ All versions containing this function")
    
    # Change tracking
    signature_changes: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="🔄 History of signature changes"
    )
    
    docstring_changes: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="📚 History of docstring changes"
    )
    
    # Stability metrics
    change_frequency: float = Field(description="📈 How often function changes")
    stability_score: float = Field(description="🛡️ Stability score (0-1)")
    
    # Related changes
    related_function_changes: List[str] = Field(
        default_factory=list,
        description="🔗 Functions that changed with this one"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "canonical_name": "pixeltable.create_table",
                "repository": "pixeltable/pixeltable",
                "first_version": "v0.2.30",
                "versions": ["v0.2.30", "v0.3.15", "v0.4.14"],
                "change_frequency": 0.3,
                "stability_score": 0.7
            }
        }


class ClassInfo(BaseModel):
    """🏛️ Complete information about a class (PAC-MAN's power pellet!)."""
    
    # Basic identification
    name: str = Field(description="📝 Class name")
    bases: List[str] = Field(default_factory=list, description="🔗 Base classes")
    
    # Location information
    file_path: str = Field(description="📁 File containing this class")
    line_number: int = Field(description="🔢 Starting line number")
    end_line: int = Field(description="🔢 Ending line number")
    
    # Documentation
    docstring: Optional[str] = Field(default=None, description="📚 Raw docstring")
    
    # Methods and decorators
    methods: List[FunctionInfo] = Field(default_factory=list, description="🔧 Class methods")
    decorators: List[str] = Field(default_factory=list, description="🎨 Class decorators")
    
    # Metadata
    is_abstract: bool = Field(default=False, description="🎭 Is this an abstract class?")
    is_dataclass: bool = Field(default=False, description="📋 Is this a dataclass?")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Table",
                "bases": ["BaseModel"],
                "file_path": "pixeltable/table.py",
                "line_number": 142,
                "end_line": 287,
                "is_dataclass": False
            }
        }


class PAC_MAN_FunctionStats(BaseModel):
    """🟡 PAC-MAN's function chomping statistics."""
    
    # Chomping totals
    total_functions_eaten: int = Field(description="🟡 Total functions processed")
    public_functions: int = Field(description="👁️ Public functions (PAC-MAN's favorites)")
    private_functions: int = Field(description="👻 Private functions (ghosts)")
    
    # Function type breakdown
    regular_functions: int = Field(default=0, description="🔧 Regular functions")
    methods: int = Field(default=0, description="🏛️ Class methods")
    properties: int = Field(default=0, description="📊 Properties")
    async_functions: int = Field(default=0, description="⚡ Async functions")
    
    # Quality metrics
    functions_with_docstrings: int = Field(description="📚 Functions with documentation")
    functions_with_types: int = Field(description="🏷️ Functions with type annotations")
    documentation_coverage: float = Field(description="📈 Documentation coverage ratio")
    
    # Complexity analysis
    average_complexity: float = Field(description="🧠 Average function complexity")
    most_complex_function: Optional[str] = Field(
        default=None,
        description="🌪️ Most complex function name"
    )
    
    # PAC-MAN achievements
    biggest_function: Optional[str] = Field(
        default=None,
        description="🐋 Biggest function (most lines)"
    )
    most_parameters: Optional[str] = Field(
        default=None,
        description="📋 Function with most parameters"
    )
    longest_name: Optional[str] = Field(
        default=None,
        description="📏 Function with longest name"
    )
    
    # Processing performance
    average_processing_time: float = Field(description="⏱️ Average processing time per function")
    total_processing_time: float = Field(description="⏰ Total processing time")
    
    def get_ghost_ratio(self) -> float:
        """👻 Calculate ratio of ghost functions to total."""
        total = self.total_functions_eaten
        return self.private_functions / total if total > 0 else 0.0
    
    def get_documentation_grade(self) -> str:
        """📚 Get letter grade for documentation quality."""
        coverage = self.documentation_coverage
        if coverage >= 0.9:
            return "A+ 🌟"
        elif coverage >= 0.8:
            return "A 🟡"
        elif coverage >= 0.7:
            return "B+ 📚"
        elif coverage >= 0.6:
            return "B 📝"
        elif coverage >= 0.5:
            return "C+ ⚠️"
        else:
            return "F 👻"
    
    class Config:
        schema_extra = {
            "example": {
                "total_functions_eaten": 1247,
                "public_functions": 892,
                "private_functions": 355,
                "functions_with_docstrings": 789,
                "documentation_coverage": 0.88,
                "average_complexity": 3.2,
                "biggest_function": "complex_data_processor",
                "ghost_ratio": 0.28
            }
        }


# Rebuild models to resolve forward references
ClassInfo.model_rebuild()
