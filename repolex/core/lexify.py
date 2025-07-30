"""
🧠 LEXIFY - Intelligent Semantic Lexicon Builder

The one-click solution for complete code intelligence:
- Discovers all project dependencies  
- Checks semantic-dna/registry for pre-built lexicons
- Downloads/builds missing repositories and graphs
- Exports complete semantic DNA collection

Usage: rlex lexify [project_path] [output_path]
"""
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass
from loguru import logger
import subprocess

from .dependency_parser import discover_project_dependencies, Dependency
from .manager import RepolexManager


@dataclass 
class LexifyStats:
    """Statistics from lexify operation"""
    total_dependencies: int = 0
    from_registry: int = 0
    built_locally: int = 0
    total_functions: int = 0
    total_size_mb: float = 0.0
    

class LexifyOrchestrator:
    """🧠 Orchestrates the complete lexify process"""
    
    def __init__(self, project_path: str = ".", output_path: str = ".", include_dependencies: bool = False):
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        self.llm_rlex_dir = self.output_path / "llm-repolex"
        self.include_dependencies = include_dependencies
        self.manager = RepolexManager()
        # Initialize the manager for repo/graph operations
        try:
            self.manager.initialize()
        except Exception as e:
            logger.warning(f"⚠️  Manager initialization warning: {e}")
        self.stats = LexifyStats()
        
    def lexify(self, progress_callback=None) -> LexifyStats:
        """🚀 Main lexify orchestration"""
        logger.info(f"🧠 Starting lexify for {self.project_path}")
        
        dependencies = []
        
        if self.include_dependencies:
            if progress_callback:
                progress_callback(0, "🔍 Discovering project dependencies...")
            
            # Phase 1: Discovery
            dependencies = self._discover_dependencies()
            self.stats.total_dependencies = len(dependencies)
            
            if dependencies:
                logger.info(f"📦 Discovered {len(dependencies)} dependencies")
                
                if progress_callback:
                    progress_callback(20, f"🌐 Checking semantic DNA registry...")
                
                # Phase 2: Registry Check (stubbed for now)
                available_deps, missing_deps = self._check_registry(dependencies)
                self.stats.from_registry = len(available_deps)
                self.stats.built_locally = len(missing_deps)
                
                if progress_callback:
                    progress_callback(40, f"📥 Processing {len(missing_deps)} missing dependencies...")
                
                # Phase 3: Build Missing Dependencies
                self._build_missing_dependencies(missing_deps, progress_callback)
                
                if progress_callback:
                    progress_callback(70, f"📤 Exporting {len(dependencies)} semantic DNA files...")
                
                # Phase 4: Export All Dependencies
                self._export_all_dependencies(dependencies, progress_callback)
            else:
                logger.warning("⚠️  No dependencies found")
        else:
            logger.info("📦 Skipping dependencies (current repo only mode)")
            if progress_callback:
                progress_callback(20, "📦 Skipping dependencies (current repo only mode)")
        
        if progress_callback:
            progress_callback(90, f"📤 Exporting current project...")
        
        # Phase 5: Export Current Repository 
        self._export_current_repository(progress_callback)
        
        if progress_callback:
            progress_callback(95, f"📝 Generating dynamic README...")
        
        # Phase 6: Generate Dynamic README
        self._generate_dynamic_readme()
        
        if progress_callback:
            progress_callback(100, f"🎉 Lexicon complete!")
        
        self._print_summary()
        return self.stats
    
    def _discover_dependencies(self) -> List[Dependency]:
        """🔍 Discover all project dependencies"""
        try:
            dependencies = discover_project_dependencies(str(self.project_path))
            
            # Log discovered dependencies
            for dep in dependencies:
                if dep.org_repo:
                    logger.debug(f"  📦 {dep.name} -> {dep.org_repo} ({dep.version or 'latest'})")
                else:
                    logger.debug(f"  📦 {dep.name} ({dep.version or 'latest'}) [PyPI only]")
            
            return dependencies
            
        except Exception as e:
            logger.error(f"❌ Failed to discover dependencies: {e}")
            return []
    
    def _check_registry(self, dependencies: List[Dependency]) -> tuple[List[Dependency], List[Dependency]]:
        """🌐 Check semantic-dna/registry for pre-built lexicons"""
        # TODO: Implement actual registry checking
        # For now, assume all deps need to be built locally
        
        logger.info("🚧 Registry checking not yet implemented - building all locally")
        available = []
        missing = [dep for dep in dependencies if dep.org_repo]  # Only GitHub deps for now
        
        return available, missing
    
    def _build_missing_dependencies(self, dependencies: List[Dependency], progress_callback=None):
        """🔧 Build repositories and graphs for missing dependencies"""
        total_deps = len(dependencies)
        
        for i, dep in enumerate(dependencies):
            if not dep.org_repo:
                logger.warning(f"⚠️  Skipping {dep.name} - no GitHub mapping available")
                continue
            
            try:
                if progress_callback:
                    progress_callback(
                        40 + (30 * i // total_deps), 
                        f"🔧 Building {dep.org_repo}..."
                    )
                
                # Ensure repository is downloaded
                logger.info(f"📥 Ensuring repo: {dep.org_repo}")
                self._ensure_repository(dep)
                
                # Ensure graphs are built  
                logger.info(f"🧬 Ensuring graphs: {dep.org_repo}")
                self._ensure_graphs(dep)
                
            except Exception as e:
                logger.error(f"❌ Failed to build {dep.org_repo}: {e}")
                continue
    
    def _ensure_repository(self, dep: Dependency):
        """📥 Ensure repository is downloaded with correct version"""
        try:
            # Check if repo already exists first
            existing_repos = self.manager.repo_list()
            if dep.org_repo in [repo.org_repo for repo in existing_repos]:
                # Repository exists, update it instead
                logger.debug(f"🔄 Updating existing repository: {dep.org_repo}")
                self.manager.repo_update(dep.org_repo)
            else:
                # Repository doesn't exist, add it
                logger.debug(f"📥 Adding new repository: {dep.org_repo}")
                self.manager.repo_add(dep.org_repo)
            logger.debug(f"✅ Repository ready: {dep.org_repo}")
        except Exception as e:
            logger.warning(f"⚠️  Repository issue for {dep.org_repo}: {e}")
    
    def _ensure_graphs(self, dep: Dependency):
        """🧬 Ensure semantic graphs are built"""
        try:
            # Check if graphs already exist first
            existing_graphs = self.manager.graph_list()
            graph_exists = any(
                graph.org_repo == dep.org_repo and (graph.version == "latest" or graph.version is None)
                for graph in existing_graphs
            )
            
            if graph_exists:
                # Graphs exist, update them instead  
                logger.debug(f"🔄 Updating existing graphs: {dep.org_repo}")
                self.manager.graph_update(dep.org_repo, "latest")
            else:
                # Graphs don't exist, add them
                logger.debug(f"🧬 Adding new graphs: {dep.org_repo}")
                self.manager.graph_add(dep.org_repo, "latest")
            logger.debug(f"✅ Graphs ready: {dep.org_repo}")
        except Exception as e:
            logger.warning(f"⚠️  Graph building issue for {dep.org_repo}: {e}")
    
    def _export_all_dependencies(self, dependencies: List[Dependency], progress_callback=None):
        """📤 Export semantic DNA for all dependencies"""
        # Ensure output directory exists
        self.llm_rlex_dir.mkdir(exist_ok=True)
        
        total_deps = len(dependencies)
        exported_count = 0
        
        for i, dep in enumerate(dependencies):
            if not dep.org_repo:
                continue
                
            try:
                if progress_callback:
                    progress_callback(
                        80 + (15 * i // total_deps),
                        f"📤 Exporting {dep.org_repo}..."
                    )
                
                # Export to msgpack using our custom output directory  
                output_file = self.manager.export_msgpack(
                    dep.org_repo, 
                    dep.version or "latest",
                    output=self.llm_rlex_dir
                )
                
                # Update stats
                if output_file.exists():
                    size_mb = output_file.stat().st_size / (1024 * 1024)
                    self.stats.total_size_mb += size_mb
                    exported_count += 1
                    
                    logger.debug(f"✅ Exported {dep.org_repo} ({size_mb:.1f}MB)")
                
            except Exception as e:
                logger.error(f"❌ Failed to export {dep.org_repo}: {e}")
                continue
        
        logger.info(f"📤 Successfully exported {exported_count}/{len(dependencies)} dependencies")
    
    def _export_current_repository(self, progress_callback=None):
        """📤 Export the current repository as semantic DNA"""
        try:
            # First, we need to determine the current repo's org/repo from git origin
            import subprocess
            
            # Try to get git remote origin URL
            try:
                git_result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if git_result.returncode == 0:
                    origin_url = git_result.stdout.strip()
                    # Parse org/repo from URL (handle both SSH and HTTPS)
                    if "github.com" in origin_url:
                        if origin_url.startswith("git@"):
                            # SSH format: git@github.com:pixeltable/pixeltable.git
                            org_repo = origin_url.split(":")[-1].replace(".git", "")
                        else:
                            # HTTPS format: https://github.com/pixeltable/pixeltable.git
                            parts = origin_url.split("/")
                            if len(parts) >= 2:
                                org_repo = f"{parts[-2]}/{parts[-1].replace('.git', '')}"
                            else:
                                raise ValueError("Could not parse org/repo from URL")
                        
                        logger.info(f"🏠 Exporting current repository: {org_repo}")
                        
                        # Ensure current repo is added and has graphs
                        self._ensure_repository_from_path(org_repo)
                        self._ensure_graphs_from_path(org_repo)
                        
                        # Export as current repo (gets all functions, not just public)
                        output_file = self.manager.export_msgpack(
                            org_repo,
                            "latest", 
                            output=self.llm_rlex_dir,
                            is_current_repo=True  # This enables full function export
                        )
                        
                        if output_file.exists():
                            size_mb = output_file.stat().st_size / (1024 * 1024)
                            self.stats.total_size_mb += size_mb
                            logger.info(f"✅ Exported current repo {org_repo} ({size_mb:.1f}MB)")
                        
                    else:
                        logger.warning("⚠️  Not a GitHub repository - skipping current repo export")
                else:
                    logger.warning("⚠️  Not a git repository - skipping current repo export")
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                logger.warning(f"⚠️  Git command failed: {e} - skipping current repo export")
                
        except Exception as e:
            logger.error(f"❌ Failed to export current repository: {e}")
    
    def _ensure_repository_from_path(self, org_repo: str):
        """📥 Ensure repository is available, add from local path if needed"""
        try:
            # Check if repo already exists first
            existing_repos = self.manager.repo_list()
            if org_repo in [repo.org_repo for repo in existing_repos]:
                # Repository exists, update it instead
                logger.debug(f"🔄 Updating existing repository: {org_repo}")
                self.manager.repo_update(org_repo)
            else:
                # Repository doesn't exist, add it
                logger.debug(f"📥 Adding new repository: {org_repo}")
                self.manager.repo_add(org_repo)
        except Exception as e:
            logger.warning(f"⚠️  Repository setup issue for {org_repo}: {e}")
    
    def _ensure_graphs_from_path(self, org_repo: str):
        """🧬 Ensure semantic graphs are built from local path"""
        try:
            # Check if graphs already exist first
            existing_graphs = self.manager.graph_list()
            graph_exists = any(
                graph.org_repo == org_repo and (graph.version == "latest" or graph.version is None)
                for graph in existing_graphs
            )
            
            if graph_exists:
                # Graphs exist, update them instead  
                logger.debug(f"🔄 Updating existing graphs: {org_repo}")
                self.manager.graph_update(org_repo, "latest")
            else:
                # Graphs don't exist, add them
                logger.debug(f"🧬 Adding new graphs: {org_repo}")
                self.manager.graph_add(org_repo, "latest")
        except Exception as e:
            logger.warning(f"⚠️  Graph building issue for current repo {org_repo}: {e}")
    
    def _generate_dynamic_readme(self):
        """📝 Generate dynamic README with actual file inventory"""
        try:
            # Scan for all msgpack files
            msgpack_files = list(self.llm_rlex_dir.glob("*.msgpack"))
            if not msgpack_files:
                logger.warning("⚠️  No msgpack files found for README generation")
                return
            
            # Analyze files by size and category
            main_repo_files = []
            dependency_files = []
            total_size = 0
            
            for file_path in msgpack_files:
                size_bytes = file_path.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
                size_kb = size_bytes / 1024
                total_size += size_mb
                
                # Determine if it's main repo or dependency
                file_name = file_path.name
                
                # Check if it matches current project pattern
                try:
                    git_result = subprocess.run(
                        ["git", "remote", "get-url", "origin"],
                        cwd=self.project_path,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if git_result.returncode == 0:
                        origin_url = git_result.stdout.strip()
                        if "github.com" in origin_url:
                            # Extract org/repo from origin
                            if origin_url.startswith("git@"):
                                repo_part = origin_url.split(":")[-1].replace(".git", "")
                            else:
                                parts = origin_url.split("/")
                                repo_part = f"{parts[-2]}/{parts[-1].replace('.git', '')}"
                            
                            expected_prefix = repo_part.replace("/", "~")
                            if file_name.startswith(expected_prefix):
                                main_repo_files.append((file_path, size_mb, size_kb))
                                continue
                except:
                    pass
                
                # If not main repo, it's a dependency
                dependency_files.append((file_path, size_mb, size_kb))
            
            # Sort by size (largest first)
            dependency_files.sort(key=lambda x: x[1], reverse=True)
            
            # Generate README content
            readme_content = self._create_readme_content(
                main_repo_files, dependency_files, total_size, len(msgpack_files)
            )
            
            # Write README
            readme_path = self.llm_rlex_dir / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            logger.info(f"📝 Generated dynamic README with {len(msgpack_files)} files ({total_size:.1f}MB)")
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to generate dynamic README: {e}")
    
    def _create_readme_content(self, main_repo_files, dependency_files, total_size_mb, total_files):
        """📝 Create the actual README content"""
        content = """# 🧬 LLM-Optimized Repository Intelligence

## FOR LLMS: 
**Use your jq tool to query these .msgpack files for complete repository understanding!**

### Quick Start for LLMs:
```bash
# First, convert msgpack to JSON for jq (msgpack files are binary)
python3 -c "import msgpack, json, sys; print(json.dumps(msgpack.unpack(open(sys.argv[1], 'rb'))))" FILENAME.msgpack | jq '.'

# List all functions from any file
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('pixeltable~pixeltable~latest.msgpack', 'rb'))))" | jq '.functions[].n'

# Get function signatures
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('numpy~numpy~latest.msgpack', 'rb'))))" | jq '.functions[] | {name: .n, signature: .s, module: .m}'

# Search specific functions across any library
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('pandas-dev~pandas~latest.msgpack', 'rb'))))" | jq '.functions[] | select(.n | contains("create"))'

# Get semantic patterns
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('sqlalchemy~sqlalchemy~latest.msgpack', 'rb'))))" | jq '.patterns[]'
```

## Files Generated by Repolex v2.0

Each `.msgpack` file contains the semantic DNA of a repository:
- **Functions**: All functions with signatures and metadata
- **Modules**: Code organization and hierarchy  
- **Patterns**: Common usage patterns for better code generation
- **Semantic Clusters**: Related function groups
- **String Table**: Compressed deduplication for minimal size

## PAC-MAN Tiered Loading Strategy 🟡

**Nibble** → **Pellet** → **Power Pellet**

1. **Nibble (jq queries)**: Quick function lookups and searches
2. **Pellet (single repo)**: Load one .msgpack for focused understanding  
3. **Power Pellet (full context)**: Load all .msgpack files for complete project intelligence

**Perfect for LLM context injection - everything you need, nothing you don't!** 

## Current Repository Intelligence

"""

        # Add main repository section
        if main_repo_files:
            content += "**🎯 MAIN REPOSITORY:**\n"
            for file_path, size_mb, size_kb in main_repo_files:
                if size_mb >= 1:
                    size_str = f"({size_mb:.1f}MB)"
                else:
                    size_str = f"({size_kb:.0f}KB)"
                content += f"- **{file_path.name}** {size_str} - Main repository (all access levels)\n"
            content += "\n"

        # Add major dependencies
        if dependency_files:
            content += f"**🔥 DEPENDENCIES ({total_size_mb:.1f}MB Total Semantic DNA):**\n"
            
            # Show top dependencies (>100KB)
            major_deps = [(f, sm, sk) for f, sm, sk in dependency_files if sk > 100]
            for file_path, size_mb, size_kb in major_deps[:10]:  # Top 10
                if size_mb >= 1:
                    size_str = f"({size_mb:.1f}MB)"
                else:
                    size_str = f"({size_kb:.0f}KB)"
                    
                # Add description based on package name
                desc = self._get_package_description(file_path.name)
                content += f"- **{file_path.name}** {size_str} - {desc}\n"
            
            # Show smaller libraries
            minor_deps = [(f, sm, sk) for f, sm, sk in dependency_files if sk <= 100]
            if minor_deps:
                content += f"\n**📦 ADDITIONAL LIBRARIES:**\n"
                for file_path, size_mb, size_kb in minor_deps:
                    if size_mb >= 1:
                        size_str = f"({size_mb:.1f}MB)"
                    else:
                        size_str = f"({size_kb:.0f}KB)"
                    desc = self._get_package_description(file_path.name)
                    content += f"- **{file_path.name}** {size_str} - {desc}\n"

        content += f"\n**Total: {total_files} semantic DNA files representing a complete Python ecosystem!**\n"

        # Add usage examples
        content += """
## Usage Examples

```bash
# Convert any msgpack to JSON first (they're binary files)
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('FILE.msgpack', 'rb'))))" | jq '.'

# Get all table-related functions from pandas
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('pandas-dev~pandas~latest.msgpack', 'rb'))))" | jq '.functions[] | select(.n | contains("table") or .n | contains("Table"))'

# Find data processing functions in numpy  
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('numpy~numpy~latest.msgpack', 'rb'))))" | jq '.functions[] | select(.n | test("^(array|matrix|reshape)"))'

# Get module overview from any library
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('sqlalchemy~sqlalchemy~latest.msgpack', 'rb'))))" | jq '.modules | keys'

# Cross-library function search
for file in *.msgpack; do echo "=== $file ==="; python3 -c "import msgpack, json, sys; print(json.dumps(msgpack.unpack(open(sys.argv[1], 'rb'))))" "$file" | jq '.functions[] | select(.n | contains("create"))' | head -3; done
```

---
*Generated by repolex v2.0 - The semantic intelligence system*  
*🧬 Semantic DNA optimized for LLM consumption*
"""

        return content
    
    def _get_package_description(self, filename):
        """📝 Get friendly description for package"""
        descriptions = {
            'pandas-dev~pandas~latest.msgpack': 'Data analysis powerhouse',
            'numpy~numpy~latest.msgpack': 'Numerical computing foundation',
            'pydantic~pydantic~latest.msgpack': 'Data validation framework',
            'apache~arrow~latest.msgpack': 'Columnar data format',
            'python-pillow~Pillow~latest.msgpack': 'Image processing library',
            'sqlalchemy~sqlalchemy~latest.msgpack': 'Database ORM',
            'pymupdf~pymupdf~latest.msgpack': 'PDF processing',
            'encode~httpx~latest.msgpack': 'HTTP client',
            'encode~httpcore~latest.msgpack': 'HTTP transport layer',
            'psf~requests~latest.msgpack': 'HTTP library',
            'giampaolo~psutil~latest.msgpack': 'System monitoring',
            'lxml~lxml~latest.msgpack': 'XML/HTML processing',
            'pallets~jinja~latest.msgpack': 'Template engine',
            'PyAV-Org~PyAV~latest.msgpack': 'Audio/video processing',
            'tqdm~tqdm~latest.msgpack': 'Progress bars',
            'jmespath~jmespath.py~latest.msgpack': 'JSON query language',
        }
        return descriptions.get(filename, 'Specialized library')
    
    def _print_summary(self):
        """🎉 Print completion summary"""
        logger.info("\n" + "="*60)
        logger.info("🎉 LEXIFY COMPLETE!")
        logger.info("="*60)
        logger.info(f"📦 Total dependencies: {self.stats.total_dependencies}")
        logger.info(f"⚡ From registry: {self.stats.from_registry}")
        logger.info(f"🔧 Built locally: {self.stats.built_locally}")
        logger.info(f"💾 Total size: {self.stats.total_size_mb:.1f}MB")
        logger.info(f"📁 Output: {self.llm_rlex_dir}")
        logger.info("\n🧬 Your semantic DNA lexicon is ready for LLM consumption!")
        logger.info("   Use PAC-MAN mode: load all .msgpack files for full power!")


def lexify_project(project_path: str = ".", output_path: str = ".", include_dependencies: bool = False, progress_callback=None) -> LexifyStats:
    """🚀 Convenience function to lexify a project"""
    orchestrator = LexifyOrchestrator(project_path, output_path, include_dependencies)
    return orchestrator.lexify(progress_callback)