#!/usr/bin/env python3
"""
🍃 Mintlifier Core - Pixeltable SDK Documentation Generator
Focused tool for generating Mintlify-compatible MDX documentation from Pixeltable.
"""

import re
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime
from dataclasses import dataclass, field
import logging
import importlib.util
import sys

logger = logging.getLogger("repolex.mintlifier")

@dataclass
class MkDocsFunction:
    """Represents a function from MKDocs whitelist"""
    name: str
    module: str
    is_explicit: bool = True  # True if explicitly listed, False if from inherited_members
    
@dataclass
class PixeltableFunction:
    """Enhanced function model for Pixeltable functions"""
    name: str
    module: str
    signature: str = ""
    docstring: str = ""
    description: str = ""
    file_path: str = ""
    line_number: int = 0
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_type: str = ""
    examples: List[str] = field(default_factory=list)
    category: str = "functions"
    subcategory: str = ""
    source_type: str = "function"  # function, class, method, udf, uda

@dataclass 
class MintlifierResult:
    """Result of mintlifier generation"""
    output_path: Path
    files_created: int = 0
    functions_documented: int = 0
    processing_time: float = 0.0
    docs_json_updated: bool = False
    errors: List[str] = field(default_factory=list)

class MkDocsParser:
    """Parser for extracting function whitelists from MKDocs .md files"""
    
    def __init__(self, mkdocs_path: Path, verbose: bool = False):
        self.mkdocs_path = mkdocs_path
        self.verbose = verbose
        
    def parse_mkdocs_whitelists(self) -> Dict[str, List[MkDocsFunction]]:
        """
        Parse all MKDocs .md files and extract function whitelists
        
        Returns:
            Dict mapping module names to lists of functions to document
        """
        whitelists = {}
        
        # Find all .md files in the mkdocs directory
        md_files = list(self.mkdocs_path.glob("**/*.md"))
        
        logger.info(f"🔍 Found {len(md_files)} MKDocs files to parse")
        
        for md_file in md_files:
            try:
                module_functions = self._parse_md_file(md_file)
                if module_functions:
                    # Use relative path as module key
                    module_key = str(md_file.relative_to(self.mkdocs_path)).replace('.md', '').replace('/', '.')
                    whitelists[module_key] = module_functions
                    
                    if self.verbose:
                        logger.info(f"📄 {md_file.name}: {len(module_functions)} functions")
                        
            except Exception as e:
                logger.warning(f"Error parsing {md_file}: {e}")
                continue
                
        total_functions = sum(len(funcs) for funcs in whitelists.values())
        logger.info(f"📋 Extracted {total_functions} functions from {len(whitelists)} modules")
        
        return whitelists
    
    def _parse_md_file(self, md_file: Path) -> List[MkDocsFunction]:
        """Parse a single MKDocs .md file for function whitelist"""
        functions = []
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for ::: module patterns
        module_pattern = r'## ::: ([\w\.]+)(?:\n|\r\n)(?:\s*options:\s*(?:\n|\r\n)(?:\s*members:\s*(?:\n|\r\n)((?:\s*-\s*[\w]+(?:\n|\r\n))*)|inherited_members:\s*true))?'
        
        matches = re.findall(module_pattern, content, re.MULTILINE)
        
        for match in matches:
            module_name = match[0] if isinstance(match, tuple) else match
            members_section = match[1] if isinstance(match, tuple) and len(match) > 1 else ""
            
            if members_section:
                # Explicit members list
                member_names = re.findall(r'-\s*([\w]+)', members_section)
                for member_name in member_names:
                    functions.append(MkDocsFunction(
                        name=member_name,
                        module=module_name,
                        is_explicit=True
                    ))
            else:
                # Check for inherited_members: true
                if 'inherited_members: true' in content:
                    # For inherited members, we'll need to introspect the actual module
                    # For now, mark this as needing introspection
                    functions.append(MkDocsFunction(
                        name="*",  # Wildcard meaning "all public members"
                        module=module_name,
                        is_explicit=False
                    ))
        
        return functions

