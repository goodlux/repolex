#!/usr/bin/env python3
"""
🌟 PAC-MAN's OPML Export Powerhouse! 🌟
Hierarchical export system with full PAC-MAN theming!

WAKA WAKA WAKA! Let's create PERFECT OPML structures for human browsing!
Transform semantic data into beautiful, navigable outlines!
"""

import asyncio
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime
import logging
from dataclasses import dataclass, asdict
import re
from xml.dom import minidom

from ..models.exceptions import (
    CodeDocError, ExportError, ValidationError, StorageError
)
from ..models.function import FunctionInfo, ParameterInfo
from ..models.results import ExportResult
from ..models.progress import ProgressCallback
from ..utils.validation import validate_org_repo, validate_release_tag, validate_file_path
from .base_exporter import PacManBaseExporter

# PAC-MAN themed logging
logger = logging.getLogger("codedoc.opml_powerhouse")

# PAC-MAN OPML Constants! 🌟
PACMAN_OPML_DOTS = "🟡"  # OPML structure dots
PACMAN_OUTLINE_PELLETS = "🔮"  # Major outline sections  
PACMAN_FUNCTION_CHERRIES = "🍒"  # Individual functions
PACMAN_PARAMETER_BONUSES = "💎"  # Function parameters
PACMAN_EXAMPLE_STARS = "⭐"  # Code examples


@dataclass
class PacManOPMLStats:
    """PAC-MAN themed OPML export statistics! 🌟"""
    outlines_created: int = 0  # Total outline nodes
    functions_exported: int = 0  # Functions processed
    parameters_mapped: int = 0  # Parameters structured
    examples_included: int = 0  # Code examples added
    hierarchy_levels: int = 0  # Depth of structure
    total_characters: int = 0  # Total OPML size
    processing_time: float = 0.0  # Time to generate
    
    def add_outline(self) -> None:
        """Add an outline node! 🌟"""
        self.outlines_created += 1
    
    def export_function(self) -> None:
        """Export a function! 🍒"""
        self.functions_exported += 1
    
    def map_parameter(self) -> None:
        """Map a parameter! 💎"""
        self.parameters_mapped += 1
    
    def include_example(self) -> None:
        """Include an example! ⭐"""
        self.examples_included += 1


@dataclass
class PacManOPMLNode:
    """PAC-MAN themed OPML outline node! 🌟"""
    text: str
    node_type: str = "outline"
    attributes: Dict[str, str] = None
    children: List['PacManOPMLNode'] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        if self.children is None:
            self.children = []
        if self.metadata is None:
            self.metadata = {}
    
    def add_child(self, child: 'PacManOPMLNode') -> None:
        """Add a child node to this outline! 🌟"""
        self.children.append(child)
    
    def set_attribute(self, key: str, value: str) -> None:
        """Set an attribute for this node! 🌟"""
        self.attributes[key] = value
    
    def get_depth(self) -> int:
        """Calculate the depth of this node tree! 🌟"""
        if not self.children:
            return 1
        return 1 + max(child.get_depth() for child in self.children)


