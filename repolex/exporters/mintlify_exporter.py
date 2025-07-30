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
            # Create SDK directory structure
            sdk_path = output_path / "sdk" / "latest"
            
            if progress_callback:
                progress_callback(15.0, f"🌳 Creating directory structure...")
            
            # Create directory structure
            self._create_directory_structure(sdk_path)
            
            if progress_callback:
                progress_callback(25.0, f"🔍 Gathering function data...")
            
            # Gather function data from semantic intelligence
            functions = self._gather_function_data_from_semantic_dna(org_repo, release)
            
            if progress_callback:
                progress_callback(40.0, f"🍎 Categorizing functions...")
            
            # Categorize functions for organization
            categorized_functions = self._categorize_functions(functions)
            
            if progress_callback:
                progress_callback(60.0, f"🍃 Generating MDX files...")
            
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
        """🌳 Create the complete directory structure for Mintlify docs"""
        
        directories = [
            "core_api/table_management",
            "core_api/data_operations", 
            "core_api/column_operations",
            "core_api/query_operations",
            "core_api/view_management",
            "core_api/directory_management",
            "core_api/index_management",
            "functions/udf",
            "media/image",
            "media/video", 
            "media/audio",
            "ml/embeddings",
            "ml/detection",
            "ml/datasets",
            "types",
            "configuration"
        ]
        
        for directory in directories:
            dir_path = sdk_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.stats.create_directory()
            logger.debug(f"🌳 Created directory: {dir_path}")
    
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
        
        # Determine title and description
        title = function.name
        if function.module and function.module != "unknown":
            # Clean module name for display
            clean_module = function.module.replace("pixeltable.", "").replace("_", "")
            if clean_module:
                title = f"{clean_module}.{function.name}"
        
        description = function.description or f"{title} - Pixeltable function"
        
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
        
        # Add location information if available
        if function.file_path:
            mdx_lines.extend([
                "## Source Location",
                "",
                f"**File:** `{function.file_path}`"
            ])
            
            if function.line_number:
                mdx_lines.append(f"**Line:** {function.line_number}")
            
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
        """Parse parameters from function signature"""
        try:
            # Extract parameter part from signature
            if '(' not in signature or ')' not in signature:
                return []
            
            param_str = signature[signature.find('(') + 1:signature.rfind(')')]
            
            if not param_str.strip():
                return []
            
            parameters = []
            # Simple parameter parsing - could be enhanced for complex types
            for param in param_str.split(','):
                param = param.strip()
                if not param or param == 'self':
                    continue
                
                # Parse parameter name and type
                if ':' in param:
                    name_part, type_part = param.split(':', 1)
                    name = name_part.strip()
                    param_type = type_part.strip()
                    
                    # Check for default value
                    required = '=' not in param_type
                    if '=' in param_type:
                        param_type = param_type.split('=')[0].strip()
                    
                    parameters.append({
                        'name': name,
                        'type': param_type,
                        'required': required
                    })
                else:
                    # No type annotation
                    name = param.split('=')[0].strip()
                    required = '=' not in param
                    
                    parameters.append({
                        'name': name,
                        'type': 'Any',
                        'required': required
                    })
            
            return parameters
            
        except Exception as e:
            logger.debug(f"Error parsing parameters from signature '{signature}': {e}")
            return []
    
    def _parse_return_type_from_signature(self, signature: str) -> str:
        """Parse return type from function signature"""
        try:
            if '->' in signature:
                return_part = signature.split('->')[-1].strip()
                return return_part
            return ""
        except:
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