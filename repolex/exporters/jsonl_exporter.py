#!/usr/bin/env python3
"""
📋 PAC-MAN's JSONL Export Powerhouse! 📋
Semantic DNA in JSONL format - the perfect balance of compression and compatibility!

Transform semantic intelligence into streamable, queryable JSONL!
Zero dependencies, maximum LLM compatibility, optimal compression!
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Iterator
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
logger = logging.getLogger("Repolex.jsonl_powerhouse")

# PAC-MAN JSONL Constants! 📋
PACMAN_JSONL_LINES = "📋"  # JSONL stream lines
PACMAN_SEMANTIC_ENTITIES = "🔮"  # Individual semantic entities
PACMAN_FUNCTION_PELLETS = "🟡"  # Function entities
PACMAN_MODULE_CLUSTERS = "🌟"  # Module entities
PACMAN_PATTERN_STARS = "⭐"  # Pattern entities


@dataclass
class PacManJSONLStats:
    """PAC-MAN themed JSONL export statistics! 📋"""
    jsonl_lines_created: int = 0  # Total JSONL lines
    functions_exported: int = 0  # Function entities
    modules_exported: int = 0  # Module entities
    patterns_exported: int = 0  # Pattern entities
    clusters_exported: int = 0  # Semantic clusters
    total_file_size: int = 0  # Final file size in bytes
    compression_ratio: float = 0.0  # vs pure JSON
    processing_time: float = 0.0  # Time to generate
    
    def add_jsonl_line(self) -> None:
        """Add a JSONL line! 📋"""
        self.jsonl_lines_created += 1
    
    def export_function(self) -> None:
        """Export a function entity! 🟡"""
        self.functions_exported += 1
        self.add_jsonl_line()
    
    def export_module(self) -> None:
        """Export a module entity! 🌟"""
        self.modules_exported += 1
        self.add_jsonl_line()
    
    def export_pattern(self) -> None:
        """Export a pattern entity! ⭐"""
        self.patterns_exported += 1
        self.add_jsonl_line()
    
    def export_cluster(self) -> None:
        """Export a semantic cluster! 🔮"""
        self.clusters_exported += 1
        self.add_jsonl_line()


class PacManJSONLExporter:
    """
    📋 PAC-MAN's Ultimate JSONL Export Powerhouse! 📋
    
    The most spectacular JSONL semantic DNA generator ever created!
    PAC-MAN will transform semantic data into streamable, queryable JSONL
    with perfect compression and zero-dependency LLM compatibility!
    
    Features:
    - 📋 Streamable JSONL format for efficient processing
    - 🔮 Rich semantic entities (functions, modules, patterns, clusters) 
    - 🟡 Optimal compression with readable field names
    - 🌟 Zero-dependency jq compatibility
    - ⭐ Self-documenting entity structure
    - 🎯 Perfect LLM context injection format
    - 🚀 Streaming support for massive datasets
    
    WAKA WAKA WAKA! Let's create the most efficient semantic intelligence ever!
    """
    
    def __init__(self):
        """Initialize PAC-MAN's JSONL Export Powerhouse! 📋"""
        self.stats = PacManJSONLStats()
        
        logger.info("📋 PAC-MAN JSONL Export Powerhouse initialized!")
        logger.info("🎮 Ready to create spectacular JSONL semantic intelligence! WAKA WAKA!")
    
    def export_jsonl_spectacular(
        self,
        org_repo: str,
        release: str,
        output_path: Optional[Path] = None,
        progress_callback: Optional[ProgressCallback] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        📋 Create a SPECTACULAR JSONL semantic DNA export!
        
        PAC-MAN will transform semantic data into the most efficient JSONL format
        that LLMs have ever consumed!
        
        Args:
            org_repo: Repository in 'org/repo' format
            release: Release tag to export
            output_path: Custom output path (auto-generated if None)
            progress_callback: Progress updates during the spectacular creation
            options: Export customization options
            
        Returns:
            Path: Location of the spectacular JSONL file
            
        Raises:
            ExportError: If JSONL generation fails
            ValidationError: If parameters are invalid
            StorageError: If semantic data cannot be accessed
        """
        # Validate the spectacular parameters! 📋
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        start_time = datetime.now()
        logger.info(f"📋 PAC-MAN starting SPECTACULAR JSONL export for {org_repo}@{release}!")
        
        if progress_callback:
            progress_callback(5.0, f"📋 PAC-MAN preparing spectacular JSONL export...")
        
        try:
            # Generate output path if not provided
            if output_path is None:
                output_path = self._generate_default_jsonl_path(org_repo, release)
            
            # Validate output path security
            validate_file_path(output_path, self.get_safe_export_directory())
            
            if progress_callback:
                progress_callback(15.0, f"🔍 Gathering semantic data for JSONL...")
            
            # Gather all the semantic data we need
            semantic_data = self._gather_semantic_data_for_jsonl(org_repo, release)
            
            if progress_callback:
                progress_callback(30.0, f"📋 Creating spectacular JSONL stream...")
            
            # Create and write the spectacular JSONL file
            self._create_and_write_jsonl(
                semantic_data, 
                output_path,
                org_repo, 
                release, 
                options,
                progress_callback=self._create_progress_wrapper(progress_callback, 30.0, 90.0)
            )
            
            # Calculate final statistics
            self.stats.processing_time = (datetime.now() - start_time).total_seconds()
            self.stats.total_file_size = output_path.stat().st_size
            
            if progress_callback:
                progress_callback(100.0, f"📋 SPECTACULAR JSONL export complete!")
            
            logger.info(f"🎉 PAC-MAN created SPECTACULAR JSONL export!")
            logger.info(f"📊 Statistics: {asdict(self.stats)}")
            logger.info(f"📁 Output: {output_path}")
            logger.info(f"💾 Size: {self.stats.total_file_size / 1024:.1f}KB")
            logger.info(f"⏱️ Time: {self.stats.processing_time:.2f}s")
            
            return output_path
            
        except Exception as e:
            logger.error(f"👻 Ghost encountered during JSONL export: {e}")
            raise ExportError(
                f"Failed to export JSONL for {org_repo}@{release}: {str(e)}",
                suggestions=[
                    "Check if semantic data exists for this repository/release",
                    "Verify output path permissions",
                    "Try with a different output location"
                ]
            )
    
    def _gather_semantic_data_for_jsonl(
        self, 
        org_repo: str, 
        release: str
    ) -> Dict[str, Any]:
        """
        🔍 Gather all semantic data needed for spectacular JSONL export!
        
        This is where PAC-MAN collects all the semantic entities for the JSONL feast!
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
                "functions": self._gather_function_data(org_repo, release),
                "modules": self._gather_module_data(org_repo, release),
                "patterns": self._gather_pattern_data(org_repo, release),
                "clusters": self._gather_cluster_data(org_repo, release),
                "metadata": self._gather_export_metadata(org_repo, release)
            }
            
            logger.info(f"🎯 Gathered {len(semantic_data['functions'])} functions for JSONL")
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
    
    def _create_and_write_jsonl(
        self,
        semantic_data: Dict[str, Any],
        output_path: Path,
        org_repo: str,
        release: str,
        options: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[ProgressCallback] = None
    ):
        """
        📋 Create and write the spectacular JSONL file!
        
        Stream semantic entities directly to file for maximum efficiency!
        """
        logger.info("📋 PAC-MAN creating spectacular JSONL stream!")
        
        if not options:
            options = {}
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header metadata
            header_entity = {
                "type": "header",
                "repo": org_repo,
                "release": release,
                "generator": "PAC-MAN JSONL Powerhouse v1.0",
                "generated_at": datetime.now().isoformat(),
                "format_version": "1.0"
            }
            f.write(json.dumps(header_entity) + '\n')
            self.stats.add_jsonl_line()
            
            if progress_callback:
                progress_callback(10.0, "📋 Writing header entity...")
            
            # Write repository metadata
            repo_entity = {
                "type": "repository",
                "org_repo": org_repo,
                "release": release,
                "name": semantic_data["repository"]["name"],
                "organization": semantic_data["repository"]["organization"]
            }
            f.write(json.dumps(repo_entity) + '\n')
            self.stats.add_jsonl_line()
            
            if progress_callback:
                progress_callback(20.0, "🔮 Writing function entities...")
            
            # Write function entities
            functions = semantic_data.get("functions", [])
            for i, function_data in enumerate(functions):
                function_entity = self._create_function_entity(function_data)
                f.write(json.dumps(function_entity) + '\n')
                self.stats.export_function()
                
                if progress_callback and i % 50 == 0:
                    progress = 20.0 + (40.0 * i / max(1, len(functions)))
                    progress_callback(progress, f"🟡 Exported {i+1}/{len(functions)} functions...")
            
            if progress_callback:
                progress_callback(60.0, "🌟 Writing module entities...")
            
            # Write module entities
            modules = semantic_data.get("modules", {})
            for module_name, module_data in modules.items():
                module_entity = self._create_module_entity(module_name, module_data)
                f.write(json.dumps(module_entity) + '\n')
                self.stats.export_module()
            
            if progress_callback:
                progress_callback(75.0, "⭐ Writing pattern entities...")
            
            # Write pattern entities
            patterns = semantic_data.get("patterns", {})
            for pattern_name, pattern_data in patterns.items():
                pattern_entity = self._create_pattern_entity(pattern_name, pattern_data)
                f.write(json.dumps(pattern_entity) + '\n')
                self.stats.export_pattern()
            
            if progress_callback:
                progress_callback(85.0, "🔮 Writing cluster entities...")
            
            # Write semantic cluster entities
            clusters = semantic_data.get("clusters", {})
            for cluster_name, cluster_data in clusters.items():
                cluster_entity = self._create_cluster_entity(cluster_name, cluster_data)
                f.write(json.dumps(cluster_entity) + '\n')
                self.stats.export_cluster()
            
            if progress_callback:
                progress_callback(95.0, "📋 Writing footer metadata...")
            
            # Write footer statistics
            footer_entity = {
                "type": "footer",
                "stats": {
                    "functions_exported": self.stats.functions_exported,
                    "modules_exported": self.stats.modules_exported,
                    "patterns_exported": self.stats.patterns_exported,
                    "clusters_exported": self.stats.clusters_exported,
                    "total_entities": self.stats.jsonl_lines_created
                },
                "completed_at": datetime.now().isoformat()
            }
            f.write(json.dumps(footer_entity) + '\n')
            self.stats.add_jsonl_line()
        
        logger.info(f"🎉 Created spectacular JSONL with {self.stats.jsonl_lines_created} entities!")
    
    def _create_function_entity(self, function_data: Dict[str, Any]) -> Dict[str, Any]:
        """🟡 Create a function entity for JSONL"""
        
        return {
            "type": "function",
            "n": function_data.get("name", "unknown"),  # name
            "s": function_data.get("signature", "def unknown()"),  # signature
            "d": function_data.get("description", ""),  # description
            "m": function_data.get("module", "unknown"),  # module
            "f": function_data.get("file_path", ""),  # file path
            "l": function_data.get("line_number", 0),  # line number
            "t": function_data.get("tags", []),  # tags
            "cat": function_data.get("category", "unknown")  # category
        }
    
    def _create_module_entity(self, module_name: str, module_data: Any) -> Dict[str, Any]:
        """🌟 Create a module entity for JSONL"""
        
        if isinstance(module_data, dict):
            function_count = len(module_data.get("functions", []))
            file_path = module_data.get("file_path", "")
        else:
            function_count = 0
            file_path = ""
        
        return {
            "type": "module",
            "name": module_name,
            "path": file_path,
            "function_count": function_count,
            "category": self._determine_module_category(module_name)
        }
    
    def _create_pattern_entity(self, pattern_name: str, pattern_data: Any) -> Dict[str, Any]:
        """⭐ Create a pattern entity for JSONL"""
        
        if isinstance(pattern_data, dict):
            functions = pattern_data.get("functions", [])
            usage = pattern_data.get("usage", "")
        else:
            functions = []
            usage = ""
        
        return {
            "type": "pattern",
            "name": pattern_name,
            "functions": functions[:10],  # Limit for size
            "function_count": len(functions) if isinstance(functions, list) else 0,
            "usage": usage,
            "category": self._determine_pattern_category(pattern_name)
        }
    
    def _create_cluster_entity(self, cluster_name: str, cluster_data: Any) -> Dict[str, Any]:
        """🔮 Create a semantic cluster entity for JSONL"""
        
        if isinstance(cluster_data, dict):
            modules = cluster_data.get("modules", [])
            description = cluster_data.get("description", "")
        else:
            modules = []
            description = ""
        
        return {
            "type": "cluster",
            "name": cluster_name,
            "modules": modules[:5],  # Limit for size
            "module_count": len(modules) if isinstance(modules, list) else 0,
            "description": description
        }
    
    def _determine_module_category(self, module_name: str) -> str:
        """Determine category for module entity"""
        
        module_lower = module_name.lower()
        
        if "api" in module_lower or "client" in module_lower:
            return "api"
        elif "core" in module_lower or "engine" in module_lower:
            return "core"
        elif "util" in module_lower or "helper" in module_lower:
            return "utility"
        elif "test" in module_lower:
            return "test"
        else:
            return "application"
    
    def _determine_pattern_category(self, pattern_name: str) -> str:
        """Determine category for pattern entity"""
        
        pattern_lower = pattern_name.lower()
        
        if "crud" in pattern_lower or "database" in pattern_lower:
            return "data_access"
        elif "api" in pattern_lower or "endpoint" in pattern_lower:
            return "api_pattern"
        elif "util" in pattern_lower or "helper" in pattern_lower:
            return "utility_pattern"
        else:
            return "domain_pattern"
    
    def _generate_default_jsonl_path(
        self, 
        org_repo: str, 
        release: str
    ) -> Path:
        """Generate default JSONL output path"""
        
        base_exports = Path.home() / ".repolex" / "exports"
        org, repo = org_repo.split('/')
        
        jsonl_path = base_exports / org / repo / f"{release}.jsonl"
        return jsonl_path
    
    def get_safe_export_directory(self) -> Path:
        """Get safe export directory for validation"""
        return Path.home() / ".repolex" / "exports"
    
    def _create_progress_wrapper(
        self, 
        callback: Optional[ProgressCallback], 
        start: float, 
        end: float
    ) -> Optional[ProgressCallback]:
        """Create a progress callback wrapper for scaled progress"""
        
        if not callback:
            return None
        
        def wrapped_callback(percent: float, message: str):
            scaled_percent = start + (percent * (end - start) / 100.0)
            callback(scaled_percent, message)
        
        return wrapped_callback
    
    def _gather_function_data(self, org_repo: str, release: str) -> List[Dict[str, Any]]:
        """Gather function data from export manager"""
        try:
            from ..core.export_manager import get_export_manager
            
            export_manager = get_export_manager()
            
            # Use the existing export functionality to get function data
            function_data = export_manager._get_functions(org_repo, release)
            
            functions = []
            for func in function_data:
                functions.append({
                    "name": func.get("name", "unknown"),
                    "signature": func.get("signature", "def unknown()"),
                    "description": func.get("description", ""),
                    "module": func.get("module", "unknown"),
                    "file_path": func.get("file_path", ""),
                    "line_number": func.get("line_number", 0),
                    "tags": func.get("tags", []),
                    "category": self._determine_function_category(func.get("name", ""), func.get("module", ""))
                })
            
            return functions
            
        except Exception as e:
            logger.warning(f"Could not gather function data: {e}")
            return []
    
    def _gather_module_data(self, org_repo: str, release: str) -> Dict[str, Any]:
        """Gather module data from export manager"""
        try:
            from ..core.export_manager import get_export_manager
            
            export_manager = get_export_manager()
            
            # Try to get module data if available
            module_data = export_manager._get_modules(org_repo, release)
            return module_data
            
        except Exception as e:
            logger.warning(f"Could not gather module data: {e}")
            return {}
    
    def _gather_pattern_data(self, org_repo: str, release: str) -> Dict[str, Any]:
        """Gather pattern data - semantic analysis of function relationships"""
        # For now, create basic patterns from function names
        functions = self._gather_function_data(org_repo, release)
        
        patterns = {}
        
        # CRUD pattern detection
        crud_functions = [f for f in functions if any(word in f["name"].lower() for word in ["create", "insert", "add", "update", "delete", "remove", "get", "find", "list"])]
        if crud_functions:
            patterns["crud_operations"] = {
                "functions": [f["name"] for f in crud_functions[:10]],
                "usage": "Create, Read, Update, Delete operations",
                "function_count": len(crud_functions)
            }
        
        # Export pattern detection  
        export_functions = [f for f in functions if "export" in f["name"].lower()]
        if export_functions:
            patterns["export_operations"] = {
                "functions": [f["name"] for f in export_functions],
                "usage": "Data export and transformation",
                "function_count": len(export_functions)
            }
        
        return patterns
    
    def _gather_cluster_data(self, org_repo: str, release: str) -> Dict[str, Any]:
        """Gather semantic cluster data - high-level architecture groupings"""
        functions = self._gather_function_data(org_repo, release)
        
        # Group by module prefixes to identify clusters
        module_groups = {}
        for func in functions:
            module = func.get("module", "unknown")
            
            # Extract high-level module category
            if "/" in module:
                parts = module.split("/")
                if len(parts) >= 3:
                    cluster_key = parts[-3]  # Third from end
                else:
                    cluster_key = parts[-2] if len(parts) >= 2 else parts[-1]
            else:
                cluster_key = "core"
            
            if cluster_key not in module_groups:
                module_groups[cluster_key] = []
            module_groups[cluster_key].append(module)
        
        clusters = {}
        for cluster_name, modules in module_groups.items():
            unique_modules = list(set(modules))
            if len(unique_modules) >= 2:  # Only clusters with multiple modules
                clusters[f"{cluster_name}_layer"] = {
                    "modules": unique_modules[:5],  # Limit for size
                    "description": f"{cluster_name.title()} layer functionality",
                    "module_count": len(unique_modules)
                }
        
        return clusters
    
    def _determine_function_category(self, func_name: str, module: str) -> str:
        """Determine category for function based on name and module"""
        
        name_lower = func_name.lower()
        module_lower = module.lower()
        
        # API functions
        if any(word in name_lower for word in ["create", "get", "list", "update", "delete"]):
            return "core_api"
        elif "export" in name_lower:
            return "export"
        elif "test" in name_lower or "test" in module_lower:
            return "test"
        elif any(word in module_lower for word in ["util", "helper", "common"]):
            return "utility"
        else:
            return "application"
    
    def _gather_export_metadata(self, org_repo: str, release: str) -> Dict[str, Any]:
        """Gather export metadata - placeholder for now"""
        return {
            "export_time": datetime.now().isoformat(),
            "exporter": "PAC-MAN JSONL Powerhouse"
        }
    
    def get_pacman_jsonl_stats(self) -> Dict[str, Any]:
        """📊 Get PAC-MAN's JSONL export statistics!"""
        
        return {
            "jsonl_stats": asdict(self.stats),
            "performance": {
                "entities_per_second": (
                    self.stats.jsonl_lines_created / max(0.1, self.stats.processing_time)
                    if self.stats.processing_time > 0 else 0
                ),
                "kb_per_second": (
                    (self.stats.total_file_size / 1024) / max(0.1, self.stats.processing_time)
                    if self.stats.processing_time > 0 else 0
                ),
                "efficiency_rating": self._calculate_jsonl_efficiency()
            }
        }
    
    def _calculate_jsonl_efficiency(self) -> str:
        """Calculate PAC-MAN's JSONL export efficiency"""
        
        if self.stats.jsonl_lines_created == 0:
            return "🆕 NEW JSONL CREATOR"
        
        # Simple efficiency calculation based on entity richness
        richness_score = (
            self.stats.functions_exported * 3 +
            self.stats.modules_exported * 2 +
            self.stats.patterns_exported * 2 +
            self.stats.clusters_exported * 1
        ) / max(1, self.stats.jsonl_lines_created)
        
        if richness_score >= 5:
            return "📋 JSONL MASTER"
        elif richness_score >= 3:
            return "🔮 SEMANTIC WIZARD"
        elif richness_score >= 1:
            return "🟡 ENTITY EXPERT"
        else:
            return "⭐ GETTING STARTED"


# Factory function for easy JSONL creation
def create_pacman_jsonl_exporter() -> PacManJSONLExporter:
    """
    📋 Create PAC-MAN's JSONL Export Powerhouse!
    
    Factory function to create the ultimate JSONL semantic intelligence system!
    
    Returns:
        PacManJSONLExporter: Ready to create spectacular JSONL files!
    """
    exporter = PacManJSONLExporter()
    logger.info("📋 PAC-MAN JSONL Export Powerhouse created and ready!")
    logger.info("🎮 WAKA WAKA WAKA! Let's create spectacular semantic intelligence!")
    return exporter


# Convenience aliases
JSONLExporter = PacManJSONLExporter


if __name__ == "__main__":
    # Quick test of PAC-MAN's JSONL Export Powerhouse!
    
    def test_pacman_jsonl_exporter():
        exporter = create_pacman_jsonl_exporter()
        print("📋 PAC-MAN JSONL Export Powerhouse test complete!")
        print("🎮 Ready to create spectacular JSONL semantic intelligence! WAKA WAKA!")
        
        stats = exporter.get_pacman_jsonl_stats()
        print(f"📊 Export stats: {stats}")
    
    test_pacman_jsonl_exporter()