class PixeltableIntrospector:
    """Introspects Pixeltable codebase to extract function information"""
    
    def __init__(self, pixeltable_repo: Path, verbose: bool = False):
        self.pixeltable_repo = pixeltable_repo
        self.verbose = verbose
        
        # Add pixeltable repo to Python path for imports
        if str(pixeltable_repo) not in sys.path:
            sys.path.insert(0, str(pixeltable_repo))
    
    def get_functions_from_whitelist(
        self, 
        whitelists: Dict[str, List[MkDocsFunction]]
    ) -> List[PixeltableFunction]:
        """
        Extract actual function information based on MKDocs whitelists
        
        Args:
            whitelists: Parsed MKDocs function whitelists
            
        Returns:
            List of PixeltableFunction objects with full introspection data
        """
        all_functions = []
        
        for module_key, mkdocs_functions in whitelists.items():
            logger.info(f"🔍 Introspecting module: {module_key}")
            
            try:
                # Convert module key to actual Python module name
                python_module = self._resolve_python_module(module_key)
                
                if not python_module:
                    logger.warning(f"Could not resolve Python module for {module_key}")
                    continue
                
                # Import the module
                module_obj = self._import_module(python_module)
                if not module_obj:
                    continue
                
                # Extract functions based on whitelist
                for mkdocs_func in mkdocs_functions:
                    if mkdocs_func.name == "*":
                        # Wildcard - get all public members
                        module_functions = self._get_all_public_members(module_obj, python_module)
                        all_functions.extend(module_functions)
                    else:
                        # Specific function
                        func = self._get_specific_function(module_obj, mkdocs_func.name, python_module)
                        if func:
                            all_functions.append(func)
                            
            except Exception as e:
                logger.error(f"Error introspecting {module_key}: {e}")
                continue
        
        logger.info(f"🔧 Introspected {len(all_functions)} functions total")
        return all_functions
    
    def _resolve_python_module(self, module_key: str) -> Optional[str]:
        """Convert MKDocs module key to actual Python module name"""
        
        # Handle common patterns
        if module_key.startswith('pixeltable.'):
            # Already a python module path
            return module_key
        elif module_key == 'pixeltable':
            return 'pixeltable'
        elif module_key.startswith('pixeltable/'):
            # Convert path to module
            return module_key.replace('/', '.')
        elif 'pixeltable' in module_key:
            # Try to construct from parts
            parts = module_key.split('.')
            if 'pixeltable' in parts:
                idx = parts.index('pixeltable')
                return '.'.join(parts[idx:])
        
        # Default attempt
        if not module_key.startswith('pixeltable'):
            return f'pixeltable.{module_key}'
        
        return module_key
    
    def _import_module(self, module_name: str) -> Optional[object]:
        """Safely import a Python module"""
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            if self.verbose:
                logger.warning(f"Could not import {module_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error importing {module_name}: {e}")
            return None
    
    def _get_all_public_members(self, module_obj: object, module_name: str) -> List[PixeltableFunction]:
        """Get all public members from a module (for inherited_members: true)"""
        functions = []
        
        # Get all attributes
        for attr_name in dir(module_obj):
            if attr_name.startswith('_'):
                continue  # Skip private members
            
            try:
                attr_obj = getattr(module_obj, attr_name)
                
                # Check if it's a function, class, or method
                if callable(attr_obj):
                    func = self._create_function_from_object(
                        attr_obj, attr_name, module_name
                    )
                    if func:
                        functions.append(func)
                        
            except Exception as e:
                if self.verbose:
                    logger.debug(f"Error getting {attr_name} from {module_name}: {e}")
                continue
        
        return functions
    
    def _get_specific_function(
        self, 
        module_obj: object, 
        func_name: str, 
        module_name: str
    ) -> Optional[PixeltableFunction]:
        """Get a specific function from a module"""
        try:
            if not hasattr(module_obj, func_name):
                logger.warning(f"Function {func_name} not found in {module_name}")
                return None
            
            func_obj = getattr(module_obj, func_name)
            return self._create_function_from_object(func_obj, func_name, module_name)
            
        except Exception as e:
            logger.error(f"Error getting {func_name} from {module_name}: {e}")
            return None
    
    def _create_function_from_object(
        self, 
        obj: object, 
        name: str, 
        module_name: str
    ) -> Optional[PixeltableFunction]:
        """Create PixeltableFunction from a Python object"""
        try:
            # Get signature
            try:
                sig = inspect.signature(obj)
                signature = f"{name}{sig}"
            except (ValueError, TypeError):
                signature = f"{name}()"
            
            # Get docstring
            docstring = inspect.getdoc(obj) or ""
            
            # Extract description (first line/paragraph of docstring)
            description = self._extract_description_from_docstring(docstring)
            
            # Get source file and line number
            file_path = ""
            line_number = 0
            try:
                file_path = inspect.getfile(obj)
                # Make relative to pixeltable repo
                if self.pixeltable_repo in Path(file_path).parents:
                    file_path = str(Path(file_path).relative_to(self.pixeltable_repo))
                    
                line_number = inspect.getsourcelines(obj)[1]
            except (OSError, TypeError):
                pass
            
            # Determine category and type
            category, source_type = self._classify_object(obj, name, module_name)
            
            return PixeltableFunction(
                name=name,
                module=module_name,
                signature=signature,
                docstring=docstring,
                description=description,
                file_path=file_path,
                line_number=line_number,
                category=category,
                source_type=source_type
            )
            
        except Exception as e:
            logger.error(f"Error creating function object for {name}: {e}")
            return None
    
    def _extract_description_from_docstring(self, docstring: str) -> str:
        """Extract clean description from docstring"""
        if not docstring:
            return ""
        
        # Get first meaningful line
        lines = docstring.strip().split('\n')
        for line in lines:
            clean_line = line.strip()
            if clean_line and not clean_line.startswith('"""') and not clean_line.startswith("'''"):
                return clean_line
        
        return ""
    
    def _classify_object(self, obj: object, name: str, module_name: str) -> Tuple[str, str]:
        """Classify object type and category"""
        
        # Determine source type
        if inspect.isclass(obj):
            source_type = "class"
        elif inspect.ismethod(obj):
            source_type = "method"
        elif inspect.isfunction(obj):
            source_type = "function"
        else:
            source_type = "function"  # Default
        
        # Determine category based on module and name patterns
        if "functions" in module_name:
            category = "functions"
        elif "type" in module_name.lower():
            category = "types"
        elif any(term in module_name.lower() for term in ["ml", "embedding", "detection"]):
            category = "ml"
        elif any(term in module_name.lower() for term in ["media", "image", "video", "audio"]):
            category = "media"
        elif any(term in name.lower() for term in ["create", "table", "insert", "update", "delete"]):
            category = "core_api"
        else:
            category = "core_api"  # Default
            
        return category, source_type