class PacManOPMLExporter(PacManBaseExporter):
    """
    🌟 PAC-MAN's Ultimate OPML Export Powerhouse! 🌟
    
    The most spectacular OPML exporter ever created!
    PAC-MAN will transform semantic data into beautiful, hierarchical outlines
    perfect for human browsing in tools like WorkFlowy, OmniOutliner, and more!
    
    Features:
    - 🌟 Perfect hierarchical structure generation
    - 🔮 Intelligent function grouping and organization  
    - 🍒 Rich function metadata and documentation
    - 💎 Detailed parameter information
    - ⭐ Code example integration
    - 🎯 Streaming support for massive datasets
    - 🚀 Beautiful XML formatting
    
    WAKA WAKA WAKA! Let's create the most beautiful OPML files ever!
    """
    
    def __init__(self):
        """Initialize PAC-MAN's OPML Export Powerhouse! 🌟"""
        super().__init__()
        self.stats = PacManOPMLStats()
        self.current_hierarchy_level = 0
        
        logger.info("🌟 PAC-MAN OPML Export Powerhouse initialized!")
        logger.info("🎮 Ready to create spectacular OPML structures! WAKA WAKA!")
    
    async def export_opml_spectacular(
        self,
        org_repo: str,
        release: str,
        output_path: Optional[Path] = None,
        progress_callback: Optional[ProgressCallback] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        🌟 Create a SPECTACULAR OPML export!
        
        PAC-MAN will transform semantic data into the most beautiful OPML structure
        that humans have ever seen!
        
        Args:
            org_repo: Repository in 'org/repo' format
            release: Release tag to export
            output_path: Custom output path (auto-generated if None)
            progress_callback: Progress updates during the spectacular creation
            options: Export customization options
            
        Returns:
            Path: Location of the spectacular OPML file
            
        Raises:
            ExportError: If OPML generation fails
            ValidationError: If parameters are invalid
            StorageError: If semantic data cannot be accessed
        """
        # Validate the spectacular parameters! 🌟
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        start_time = datetime.now()
        logger.info(f"🌟 PAC-MAN starting SPECTACULAR OPML export for {org_repo}@{release}!")
        
        if progress_callback:
            await progress_callback(5.0, f"🌟 PAC-MAN preparing spectacular OPML export...")
        
        try:
            # Generate output path if not provided
            if output_path is None:
                output_path = await self._generate_default_opml_path(org_repo, release)
            
            # Validate output path security
            validate_file_path(output_path, self.get_safe_export_directory())
            
            if progress_callback:
                await progress_callback(15.0, f"🔍 Gathering semantic data for OPML...")
            
            # Gather all the semantic data we need
            semantic_data = await self._gather_semantic_data_for_opml(org_repo, release)
            
            if progress_callback:
                await progress_callback(30.0, f"🌟 Creating spectacular OPML structure...")
            
            # Create the spectacular OPML structure
            opml_root = await self._create_spectacular_opml_structure(
                semantic_data, 
                org_repo, 
                release, 
                options,
                progress_callback=self._create_progress_wrapper(progress_callback, 30.0, 80.0)
            )
            
            if progress_callback:
                await progress_callback(85.0, f"✨ Formatting spectacular OPML output...")
            
            # Generate the beautiful XML
            xml_content = await self._generate_beautiful_xml(opml_root)
            
            if progress_callback:
                await progress_callback(95.0, f"💾 Saving spectacular OPML file...")
            
            # Save the spectacular OPML file
            await self._save_opml_file(output_path, xml_content)
            
            # Calculate final statistics
            self.stats.processing_time = (datetime.now() - start_time).total_seconds()
            self.stats.total_characters = len(xml_content)
            self.stats.hierarchy_levels = opml_root.get_depth()
            
            if progress_callback:
                await progress_callback(100.0, f"🌟 SPECTACULAR OPML export complete!")
            
            logger.info(f"🎉 PAC-MAN created SPECTACULAR OPML export!")
            logger.info(f"📊 Statistics: {asdict(self.stats)}")
            logger.info(f"📁 Output: {output_path}")
            logger.info(f"⏱️ Time: {self.stats.processing_time:.2f}s")
            
            return output_path
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered during OPML export: {e}")
            raise ExportError(
                f"Failed to export OPML for {org_repo}@{release}: {str(e)}",
                suggestions=[
                    "Check if semantic data exists for this repository/release",
                    "Verify output path permissions",
                    "Try with a different output location"
                ]
            )
    
    async def _gather_semantic_data_for_opml(
        self, 
        org_repo: str, 
        release: str
    ) -> Dict[str, Any]:
        """
        🔍 Gather all semantic data needed for spectacular OPML export!
        
        This is where PAC-MAN collects all the dots needed for the OPML feast!
        """
        logger.info(f"🔍 PAC-MAN gathering semantic data for {org_repo}@{release}")
        
        try:
            # This would normally interface with the Oxigraph database
            # For now, we'll structure it to work with the expected data format
            
            semantic_data = {
                "repository": {
                    "org_repo": org_repo,
                    "release": release,
                    "name": org_repo.split('/')[-1],
                    "organization": org_repo.split('/')[0]
                },
                "functions": await self._gather_function_data(org_repo, release),
                "modules": await self._gather_module_data(org_repo, release),
                "types": await self._gather_type_data(org_repo, release),
                "metadata": await self._gather_export_metadata(org_repo, release)
            }
            
            logger.info(f"🎯 Gathered {len(semantic_data['functions'])} functions for OPML")
            return semantic_data
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered gathering semantic data: {e}")
            raise StorageError(
                f"Failed to gather semantic data for {org_repo}@{release}: {str(e)}",
                suggestions=[
                    "Ensure repository has been parsed to semantic graphs",
                    "Check if the specified release exists",
                    "Verify Oxigraph database connectivity"
                ]
            )
    
    async def _create_spectacular_opml_structure(
        self,
        semantic_data: Dict[str, Any],
        org_repo: str,
        release: str,
        options: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[ProgressCallback] = None
    ) -> PacManOPMLNode:
        """
        🌟 Create the most SPECTACULAR OPML structure ever!
        
        PAC-MAN will organize everything perfectly for human browsing!
        """
        logger.info("🌟 PAC-MAN creating spectacular OPML structure!")
        
        if not options:
            options = {}
        
        # Create the root OPML node
        root = PacManOPMLNode(
            text=f"{semantic_data['repository']['name']} API Documentation",
            node_type="root",
            attributes={
                "type": "repository_documentation",
                "version": release,
                "generated_by": "PAC-MAN OPML Powerhouse",
                "generated_at": datetime.now().isoformat()
            }
        )
        
        if progress_callback:
            await progress_callback(10.0, "🌟 Creating repository overview...")
        
        # Add repository overview section
        overview_node = await self._create_repository_overview_node(semantic_data)
        root.add_child(overview_node)
        self.stats.add_outline()
        
        if progress_callback:
            await progress_callback(25.0, "🔮 Organizing functions by modules...")
        
        # Organize functions by modules
        modules_data = await self._organize_functions_by_modules(semantic_data["functions"])
        
        progress_per_module = 50.0 / max(1, len(modules_data))
        current_progress = 25.0
        
        for module_name, module_functions in modules_data.items():
            if progress_callback:
                await progress_callback(current_progress, f"🔮 Processing module: {module_name}...")
            
            module_node = await self._create_module_node(module_name, module_functions)
            root.add_child(module_node)
            self.stats.add_outline()
            
            current_progress += progress_per_module
        
        if progress_callback:
            await progress_callback(80.0, "📚 Adding reference sections...")
        
        # Add reference sections
        reference_node = await self._create_reference_sections(semantic_data)
        root.add_child(reference_node)
        self.stats.add_outline()
        
        if progress_callback:
            await progress_callback(95.0, "✨ Finalizing spectacular structure...")
        
        # Add metadata and statistics
        stats_node = await self._create_statistics_node(semantic_data)
        root.add_child(stats_node)
        self.stats.add_outline()
        
        logger.info(f"🎉 Created spectacular OPML structure with {self.stats.outlines_created} outline nodes!")
        return root
    
    async def _create_repository_overview_node(
        self, 
        semantic_data: Dict[str, Any]
    ) -> PacManOPMLNode:
        """🌟 Create a spectacular repository overview node!"""
        
        overview = PacManOPMLNode(
            text="📋 Repository Overview",
            node_type="section",
            attributes={"type": "overview"}
        )
        
        repo_info = semantic_data["repository"]
        
        # Basic information
        info_node = PacManOPMLNode(
            text="ℹ️ Basic Information",
            node_type="subsection"
        )
        
        info_node.add_child(PacManOPMLNode(
            text=f"Repository: {repo_info['org_repo']}",
            attributes={"type": "info_item"}
        ))
        
        info_node.add_child(PacManOPMLNode(
            text=f"Release: {repo_info['release']}",
            attributes={"type": "info_item"}
        ))
        
        info_node.add_child(PacManOPMLNode(
            text=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            attributes={"type": "info_item"}
        ))
        
        overview.add_child(info_node)
        
        # Function summary
        function_count = len(semantic_data.get("functions", []))
        summary_node = PacManOPMLNode(
            text="📊 API Summary",
            node_type="subsection"
        )
        
        summary_node.add_child(PacManOPMLNode(
            text=f"Total Functions: {function_count}",
            attributes={"type": "summary_item"}
        ))
        
        # Group functions by type/category for summary
        function_categories = self._categorize_functions(semantic_data.get("functions", []))
        for category, count in function_categories.items():
            summary_node.add_child(PacManOPMLNode(
                text=f"{category}: {count} functions",
                attributes={"type": "category_summary"}
            ))
        
        overview.add_child(summary_node)
        
        self.stats.add_outline()
        return overview
    
    async def _organize_functions_by_modules(
        self, 
        functions: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """🔮 Organize functions by modules for spectacular display!"""
        
        modules = {}
        
        for function in functions:
            module_name = function.get("module", "Unknown Module")
            
            # Clean up module name for display
            if module_name.startswith("pixeltable."):
                module_name = module_name[11:]  # Remove 'pixeltable.' prefix
            
            # Capitalize for display
            display_name = module_name.replace("_", " ").title()
            
            if display_name not in modules:
                modules[display_name] = []
            
            modules[display_name].append(function)
        
        # Sort modules by name
        return dict(sorted(modules.items()))
    
    async def _create_module_node(
        self, 
        module_name: str, 
        functions: List[Dict[str, Any]]
    ) -> PacManOPMLNode:
        """🔮 Create a spectacular module node with all its functions!"""
        
        module_node = PacManOPMLNode(
            text=f"📁 {module_name} ({len(functions)} functions)",
            node_type="module",
            attributes={
                "type": "module",
                "function_count": str(len(functions))
            }
        )
        
        # Sort functions alphabetically
        sorted_functions = sorted(functions, key=lambda f: f.get("name", ""))
        
        for function_data in sorted_functions:
            function_node = await self._create_function_node(function_data)
            module_node.add_child(function_node)
            self.stats.export_function()
        
        self.stats.add_outline()
        return module_node
    
    async def _create_function_node(
        self, 
        function_data: Dict[str, Any]
    ) -> PacManOPMLNode:
        """🍒 Create a spectacular function node with all details!"""
        
        function_name = function_data.get("name", "unknown_function")
        signature = function_data.get("signature", f"{function_name}()")
        
        # Create main function node
        function_node = PacManOPMLNode(
            text=f"🍒 {signature}",
            node_type="function",
            attributes={
                "type": "function",
                "name": function_name,
                "signature": signature
            }
        )
        
        # Add description if available
        description = function_data.get("description") or function_data.get("docstring")
        if description:
            # Clean up description (first line only for OPML)
            clean_description = description.split('\n')[0].strip()
            if clean_description:
                desc_node = PacManOPMLNode(
                    text=f"📝 {clean_description}",
                    attributes={"type": "description"}
                )
                function_node.add_child(desc_node)
        
        # Add parameters section
        parameters = function_data.get("parameters", [])
        if parameters:
            params_node = await self._create_parameters_node(parameters)
            function_node.add_child(params_node)
        
        # Add return information
        return_info = function_data.get("returns") or function_data.get("return_type")
        if return_info:
            return_node = PacManOPMLNode(
                text=f"↩️ Returns: {return_info}",
                attributes={"type": "returns"}
            )
            function_node.add_child(return_node)
        
        # Add examples if available
        examples = function_data.get("examples", [])
        if examples:
            examples_node = await self._create_examples_node(examples)
            function_node.add_child(examples_node)
        
        # Add source location if available
        file_path = function_data.get("file_path")
        line_number = function_data.get("line_number")
        if file_path:
            location_text = f"📍 {file_path}"
            if line_number:
                location_text += f":{line_number}"
            
            location_node = PacManOPMLNode(
                text=location_text,
                attributes={"type": "source_location"}
            )
            function_node.add_child(location_node)
        
        self.stats.add_outline()
        return function_node
    
    async def _create_parameters_node(
        self, 
        parameters: List[Dict[str, Any]]
    ) -> PacManOPMLNode:
        """💎 Create a spectacular parameters node!"""
        
        params_node = PacManOPMLNode(
            text=f"💎 Parameters ({len(parameters)})",
            node_type="parameters",
            attributes={"type": "parameters"}
        )
        
        for param in parameters:
            param_name = param.get("name", "unknown")
            param_type = param.get("type", "Any")
            required = param.get("required", True)
            default = param.get("default")
            description = param.get("description", "")
            
            # Build parameter display text
            param_text = f"{param_name}: {param_type}"
            
            if not required:
                if default:
                    param_text += f" = {default}"
                else:
                    param_text += " (optional)"
            
            param_node = PacManOPMLNode(
                text=f"• {param_text}",
                attributes={
                    "type": "parameter",
                    "name": param_name,
                    "param_type": param_type,
                    "required": str(required)
                }
            )
            
            # Add parameter description if available
            if description:
                desc_node = PacManOPMLNode(
                    text=f"  📝 {description}",
                    attributes={"type": "parameter_description"}
                )
                param_node.add_child(desc_node)
            
            params_node.add_child(param_node)
            self.stats.map_parameter()
        
        self.stats.add_outline()
        return params_node
    
    async def _create_examples_node(
        self, 
        examples: List[Dict[str, Any]]
    ) -> PacManOPMLNode:
        """⭐ Create a spectacular examples node!"""
        
        examples_node = PacManOPMLNode(
            text=f"⭐ Examples ({len(examples)})",
            node_type="examples",
            attributes={"type": "examples"}
        )
        
        for i, example in enumerate(examples, 1):
            title = example.get("title", f"Example {i}")
            code = example.get("code", "")
            description = example.get("description", "")
            
            example_node = PacManOPMLNode(
                text=f"⭐ {title}",
                attributes={"type": "example"}
            )
            
            # Add description if available
            if description:
                desc_node = PacManOPMLNode(
                    text=f"📝 {description}",
                    attributes={"type": "example_description"}
                )
                example_node.add_child(desc_node)
            
            # Add code (formatted for OPML)
            if code:
                # Clean up code for OPML display
                clean_code = code.strip().replace('\n', ' ↵ ')
                code_node = PacManOPMLNode(
                    text=f"💻 {clean_code}",
                    attributes={"type": "example_code"}
                )
                example_node.add_child(code_node)
            
            examples_node.add_child(example_node)
            self.stats.include_example()
        
        self.stats.add_outline()
        return examples_node
    
    async def _create_reference_sections(
        self, 
        semantic_data: Dict[str, Any]
    ) -> PacManOPMLNode:
        """📚 Create spectacular reference sections!"""
        
        reference_node = PacManOPMLNode(
            text="📚 Reference",
            node_type="reference",
            attributes={"type": "reference"}
        )
        
        # Function index (alphabetical)
        functions = semantic_data.get("functions", [])
        if functions:
            index_node = PacManOPMLNode(
                text=f"🔤 Function Index ({len(functions)} functions)",
                attributes={"type": "function_index"}
            )
            
            # Sort functions alphabetically
            sorted_functions = sorted(functions, key=lambda f: f.get("name", ""))
            
            for function in sorted_functions:
                name = function.get("name", "unknown")
                signature = function.get("signature", f"{name}()")
                module = function.get("module", "Unknown")
                
                index_item = PacManOPMLNode(
                    text=f"• {name} - {module}",
                    attributes={
                        "type": "index_item",
                        "function_name": name,
                        "signature": signature,
                        "module": module
                    }
                )
                index_node.add_child(index_item)
            
            reference_node.add_child(index_node)
        
        # Type index if available
        types = semantic_data.get("types", [])
        if types:
            type_index_node = PacManOPMLNode(
                text=f"🏷️ Type Index ({len(types)} types)",
                attributes={"type": "type_index"}
            )
            
            for type_info in sorted(types, key=lambda t: t.get("name", "")):
                type_name = type_info.get("name", "unknown")
                type_item = PacManOPMLNode(
                    text=f"• {type_name}",
                    attributes={"type": "type_item", "type_name": type_name}
                )
                type_index_node.add_child(type_item)
            
            reference_node.add_child(type_index_node)
        
        self.stats.add_outline()
        return reference_node
    
    async def _create_statistics_node(
        self, 
        semantic_data: Dict[str, Any]
    ) -> PacManOPMLNode:
        """📊 Create spectacular statistics node!"""
        
        stats_node = PacManOPMLNode(
            text="📊 Export Statistics",
            node_type="statistics",
            attributes={"type": "statistics"}
        )
        
        # Export statistics
        stats_node.add_child(PacManOPMLNode(
            text=f"📈 Outline Nodes Created: {self.stats.outlines_created}",
            attributes={"type": "stat_item"}
        ))
        
        stats_node.add_child(PacManOPMLNode(
            text=f"🍒 Functions Exported: {self.stats.functions_exported}",
            attributes={"type": "stat_item"}
        ))
        
        stats_node.add_child(PacManOPMLNode(
            text=f"💎 Parameters Mapped: {self.stats.parameters_mapped}",
            attributes={"type": "stat_item"}
        ))
        
        stats_node.add_child(PacManOPMLNode(
            text=f"⭐ Examples Included: {self.stats.examples_included}",
            attributes={"type": "stat_item"}
        ))
        
        # PAC-MAN signature
        signature_node = PacManOPMLNode(
            text="🟡 Generated by PAC-MAN OPML Powerhouse! WAKA WAKA!",
            attributes={
                "type": "generator_signature",
                "version": "PAC-MAN v1.0",
                "timestamp": datetime.now().isoformat()
            }
        )
        stats_node.add_child(signature_node)
        
        self.stats.add_outline()
        return stats_node
    
    async def _generate_beautiful_xml(
        self, 
        opml_root: PacManOPMLNode
    ) -> str:
        """✨ Generate beautiful, formatted OPML XML!"""
        
        logger.info("✨ PAC-MAN generating beautiful OPML XML!")
        
        # Create OPML document structure
        opml_elem = ET.Element("opml", version="2.0")
        
        # Create head section
        head_elem = ET.SubElement(opml_elem, "head")
        
        title_elem = ET.SubElement(head_elem, "title")
        title_elem.text = opml_root.text
        
        created_elem = ET.SubElement(head_elem, "dateCreated")
        created_elem.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        generator_elem = ET.SubElement(head_elem, "ownerId")
        generator_elem.text = "PAC-MAN OPML Powerhouse v1.0"
        
        # Create body section
        body_elem = ET.SubElement(opml_elem, "body")
        
        # Convert our PAC-MAN nodes to XML
        for child in opml_root.children:
            xml_child = self._convert_node_to_xml(child)
            body_elem.append(xml_child)
        
        # Generate beautiful formatted XML
        rough_string = ET.tostring(opml_elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        beautiful_xml = reparsed.toprettyxml(indent="  ")
        
        # Clean up the XML (remove empty lines)
        lines = [line for line in beautiful_xml.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _convert_node_to_xml(self, node: PacManOPMLNode) -> ET.Element:
        """Convert PAC-MAN OPML node to XML element"""
        
        # Create outline element
        outline_elem = ET.Element("outline")
        
        # Set text attribute
        outline_elem.set("text", node.text)
        
        # Set additional attributes
        for key, value in node.attributes.items():
            outline_elem.set(key, str(value))
        
        # Add children recursively
        for child in node.children:
            child_elem = self._convert_node_to_xml(child)
            outline_elem.append(child_elem)
        
        return outline_elem
    
    async def _save_opml_file(self, output_path: Path, xml_content: str):
        """💾 Save the spectacular OPML file!"""
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the beautiful OPML content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        logger.info(f"💾 Saved spectacular OPML file: {output_path}")
        logger.info(f"📊 File size: {len(xml_content)} characters")
    
    def _categorize_functions(self, functions: List[Dict[str, Any]]) -> Dict[str, int]:
        """📊 Categorize functions for summary statistics"""
        
        categories = {
            "Core Functions": 0,
            "Data Operations": 0,
            "Utility Functions": 0,
            "Advanced Features": 0
        }
        
        for function in functions:
            name = function.get("name", "").lower()
            description = (function.get("description", "") + 
                          function.get("docstring", "")).lower()
            
            # Simple categorization based on function names and descriptions
            if any(word in name for word in ["create", "add", "new", "init"]):
                categories["Core Functions"] += 1
            elif any(word in name for word in ["insert", "update", "delete", "select", "query"]):
                categories["Data Operations"] += 1
            elif any(word in name for word in ["get", "set", "list", "show", "find"]):
                categories["Utility Functions"] += 1
            else:
                categories["Advanced Features"] += 1
        
        return categories
    
    async def _generate_default_opml_path(
        self, 
        org_repo: str, 
        release: str
    ) -> Path:
        """Generate default OPML output path"""
        
        base_exports = Path.home() / ".codedoc" / "exports"
        org, repo = org_repo.split('/')
        
        opml_path = base_exports / org / repo / f"{release}.opml"
        return opml_path
    
    def get_pacman_opml_stats(self) -> Dict[str, Any]:
        """📊 Get PAC-MAN's OPML export statistics!"""
        
        return {
            "opml_stats": asdict(self.stats),
            "performance": {
                "outlines_per_second": (
                    self.stats.outlines_created / max(0.1, self.stats.processing_time)
                    if self.stats.processing_time > 0 else 0
                ),
                "functions_per_second": (
                    self.stats.functions_exported / max(0.1, self.stats.processing_time)
                    if self.stats.processing_time > 0 else 0
                ),
                "efficiency_rating": self._calculate_opml_efficiency()
            }
        }
    
    def _calculate_opml_efficiency(self) -> str:
        """Calculate PAC-MAN's OPML export efficiency"""
        
        if self.stats.outlines_created == 0:
            return "🆕 NEW OPML CREATOR"
        
        # Simple efficiency calculation based on structure richness
        richness_score = (
            self.stats.functions_exported * 2 +
            self.stats.parameters_mapped +
            self.stats.examples_included * 3
        ) / max(1, self.stats.outlines_created)
        
        if richness_score >= 10:
            return "🌟 OPML MASTER"
        elif richness_score >= 7:
            return "🔮 STRUCTURE WIZARD"
        elif richness_score >= 4:
            return "🍒 OUTLINE EXPERT"
        else:
            return "💎 GETTING STARTED"


# Factory function for easy OPML creation
def create_pacman_opml_exporter() -> PacManOPMLExporter:
    """
    🌟 Create PAC-MAN's OPML Export Powerhouse!
    
    Factory function to create the ultimate OPML export system!
    
    Returns:
        PacManOPMLExporter: Ready to create spectacular OPML files!
    """
    exporter = PacManOPMLExporter()
    logger.info("🌟 PAC-MAN OPML Export Powerhouse created and ready!")
    logger.info("🎮 WAKA WAKA WAKA! Let's create spectacular OPML structures!")
    return exporter


# Convenience aliases
OPMLExporter = PacManOPMLExporter  # For those who prefer shorter names


if __name__ == "__main__":
    # Quick test of PAC-MAN's OPML Export Powerhouse!
    import asyncio
    
    async def test_pacman_opml_exporter():
        exporter = create_pacman_opml_exporter()
        print("🌟 PAC-MAN OPML Export Powerhouse test complete!")
        print("🎮 Ready to create spectacular OPML files! WAKA WAKA!")
        
        stats = exporter.get_pacman_opml_stats()
        print(f"📊 Export stats: {stats}")
    
    asyncio.run(test_pacman_opml_exporter())
