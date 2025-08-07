"""
🟡 PAC-MAN's Python AST Chomper 🟡

This is where PAC-MAN chomps through Python code and turns it into delicious semantic dots!

WAKA WAKA! Every function becomes a tasty dot in our semantic maze!
"""

import ast
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Set, Tuple
from pathlib import Path
import re
import logging

from ..models.function import FunctionInfo, ParameterInfo, DocstringInfo, ParameterKind, FunctionLocation, FunctionType, FunctionVisibility, ClassInfo
from ..models.results import ParsedRepository, ParsedFile, ProcessingResult
from ..models.exceptions import ProcessingError, ValidationError
from ..models.progress import ProgressCallback, ProgressReport
from ..utils.validation import validate_file_path

logger = logging.getLogger(__name__)


@dataclass
class PacManCodeStats:
    """🟡 PAC-MAN's chomping statistics!"""
    dots_chomped: int = 0  # Functions processed
    power_pellets_found: int = 0  # Classes processed
    ghost_encounters: int = 0  # Errors handled
    bonus_items: int = 0  # Special decorators found
    maze_levels_cleared: int = 0  # Files processed


class PythonASTChomper(ast.NodeVisitor):
    """
    🟡 PAC-MAN's AST Chomping Engine! 🟡
    
    Chomps through Python AST nodes and turns them into semantic dots!
    Each function is a delicious dot, each class is a power pellet!
    """

    def __init__(self, file_path: Path, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        
        # PAC-MAN's collection bags! 🟡
        self.chomped_functions: List[FunctionInfo] = []
        self.power_pellets: List[ClassInfo] = []  # Classes
        self.import_dots: List[str] = []
        self.current_class: Optional[str] = None
        
        # PAC-MAN stats! 
        self.stats = PacManCodeStats()
        
        logger.info(f"🟡 PAC-MAN starting to chomp: {file_path}")

    def visit_Import(self, node: ast.Import) -> None:
        """🟡 Chomp chomp! Found some import dots!"""
        for alias in node.names:
            self.import_dots.append(alias.name)
            logger.debug(f"🟡 Chomped import dot: {alias.name}")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """🟡 From-import dots are extra tasty!"""
        if node.module:
            for alias in node.names:
                import_name = f"{node.module}.{alias.name}"
                self.import_dots.append(import_name)
                logger.debug(f"🟡 Chomped from-import dot: {import_name}")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        💊 POWER PELLET DETECTED! 💊
        PAC-MAN found a class - this gives us special powers!
        """
        old_class = self.current_class
        self.current_class = node.name
        
        logger.info(f"💊 PAC-MAN chomping power pellet (class): {node.name}")
        
        # Chomp all the method dots inside this power pellet!
        method_dots = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_info = self._chomp_function_dot(item)
                method_dots.append(method_info)

        class_info = ClassInfo(
            name=node.name,
            bases=[self._extract_name(base) for base in node.bases],
            docstring=ast.get_docstring(node),
            line_number=node.lineno,
            end_line=getattr(node, 'end_lineno', node.lineno),
            methods=method_dots,
            decorators=[self._extract_decorator_name(d) for d in node.decorator_list],
            file_path=str(self.file_path)
        )
        
        self.power_pellets.append(class_info)
        self.stats.power_pellets_found += 1
        
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """🟡 Regular dot detected! Nom nom nom!"""
        if self.current_class is None:  # Only top-level functions
            func_info = self._chomp_function_dot(node)
            self.chomped_functions.append(func_info)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """⚡ Async dot detected! Special electric flavor!"""
        if self.current_class is None:  # Only top-level functions
            func_info = self._chomp_function_dot(node, is_async=True)
            self.chomped_functions.append(func_info)

    def _chomp_function_dot(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool = False) -> FunctionInfo:
        """
        🟡 CHOMP! The main dot-chomping function!
        
        This is where PAC-MAN takes a delicious function and turns it into semantic goodness!
        """
        try:
            # Extract parameters (the dot's ingredients!)
            parameters = self._extract_parameters(node.args)
            
            # Extract return type annotation
            return_type = None
            if node.returns:
                return_type = self._extract_name(node.returns)
            
            # Parse the docstring for extra flavor!
            docstring_info = self._parse_docstring(ast.get_docstring(node))
            
            # Check for special decorators (bonus items!)
            decorators = [self._extract_decorator_name(d) for d in node.decorator_list]
            if any(dec in ['@property', '@staticmethod', '@classmethod'] for dec in decorators):
                self.stats.bonus_items += 1
                logger.debug(f"🍎 Bonus decorator found: {decorators}")
            
            # Determine visibility (how visible is this dot in the maze?)
            visibility = self._determine_visibility(node.name)
            
            # Map visibility string to enum
            visibility_map = {
                "public": FunctionVisibility.PUBLIC,
                "private": FunctionVisibility.PRIVATE,
                "protected": FunctionVisibility.PROTECTED,
                "internal": FunctionVisibility.INTERNAL
            }
            visibility_enum = visibility_map.get(visibility, FunctionVisibility.PUBLIC)
            
            # Determine function type
            function_type = FunctionType.COROUTINE if is_async else FunctionType.FUNCTION
            if any('property' in dec for dec in decorators):
                function_type = FunctionType.PROPERTY
            elif any('staticmethod' in dec for dec in decorators):
                function_type = FunctionType.STATICMETHOD
            elif any('classmethod' in dec for dec in decorators):
                function_type = FunctionType.CLASSMETHOD
            elif self.current_class is not None:
                function_type = FunctionType.METHOD
            
            # Create location object
            # Try to get relative path from repository root
            try:
                # Assume file_path is like: /Users/rob/.repolex/repos/org/repo/src/module.py
                # We want: src/module.py
                path_parts = self.file_path.parts
                if 'repos' in path_parts:
                    repos_index = path_parts.index('repos')
                    # Skip repos/org/repo to get the actual file path within the repo
                    relative_path = '/'.join(path_parts[repos_index + 3:])
                else:
                    relative_path = str(self.file_path.name)
            except:
                relative_path = str(self.file_path.name)
            
            location = FunctionLocation(
                file_path=relative_path,
                start_line=node.lineno,
                end_line=getattr(node, 'end_lineno', node.lineno),
                module_name=self._get_module_path(),
                class_name=self.current_class
            )
            
            # Build canonical name
            canonical_name = f"{self._get_module_path()}.{node.name}"
            if self.current_class:
                canonical_name = f"{self._get_module_path()}.{self.current_class}.{node.name}"
            
            # Create the chomped function info!
            func_info = FunctionInfo(
                name=node.name,
                canonical_name=canonical_name,
                signature=self._build_signature(node, parameters, return_type),
                function_type=function_type,
                visibility=visibility_enum,
                location=location,
                return_type=return_type,
                parameters=parameters,
                docstring=ast.get_docstring(node),
                docstring_info=docstring_info
            )
            
            self.stats.dots_chomped += 1
            logger.debug(f"🟡 Chomped function dot: {node.name}")
            
            return func_info
            
        except Exception as e:
            self.stats.ghost_encounters += 1
            logger.warning(f"👻 Ghost encountered while chomping {node.name}: {e}")
            raise ProcessingError(f"Failed to process function {node.name}: {e}")

    def _extract_parameters(self, args: ast.arguments) -> List[ParameterInfo]:
        """🔍 Extract the parameter dots from function arguments!"""
        parameters = []
        
        # Regular arguments
        for i, arg in enumerate(args.args):
            param_type = None
            if arg.annotation:
                param_type = self._extract_name(arg.annotation)
            
            # Check if this parameter has a default value
            default_value = None
            default_offset = len(args.args) - len(args.defaults)
            if i >= default_offset:
                default_idx = i - default_offset
                default_value = self._extract_default_value(args.defaults[default_idx])
            
            param_info = ParameterInfo(
                name=arg.arg,
                type_annotation=param_type,
                default_value=default_value,
                has_default=default_value is not None,
                required=default_value is None,
                kind=ParameterKind.POSITIONAL
            )
            parameters.append(param_info)
        
        # *args parameter
        if args.vararg:
            vararg_type = None
            if args.vararg.annotation:
                vararg_type = self._extract_name(args.vararg.annotation)
            
            param_info = ParameterInfo(
                name=args.vararg.arg,
                type_annotation=vararg_type,
                default_value=None,
                has_default=False,
                required=False,
                kind=ParameterKind.VAR_POSITIONAL
            )
            parameters.append(param_info)
        
        # **kwargs parameter
        if args.kwarg:
            kwarg_type = None
            if args.kwarg.annotation:
                kwarg_type = self._extract_name(args.kwarg.annotation)
            
            param_info = ParameterInfo(
                name=args.kwarg.arg,
                type_annotation=kwarg_type,
                default_value=None,
                has_default=False,
                required=False,
                kind=ParameterKind.VAR_KEYWORD
            )
            parameters.append(param_info)
        
        return parameters

    def _parse_docstring(self, docstring: Optional[str]) -> DocstringInfo:
        """🛸 THE ULTIMATE SEMANTIC DOCSTRING EXTRACTOR! 🛸"""
        if not docstring:
            return DocstringInfo()
        
        # Initialize ALL the knowledge containers! 🧠
        lines = docstring.strip().split('\n')
        
        # Basic content
        description = ""
        summary = ""
        parameters = {}
        returns = ""
        yields = ""
        raises = {}
        examples = []
        
        # 🚀 METADATA GOLDMINE! 🚀
        author = None
        authors = []
        since = None
        version = None
        deprecated = False
        deprecated_since = None
        deprecated_reason = None
        removal_version = None
        complexity = None
        performance_notes = []
        memory_usage = None
        tags = []
        categories = []
        domains = []
        references = []
        external_links = []
        todo = []
        notes = []
        warnings = []
        see_also = []
        tested = False
        test_examples = []
        edge_cases = []
        known_issues = []
        usage_patterns = []
        best_practices = []
        experimental = False
        internal = False
        stable = True
        
        current_section = None
        current_content = []
        
        # Extract summary (first line)
        if lines:
            summary = lines[0].strip()
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 🚀 MEGA SECTION DETECTION! 🚀
            section_detected = False
            
            # Standard sections
            if line.lower().startswith(('args:', 'arguments:', 'parameters:')):
                current_section = 'args'
                section_detected = True
            elif line.lower().startswith(('returns:', 'return:')):
                current_section = 'returns'
                section_detected = True
            elif line.lower().startswith(('yields:', 'yield:')):
                current_section = 'yields'
                section_detected = True
            elif line.lower().startswith(('raises:', 'raise:', 'exceptions:')):
                current_section = 'raises'
                section_detected = True
            elif line.lower().startswith(('examples:', 'example:')):
                current_section = 'examples'
                section_detected = True
            
            # 🎯 METADATA SECTIONS! 🎯
            elif line.lower().startswith(('author:', '@author')):
                current_section = 'author'
                section_detected = True
            elif line.lower().startswith(('since:', '@since', 'version:')):
                current_section = 'since'
                section_detected = True
            elif line.lower().startswith(('deprecated:', '@deprecated')):
                current_section = 'deprecated'
                section_detected = True
            elif line.lower().startswith(('complexity:', 'time complexity:', 'space complexity:')):
                current_section = 'complexity'
                section_detected = True
            elif line.lower().startswith(('performance:', 'perf:')):
                current_section = 'performance'
                section_detected = True
            elif line.lower().startswith(('memory:', 'memory usage:')):
                current_section = 'memory'
                section_detected = True
            elif line.lower().startswith(('todo:', '@todo', 'fixme:')):
                current_section = 'todo'
                section_detected = True
            elif line.lower().startswith(('note:', 'notes:')):
                current_section = 'notes'
                section_detected = True
            elif line.lower().startswith(('warning:', 'warnings:', '@warning')):
                current_section = 'warnings'
                section_detected = True
            elif line.lower().startswith(('see also:', 'see_also:', 'related:')):
                current_section = 'see_also'
                section_detected = True
            elif line.lower().startswith(('references:', 'refs:', 'bibliography:')):
                current_section = 'references'
                section_detected = True
            elif line.lower().startswith(('links:', 'external links:')):
                current_section = 'external_links'
                section_detected = True
            elif line.lower().startswith(('test:', 'tests:', 'testing:')):
                current_section = 'test_examples'
                section_detected = True
            elif line.lower().startswith(('edge cases:', 'edge case:')):
                current_section = 'edge_cases'
                section_detected = True
            elif line.lower().startswith(('known issues:', 'bugs:', 'issues:')):
                current_section = 'known_issues'
                section_detected = True
            elif line.lower().startswith(('usage:', 'usage patterns:')):
                current_section = 'usage_patterns'
                section_detected = True
            elif line.lower().startswith(('best practices:', 'best practice:')):
                current_section = 'best_practices'
                section_detected = True
            
            # 🏷️ INLINE TAGS AND MARKERS! 🏷️
            elif '@experimental' in line.lower():
                experimental = True
            elif '@internal' in line.lower():
                internal = True
            elif '@unstable' in line.lower():
                stable = False
            elif '@tested' in line.lower():
                tested = True
            
            if section_detected:
                # Process previous section
                if current_section and current_content:
                    # Use a mutable container to pass values by reference
                    metadata = {
                        'author': author, 'since': since, 'version': version,
                        'deprecated': deprecated, 'deprecated_since': deprecated_since,
                        'deprecated_reason': deprecated_reason, 'removal_version': removal_version,
                        'complexity': complexity, 'memory_usage': memory_usage,
                        'returns': returns, 'yields': yields
                    }
                    self._process_enhanced_docstring_section(
                        current_section, current_content, metadata,
                        description, parameters, raises, examples,
                        authors, performance_notes, tags, categories, domains, 
                        references, external_links, todo, notes, warnings, 
                        see_also, test_examples, edge_cases, known_issues, 
                        usage_patterns, best_practices
                    )
                    # Extract back from metadata
                    author = metadata['author']
                    since = metadata['since']  
                    version = metadata['version']
                    deprecated = metadata['deprecated']
                    deprecated_since = metadata['deprecated_since']
                    deprecated_reason = metadata['deprecated_reason']
                    removal_version = metadata['removal_version']
                    complexity = metadata['complexity']
                    memory_usage = metadata['memory_usage']
                    returns = metadata['returns']
                    yields = metadata['yields']
                current_content = []
                # Check if section has inline content
                if ':' in line:
                    inline_content = line.split(':', 1)[1].strip()
                    if inline_content:
                        current_content.append(inline_content)
            else:
                if current_section:
                    current_content.append(line)
                else:
                    if line and i > 0:  # Skip first line (summary), only add non-empty lines
                        description += line + "\n"
            
            # 🔍 EXTRACT INLINE PATTERNS! 🔍
            self._extract_inline_patterns(line, tags, categories, domains, references, external_links)
        
        # Process final section
        if current_section and current_content:
            metadata = {
                'author': author, 'since': since, 'version': version,
                'deprecated': deprecated, 'deprecated_since': deprecated_since,
                'deprecated_reason': deprecated_reason, 'removal_version': removal_version,
                'complexity': complexity, 'memory_usage': memory_usage,
                'returns': returns, 'yields': yields
            }
            self._process_enhanced_docstring_section(
                current_section, current_content, metadata,
                description, parameters, raises, examples,
                authors, performance_notes, tags, categories, domains, 
                references, external_links, todo, notes, warnings, 
                see_also, test_examples, edge_cases, known_issues, 
                usage_patterns, best_practices
            )
            # Extract back from metadata
            author = metadata['author']
            since = metadata['since']  
            version = metadata['version']
            deprecated = metadata['deprecated']
            deprecated_since = metadata['deprecated_since']
            deprecated_reason = metadata['deprecated_reason']
            removal_version = metadata['removal_version']
            complexity = metadata['complexity']
            memory_usage = metadata['memory_usage']
            returns = metadata['returns']
            yields = metadata['yields']
        
        return DocstringInfo(
            summary=summary,
            short_description=summary,
            long_description=description.strip(),
            parameters=parameters,
            returns=returns.strip(),
            yields=yields.strip(),
            raises=raises,
            examples=examples,
            author=author,
            authors=authors,
            since=since,
            version=version,
            deprecated=deprecated,
            deprecated_since=deprecated_since,
            deprecated_reason=deprecated_reason,
            removal_version=removal_version,
            complexity=complexity,
            performance_notes=performance_notes,
            memory_usage=memory_usage,
            tags=tags,
            categories=categories,
            domains=domains,
            references=references,
            external_links=external_links,
            todo=todo,
            notes=notes,
            warnings=warnings,
            see_also=see_also,
            tested=tested,
            test_examples=test_examples,
            edge_cases=edge_cases,
            known_issues=known_issues,
            usage_patterns=usage_patterns,
            best_practices=best_practices,
            experimental=experimental,
            internal=internal,
            stable=stable
        )
    
    def _process_enhanced_docstring_section(self, section: str, content: List[str], 
                                          metadata: Dict[str, Any],
                                          description: str, parameters: Dict[str, str], 
                                          raises: Dict[str, str], examples: List[str],
                                          authors: List[str], performance_notes: List[str],
                                          tags: List[str], categories: List[str], domains: List[str],
                                          references: List[str], external_links: List[str],
                                          todo: List[str], notes: List[str], warnings: List[str],
                                          see_also: List[str], test_examples: List[str],
                                          edge_cases: List[str], known_issues: List[str],
                                          usage_patterns: List[str], best_practices: List[str]) -> None:
        """🛸 PROCESS ENHANCED DOCSTRING SECTIONS! 🛸"""
        content_text = '\n'.join(content).strip()
        
        if section == 'args':
            # Parse parameter documentation
            for line in content:
                if ':' in line:
                    param_name = line.split(':')[0].strip()
                    param_desc = ':'.join(line.split(':')[1:]).strip()
                    parameters[param_name] = param_desc
        elif section == 'returns':
            metadata['returns'] = content_text
        elif section == 'yields':
            metadata['yields'] = content_text
        elif section == 'raises':
            # Parse raises section as key-value pairs
            for line in content:
                if ':' in line:
                    exc_name = line.split(':')[0].strip()
                    exc_desc = ':'.join(line.split(':')[1:]).strip()
                    raises[exc_name] = exc_desc
                elif line.strip():
                    # If no colon, use the whole line as both key and description
                    raises[line.strip()] = line.strip()
        elif section == 'examples':
            examples.append(content_text)
        
        # 🚀 ENHANCED METADATA PROCESSING! 🚀
        elif section == 'author':
            content_text = content_text.strip()
            if content_text and not metadata['author']:
                metadata['author'] = content_text
            if content_text and content_text not in authors:
                authors.append(content_text)
        elif section == 'since':
            metadata['since'] = content_text.strip()
        elif section == 'deprecated':
            metadata['deprecated'] = True
            metadata['deprecated_reason'] = content_text.strip()
            # Look for version info in deprecation
            for line in content:
                if 'since' in line.lower():
                    version_match = re.search(r'v?(\d+\.\d+(?:\.\d+)?)', line)
                    if version_match:
                        metadata['deprecated_since'] = version_match.group(1)
                elif 'removal' in line.lower() or 'removed' in line.lower():
                    version_match = re.search(r'v?(\d+\.\d+(?:\.\d+)?)', line)
                    if version_match:
                        metadata['removal_version'] = version_match.group(1)
        elif section == 'complexity':
            metadata['complexity'] = content_text.strip()
        elif section == 'performance':
            performance_notes.extend([line.strip() for line in content if line.strip()])
        elif section == 'memory':
            metadata['memory_usage'] = content_text.strip()
        elif section == 'todo':
            todo.extend([line.strip() for line in content if line.strip()])
        elif section == 'notes':
            notes.extend([line.strip() for line in content if line.strip()])
        elif section == 'warnings':
            warnings.extend([line.strip() for line in content if line.strip()])
        elif section == 'see_also':
            see_also.extend([line.strip() for line in content if line.strip()])
        elif section == 'references':
            references.extend([line.strip() for line in content if line.strip()])
        elif section == 'external_links':
            external_links.extend([line.strip() for line in content if line.strip()])
        elif section == 'test_examples':
            test_examples.extend([line.strip() for line in content if line.strip()])
        elif section == 'edge_cases':
            edge_cases.extend([line.strip() for line in content if line.strip()])
        elif section == 'known_issues':
            known_issues.extend([line.strip() for line in content if line.strip()])
        elif section == 'usage_patterns':
            usage_patterns.extend([line.strip() for line in content if line.strip()])
        elif section == 'best_practices':
            best_practices.extend([line.strip() for line in content if line.strip()])
    
    def _extract_inline_patterns(self, line: str, tags: List[str], categories: List[str], 
                                domains: List[str], references: List[str], 
                                external_links: List[str]) -> None:
        """🔍 EXTRACT INLINE PATTERNS FROM DOCSTRING LINES! 🔍"""
        line_lower = line.lower()
        
        # 🏷️ HASHTAG EXTRACTION! 🏷️
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, line)
        for tag in hashtags:
            if tag not in tags:
                tags.append(tag)
        
        # 🔗 URL EXTRACTION! 🔗
        url_pattern = r'https?://[^\s\)]+|www\.[^\s\)]+'
        urls = re.findall(url_pattern, line)
        for url in urls:
            if url not in external_links:
                external_links.append(url)
        
        # 📖 REFERENCE EXTRACTION! 📖
        # Look for patterns like "See [Author Year]", "Based on [Paper]", etc.
        ref_patterns = [
            r'see\s+\[([^\]]+)\]',
            r'based\s+on\s+\[([^\]]+)\]', 
            r'from\s+\[([^\]]+)\]',
            r'reference:\s*\[([^\]]+)\]',
            r'ref:\s*\[([^\]]+)\]'
        ]
        for pattern in ref_patterns:
            matches = re.findall(pattern, line_lower)
            for match in matches:
                if match not in references:
                    references.append(match)
        
        # 📂 CATEGORY INFERENCE! 📂
        category_keywords = {
            'algorithm': ['algorithm', 'sorting', 'search', 'optimization'],
            'data_structure': ['list', 'dict', 'tree', 'graph', 'array'],
            'utility': ['helper', 'utility', 'util', 'tool'],
            'validation': ['validate', 'check', 'verify', 'sanitize'],
            'conversion': ['convert', 'transform', 'parse', 'format'],
            'io': ['read', 'write', 'save', 'load', 'file', 'stream'],
            'api': ['endpoint', 'route', 'request', 'response', 'http'],
            'database': ['query', 'sql', 'database', 'table', 'record'],
            'computation': ['calculate', 'compute', 'process', 'analyze']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                if category not in categories:
                    categories.append(category)
        
        # 🌐 DOMAIN CLASSIFICATION! 🌐
        domain_keywords = {
            'machine_learning': ['ml', 'model', 'train', 'predict', 'neural', 'ai'],
            'data_science': ['data', 'dataset', 'analysis', 'statistics', 'analytics'],
            'web_development': ['web', 'html', 'css', 'javascript', 'frontend', 'backend'],
            'security': ['security', 'auth', 'encryption', 'password', 'token'],
            'graphics': ['image', 'pixel', 'render', 'graphics', 'visual'],
            'network': ['network', 'http', 'tcp', 'socket', 'protocol'],
            'database': ['database', 'sql', 'query', 'orm', 'migration'],
            'testing': ['test', 'mock', 'assert', 'verify', 'validate'],
            'configuration': ['config', 'settings', 'environment', 'params']
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                if domain not in domains:
                    domains.append(domain)

    def _process_docstring_section(self, section: str, content: List[str],
                                 description: str, parameters: Dict[str, str], 
                                 returns: str, raises: Dict[str, str], examples: List[str]) -> None:
        """Process a specific section of the docstring"""
        content_text = '\n'.join(content).strip()
        
        if section == 'args':
            # Parse parameter documentation
            for line in content:
                if ':' in line:
                    param_name = line.split(':')[0].strip()
                    param_desc = ':'.join(line.split(':')[1:]).strip()
                    parameters[param_name] = param_desc
        elif section == 'returns':
            returns = content_text
        elif section == 'raises':
            # Parse raises section as key-value pairs
            for line in content:
                if ':' in line:
                    exc_name = line.split(':')[0].strip()
                    exc_desc = ':'.join(line.split(':')[1:]).strip()
                    raises[exc_name] = exc_desc
                elif line.strip():
                    # If no colon, use the whole line as both key and description
                    raises[line.strip()] = line.strip()
        elif section == 'examples':
            examples.append(content_text)

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef, 
                        parameters: List[ParameterInfo], return_type: Optional[str]) -> str:
        """🔧 Build the complete function signature string"""
        param_strs = []
        
        for param in parameters:
            param_str = param.name
            
            if param.type_annotation:
                param_str += f": {param.type_annotation}"
            
            if param.default_value is not None:
                param_str += f" = {param.default_value}"
            
            if param.kind == ParameterKind.VAR_POSITIONAL:
                param_str = f"*{param_str}"
            elif param.kind == ParameterKind.VAR_KEYWORD:
                param_str = f"**{param_str}"
            
            param_strs.append(param_str)
        
        signature = f"{node.name}({', '.join(param_strs)})"
        
        if return_type:
            signature += f" -> {return_type}"
        
        if isinstance(node, ast.AsyncFunctionDef):
            signature = f"async {signature}"
        
        return signature

    def _extract_name(self, node: ast.AST) -> str:
        """Extract name from various AST node types."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._extract_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Subscript):
            return f"{self._extract_name(node.value)}[{self._extract_name(node.slice)}]"
        else:
            try:
                return ast.unparse(node)
            except:
                return "Unknown"

    def _extract_decorator_name(self, node: ast.AST) -> str:
        """Extract decorator name from AST node."""
        return self._extract_name(node)

    def _extract_default_value(self, node: ast.AST) -> str:
        """Extract default value as string."""
        try:
            if isinstance(node, ast.Constant):
                if isinstance(node.value, str):
                    return f'"{node.value}"'
                return str(node.value)
            elif isinstance(node, ast.Name):
                return node.id
            else:
                return ast.unparse(node)
        except:
            return "..."

    def _determine_visibility(self, name: str) -> str:
        """🔍 Determine function visibility (how visible in the maze?)"""
        if name.startswith('__') and name.endswith('__'):
            return "public"  # Dunder methods are public API
        elif name.startswith('__'):
            return "private"  # Name mangling
        elif name.startswith('_'):
            return "protected"  # Protected
        else:
            return "public"  # Public

    def _get_module_path(self) -> str:
        """Get the module path for this file"""
        # Convert file path to module path with proper file-specific detection
        try:
            # Assume file_path is like: /Users/rob/.repolex/repos/org/repo/src/module.py
            # We want: src/module (without .py extension)
            path_parts = self.file_path.parts
            if 'repos' in path_parts:
                repos_index = path_parts.index('repos')
                # Skip repos/org/repo to get the actual file path within the repo
                relative_parts = path_parts[repos_index + 3:]
                if relative_parts:
                    # Join the parts and remove .py extension
                    module_path = '/'.join(relative_parts)
                    return str(Path(module_path).with_suffix(''))
                else:
                    return str(self.file_path.stem)  # Just filename without extension
            else:
                return str(self.file_path.with_suffix(''))
        except Exception as e:
            logger.debug(f"Error getting module path for {self.file_path}: {e}")
            return str(self.file_path.with_suffix(''))



class PythonParser:
    """
    🟡 PAC-MAN's Main Python Parsing System 🟡
    
    This is the main interface for chomping through Python code!
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stats = PacManCodeStats()

    def parse_repository(self, repo_path: Path, release: str, org_repo: str = None, progress_callback: Optional[ProgressCallback] = None) -> ParsedRepository:
        """
        🟡 CHOMP THE ENTIRE REPOSITORY! 🟡
        
        PAC-MAN goes through every Python file and chomps all the semantic dots!
        """
        self.logger.info(f"🟡 PAC-MAN starting repository chomp: {repo_path} ({release})")
        
        try:
            # Find all Python files in the repository
            python_files = list(repo_path.rglob("*.py"))
            
            if not python_files:
                raise ProcessingError(f"No Python files found in {repo_path}")
            
            parsed_files = []
            total_functions = 0
            total_classes = 0
            
            for i, py_file in enumerate(python_files):
                try:
                    # Skip certain directories/files (but not our storage directory)
                    # Get the relative path from the repo root
                    relative_parts = py_file.relative_to(repo_path).parts
                    if any(part.startswith('.') for part in relative_parts):
                        continue
                    if 'test' in py_file.name.lower() and not py_file.name.startswith('test_'):
                        continue
                    
                    parsed_file = self.parse_file(py_file)
                    parsed_files.append(parsed_file)
                    
                    total_functions += len(parsed_file.functions)
                    total_classes += len(parsed_file.classes)
                    
                    self.logger.debug(f"🟡 Chomped {py_file}: {len(parsed_file.functions)} functions, {len(parsed_file.classes)} classes")
                    
                    # Progress reporting
                    if progress_callback:
                        progress = (i + 1) / len(python_files) * 100
                        progress_callback(ProgressReport(
                            phase="parsing",
                            message=f"🟡 PAC-MAN chomped {py_file.name}",
                            progress=progress
                        ))
                    
                except Exception as e:
                    self.logger.warning(f"👻 Ghost encountered in {py_file}: {e}")
                    continue
            
            self.logger.info(f"🟡 Repository chomp complete! {total_functions} functions, {total_classes} classes from {len(parsed_files)} files")
            
            return ParsedRepository(
                org_repo=org_repo or repo_path.name,
                release=release,
                files=parsed_files,
                total_functions=total_functions,
                total_classes=total_classes,
                processing_stats=self.stats
            )
            
        except Exception as e:
            raise ProcessingError(f"Failed to parse repository {repo_path}: {e}")

    def parse_file(self, file_path: Path) -> ParsedFile:
        """
        🟡 Chomp a single Python file! 🟡
        
        Turn one file into delicious semantic dots!
        """
        try:
            validate_file_path(file_path, file_path.parent)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse the AST
            try:
                tree = ast.parse(source_code)
            except SyntaxError as e:
                raise ProcessingError(f"Syntax error in {file_path}: {e}")
            
            # Create the chomper and chomp away!
            chomper = PythonASTChomper(file_path, source_code)
            chomper.visit(tree)
            
            # Update our global stats
            self.stats.dots_chomped += chomper.stats.dots_chomped
            self.stats.power_pellets_found += chomper.stats.power_pellets_found
            self.stats.ghost_encounters += chomper.stats.ghost_encounters
            self.stats.bonus_items += chomper.stats.bonus_items
            self.stats.maze_levels_cleared += 1
            
            return ParsedFile(
                file_path=file_path,
                functions=chomper.chomped_functions,
                classes=chomper.power_pellets,
                imports=chomper.import_dots,
                line_count=len(chomper.source_lines)
            )
            
        except Exception as e:
            raise ProcessingError(f"Failed to parse file {file_path}: {e}")

    def extract_functions(self, ast_node: ast.AST) -> List[FunctionInfo]:
        """Extract function definitions from AST - helper method"""
        chomper = PythonASTChomper(Path("unknown"), "")
        
        functions = []
        for node in ast.walk(ast_node):
            if isinstance(node, ast.FunctionDef):
                functions.append(chomper._chomp_function_dot(node))
            elif isinstance(node, ast.AsyncFunctionDef):
                functions.append(chomper._chomp_function_dot(node, is_async=True))
        
        return functions

    def extract_docstring_info(self, docstring: str) -> DocstringInfo:
        """Parse docstrings for parameters, returns, examples - helper method"""
        chomper = PythonASTChomper(Path("unknown"), "")
        return chomper._parse_docstring(docstring)


# 🟡 PAC-MAN says: "WAKA WAKA! Let's chomp some code!" 🟡
def create_python_parser() -> PythonParser:
    """Factory function to create a PAC-MAN Python parser!"""
    return PythonParser()