class MintlifyMDXGenerator:
    """Generates Mintlify-compatible MDX files from Pixeltable functions"""
    
    def __init__(self, output_path: Path, verbose: bool = False):
        self.output_path = output_path
        self.verbose = verbose
        
    def generate_mdx_files(
        self, 
        functions: List[PixeltableFunction],
        release: str = "latest"
    ) -> Dict[str, Any]:
        """Generate all MDX files and return statistics"""
        
        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        stats = {
            "files_created": 0,
            "functions_documented": len(functions),
            "categories": set(),
            "total_lines": 0
        }
        
        # Generate one MDX file per function
        for function in functions:
            try:
                mdx_path = self._get_mdx_path(function, release)
                mdx_content = self._generate_mdx_content(function)
                
                # Ensure directory exists
                mdx_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write MDX file
                with open(mdx_path, 'w', encoding='utf-8') as f:
                    f.write(mdx_content)
                
                stats["files_created"] += 1
                stats["categories"].add(function.category)
                stats["total_lines"] += len(mdx_content.split('\n'))
                
                if self.verbose:
                    logger.debug(f"📝 Created: {mdx_path}")
                    
            except Exception as e:
                logger.error(f"Error generating MDX for {function.name}: {e}")
                continue
        
        stats["categories"] = len(stats["categories"])
        logger.info(f"📝 Generated {stats['files_created']} MDX files")
        
        return stats
    
    def _get_mdx_path(self, function: PixeltableFunction, release: str) -> Path:
        """Determine output path for function's MDX file"""
        
        # Build path: output/release/category/[subcategory/]function.mdx
        path_parts = [release, function.category]
        
        if function.subcategory:
            path_parts.append(function.subcategory)
        
        path_parts.append(f"{function.name}.mdx")
        
        return self.output_path / Path(*path_parts)
    
    def _generate_mdx_content(self, function: PixeltableFunction) -> str:
        """Generate complete MDX content for a function"""
        
        # Generate title and description
        title = self._generate_title(function)
        description = self._generate_description(function)
        
        # Build MDX content
        lines = [
            "---",
            f'title: "{title}"',
            f'description: "{description}"',
            "---",
            "",
            f"# {title}",
            "",
            "## Signature",
            "",
            "```python",
            function.signature,
            "```",
            "",
            "## Description",
            ""
        ]
        
        # Add docstring content
        if function.docstring:
            docstring_lines = function.docstring.strip().split('\n')
            for line in docstring_lines:
                lines.append(line.rstrip())
        else:
            lines.append(f"Function `{function.name}` from the Pixeltable library.")
        
        # Add examples section
        lines.extend([
            "",
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
        
        # Add source information if available
        if function.file_path:
            lines.extend([
                "## Source",
                "",
                f"**File:** `{function.file_path}`",
            ])
            if function.line_number:
                lines.append(f"**Line:** {function.line_number}")
            lines.append("")
        
        # Add footer
        lines.extend([
            "---",
            "",
            "*Generated by repolex mintlifier*"
        ])
        
        return '\n'.join(lines)
    
    def _generate_title(self, function: PixeltableFunction) -> str:
        """Generate clean title for function"""
        if "." in function.module and function.module != "pixeltable":
            # Extract meaningful module part
            parts = function.module.split(".")
            if len(parts) > 1 and parts[-1] != "pixeltable":
                return f"{parts[-1]}.{function.name}"
        
        return function.name
    
    def _generate_description(self, function: PixeltableFunction) -> str:
        """Generate clean description for function"""
        if function.description:
            return function.description
        
        # Generate default based on category and name
        category_descriptions = {
            "core_api": "Core API function",
            "functions": "Function utility",
            "media": "Media processing function", 
            "ml": "Machine learning function",
            "types": "Type system function"
        }
        
        return f"{category_descriptions.get(function.category, 'Function')} from Pixeltable"

class DocsJsonManager:
    """Manages docs.json navigation generation and merging"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def generate_docs_json_navigation(
        self,
        functions: List[PixeltableFunction],
        release: str,
        org_repo: str = "pixeltable/pixeltable"
    ) -> Dict[str, Any]:
        """Generate docs.json navigation structure for Mintlify"""
        
        # Categorize functions
        categorized = self._categorize_functions(functions)
        
        # Build navigation structure
        navigation = [
            {
                "group": "Getting Started", 
                "pages": [f"sdk/{release}/overview"]
            }
        ]
        
        # Add function categories
        for category, funcs in categorized.items():
            if not funcs:
                continue
                
            category_name = self._format_category_name(category)
            
            navigation.append({
                "group": category_name,
                "pages": [
                    f"sdk/{release}/{category}/{func.name}"
                    for func in funcs
                ]
            })
        
        # Complete docs.json structure
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
                "dark": "#0D9373"
            },
            "tabs": [
                {
                    "name": "Python SDK",
                    "url": "sdk"
                }
            ],
            "navigation": navigation
        }
        
        logger.info(f"📋 Generated docs.json with {len(navigation)} sections")
        return docs_json
    
    def _categorize_functions(
        self, 
        functions: List[PixeltableFunction]
    ) -> Dict[str, List[PixeltableFunction]]:
        """Group functions by category"""
        categorized = {}
        
        for func in functions:
            if func.category not in categorized:
                categorized[func.category] = []
            categorized[func.category].append(func)
        
        return categorized
    
    def _format_category_name(self, category: str) -> str:
        """Format category name for display"""
        return category.replace('_', ' ').title()
    
    def merge_with_existing_docs_json(
        self,
        new_docs_json: Dict[str, Any],
        existing_path: Path
    ) -> Dict[str, Any]:
        """Merge new navigation with existing docs.json"""
        try:
            import json
            
            with open(existing_path, 'r', encoding='utf-8') as f:
                existing_docs = json.load(f)
            
            # Preserve existing configuration
            merged = existing_docs.copy()
            
            # Replace SDK/API sections in navigation
            existing_nav = merged.get('navigation', [])
            new_nav = new_docs_json.get('navigation', [])
            
            # Remove old SDK sections
            filtered_nav = [
                nav for nav in existing_nav
                if not self._is_sdk_section(nav)
            ]
            
            # Add new SDK sections
            filtered_nav.extend(new_nav)
            merged['navigation'] = filtered_nav
            
            logger.info("🔄 Merged with existing docs.json")
            return merged
            
        except Exception as e:
            logger.warning(f"Failed to merge docs.json: {e}")
            return new_docs_json
    
    def _is_sdk_section(self, nav_item: Dict[str, Any]) -> bool:
        """Check if navigation item is an SDK section"""
        if not isinstance(nav_item, dict):
            return False
        
        group_name = nav_item.get('group', '').lower()
        pages = nav_item.get('pages', [])
        
        # Check group name or page paths
        return (
            any(term in group_name for term in ['api', 'reference', 'sdk', 'python']) or
            any(isinstance(page, str) and 'sdk/' in page for page in pages)
        )

class MintlifierGenerator:
    """Main coordinator for Mintlifier generation process"""
    
    def __init__(
        self, 
        pixeltable_repo: Path, 
        mkdocs_path: Path, 
        verbose: bool = False
    ):
        self.pixeltable_repo = pixeltable_repo
        self.mkdocs_path = mkdocs_path
        self.verbose = verbose
        
        # Initialize components
        self.mkdocs_parser = MkDocsParser(mkdocs_path, verbose)
        self.introspector = PixeltableIntrospector(pixeltable_repo, verbose)
        self.docs_json_manager = DocsJsonManager(verbose)
        
    def generate_mintlify_docs(
        self,
        output_path: Path,
        release: str = "latest",
        docs_json_path: Optional[Path] = None,
        merge_navigation: bool = False,
        progress_callback: Optional[callable] = None
    ) -> MintlifierResult:
        """
        Generate complete Mintlify documentation
        
        Returns:
            MintlifierResult with statistics and status
        """
        start_time = datetime.now()
        result = MintlifierResult(output_path=output_path)
        
        try:
            if progress_callback:
                progress_callback(10.0, "🔍 Parsing MKDocs whitelists...")
            
            # Step 1: Parse MKDocs whitelists
            whitelists = self.mkdocs_parser.parse_mkdocs_whitelists()
            if not whitelists:
                raise ValueError("No function whitelists found in MKDocs files")
            
            if progress_callback:
                progress_callback(30.0, "🔧 Introspecting Pixeltable functions...")
            
            # Step 2: Introspect actual functions
            functions = self.introspector.get_functions_from_whitelist(whitelists)
            if not functions:
                raise ValueError("No functions could be introspected from Pixeltable")
            
            result.functions_documented = len(functions)
            
            if progress_callback:
                progress_callback(60.0, "📝 Generating MDX files...")
            
            # Step 3: Generate MDX files
            mdx_generator = MintlifyMDXGenerator(output_path, self.verbose)
            mdx_stats = mdx_generator.generate_mdx_files(functions, release)
            result.files_created = mdx_stats["files_created"]
            
            if progress_callback:
                progress_callback(80.0, "📋 Creating docs.json navigation...")
            
            # Step 4: Generate/merge docs.json
            if docs_json_path:
                docs_json = self.docs_json_manager.generate_docs_json_navigation(
                    functions, release
                )
                
                if merge_navigation and docs_json_path.exists():
                    docs_json = self.docs_json_manager.merge_with_existing_docs_json(
                        docs_json, docs_json_path
                    )
                
                # Write docs.json
                import json
                with open(docs_json_path, 'w', encoding='utf-8') as f:
                    json.dump(docs_json, f, indent=2)
                
                result.docs_json_updated = True
            
            if progress_callback:
                progress_callback(100.0, "🎉 Mintlifier completed!")
            
            result.processing_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"🎉 Mintlifier completed successfully!")
            logger.info(f"📄 Files: {result.files_created}")
            logger.info(f"🔧 Functions: {result.functions_documented}") 
            logger.info(f"⏱️ Time: {result.processing_time:.1f}s")
            
            return result
            
        except Exception as e:
            result.errors.append(str(e))
            result.processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Mintlifier failed: {e}")
            raise


if __name__ == "__main__":
    # Quick test
    def test_mintlifier():
        """Test mintlifier components"""
        print("🍃 Testing Mintlifier components...")
        
        # This would be called from the CLI
        print("✅ Mintlifier core module loaded successfully!")
    
    test_mintlifier()
