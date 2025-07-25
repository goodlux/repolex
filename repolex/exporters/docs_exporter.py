"""
🟡 PAC-MAN's Documentation Export Powerhouse! 🟡

Transforms semantic intelligence into beautiful documentation formats.
PAC-MAN chomps through semantic data and produces perfect docs in:
- MDX format (for Mintlify/Docusaurus)
- HTML format (standalone documentation)
- Markdown format (GitHub-style docs)

WAKA WAKA! Let's generate some documentation!
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import json
from datetime import datetime

from ..models.exceptions import ExportError, ValidationError
from ..models.results import ExportResult, ProgressInfo
from ..models.function import FunctionInfo
from ..storage.oxigraph_client import OxigraphClient
from ..utils.validation import validate_org_repo, validate_release_tag
from .base_exporter import BaseExporter


class DocumentationExporter(BaseExporter):
    """
    🟡 PAC-MAN's Documentation Export Powerhouse! 🟡
    
    Chomps semantic data and generates beautiful documentation in multiple formats.
    Each format is optimized for different use cases:
    - MDX: Perfect for Mintlify, Docusaurus, and modern doc platforms
    - HTML: Self-contained documentation with styling
    - Markdown: GitHub-compatible documentation
    
    The PAC-MAN way: Eat semantic dots, produce documentation gold!
    """
    
    def __init__(self, oxigraph_client: OxigraphClient):
        super().__init__(oxigraph_client)
        self.templates = self._load_templates()
        
    def export_docs(
        self,
        org_repo: str,
        release: str,
        format: str,
        output_dir: Path,
        template: Optional[str] = None,
        progress_callback: Optional[callable] = None
    ) -> ExportResult:
        """
        🟡 PAC-MAN's main documentation export function!
        
        Chomps through semantic data and produces documentation in the specified format.
        
        Args:
            org_repo: Repository in 'org/repo' format
            release: Release tag to export
            format: Documentation format ('mdx', 'html', 'markdown')
            output_dir: Directory to write documentation files
            template: Template name (optional, uses default for format)
            progress_callback: Progress updates (PAC-MAN style!)
            
        Returns:
            ExportResult with paths and statistics
        """
        validate_org_repo(org_repo)
        validate_release_tag(release)
        
        if format not in ['mdx', 'html', 'markdown']:
            raise ValidationError(
                f"Unsupported format: {format}",
                suggestions=["Use: 'mdx', 'html', or 'markdown'"]
            )
        
        start_time = datetime.now()
        if progress_callback:
            progress_callback(ProgressInfo(
                step="initialization",
                message="🟡 PAC-MAN starting documentation export...",
                progress=0.0
            ))
        
        try:
            # Step 1: Chomp semantic data from Oxigraph
            if progress_callback:
                progress_callback(ProgressInfo(
                    step="data_extraction",
                    message="🍎 Chomping semantic data from the maze...",
                    progress=0.1
                ))
                
            functions = self._extract_functions(org_repo, release)
            modules = self._extract_modules(org_repo, release)
            repository_info = self._extract_repository_info(org_repo, release)
            
            # Step 2: Organize documentation structure
            if progress_callback:
                progress_callback(ProgressInfo(
                    step="organization",
                    message="🏗️ Building documentation maze structure...",
                    progress=0.3
                ))
                
            doc_structure = self._organize_documentation(functions, modules)
            
            # Step 3: Generate documentation files
            if progress_callback:
                progress_callback(ProgressInfo(
                    step="generation",
                    message=f"📝 Generating {format.upper()} documentation...",
                    progress=0.5
                ))
                
            output_dir.mkdir(parents=True, exist_ok=True)
            generated_files = []
            
            if format == 'mdx':
                generated_files = self._generate_mdx_docs(
                    doc_structure, output_dir, template, progress_callback
                )
            elif format == 'html':
                generated_files = self._generate_html_docs(
                    doc_structure, output_dir, template, progress_callback
                )
            elif format == 'markdown':
                generated_files = self._generate_markdown_docs(
                    doc_structure, output_dir, template, progress_callback
                )
            
            # Step 4: Generate index and navigation
            if progress_callback:
                progress_callback(ProgressInfo(
                    step="navigation",
                    message="🗺️ Creating navigation maze...",
                    progress=0.8
                ))
                
            index_file = self._generate_index_file(
                doc_structure, output_dir, format, repository_info
            )
            generated_files.append(index_file)
            
            # Step 5: Copy assets and finish
            if progress_callback:
                progress_callback(ProgressInfo(
                    step="assets",
                    message="🎨 Adding PAC-MAN styling...",
                    progress=0.9
                ))
                
            self._copy_assets(output_dir, format, template)
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            if progress_callback:
                progress_callback(ProgressInfo(
                    step="complete",
                    message="🟡 WAKA WAKA! Documentation generation complete!",
                    progress=1.0
                ))
            
            return ExportResult(
                success=True,
                output_path=output_dir,
                format=format,
                files_generated=len(generated_files),
                functions_documented=len(functions),
                processing_time=processing_time,
                file_paths=generated_files,
                metadata={
                    'org_repo': org_repo,
                    'release': release,
                    'template': template or f"default_{format}",
                    'total_functions': len(functions),
                    'total_modules': len(modules)
                }
            )
            
        except Exception as e:
            raise ExportError(
                f"Documentation export failed: {str(e)}",
                suggestions=[
                    "Check that semantic graphs exist for this repository/release",
                    "Verify output directory is writable",
                    "Ensure format is supported"
                ]
            )
    
    def _extract_functions(self, org_repo: str, release: str) -> List[FunctionInfo]:
        """🍎 Extract function data from semantic graphs"""
        org, repo = org_repo.split('/')
        
        query = f"""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?function ?name ?signature ?docstring ?file_path ?start_line ?end_line WHERE {{
            GRAPH <http://Repolex.org/repo/{org}/{repo}/functions/implementations> {{
                ?function woc:belongsToVersion "{release}" ;
                         woc:hasSignature ?signature ;
                         woc:definedInFile ?file_path ;
                         woc:startLine ?start_line ;
                         woc:endLine ?end_line .
                OPTIONAL {{ ?function rdfs:comment ?docstring }}
            }}
            GRAPH <http://Repolex.org/repo/{org}/{repo}/functions/stable> {{
                ?stable_function woc:canonicalName ?name .
                ?function woc:implementsFunction ?stable_function .
            }}
        }}
        ORDER BY ?name
        """
        
        results = self.oxigraph_client.query_sparql(query)
        functions = []
        
        for result in results:
            # Parse docstring for structured information
            docstring_info = self._parse_docstring(result.get('docstring', ''))
            
            function = FunctionInfo(
                name=result['name'],
                signature=result['signature'],
                docstring=result.get('docstring', ''),
                file_path=result['file_path'],
                start_line=int(result['start_line']),
                end_line=int(result['end_line']),
                parameters=docstring_info.get('parameters', []),
                returns=docstring_info.get('returns', ''),
                examples=docstring_info.get('examples', []),
                raises=docstring_info.get('raises', []),
                github_url=self._generate_github_url(org_repo, release, result['file_path'], 
                                                   int(result['start_line']), int(result['end_line']))
            )
            functions.append(function)
        
        return functions
        
    def _extract_modules(self, org_repo: str, release: str) -> List[Dict[str, Any]]:
        """🏗️ Extract module structure from semantic graphs"""
        # This would extract module hierarchy information
        # For now, we'll organize by file path
        org, repo = org_repo.split('/')
        
        query = f"""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        
        SELECT DISTINCT ?file_path WHERE {{
            GRAPH <http://Repolex.org/repo/{org}/{repo}/functions/implementations> {{
                ?function woc:belongsToVersion "{release}" ;
                         woc:definedInFile ?file_path .
            }}
        }}
        ORDER BY ?file_path
        """
        
        results = self.oxigraph_client.query_sparql(query)
        
        modules = []
        for result in results:
            file_path = result['file_path']
            module_name = file_path.replace('/', '.').replace('.py', '')
            
            modules.append({
                'name': module_name,
                'file_path': file_path,
                'category': self._categorize_module(file_path)
            })
        
        return modules
    
    def _extract_repository_info(self, org_repo: str, release: str) -> Dict[str, Any]:
        """📊 Extract repository metadata"""
        return {
            'name': org_repo,
            'release': release,
            'generated_at': datetime.now().isoformat(),
            'generator': 'PAC-MAN Documentation Powerhouse 🟡'
        }
    
    def _organize_documentation(self, functions: List[FunctionInfo], modules: List[Dict]) -> Dict[str, Any]:
        """🗂️ Organize functions into documentation structure"""
        
        # Group functions by category
        categories = {
            'Core API': [],
            'Data Operations': [],
            'Utilities': [],
            'Advanced': []
        }
        
        for function in functions:
            category = self._categorize_function(function)
            categories[category].append(function)
        
        # Sort functions within each category
        for category in categories:
            categories[category].sort(key=lambda f: f.name)
        
        return {
            'categories': categories,
            'all_functions': functions,
            'modules': modules,
            'function_count': len(functions)
        }
    
    def _generate_mdx_docs(
        self, 
        doc_structure: Dict[str, Any], 
        output_dir: Path, 
        template: Optional[str],
        progress_callback: Optional[callable]
    ) -> List[Path]:
        """📝 Generate MDX documentation files (PAC-MAN style!)"""
        
        generated_files = []
        categories = doc_structure['categories']
        
        for category, functions in categories.items():
            if not functions:
                continue
                
            category_dir = output_dir / category.lower().replace(' ', '_')
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate individual function files
            for i, function in enumerate(functions):
                if progress_callback:
                    progress = 0.5 + (0.3 * i / len(functions))
                    progress_callback(ProgressInfo(
                        step="mdx_generation",
                        message=f"🟡 Documenting {function.name}...",
                        progress=progress
                    ))
                
                file_path = category_dir / f"{function.name}.mdx"
                mdx_content = self._generate_function_mdx(function, template)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(mdx_content)
                
                generated_files.append(file_path)
        
        return generated_files
    
    def _generate_html_docs(
        self, 
        doc_structure: Dict[str, Any], 
        output_dir: Path, 
        template: Optional[str],
        progress_callback: Optional[callable]
    ) -> List[Path]:
        """🌐 Generate HTML documentation files"""
        
        generated_files = []
        categories = doc_structure['categories']
        
        # Generate CSS file
        css_file = output_dir / "pacman-docs.css"
        with open(css_file, 'w') as f:
            f.write(self._get_pacman_css())
        generated_files.append(css_file)
        
        for category, functions in categories.items():
            if not functions:
                continue
                
            category_dir = output_dir / category.lower().replace(' ', '_')
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate individual function files
            for i, function in enumerate(functions):
                if progress_callback:
                    progress = 0.5 + (0.3 * i / len(functions))
                    progress_callback(ProgressInfo(
                        step="html_generation",
                        message=f"🌐 Creating HTML for {function.name}...",
                        progress=progress
                    ))
                
                file_path = category_dir / f"{function.name}.html"
                html_content = self._generate_function_html(function, template)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                generated_files.append(file_path)
        
        return generated_files
    
    def _generate_markdown_docs(
        self, 
        doc_structure: Dict[str, Any], 
        output_dir: Path, 
        template: Optional[str],
        progress_callback: Optional[callable]
    ) -> List[Path]:
        """📖 Generate Markdown documentation files"""
        
        generated_files = []
        categories = doc_structure['categories']
        
        for category, functions in categories.items():
            if not functions:
                continue
                
            category_dir = output_dir / category.lower().replace(' ', '_')
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate individual function files
            for i, function in enumerate(functions):
                if progress_callback:
                    progress = 0.5 + (0.3 * i / len(functions))
                    progress_callback(ProgressInfo(
                        step="markdown_generation",
                        message=f"📖 Writing Markdown for {function.name}...",
                        progress=progress
                    ))
                
                file_path = category_dir / f"{function.name}.md"
                markdown_content = self._generate_function_markdown(function, template)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                generated_files.append(file_path)
        
        return generated_files
    
    def _generate_function_mdx(self, function: FunctionInfo, template: Optional[str]) -> str:
        """🟡 Generate MDX content for a single function (PAC-MAN style!)"""
        
        # Determine badge color based on function type
        badge_info = self._get_function_badge(function)
        
        mdx_content = f'''---
title: "pxt.{function.name}"
description: "{function.signature} - {self._get_brief_description(function.docstring)}"
---

<Badge text="{badge_info['text']}" color="{badge_info['color']}" size="small" />

## Function Signature

```python
{function.signature}
```

## Description

{self._format_description(function.docstring)}

'''
        
        # Add parameters section
        if function.parameters:
            mdx_content += "## Parameters\n\n"
            for param in function.parameters:
                param_type = param.get('type', 'Any')
                param_default = param.get('default')
                param_required = param.get('required', True)
                
                mdx_content += f'<ParamField path="{param["name"]}" type="{param_type}"'
                if not param_required:
                    mdx_content += f' default="{param_default}"'
                else:
                    mdx_content += ' required'
                mdx_content += f'>\n  {param.get("description", "Parameter description")}\n</ParamField>\n\n'
        
        # Add returns section
        if function.returns:
            mdx_content += "## Returns\n\n"
            mdx_content += f'<ResponseField name="return_value" type="{function.returns}">\n'
            mdx_content += f'  {function.returns}\n'
            mdx_content += '</ResponseField>\n\n'
        
        # Add examples section
        if function.examples:
            mdx_content += "## Examples\n\n"
            for i, example in enumerate(function.examples):
                mdx_content += f"### Example {i + 1}\n\n"
                mdx_content += f"```python\n{example}\n```\n\n"
        
        # Add GitHub link
        if function.github_url:
            mdx_content += f"## Source Code\n\n"
            mdx_content += f"[View source on GitHub]({function.github_url}) 🟡\n\n"
        
        # Add footer
        mdx_content += f"---\n\n"
        mdx_content += f"*Generated by PAC-MAN Documentation Powerhouse 🟡*\n"
        
        return mdx_content
    
    def _generate_function_html(self, function: FunctionInfo, template: Optional[str]) -> str:
        """🌐 Generate HTML content for a single function"""
        
        badge_info = self._get_function_badge(function)
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{function.name} - PAC-MAN Documentation</title>
    <link rel="stylesheet" href="../pacman-docs.css">
</head>
<body>
    <div class="pac-man-container">
        <header class="pac-man-header">
            <h1>🟡 {function.name}</h1>
            <span class="badge badge-{badge_info['color']}">{badge_info['text']}</span>
        </header>
        
        <section class="function-signature">
            <h2>Function Signature</h2>
            <pre><code class="python">{function.signature}</code></pre>
        </section>
        
        <section class="description">
            <h2>Description</h2>
            <p>{self._format_description(function.docstring)}</p>
        </section>
'''
        
        # Add parameters
        if function.parameters:
            html_content += '''
        <section class="parameters">
            <h2>Parameters</h2>
            <div class="param-list">
'''
            for param in function.parameters:
                param_type = param.get('type', 'Any')
                param_required = param.get('required', True)
                required_class = 'required' if param_required else 'optional'
                
                html_content += f'''
                <div class="param-item {required_class}">
                    <h3>{param["name"]} <span class="param-type">({param_type})</span></h3>
                    <p>{param.get("description", "Parameter description")}</p>
                </div>
'''
            html_content += '            </div>\n        </section>\n'
        
        # Add examples
        if function.examples:
            html_content += '''
        <section class="examples">
            <h2>Examples</h2>
'''
            for i, example in enumerate(function.examples):
                html_content += f'''
            <div class="example">
                <h3>Example {i + 1}</h3>
                <pre><code class="python">{example}</code></pre>
            </div>
'''
            html_content += '        </section>\n'
        
        # Add GitHub link
        if function.github_url:
            html_content += f'''
        <section class="source-link">
            <h2>Source Code</h2>
            <p><a href="{function.github_url}" target="_blank">View source on GitHub 🟡</a></p>
        </section>
'''
        
        html_content += '''
        <footer class="pac-man-footer">
            <p><em>Generated by PAC-MAN Documentation Powerhouse 🟡</em></p>
        </footer>
    </div>
</body>
</html>'''
        
        return html_content
    
    def _generate_function_markdown(self, function: FunctionInfo, template: Optional[str]) -> str:
        """📖 Generate Markdown content for a single function"""
        
        badge_info = self._get_function_badge(function)
        
        markdown_content = f'''# {function.name} 🟡

**{badge_info['text']}**

## Function Signature

```python
{function.signature}
```

## Description

{self._format_description(function.docstring)}

'''
        
        # Add parameters
        if function.parameters:
            markdown_content += "## Parameters\n\n"
            for param in function.parameters:
                param_type = param.get('type', 'Any')
                param_required = " (required)" if param.get('required', True) else " (optional)"
                
                markdown_content += f"### `{param['name']}` ({param_type}){param_required}\n\n"
                markdown_content += f"{param.get('description', 'Parameter description')}\n\n"
        
        # Add returns
        if function.returns:
            markdown_content += f"## Returns\n\n**{function.returns}**\n\n"
        
        # Add examples
        if function.examples:
            markdown_content += "## Examples\n\n"
            for i, example in enumerate(function.examples):
                markdown_content += f"### Example {i + 1}\n\n"
                markdown_content += f"```python\n{example}\n```\n\n"
        
        # Add GitHub link
        if function.github_url:
            markdown_content += f"## Source Code\n\n"
            markdown_content += f"[View source on GitHub]({function.github_url}) 🟡\n\n"
        
        # Add footer
        markdown_content += "---\n\n"
        markdown_content += "*Generated by PAC-MAN Documentation Powerhouse 🟡*\n"
        
        return markdown_content
    
    def _generate_index_file(
        self, 
        doc_structure: Dict[str, Any], 
        output_dir: Path, 
        format: str,
        repository_info: Dict[str, Any]
    ) -> Path:
        """🗺️ Generate index/navigation file"""
        
        if format == 'mdx':
            index_file = output_dir / "index.mdx"
            content = self._generate_mdx_index(doc_structure, repository_info)
        elif format == 'html':
            index_file = output_dir / "index.html"
            content = self._generate_html_index(doc_structure, repository_info)
        else:  # markdown
            index_file = output_dir / "README.md"
            content = self._generate_markdown_index(doc_structure, repository_info)
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return index_file
    
    def _generate_mdx_index(self, doc_structure: Dict[str, Any], repo_info: Dict[str, Any]) -> str:
        """🗺️ Generate MDX index page"""
        
        content = f'''---
title: "{repo_info['name']} API Documentation"
description: "Complete API reference for {repo_info['name']} {repo_info['release']}"
---

# 🟡 {repo_info['name']} API Documentation

**Generated by PAC-MAN Documentation Powerhouse**

Version: `{repo_info['release']}`  
Generated: {datetime.fromisoformat(repo_info['generated_at']).strftime('%Y-%m-%d %H:%M:%S')}  
Total Functions: {doc_structure['function_count']}

## 📚 Function Categories

'''
        
        for category, functions in doc_structure['categories'].items():
            if functions:
                content += f"### {category} ({len(functions)} functions)\n\n"
                for function in functions[:10]:  # Show first 10
                    content += f"- [{function.name}](./{category.lower().replace(' ', '_')}/{function.name})\n"
                if len(functions) > 10:
                    content += f"- ... and {len(functions) - 10} more\n"
                content += "\n"
        
        content += "---\n\n*WAKA WAKA! All your functions are documented! 🟡*\n"
        
        return content
    
    def _generate_html_index(self, doc_structure: Dict[str, Any], repo_info: Dict[str, Any]) -> str:
        """🗺️ Generate HTML index page"""
        
        content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{repo_info['name']} API Documentation - PAC-MAN</title>
    <link rel="stylesheet" href="pacman-docs.css">
</head>
<body>
    <div class="pac-man-container">
        <header class="pac-man-header">
            <h1>🟡 {repo_info['name']} API Documentation</h1>
            <p class="subtitle">Generated by PAC-MAN Documentation Powerhouse</p>
            <div class="repo-info">
                <span class="version">Version: {repo_info['release']}</span>
                <span class="generated">Generated: {datetime.fromisoformat(repo_info['generated_at']).strftime('%Y-%m-%d %H:%M:%S')}</span>
                <span class="count">Total Functions: {doc_structure['function_count']}</span>
            </div>
        </header>
        
        <nav class="function-categories">
            <h2>📚 Function Categories</h2>
'''
        
        for category, functions in doc_structure['categories'].items():
            if functions:
                category_slug = category.lower().replace(' ', '_')
                content += f'''
            <div class="category">
                <h3>{category} ({len(functions)} functions)</h3>
                <ul class="function-list">
'''
                for function in functions[:10]:
                    content += f'                    <li><a href="./{category_slug}/{function.name}.html">{function.name}</a></li>\n'
                if len(functions) > 10:
                    content += f'                    <li><em>... and {len(functions) - 10} more</em></li>\n'
                content += '                </ul>\n            </div>\n'
        
        content += '''
        </nav>
        
        <footer class="pac-man-footer">
            <p><em>WAKA WAKA! All your functions are documented! 🟡</em></p>
        </footer>
    </div>
</body>
</html>'''
        
        return content
    
    def _generate_markdown_index(self, doc_structure: Dict[str, Any], repo_info: Dict[str, Any]) -> str:
        """🗺️ Generate Markdown index page"""
        
        content = f'''# 🟡 {repo_info['name']} API Documentation

**Generated by PAC-MAN Documentation Powerhouse**

- **Version:** `{repo_info['release']}`
- **Generated:** {datetime.fromisoformat(repo_info['generated_at']).strftime('%Y-%m-%d %H:%M:%S')}
- **Total Functions:** {doc_structure['function_count']}

## 📚 Function Categories

'''
        
        for category, functions in doc_structure['categories'].items():
            if functions:
                category_slug = category.lower().replace(' ', '_')
                content += f"### {category} ({len(functions)} functions)\n\n"
                for function in functions[:10]:
                    content += f"- [{function.name}](./{category_slug}/{function.name}.md)\n"
                if len(functions) > 10:
                    content += f"- ... and {len(functions) - 10} more\n"
                content += "\n"
        
        content += "---\n\n*WAKA WAKA! All your functions are documented! 🟡*\n"
        
        return content
    
    def _copy_assets(self, output_dir: Path, format: str, template: Optional[str]):
        """🎨 Copy CSS and other assets"""
        if format == 'html':
            # CSS is already generated in _generate_html_docs
            pass
    
    def _get_pacman_css(self) -> str:
        """🎨 PAC-MAN themed CSS for HTML documentation"""
        return '''
/* 🟡 PAC-MAN Documentation CSS 🟡 */

:root {
    --pac-yellow: #FFFF00;
    --pac-blue: #0000FF;
    --ghost-red: #FF0000;
    --ghost-pink: #FFB8FF;
    --ghost-cyan: #00FFFF;
    --ghost-orange: #FFBFFF;
    --maze-bg: #000000;
    --text-white: #FFFFFF;
    --dot-color: #FFFF8D;
}

body {
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    background-color: var(--maze-bg);
    color: var(--text-white);
    margin: 0;
    padding: 20px;
    line-height: 1.6;
}

.pac-man-container {
    max-width: 1200px;
    margin: 0 auto;
    background: linear-gradient(135deg, #001122 0%, #000044 100%);
    border: 3px solid var(--pac-yellow);
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 0 20px var(--pac-yellow);
}

.pac-man-header {
    text-align: center;
    margin-bottom: 40px;
    border-bottom: 2px solid var(--pac-yellow);
    padding-bottom: 20px;
}

.pac-man-header h1 {
    color: var(--pac-yellow);
    font-size: 2.5em;
    margin: 0;
    text-shadow: 0 0 10px var(--pac-yellow);
}

.subtitle {
    color: var(--dot-color);
    font-size: 1.2em;
    margin: 10px 0;
}

.repo-info {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 15px;
}

.repo-info span {
    background: var(--pac-blue);
    color: var(--text-white);
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.9em;
}

.badge {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: bold;
    text-transform: uppercase;
}

.badge-blue { background-color: var(--pac-blue); color: white; }
.badge-green { background-color: #00AA00; color: white; }
.badge-red { background-color: var(--ghost-red); color: white; }
.badge-purple { background-color: #AA00AA; color: white; }
.badge-orange { background-color: var(--ghost-orange); color: black; }

.function-signature {
    background: #002244;
    border: 2px solid var(--pac-blue);
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.function-signature pre {
    margin: 0;
    color: var(--pac-yellow);
    font-size: 1.1em;
    overflow-x: auto;
}

.description {
    margin: 20px 0;
    font-size: 1.1em;
    line-height: 1.7;
}

.parameters {
    margin: 30px 0;
}

.param-list {
    display: grid;
    gap: 15px;
}

.param-item {
    background: #001133;
    border-left: 4px solid var(--pac-yellow);
    padding: 15px;
    border-radius: 5px;
}

.param-item.required {
    border-left-color: var(--ghost-red);
}

.param-item.optional {
    border-left-color: var(--pac-blue);
}

.param-item h3 {
    margin: 0 0 10px 0;
    color: var(--pac-yellow);
}

.param-type {
    color: var(--dot-color);
    font-weight: normal;
    font-size: 0.9em;
}

.examples {
    margin: 30px 0;
}

.example {
    margin: 20px 0;
    background: #002200;
    border: 2px solid #00AA00;
    border-radius: 8px;
    padding: 20px;
}

.example h3 {
    color: #00FF00;
    margin-top: 0;
}

.example pre {
    background: #001100;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    color: #00FF88;
}

.source-link {
    margin: 30px 0;
    text-align: center;
}

.source-link a {
    color: var(--pac-yellow);
    text-decoration: none;
    font-weight: bold;
    font-size: 1.1em;
}

.source-link a:hover {
    text-shadow: 0 0 5px var(--pac-yellow);
    text-decoration: underline;
}

.function-categories {
    margin: 30px 0;
}

.category {
    margin: 25px 0;
    background: #001122;
    border: 2px solid var(--pac-blue);
    border-radius: 8px;
    padding: 20px;
}

.category h3 {
    color: var(--pac-yellow);
    margin-top: 0;
    border-bottom: 1px solid var(--pac-blue);
    padding-bottom: 10px;
}

.function-list {
    list-style: none;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
}

.function-list li {
    background: #000033;
    border: 1px solid var(--pac-blue);
    border-radius: 5px;
    padding: 8px 12px;
}

.function-list a {
    color: var(--dot-color);
    text-decoration: none;
}

.function-list a:hover {
    color: var(--pac-yellow);
    text-shadow: 0 0 3px var(--pac-yellow);
}

.pac-man-footer {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 2px solid var(--pac-yellow);
    color: var(--dot-color);
}

h2 {
    color: var(--pac-yellow);
    border-bottom: 2px solid var(--pac-blue);
    padding-bottom: 8px;
}

h3 {
    color: var(--dot-color);
}

code {
    background: #002244;
    color: var(--pac-yellow);
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
}

pre code {
    background: transparent;
    padding: 0;
}

/* Responsive design */
@media (max-width: 768px) {
    .pac-man-container {
        padding: 15px;
    }
    
    .pac-man-header h1 {
        font-size: 2em;
    }
    
    .repo-info {
        flex-direction: column;
        align-items: center;
    }
    
    .function-list {
        grid-template-columns: 1fr;
    }
}
'''
    
    def _categorize_function(self, function: FunctionInfo) -> str:
        """🏷️ Categorize function based on name and signature"""
        name = function.name.lower()
        
        if any(keyword in name for keyword in ['create', 'add', 'insert', 'new']):
            return 'Core API'
        elif any(keyword in name for keyword in ['update', 'modify', 'change', 'set']):
            return 'Data Operations'
        elif any(keyword in name for keyword in ['get', 'list', 'show', 'find', 'search']):
            return 'Data Operations'
        elif any(keyword in name for keyword in ['delete', 'remove', 'drop', 'clear']):
            return 'Data Operations'
        elif any(keyword in name for keyword in ['util', 'helper', 'format', 'parse']):
            return 'Utilities'
        else:
            return 'Advanced'
    
    def _categorize_module(self, file_path: str) -> str:
        """🏷️ Categorize module based on file path"""
        if 'core' in file_path:
            return 'core'
        elif any(keyword in file_path for keyword in ['util', 'helper', 'common']):
            return 'utilities'
        elif any(keyword in file_path for keyword in ['test', 'spec']):
            return 'testing'
        else:
            return 'general'
    
    def _get_function_badge(self, function: FunctionInfo) -> Dict[str, str]:
        """🏷️ Get badge info for function"""
        name = function.name.lower()
        
        if any(keyword in name for keyword in ['create', 'add', 'insert']):
            return {'text': 'Core API', 'color': 'blue'}
        elif any(keyword in name for keyword in ['delete', 'remove', 'drop']):
            return {'text': 'Destructive', 'color': 'red'}
        elif any(keyword in name for keyword in ['update', 'modify']):
            return {'text': 'Data Operations', 'color': 'green'}
        elif any(keyword in name for keyword in ['image', 'video', 'media']):
            return {'text': 'Media', 'color': 'purple'}
        elif any(keyword in name for keyword in ['ml', 'ai', 'model', 'train']):
            return {'text': 'ML/AI', 'color': 'orange'}
        else:
            return {'text': 'General', 'color': 'blue'}
    
    def _get_brief_description(self, docstring: str) -> str:
        """📝 Extract brief description from docstring"""
        if not docstring:
            return "Function description"
        
        # Get first sentence
        lines = docstring.strip().split('\n')
        first_line = lines[0].strip()
        
        # Remove common prefixes
        for prefix in ['"""', "'''", "Args:", "Parameters:", "Returns:"]:
            first_line = first_line.replace(prefix, '').strip()
        
        # Truncate if too long
        if len(first_line) > 100:
            first_line = first_line[:97] + "..."
        
        return first_line or "Function description"
    
    def _format_description(self, docstring: str) -> str:
        """📝 Format docstring for documentation"""
        if not docstring:
            return "Function description not available."
        
        # Clean up docstring
        lines = docstring.strip().split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Args:', 'Parameters:', 'Returns:', 'Raises:', 'Example:')):
                # Remove docstring quotes
                line = line.replace('"""', '').replace("'''", '').strip()
                if line:
                    cleaned_lines.append(line)
        
        return ' '.join(cleaned_lines) or "Function description not available."
    
    def _parse_docstring(self, docstring: str) -> Dict[str, Any]:
        """📝 Parse docstring for structured information"""
        if not docstring:
            return {}
        
        # Simple docstring parsing - could be enhanced
        info = {
            'parameters': [],
            'returns': '',
            'examples': [],
            'raises': []
        }
        
        # This is a simplified parser - in practice, you'd want a more robust solution
        # like docstring_parser or similar
        
        return info
    
    def _generate_github_url(
        self, 
        org_repo: str, 
        release: str, 
        file_path: str, 
        start_line: int, 
        end_line: int
    ) -> str:
        """🔗 Generate GitHub source URL"""
        return f"https://github.com/{org_repo}/blob/{release}/{file_path}#L{start_line}-L{end_line}"
    
    def _load_templates(self) -> Dict[str, Any]:
        """📋 Load documentation templates"""
        # In a full implementation, this would load templates from files
        return {
            'default_mdx': 'default',
            'default_html': 'default',
            'default_markdown': 'default'
        }
