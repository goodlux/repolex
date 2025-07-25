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

from ..models.function import FunctionInfo, ParameterInfo, DocstringInfo
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
            
            # Create the chomped function info!
            func_info = FunctionInfo(
                name=node.name,
                signature=self._build_signature(node, parameters, return_type),
                parameters=parameters,
                return_type=return_type,
                docstring_info=docstring_info,
                decorators=decorators,
                is_async=is_async,
                visibility=visibility,
                line_number=node.lineno,
                end_line=getattr(node, 'end_lineno', node.lineno),
                file_path=str(self.file_path),
                module_path=self._get_module_path()
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
                is_required=default_value is None,
                is_vararg=False,
                is_kwarg=False
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
                is_required=False,
                is_vararg=True,
                is_kwarg=False
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
                is_required=False,
                is_vararg=False,
                is_kwarg=True
            )
            parameters.append(param_info)
        
        return parameters

    def _parse_docstring(self, docstring: Optional[str]) -> DocstringInfo:
        """📚 Parse docstring for extra semantic flavor!"""
        if not docstring:
            return DocstringInfo()
        
        # Basic docstring parsing - could be enhanced with more sophisticated parsing
        lines = docstring.strip().split('\n')
        
        description = ""
        parameters = {}
        returns = ""
        raises = []
        examples = []
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Section detection
            if line.lower().startswith(('args:', 'arguments:', 'parameters:')):
                if current_section and current_content:
                    self._process_docstring_section(current_section, current_content, 
                                                  description, parameters, returns, raises, examples)
                current_section = 'args'
                current_content = []
            elif line.lower().startswith(('returns:', 'return:')):
                if current_section and current_content:
                    self._process_docstring_section(current_section, current_content,
                                                  description, parameters, returns, raises, examples)
                current_section = 'returns'
                current_content = []
            elif line.lower().startswith(('raises:', 'raise:')):
                if current_section and current_content:
                    self._process_docstring_section(current_section, current_content,
                                                  description, parameters, returns, raises, examples)
                current_section = 'raises'
                current_content = []
            elif line.lower().startswith(('examples:', 'example:')):
                if current_section and current_content:
                    self._process_docstring_section(current_section, current_content,
                                                  description, parameters, returns, raises, examples)
                current_section = 'examples'
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
                else:
                    if line:  # Only add non-empty lines to description
                        description += line + "\n"
        
        # Process final section
        if current_section and current_content:
            self._process_docstring_section(current_section, current_content,
                                          description, parameters, returns, raises, examples)
        
        return DocstringInfo(
            description=description.strip(),
            parameters=parameters,
            returns=returns.strip(),
            raises=raises,
            examples=examples
        )

    def _process_docstring_section(self, section: str, content: List[str],
                                 description: str, parameters: Dict[str, str], 
                                 returns: str, raises: List[str], examples: List[str]) -> None:
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
            raises.extend([line.strip() for line in content if line.strip()])
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
            
            if param.is_vararg:
                param_str = f"*{param_str}"
            elif param.is_kwarg:
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
        # Convert file path to module path
        # This is simplified - could be enhanced with proper package detection
        return str(self.file_path.with_suffix(''))


@dataclass
class ClassInfo:
    """Information about a class (power pellet!)"""
    name: str
    bases: List[str]
    docstring: Optional[str]
    line_number: int
    end_line: int
    methods: List[FunctionInfo]
    decorators: List[str]
    file_path: str


class PythonParser:
    """
    🟡 PAC-MAN's Main Python Parsing System 🟡
    
    This is the main interface for chomping through Python code!
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stats = PacManCodeStats()

    async def parse_repository(self, repo_path: Path, release: str, org_repo: str = None, progress_callback: Optional[ProgressCallback] = None) -> ParsedRepository:
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
                    # Skip certain directories/files
                    if any(part.startswith('.') for part in py_file.parts):
                        continue
                    if 'test' in py_file.name.lower() and not py_file.name.startswith('test_'):
                        continue
                    
                    parsed_file = await self.parse_file(py_file)
                    parsed_files.append(parsed_file)
                    
                    total_functions += len(parsed_file.functions)
                    total_classes += len(parsed_file.classes)
                    
                    self.logger.debug(f"🟡 Chomped {py_file}: {len(parsed_file.functions)} functions, {len(parsed_file.classes)} classes")
                    
                    # Progress reporting
                    if progress_callback:
                        progress = (i + 1) / len(python_files) * 100
                        await progress_callback(ProgressReport(
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

    async def parse_file(self, file_path: Path) -> ParsedFile:
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
                path=file_path,
                module_name=file_path.stem,
                docstring=ast.get_docstring(tree),
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
