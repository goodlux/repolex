#!/usr/bin/env python3
"""
🍃 PAC-MAN's Mintlify Export Powerhouse! 🍃
Automated MDX documentation generation with full PAC-MAN theming!

Transform semantic intelligence into beautiful Mintlify documentation!
Perfect for creating comprehensive API docs automatically!
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

from ..models.exceptions import (
    RepolexError, ExportError, ValidationError, StorageError
)
from ..models.results import ExportResult
from ..models.progress import ProgressCallback
from ..utils.validation import validate_org_repo, validate_release_tag, validate_file_path

# PAC-MAN themed logging
logger = logging.getLogger("Repolex.mintlify_powerhouse")

# PAC-MAN Mintlify Constants! 🍃
PACMAN_MINTLIFY_LEAVES = "🍃"  # MDX files
PACMAN_DOCUMENTATION_TREES = "🌳"  # Directory structure
PACMAN_FUNCTION_FRUITS = "🍎"  # Individual functions
PACMAN_PARAMETER_SEEDS = "🌰"  # Function parameters  
PACMAN_EXAMPLE_FLOWERS = "🌸"  # Code examples


@dataclass
class PacManMintlifyStats:
    """PAC-MAN themed Mintlify export statistics! 🍃"""
    mdx_files_created: int = 0  # Total MDX files generated
    functions_documented: int = 0  # Functions processed
    directories_created: int = 0  # Directory structure built
    examples_included: int = 0  # Code examples added
    total_content_lines: int = 0  # Total lines of content
    processing_time: float = 0.0  # Time to generate
    
    def create_mdx_file(self) -> None:
        """Create an MDX file! 🍃"""
        self.mdx_files_created += 1
    
    def document_function(self) -> None:
        """Document a function! 🍎"""
        self.functions_documented += 1
    
    def create_directory(self) -> None:
        """Create a directory! 🌳"""
        self.directories_created += 1
    
    def include_example(self) -> None:
        """Include an example! 🌸"""
        self.examples_included += 1


@dataclass
class MintlifyFunction:
    """Structured function data for Mintlify export"""
    name: str
    signature: str
    description: str
    docstring: str
    module: str
    file_path: str = ""
    line_number: int = 0
    parameters: List[Dict[str, Any]] = None
    returns: str = ""
    examples: List[str] = None
    category: str = "functions"  # core_api, functions, media, etc.
    subcategory: str = ""  # table_management, data_operations, etc.
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = []
        if self.examples is None:
            self.examples = []


class PacManMintlifyExporter:
    """
    🍃 PAC-MAN's Ultimate Mintlify Export Powerhouse! 🍃
    
    The most spectacular Mintlify MDX documentation generator ever created!
    PAC-MAN will transform semantic data into beautiful, structured MDX files
    perfect for Mintlify documentation sites!
    
    Features:
    - 🍃 Automated MDX file generation with proper frontmatter
    - 🌳 Intelligent directory structure creation
    - 🍎 Rich function documentation with examples
    - 🌰 Detailed parameter documentation
    - 🌸 Code example integration
    - 🎯 Categorization by module and function type
    - 🚀 Beautiful MDX formatting
    
    WAKA WAKA WAKA! Let's create the most beautiful documentation ever!
    """
    
    def __init__(self):
        """Initialize PAC-MAN's Mintlify Export Powerhouse! 🍃"""
        self.stats = PacManMintlifyStats()
        
        # Category mapping for organizing functions
        self.category_patterns = {
            "core_api": {
                "table_management": ["create_table", "drop_table", "get_table", "list_tables"],
                "data_operations": ["insert", "update", "delete", "select"],
                "column_operations": ["add_column", "drop_column", "rename_column", "add_computed_column"],
                "query_operations": ["where", "order_by", "limit", "join"],
                "view_management": ["create_view", "drop_view", "list_views"],
                "directory_management": ["create_dir", "drop_dir", "list_dirs"],
                "index_management": ["add_index", "drop_index", "add_embedding_index", "drop_embedding_index"]
            },
            "functions": {
                "udf": ["udf", "expr_udf", "mcp_tool_to_udf", "mcp_udfs"]
            },
            "media": {
                "image": ["resize", "crop", "rotate", "width", "height", "alpha_composite"],
                "video": ["extract_audio", "extract_first_video_frame"],
                "audio": ["duration", "sample_rate", "channels"]
            },
            "ml": {
                "embeddings": ["clip", "sentence_transformer", "openai"],
                "detection": ["yolox", "detectron2"],
                "datasets": ["import_huggingface_dataset"]
            },
            "types": {
                "": ["Image", "Video", "Audio", "Json", "Array", "Basic"]
            },
            "configuration": {
                "": ["configure_logging", "get_client", "set_api_key"]
            }
        }
        
        logger.info("🍃 PAC-MAN Mintlify Export Powerhouse initialized!")
        logger.info("🎮 Ready to create spectacular MDX documentation! WAKA WAKA!")
    
    def export_mintlify_spectacular(
        self,
        org_repo: str,
        release: str,
        output_path: Path,
        progress_callback: Optional[ProgressCallback] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        🍃 Create a SPECTACULAR Mintlify MDX export!
        
        PAC-MAN will transform semantic data into the most beautiful MDX documentation
        that developers have ever seen!
        
        Args:
            org_repo: Repository in 'org/repo' format
            release: Release tag to export
            output_path: Directory path where MDX files will be created
            progress_callback: Progress updates during the spectacular creation
            options: Export customization options
            
        Returns:
            Path: Location of the created SDK directory
            
        Raises:
            ExportError: If MDX generation fails
            ValidationError: If parameters are invalid
            StorageError: If semantic data cannot be accessed
        """
        # Validate the spectacular parameters! 🍃
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        start_time = datetime.now()
        logger.info(f"🍃 PAC-MAN starting SPECTACULAR Mintlify export for {org_repo}@{release}!")
        
        if progress_callback:
            progress_callback(5.0, f"🍃 PAC-MAN preparing spectacular Mintlify export...")
        
        try:
            # Determine SDK path from options or default
            if options and options.get('sdk_root'):
                sdk_path = Path(options['sdk_root']) / release
            else:
                sdk_path = output_path / "sdk" / release
            
            if progress_callback:
                progress_callback(15.0, f"🌳 Creating directory structure...")
            
            # Create directory structure
            self._create_directory_structure(sdk_path)
            
            if progress_callback:
                progress_callback(25.0, f"🔍 Gathering function data...")
            
            # Gather function data from semantic intelligence
            all_functions = self._gather_function_data_from_semantic_dna(org_repo, release)
            
            # Filter to public functions only (critical requirement!)
            functions = self._filter_to_public_functions(all_functions)
            
            logger.info(f"📋 Filtered from {len(all_functions)} to {len(functions)} public functions")
            
            if progress_callback:
                progress_callback(40.0, f"🍎 Categorizing functions...")
            
            # Categorize functions for organization
            categorized_functions = self._categorize_functions(functions)
            
            # Debug: Log what we actually discovered
            logger.info(f"🔍 DEBUG: Discovered {len(functions)} actual functions:")
            for func in functions[:10]:  # Show first 10
                logger.info(f"   - {func.name} ({func.category}/{func.subcategory})")
            if len(functions) > 10:
                logger.info(f"   ... and {len(functions) - 10} more")
            
            if progress_callback:
                progress_callback(60.0, f"🍃 Generating MDX files...")
            
            # Store GitHub URL context in functions (auto-inferred from org_repo)
            for function in functions:
                function._org_repo = org_repo
            
            # Generate MDX files for each function
            total_functions = len(functions)
            for i, function in enumerate(functions):
                self._create_function_mdx(function, sdk_path)
                
                if progress_callback:
                    current_progress = 60.0 + (30.0 * i / max(1, total_functions))
                    progress_callback(current_progress, f"🍎 Documented {function.name}...")
            
            if progress_callback:
                progress_callback(90.0, f"📝 Creating overview files...")
            
            # Create overview and index files
            self._create_overview_files(sdk_path, categorized_functions, org_repo, release)
            
            if progress_callback:
                progress_callback(95.0, f"📋 Generating docs.json navigation...")
            
            # Generate docs.json navigation structure (critical for Mintlify!)
            self._generate_docs_json_navigation(
                sdk_path, categorized_functions, org_repo, release, options
            )
            
            # Calculate final statistics
            self.stats.processing_time = (datetime.now() - start_time).total_seconds()
            
            if progress_callback:
                progress_callback(100.0, f"🍃 SPECTACULAR Mintlify export complete!")
            
            logger.info(f"🎉 PAC-MAN created SPECTACULAR Mintlify export!")
            logger.info(f"📊 Statistics: {asdict(self.stats)}")
            logger.info(f"📁 Output: {sdk_path}")
            logger.info(f"⏱️ Time: {self.stats.processing_time:.2f}s")
            
            return sdk_path
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered during Mintlify export: {e}")
            raise ExportError(
                f"Failed to export Mintlify docs for {org_repo}@{release}: {str(e)}",
                suggestions=[
                    "Check if semantic data exists for this repository/release",
                    "Verify output path permissions",
                    "Try with a different output location"
                ]
            )
    
    def _gather_function_data_from_semantic_dna(
        self, 
        org_repo: str, 
        release: str
    ) -> List[MintlifyFunction]:
        """
        🔍 Gather function data from semantic DNA files!
        
        Load the power pellets and extract function intelligence!
        """
        logger.info(f"🔍 PAC-MAN loading semantic DNA for {org_repo}@{release}")
        
        try:
            # First try to get from semantic DNA files (msgpack)
            functions = self._load_from_semantic_dna(org_repo, release)
            
            if not functions:
                # Fallback to SPARQL query if available
                functions = self._load_from_sparql_database(org_repo, release)
            
            logger.info(f"🎯 Loaded {len(functions)} functions from semantic intelligence")
            return functions
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered loading function data: {e}")
            raise StorageError(
                f"Failed to load function data for {org_repo}@{release}: {str(e)}",
                suggestions=[
                    "Ensure semantic DNA files exist in llm-repolex directory",
                    "Check if the repository has been processed with rlex lexify",
                    "Verify semantic graph database connectivity"
                ]
            )
    
    def _load_from_semantic_dna(self, org_repo: str, release: str) -> List[MintlifyFunction]:
        """Load function data from semantic DNA msgpack files"""
        try:
            import msgpack
            
            # Try to find the semantic DNA file
            org, repo = org_repo.split('/')
            possible_files = [
                f"{org}~{repo}~{release}.msgpack",
                f"{org}~{repo}~latest.msgpack",
                f"{repo}~{repo}~{release}.msgpack",
                f"{repo}~{repo}~latest.msgpack"
            ]
            
            # Look in llm-repolex directory
            llm_repolex_path = Path("llm-repolex")
            if not llm_repolex_path.exists():
                llm_repolex_path = Path("../llm-repolex")
            
            semantic_file = None
            for filename in possible_files:
                candidate = llm_repolex_path / filename
                if candidate.exists():
                    semantic_file = candidate
                    break
            
            if not semantic_file:
                logger.warning(f"No semantic DNA file found for {org_repo}")
                return []
            
            logger.info(f"📦 Loading semantic DNA from {semantic_file}")
            
            # Load and parse the msgpack data
            with open(semantic_file, 'rb') as f:
                data = msgpack.unpack(f)
            
            # Get string table for docstring lookups
            string_table = data.get('strings', [])
            
            functions = []
            for func_data in data.get('functions', []):
                # Extract function information
                name = func_data.get('n', 'unknown')
                signature = func_data.get('s', f'{name}()')
                module = func_data.get('m', 'unknown')
                file_path = func_data.get('f', '')
                line_number = func_data.get('l', 0)
                
                # Extract description from docstring using string table
                docstring_idx = func_data.get('d', 0)
                docstring = ""
                if isinstance(docstring_idx, int) and docstring_idx < len(string_table):
                    docstring = string_table[docstring_idx]
                elif isinstance(docstring_idx, str):
                    docstring = docstring_idx
                
                description = self._extract_description_from_docstring(docstring)
                
                function = MintlifyFunction(
                    name=name,
                    signature=signature,
                    description=description,
                    docstring=docstring,
                    module=module,
                    file_path=file_path,
                    line_number=line_number
                )
                
                functions.append(function)
            
            return functions
            
        except ImportError:
            logger.warning("msgpack not available, falling back to SPARQL")
            return []
        except Exception as e:
            logger.error(f"Error loading semantic DNA: {e}")
            return []
    
    def _load_from_sparql_database(self, org_repo: str, release: str) -> List[MintlifyFunction]:
        """Load function data from SPARQL database as fallback"""
        try:
            # This would query the Oxigraph database directly
            # For now, return empty list - implement if semantic DNA files not available
            logger.info("SPARQL fallback not yet implemented")
            return []
            
        except Exception as e:
            logger.error(f"Error loading from SPARQL: {e}")
            return []
    
    def _extract_description_from_docstring(self, docstring: str) -> str:
        """Extract a clean description from function docstring"""
        if not docstring:
            return ""
        
        # Get first line or paragraph as description
        lines = docstring.strip().split('\n')
        
        # Find first non-empty line
        for line in lines:
            clean_line = line.strip()
            if clean_line and not clean_line.startswith('"""') and not clean_line.startswith("'''"):
                return clean_line
        
        return ""
    
    def _categorize_functions(self, functions: List[MintlifyFunction]) -> Dict[str, Dict[str, List[MintlifyFunction]]]:
        """🍎 Categorize functions for directory organization"""
        
        categorized = {}
        
        for function in functions:
            category, subcategory = self._determine_function_category(function)
            
            if category not in categorized:
                categorized[category] = {}
                
            if subcategory not in categorized[category]:
                categorized[category][subcategory] = []
            
            function.category = category
            function.subcategory = subcategory
            categorized[category][subcategory].append(function)
        
        return categorized
    
    def _determine_function_category(self, function: MintlifyFunction) -> tuple[str, str]:
        """Determine the category and subcategory for a function"""
        
        func_name = function.name.lower()
        module = function.module.lower()
        
        # Check each category pattern
        for category, subcategories in self.category_patterns.items():
            for subcategory, patterns in subcategories.items():
                for pattern in patterns:
                    if pattern.lower() in func_name or pattern.lower() in module:
                        return category, subcategory
        
        # Default categorization based on module
        if "media" in module or "image" in module or "video" in module or "audio" in module:
            if "image" in module:
                return "media", "image"
            elif "video" in module:
                return "media", "video"
            elif "audio" in module:
                return "media", "audio"
            else:
                return "media", ""
        elif "ml" in module or "embedding" in module or "detection" in module:
            return "ml", "embeddings" if "embedding" in module else "detection"
        elif any(word in func_name for word in ["create", "table", "insert", "update", "delete"]):
            return "core_api", "table_management" if "table" in func_name else "data_operations"
        else:
            return "functions", "udf"
    
    def _create_directory_structure(self, sdk_path: Path):
        """🌳 Create base SDK directory structure (specific dirs created as needed)"""
        
        # Only create the base SDK directory
        # Individual function directories will be created in _create_function_mdx
        sdk_path.mkdir(parents=True, exist_ok=True)
        self.stats.create_directory()
        logger.debug(f"🌳 Created base SDK directory: {sdk_path}")
    
    def _create_function_mdx(self, function: MintlifyFunction, sdk_path: Path):
        """🍃 Create MDX file for a single function"""
        
        # Determine output path
        if function.subcategory:
            output_path = sdk_path / function.category / function.subcategory / f"{function.name}.mdx"
        else:
            output_path = sdk_path / function.category / f"{function.name}.mdx"
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate MDX content
        mdx_content = self._generate_mdx_content(function)
        
        # Write the file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mdx_content)
        
        self.stats.create_mdx_file()
        self.stats.document_function()
        self.stats.total_content_lines += len(mdx_content.split('\n'))
        
        logger.debug(f"🍃 Created MDX file: {output_path}")
    
    def _generate_mdx_content(self, function: MintlifyFunction) -> str:
        """Generate complete MDX content for a function"""
        
        # Generate proper title and description
        title = self._generate_function_title(function)
        description = self._generate_function_description(function, title)
        
        # Determine badge based on category
        badge_text, badge_color = self._get_badge_for_category(function.category)
        
        # Build the MDX content
        mdx_lines = [
            "---",
            f'title: "{title}"',
            f'description: "{description}"',
            "---",
            "",
            f'<Badge text="{badge_text}" color="{badge_color}" size="small" />',
            "",
            "## Function Signature",
            "",
            "```python",
            function.signature,
            "```",
            "",
            "## Description",
            ""
        ]
        
        # Add description from docstring
        if function.docstring:
            docstring_lines = function.docstring.strip().split('\n')
            for line in docstring_lines:
                if line.strip():
                    mdx_lines.append(line.strip())
                else:
                    mdx_lines.append("")
        else:
            mdx_lines.append(f"Function `{function.name}` from the Pixeltable library.")
        
        # Add parameters section if we can parse them from signature
        parameters = self._parse_parameters_from_signature(function.signature)
        if parameters:
            mdx_lines.extend([
                "",
                "## Parameters",
                ""
            ])
            
            for param in parameters:
                param_name = param.get('name', 'param')
                param_type = param.get('type', 'Any')
                required = param.get('required', True)
                
                mdx_lines.extend([
                    f'<ParamField path="{param_name}" type="{param_type}" {"required" if required else "default=None"}>',
                    f"  Parameter {param_name} of type {param_type}",
                    "</ParamField>",
                    ""
                ])
        
        # Add returns section
        return_type = self._parse_return_type_from_signature(function.signature)
        if return_type:
            mdx_lines.extend([
                "## Returns",
                "",
                f'<ResponseField name="result" type="{return_type}">',
                f"  Returns a value of type {return_type}",
                "</ResponseField>",
                ""
            ])
        
        # Add example section
        mdx_lines.extend([
            "## Examples",
            "",
            "```python",
            "import pixeltable as pxt",
            "",
            f"# Example usage of {function.name}",
            f"result = pxt.{function.name}()",
            "```",
            ""
        ])
        
        # Add GitHub source links (GAME CHANGER!)
        if function.file_path:
            github_url = self._generate_github_source_link(
                function.file_path, 
                function.line_number,
                org_repo
            )
            
            mdx_lines.extend([
                "## Source Code",
                "",
                f"📁 **File:** `{function.file_path}`"
            ])
            
            if function.line_number:
                mdx_lines.append(f"📍 **Line:** {function.line_number}")
            
            if github_url:
                mdx_lines.extend([
                    "",
                    f"🔗 **[View Source on GitHub]({github_url})**",
                    ""
                ])
            else:
                mdx_lines.append("")
        
        # Add footer
        mdx_lines.extend([
            "---",
            "",
            f"*Generated by repolex Mintlify exporter from semantic intelligence*"
        ])
        
        return '\n'.join(mdx_lines)
    
    def _get_badge_for_category(self, category: str) -> tuple[str, str]:
        """Get badge text and color for function category"""
        
        badge_map = {
            "core_api": ("Core API", "blue"),
            "functions": ("UDF System", "green"),
            "media": ("Media Processing", "purple"),
            "ml": ("Machine Learning", "orange"),
            "types": ("Data Types", "gray"),
            "configuration": ("Configuration", "yellow")
        }
        
        return badge_map.get(category, ("Function", "blue"))
    
    def _parse_parameters_from_signature(self, signature: str) -> List[Dict[str, Any]]:
        """🔧 Enhanced parameter parsing from function signature"""
        try:
            # Extract parameter part from signature
            if '(' not in signature or ')' not in signature:
                return []
            
            # Handle multi-line signatures by cleaning them up
            clean_signature = signature.replace('\n', ' ').replace('\r', ' ')
            
            # Find the parameter section
            start_paren = clean_signature.find('(')
            end_paren = clean_signature.rfind(')')
            
            if start_paren == -1 or end_paren == -1 or start_paren >= end_paren:
                return []
            
            param_str = clean_signature[start_paren + 1:end_paren]
            
            if not param_str.strip():
                return []
            
            parameters = []
            
            # Split parameters more intelligently (handle nested types)
            param_parts = self._smart_split_parameters(param_str)
            
            for param in param_parts:
                param = param.strip()
                if not param or param == 'self':
                    continue
                
                param_info = self._parse_single_parameter(param)
                if param_info:
                    parameters.append(param_info)
            
            return parameters
            
        except Exception as e:
            logger.debug(f"Error parsing parameters from signature '{signature}': {e}")
            return []
    
    def _smart_split_parameters(self, param_str: str) -> List[str]:
        """🧠 Smart parameter splitting that handles nested types"""
        parameters = []
        current_param = ""
        bracket_depth = 0
        paren_depth = 0
        
        for char in param_str:
            if char == ',' and bracket_depth == 0 and paren_depth == 0:
                # Found a parameter boundary
                if current_param.strip():
                    parameters.append(current_param.strip())
                current_param = ""
            else:
                if char == '[':
                    bracket_depth += 1
                elif char == ']':
                    bracket_depth -= 1
                elif char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                
                current_param += char
        
        # Add the last parameter
        if current_param.strip():
            parameters.append(current_param.strip())
        
        return parameters
    
    def _parse_single_parameter(self, param: str) -> Optional[Dict[str, Any]]:
        """🔍 Parse a single parameter with type and default value"""
        try:
            # Handle parameter with type annotation and/or default value
            if ':' in param:
                name_part, type_and_default = param.split(':', 1)
                name = name_part.strip()
                
                # Check for default value
                if '=' in type_and_default:
                    type_part, default_part = type_and_default.split('=', 1)
                    param_type = type_part.strip()
                    default_value = default_part.strip()
                    required = False
                else:
                    param_type = type_and_default.strip()
                    default_value = None
                    required = True
            else:
                # No type annotation, but might have default value
                if '=' in param:
                    name_part, default_part = param.split('=', 1)
                    name = name_part.strip()
                    default_value = default_part.strip()
                    param_type = 'Any'
                    required = False
                else:
                    name = param.strip()
                    param_type = 'Any'
                    default_value = None
                    required = True
            
            # Clean up type annotations
            param_type = self._clean_type_annotation(param_type)
            
            return {
                'name': name,
                'type': param_type,
                'required': required,
                'default': default_value
            }
            
        except Exception as e:
            logger.debug(f"Error parsing single parameter '{param}': {e}")
            return None
    
    def _clean_type_annotation(self, type_str: str) -> str:
        """🧹 Clean up type annotations for better display"""
        if not type_str:
            return 'Any'
        
        # Remove common import prefixes
        type_str = type_str.replace('typing.', '').replace('pixeltable.', '')
        
        # Handle common type patterns
        type_mapping = {
            'str': 'string',
            'int': 'integer',
            'float': 'number',
            'bool': 'boolean',
            'dict': 'object',
            'list': 'array'
        }
        
        # Simple mapping for basic types
        for py_type, display_type in type_mapping.items():
            if type_str.lower() == py_type:
                return display_type
        
        # Handle Union types
        if 'Union[' in type_str:
            # Simplify Union[str, None] to "string | null"
            inner = type_str[type_str.find('[') + 1:type_str.rfind(']')]
            union_types = [t.strip() for t in inner.split(',')]
            clean_types = [self._clean_type_annotation(t) for t in union_types]
            return ' | '.join(clean_types)
        
        # Handle Optional types
        if 'Optional[' in type_str:
            inner = type_str[type_str.find('[') + 1:type_str.rfind(']')]
            return f"{self._clean_type_annotation(inner)} | null"
        
        # Handle List types
        if type_str.startswith('List[') or type_str.startswith('list['):
            inner = type_str[type_str.find('[') + 1:type_str.rfind(']')]
            return f"array<{self._clean_type_annotation(inner)}>"
        
        # Handle Dict types
        if type_str.startswith('Dict[') or type_str.startswith('dict['):
            return 'object'
        
        return type_str
    
    def _parse_return_type_from_signature(self, signature: str) -> str:
        """🎯 Enhanced return type parsing from function signature"""
        try:
            if '->' not in signature:
                return ""
            
            # Clean up signature for parsing
            clean_signature = signature.replace('\n', ' ').replace('\r', ' ')
            
            # Find the return type part
            arrow_pos = clean_signature.rfind('->')
            if arrow_pos == -1:
                return ""
            
            return_part = clean_signature[arrow_pos + 2:].strip()
            
            # Clean up the return type
            return_type = self._clean_type_annotation(return_part)
            
            logger.debug(f"🎯 Parsed return type: {return_type} from {signature}")
            return return_type
            
        except Exception as e:
            logger.debug(f"Error parsing return type from '{signature}': {e}")
            return ""
    
    def _create_overview_files(
        self, 
        sdk_path: Path, 
        categorized_functions: Dict[str, Dict[str, List[MintlifyFunction]]],
        org_repo: str,
        release: str
    ):
        """📝 Create overview and index files"""
        
        # Create main overview file
        overview_content = self._generate_overview_content(categorized_functions, org_repo, release)
        overview_path = sdk_path / "overview.mdx"
        
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(overview_content)
        
        self.stats.create_mdx_file()
        logger.info(f"📝 Created overview file: {overview_path}")
    
    def _generate_docs_json_navigation(
        self,
        sdk_path: Path,
        categorized_functions: Dict[str, Dict[str, List[MintlifyFunction]]],
        org_repo: str,
        release: str,
        options: Optional[Dict[str, Any]] = None
    ):
        """
        📋 Generate docs.json navigation structure for Mintlify!
        
        Creates navigation ONLY for functions that actually exist as MDX files.
        This prevents phantom navigation entries for non-existent functions.
        """
        logger.info("📋 Generating docs.json navigation structure...")
        
        navigation = [
            {
                "group": "Getting Started",
                "pages": [
                    f"sdk/{release}/overview"
                ]
            }
        ]
        
        # Generate navigation ONLY for actual categorized functions (no phantom entries!)
        for category, subcategories in categorized_functions.items():
            if not subcategories:
                continue
            
            category_name = self._format_category_name(category)
            
            # Handle subcategories
            for subcategory, functions in subcategories.items():
                if not functions:  # Skip empty subcategories
                    continue
                    
                if subcategory:
                    # Create subcategory group ONLY if it has actual functions
                    subcategory_name = self._format_category_name(subcategory)
                    subcategory_group = {
                        "group": f"{category_name} - {subcategory_name}",
                        "pages": []
                    }
                    
                    # Only add pages for functions that actually exist
                    for function in functions:
                        page_path = f"sdk/{release}/{category}/{subcategory}/{function.name}"
                        subcategory_group["pages"].append(page_path)
                    
                    # Only add the group if it has pages
                    if subcategory_group["pages"]:
                        navigation.append(subcategory_group)
                else:
                    # Create category group for functions without subcategory
                    category_group = {
                        "group": category_name,
                        "pages": []
                    }
                    
                    # Add functions directly to category
                    for function in functions:
                        page_path = f"sdk/{release}/{category}/{function.name}"
                        category_group["pages"].append(page_path)
                    
                    # Only add category group if it has pages
                    if category_group["pages"]:
                        navigation.append(category_group)
        
        # Create the complete docs.json structure
        docs_json = {
            "$schema": "https://mintlify.com/schema.json",
            "name": f"{org_repo.split('/')[-1]} Python SDK",
            "logo": {
                "dark": "/logo/dark.svg",
                "light": "/logo/light.svg"
            },
            "favicon": "/favicon.svg",
            "colors": {
                "primary": "#0D9373",
                "light": "#07C983",
                "dark": "#0D9373",
                "anchors": {
                    "from": "#0D9373",
                    "to": "#07C983"
                }
            },
            "topbarLinks": [
                {
                    "name": "Support",
                    "url": "mailto:hi@mintlify.com"
                }
            ],
            "topbarCtaButton": {
                "name": "Dashboard",
                "url": "https://dashboard.mintlify.com"
            },
            "tabs": [
                {
                    "name": "Python SDK",
                    "url": "sdk"
                }
            ],
            "anchors": [
                {
                    "name": "Documentation",
                    "icon": "book-open-cover",
                    "url": "https://mintlify.com/docs"
                },
                {
                    "name": "Community",
                    "icon": "slack",
                    "url": "https://mintlify.com/community"
                },
                {
                    "name": "Blog",
                    "icon": "newspaper",
                    "url": "https://mintlify.com/blog"
                }
            ],
            "navigation": navigation,
            "footerSocials": {
                "x": f"https://x.com/{org_repo.split('/')[0]}",
                "github": f"https://github.com/{org_repo}",
                "linkedin": f"https://www.linkedin.com/company/{org_repo.split('/')[0]}"
            },
            "analytics": {
                "gtag": {
                    "measurementId": "G-XXXXXXXXXX"
                }
            }
        }
        
        # Handle existing docs.json merge if requested
        if options and options.get('docs_json_path') and options.get('merge_navigation'):
            docs_json = self._merge_with_existing_docs_json(
                docs_json, options['docs_json_path'], org_repo
            )
        
        # Determine output path
        if options and options.get('docs_json_path') and not options.get('merge_navigation'):
            # Use existing docs.json location but overwrite
            docs_json_path = Path(options['docs_json_path'])
        else:
            # Default location
            docs_json_path = sdk_path.parent.parent / "docs.json"
        
        docs_json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(docs_json_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(docs_json, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📋 Created docs.json navigation: {docs_json_path}")
        
        # Count actual function pages in navigation
        total_pages = sum(
            len(group.get('pages', [])) 
            for group in navigation 
            if isinstance(group, dict)
        )
        logger.info(f"📊 Navigation includes {len(navigation)} groups with {total_pages} actual function pages")
        
        # Debug: Log all navigation entries
        logger.info("🔍 DEBUG: Navigation entries created:")
        for group in navigation:
            if isinstance(group, dict) and 'pages' in group:
                logger.info(f"   Group '{group.get('group', 'Unknown')}': {len(group['pages'])} pages")
                for page in group['pages'][:3]:  # Show first 3 pages per group
                    logger.info(f"     - {page}")
                if len(group['pages']) > 3:
                    logger.info(f"     ... and {len(group['pages']) - 3} more")
    
    def _format_category_name(self, category: str) -> str:
        """Format category name for display in navigation"""
        return category.replace('_', ' ').title()
    
    def _merge_with_existing_docs_json(
        self, 
        new_docs_json: Dict[str, Any], 
        existing_path: str, 
        org_repo: str
    ) -> Dict[str, Any]:
        """
        🔄 Merge new navigation with existing docs.json
        
        Intelligently merges API reference navigation while preserving
        existing structure and configuration.
        """
        try:
            import json
            
            # Load existing docs.json
            with open(existing_path, 'r', encoding='utf-8') as f:
                existing_docs = json.load(f)
            
            logger.info(f"🔄 Merging with existing docs.json from {existing_path}")
            
            # Preserve existing configuration but update key fields
            merged_docs = existing_docs.copy()
            
            # Update name if it contains the repo name
            repo_name = org_repo.split('/')[-1]
            if repo_name.lower() in merged_docs.get('name', '').lower():
                merged_docs['name'] = new_docs_json['name']
            
            # Merge navigation - add API reference sections
            existing_nav = merged_docs.get('navigation', [])
            new_nav = new_docs_json.get('navigation', [])
            
            # Find existing SDK/API sections to replace (enhanced detection)
            sections_to_remove = []
            for i, nav_item in enumerate(existing_nav):
                if isinstance(nav_item, dict):
                    group_name = nav_item.get('group', '').lower()
                    pages = nav_item.get('pages', [])
                    
                    # Check if this is an SDK/API section by group name OR by page paths
                    is_sdk_section = (
                        # Group name contains SDK/API terms
                        any(term in group_name for term in ['api', 'reference', 'core', 'function', 'sdk', 'python']) or
                        # OR any page path contains sdk/ (handles old "latest" paths)
                        any(isinstance(page, str) and 'sdk/' in page for page in pages)
                    )
                    
                    if is_sdk_section:
                        sections_to_remove.append(i)
                        logger.debug(f"🗑️ Will remove existing section: '{nav_item.get('group')}' ({len(pages)} pages)")
            
            # Remove old SDK/API sections
            for index in reversed(sections_to_remove):
                existing_nav.pop(index)
            
            logger.info(f"🧹 Removed {len(sections_to_remove)} existing SDK sections from navigation")
            
            # Add new API sections (skip the "Getting Started" from template)
            api_sections = [nav for nav in new_nav if nav.get('group') != 'Getting Started']
            existing_nav.extend(api_sections)
            
            merged_docs['navigation'] = existing_nav
            
            # Update GitHub link if present
            if 'footerSocials' in merged_docs and 'github' in merged_docs['footerSocials']:
                merged_docs['footerSocials']['github'] = f"https://github.com/{org_repo}"
            
            logger.info(f"✅ Successfully merged navigation with {len(api_sections)} API sections")
            return merged_docs
            
        except Exception as e:
            logger.warning(f"Failed to merge with existing docs.json: {e}")
            logger.info("Using new docs.json structure instead")
            return new_docs_json
    
    def _generate_function_title(self, function: MintlifyFunction) -> str:
        """
        🏷️ Generate proper function title with smart module handling!
        
        Creates clean, readable titles like:
        - "create_table" (for core functions)
        - "Image.resize" (for media functions)
        - "ml.embeddings.clip" (for ML functions)
        """
        try:
            # Start with the function name
            title = function.name
            
            # Skip if module is unknown or empty
            if not function.module or function.module in ["unknown", ""]:
                return title
            
            module = function.module.lower()
            
            # Smart module prefix logic
            if "pixeltable" in module:
                # Remove pixeltable prefix and clean up
                clean_module = module.replace("pixeltable.", "").replace("pixeltable", "")
                
                # Handle different module patterns
                if clean_module.startswith("functions."):
                    # pixeltable.functions.video -> video
                    parts = clean_module.split(".")
                    if len(parts) >= 2:
                        category = parts[1]  # video, audio, image, etc
                        title = f"{category}.{function.name}"
                elif clean_module.startswith("type_system."):
                    # pixeltable.type_system -> Types
                    title = f"Types.{function.name}"
                elif any(api_marker in clean_module for api_marker in ["api", "client", "core"]):
                    # Core API functions - use bare name
                    title = function.name
                elif clean_module:
                    # Other modules - use cleaned module name
                    clean_parts = [p for p in clean_module.split(".") if p and p != "functions"]
                    if clean_parts:
                        if len(clean_parts) == 1:
                            title = f"{clean_parts[0]}.{function.name}"
                        else:
                            # For deep nesting, use last two parts
                            title = f"{'.'.join(clean_parts[-2:])}.{function.name}"
            else:
                # Non-pixeltable modules - use as-is but clean
                clean_module = module.replace("_", ".")
                # Take last part for brevity
                module_parts = clean_module.split(".")
                if len(module_parts) > 2:
                    title = f"{module_parts[-1]}.{function.name}"
                else:
                    title = f"{clean_module}.{function.name}"
            
            logger.debug(f"🏷️ Generated title '{title}' for {function.name} in {function.module}")
            return title
            
        except Exception as e:
            logger.warning(f"Failed to generate title for {function.name}: {e}")
            return function.name
    
    def _generate_function_description(self, function: MintlifyFunction, title: str) -> str:
        """
        📝 Generate proper function description with fallbacks!
        
        Creates meaningful descriptions from docstrings or generates smart defaults.
        """
        try:
            # Use existing description if available and meaningful
            if function.description and len(function.description.strip()) > 10:
                return function.description.strip()
            
            # Extract from docstring first line
            if function.docstring:
                lines = function.docstring.strip().split('\n')
                for line in lines:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith('"""') and not clean_line.startswith("'''"):
                        if len(clean_line) > 10:  # Meaningful description
                            return clean_line
            
            # Generate smart default based on function name and category
            category_descriptions = {
                "core_api": "Core API function for data operations",
                "media": "Media processing function",
                "ml": "Machine learning function",
                "functions": "User-defined function utility",
                "types": "Type system function",
                "configuration": "Configuration and setup function"
            }
            
            base_desc = category_descriptions.get(function.category, "Function")
            
            # Make it more specific based on function name
            name_lower = function.name.lower()
            if "create" in name_lower:
                return f"Creates and configures {function.name} - {base_desc}"
            elif "get" in name_lower or "list" in name_lower:
                return f"Retrieves {function.name} information - {base_desc}"
            elif "update" in name_lower or "set" in name_lower:
                return f"Updates {function.name} settings - {base_desc}"
            elif "delete" in name_lower or "remove" in name_lower:
                return f"Removes {function.name} - {base_desc}"
            else:
                return f"{title} - {base_desc}"
            
        except Exception as e:
            logger.warning(f"Failed to generate description for {function.name}: {e}")
            return f"{title} - Function from the API"
    
    def _filter_to_public_functions(self, functions: List[MintlifyFunction]) -> List[MintlifyFunction]:
        """
        📋 Filter to public functions only - no private/internal functions!
        
        Removes:
        - Functions starting with underscore (_private, __internal)
        - Functions in test modules
        - Functions in internal/private modules
        - Helper/utility functions not meant for public API
        """
        public_functions = []
        
        for function in functions:
            # Skip private functions (start with underscore)
            if function.name.startswith('_'):
                logger.debug(f"🚫 Skipping private function: {function.name}")
                continue
            
            # Skip test functions
            if 'test' in function.name.lower() or 'test' in function.module.lower():
                logger.debug(f"🚫 Skipping test function: {function.name}")
                continue
            
            # Skip internal modules
            module_lower = function.module.lower()
            if any(internal_marker in module_lower for internal_marker in [
                'internal', 'private', '_internal', '_private', 
                'impl', '_impl', 'test', 'testing'
            ]):
                logger.debug(f"🚫 Skipping internal module function: {function.name} in {function.module}")
                continue
            
            # Skip utility functions that aren't part of public API
            if any(util_marker in function.name.lower() for util_marker in [
                'helper', '_helper', 'util_', '_util'
            ]):
                logger.debug(f"🚫 Skipping utility function: {function.name}")
                continue
            
            # This is a public function!
            public_functions.append(function)
        
        logger.info(f"🔓 Kept {len(public_functions)} public functions out of {len(functions)} total")
        return public_functions
    
    def _generate_github_source_link(
        self, 
        file_path: str, 
        line_number: int,
        org_repo: str
    ) -> str:
        """
        🔗 Generate GitHub source link - THE GAME CHANGER!
        
        Creates direct links to source code on GitHub using file path and line data.
        This bridges documentation to actual implementation - driving developers into the repo!
        Auto-infers GitHub URL from org_repo parameter.
        """
        try:
            if not file_path or not org_repo:
                return ""
            
            # Clean up file path - remove leading slashes or relative paths
            clean_path = file_path.lstrip('./').lstrip('/')
            
            # Auto-construct GitHub URL from org_repo
            full_url = f"https://github.com/{org_repo}/blob/main/{clean_path}"
            
            # Add line number anchor if available
            if line_number and line_number > 0:
                full_url += f"#L{line_number}"
            
            logger.debug(f"🔗 Generated GitHub link: {full_url}")
            return full_url
            
        except Exception as e:
            logger.warning(f"Failed to generate GitHub source link: {e}")
            return ""
    
    def _generate_overview_content(
        self,
        categorized_functions: Dict[str, Dict[str, List[MintlifyFunction]]],
        org_repo: str,
        release: str
    ) -> str:
        """Generate overview MDX content"""
        
        total_functions = sum(
            len(functions) 
            for category in categorized_functions.values()
            for functions in category.values()
        )
        
        lines = [
            "---",
            f'title: "{org_repo.split("/")[-1]} API Reference"',
            f'description: "Complete API reference for {org_repo} {release}"',
            "---",
            "",
            f"# {org_repo.split('/')[-1]} API Reference",
            "",
            f"Welcome to the complete API reference for {org_repo}. This documentation covers all {total_functions} public functions available in version {release}.",
            "",
            "## API Categories",
            ""
        ]
        
        # Add category overview
        for category, subcategories in categorized_functions.items():
            category_total = sum(len(funcs) for funcs in subcategories.values())
            category_name = category.replace('_', ' ').title()
            
            lines.extend([
                f"### {category_name}",
                f"*{category_total} functions*",
                ""
            ])
            
            for subcategory, functions in subcategories.items():
                if subcategory:
                    subcategory_name = subcategory.replace('_', ' ').title()
                    lines.append(f"- **{subcategory_name}**: {len(functions)} functions")
                else:
                    lines.append(f"- {len(functions)} functions")
            
            lines.append("")
        
        lines.extend([
            "## Getting Started",
            "",
            "```python",
            "import pixeltable as pxt",
            "",
            "# Initialize your workspace",
            "pxt.configure_logging()",
            "```",
            "",
            "---",
            "",
            f"*Generated by repolex Mintlify exporter • {datetime.now().strftime('%Y-%m-%d')}*"
        ])
        
        return '\n'.join(lines)


# Factory function for easy Mintlify export creation
def create_pacman_mintlify_exporter() -> PacManMintlifyExporter:
    """
    🍃 Create PAC-MAN's Mintlify Export Powerhouse!
    
    Factory function to create the ultimate Mintlify documentation system!
    
    Returns:
        PacManMintlifyExporter: Ready to create spectacular MDX files!
    """
    exporter = PacManMintlifyExporter()
    logger.info("🍃 PAC-MAN Mintlify Export Powerhouse created and ready!")
    logger.info("🎮 WAKA WAKA WAKA! Let's create spectacular documentation!")
    return exporter


# Convenience aliases
MintlifyExporter = PacManMintlifyExporter


if __name__ == "__main__":
    # Quick test of PAC-MAN's Mintlify Export Powerhouse!
    
    def test_pacman_mintlify_exporter():
        exporter = create_pacman_mintlify_exporter()
        print("🍃 PAC-MAN Mintlify Export Powerhouse test complete!")
        print("🎮 Ready to create spectacular MDX documentation! WAKA WAKA!")
        
        print(f"📊 Stats: {asdict(exporter.stats)}")
    
    test_pacman_mintlify_exporter()