"""
Simple AST Parser - Stage 1 of Two-Stage Pipeline

Based on the working codedoc parser. Extracts basic semantic information
without complex ontological models.
"""

import ast
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path


@dataclass
class SimpleFunctionInfo:
    """Simple function information from AST parsing."""
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    line_number: int
    end_line: int
    decorators: List[str]
    is_async: bool = False
    visibility: str = "public"  # "public", "protected", "private"


@dataclass
class SimpleClassInfo:
    """Simple class information from AST parsing."""
    name: str
    bases: List[str]
    docstring: Optional[str]
    line_number: int
    end_line: int
    methods: List[SimpleFunctionInfo]
    decorators: List[str]


@dataclass
class SimpleModuleInfo:
    """Simple module information from AST parsing."""
    name: str
    docstring: Optional[str]
    functions: List[SimpleFunctionInfo]
    classes: List[SimpleClassInfo]
    imports: List[str]


class SimpleASTParser(ast.NodeVisitor):
    """Simple AST visitor that extracts basic semantic information."""

    def __init__(self):
        self.functions: List[SimpleFunctionInfo] = []
        self.classes: List[SimpleClassInfo] = []
        self.imports: List[str] = []
        self.current_class: Optional[str] = None

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            for alias in node.names:
                self.imports.append(f"{node.module}.{alias.name}")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        old_class = self.current_class
        self.current_class = node.name
        
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(self._extract_function_info(item))

        class_info = SimpleClassInfo(
            name=node.name,
            bases=[self._get_name(base) for base in node.bases],
            docstring=ast.get_docstring(node),
            line_number=node.lineno,
            end_line=getattr(node, 'end_lineno', node.lineno),
            methods=methods,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list]
        )
        self.classes.append(class_info)
        
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self.current_class is None:
            func_info = self._extract_function_info(node)
            self.functions.append(func_info)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if self.current_class is None:
            func_info = self._extract_function_info(node, is_async=True)
            self.functions.append(func_info)

    def _extract_function_info(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool = False) -> SimpleFunctionInfo:
        """Extract function information from AST node."""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)

        returns = None
        if node.returns:
            returns = self._get_name(node.returns)

        return SimpleFunctionInfo(
            name=node.name,
            args=args,
            returns=returns,
            docstring=ast.get_docstring(node),
            line_number=node.lineno,
            end_line=getattr(node, 'end_lineno', node.lineno),
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
            is_async=is_async,
            visibility=self._get_function_visibility(node.name)
        )

    def _get_function_visibility(self, name: str) -> str:
        """Determine function visibility based on Python naming conventions."""
        if name.startswith('__') and name.endswith('__'):
            return "public"  # Dunder methods are public API
        elif name.startswith('__'):
            return "private"  # Private functions (name mangling)
        elif name.startswith('_'):
            return "protected"  # Protected functions
        else:
            return "public"  # Public functions

    def _get_name(self, node: ast.AST) -> str:
        """Extract name from various AST node types."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        else:
            try:
                return ast.unparse(node)
            except:
                return "Unknown"

    def _get_decorator_name(self, node: ast.AST) -> str:
        """Extract decorator name from AST node."""
        return self._get_name(node)


def parse_python_file(file_path: Path) -> SimpleModuleInfo:
    """Parse a Python file and extract simple semantic information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise ValueError(f"Syntax error in {file_path}: {e}")
    
    parser = SimpleASTParser()
    parser.visit(tree)

    return SimpleModuleInfo(
        name=file_path.stem,
        docstring=ast.get_docstring(tree),
        functions=parser.functions,
        classes=parser.classes,
        imports=parser.imports
    )