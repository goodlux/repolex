"""
🔮 PAC-MAN's Semantic Maze Builder 🔮

This is where PAC-MAN's chomped code gets transformed into the ultimate semantic maze!
Every function becomes a perfectly mapped RDF triple in our Web of Code ontology!

WAKA WAKA! From AST dots to semantic gold!
"""

from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import uuid
from datetime import datetime
import logging

from ..models.function import FunctionInfo, ParameterInfo, DocstringInfo
from ..models.results import ParsedRepository, ParsedFile
from ..models.graph import GraphTriple, BuiltGraph
from ..models.exceptions import ProcessingError
from ..storage.graph_schemas import GraphSchemas

logger = logging.getLogger(__name__)


class OntologyMapper:
    """
    🔮 PAC-MAN's Semantic Transformation Engine! 🔮
    
    Converts chomped Python code into Web of Code ontology RDF triples!
    Every dot becomes a perfectly formed semantic relationship!
    """
    
    # Web of Code ontology namespaces
    WOC_NS = "http://rdf.webofcode.org/woc/"
    RDFS_NS = "http://www.w3.org/2000/01/rdf-schema#"
    RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def map_repository_to_rdf(self, parsed_repo: ParsedRepository, 
                                  org: str, repo: str) -> List[BuiltGraph]:
        """
        🔮 Transform entire repository into semantic RDF graphs! 🔮
        
        This is where the magic happens - PAC-MAN's chomped code becomes
        a beautiful semantic web of interconnected knowledge!
        """
        self.logger.info(f"🔮 Starting semantic transformation: {org}/{repo}")
        
        try:
            graphs = []
            
            # Build stable function identities graph
            stable_graph = await self._build_stable_function_graph(
                parsed_repo, org, repo
            )
            graphs.append(stable_graph)
            
            # Build implementation graph for this release
            impl_graph = await self._build_implementation_graph(
                parsed_repo, org, repo, parsed_repo.release
            )
            graphs.append(impl_graph)
            
            # Build file structure graph
            file_graph = await self._build_file_structure_graph(
                parsed_repo, org, repo, parsed_repo.release
            )
            graphs.append(file_graph)
            
            self.logger.info(f"🔮 Semantic transformation complete! {len(graphs)} graphs created")
            return graphs
            
        except Exception as e:
            raise ProcessingError(f"Failed to map repository to RDF: {e}")
    
    async def _build_stable_function_graph(self, parsed_repo: ParsedRepository,
                                         org: str, repo: str) -> BuiltGraph:
        """
        🟡 Build the stable function identities graph! 🟡
        
        These are the eternal dots that never disappear - stable function identities
        that persist across all versions!
        """
        graph_uri = GraphSchemas.get_stable_functions_uri(org, repo)
        triples = []
        
        # Collect all unique functions across all files
        all_functions = []
        for file in parsed_repo.files:
            all_functions.extend(file.functions)
        
        for func in all_functions:
            # Create stable function identity URI
            func_uri = self._get_stable_function_uri(org, repo, func.name)
            
            # Basic function identity triples
            triples.extend([
                GraphTriple(
                    subject=func_uri,
                    predicate=f"{self.RDF_NS}type",
                    object=f"{self.WOC_NS}Function"
                ),
                GraphTriple(
                    subject=func_uri,
                    predicate=f"{self.WOC_NS}canonicalName",
                    object=self._literal(func.name)
                ),
                GraphTriple(
                    subject=func_uri,
                    predicate=f"{self.WOC_NS}firstAppearedIn",
                    object=self._literal(parsed_repo.release)
                ),
                GraphTriple(
                    subject=func_uri,
                    predicate=f"{self.WOC_NS}module",
                    object=self._literal(func.module_path)
                ),
                GraphTriple(
                    subject=func_uri,
                    predicate=f"{self.WOC_NS}githubUrl",
                    object=self._literal(f"https://github.com/{org}/{repo}")
                )
            ])
        
        self.logger.info(f"🟡 Built stable function graph: {len(triples)} triples")
        
        return BuiltGraph(
            uri=graph_uri,
            triples=triples,
            description=f"Stable function identities for {org}/{repo}"
        )
    
    async def _build_implementation_graph(self, parsed_repo: ParsedRepository,
                                        org: str, repo: str, release: str) -> BuiltGraph:
        """
        💊 Build the implementation graph - version-specific power pellets! 💊
        
        These are the detailed implementations that can change between versions!
        """
        graph_uri = GraphSchemas.get_implementation_uri(org, repo)
        triples = []
        
        for file in parsed_repo.files:
            for func in file.functions:
                # Create implementation URI
                impl_uri = self._get_implementation_uri(org, repo, func.name, release)
                stable_uri = self._get_stable_function_uri(org, repo, func.name)
                
                # Link to stable identity
                triples.append(GraphTriple(
                    subject=impl_uri,
                    predicate=f"{self.WOC_NS}implementsFunction",
                    object=stable_uri
                ))
                
                # Implementation details
                triples.extend([
                    GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.RDF_NS}type",
                        object=f"{self.WOC_NS}MethodImplementation"
                    ),
                    GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}belongsToVersion",
                        object=self._literal(release)
                    ),
                    GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}hasSignature",
                        object=self._literal(func.signature)
                    ),
                    GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}definedInFile",
                        object=self._literal(str(func.file_path))
                    ),
                    GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}startLine",
                        object=self._literal(str(func.line_number))
                    ),
                    GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}endLine",
                        object=self._literal(str(func.end_line))
                    )
                ])
                
                # Add docstring if present
                if func.docstring_info and func.docstring_info.description:
                    triples.append(GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.RDFS_NS}comment",
                        object=self._literal(func.docstring_info.description)
                    ))
                
                # Add visibility
                triples.append(GraphTriple(
                    subject=impl_uri,
                    predicate=f"{self.WOC_NS}hasVisibility",
                    object=self._literal(func.visibility)
                ))
                
                # Add parameters
                for i, param in enumerate(func.parameters):
                    param_uri = f"{impl_uri}/param/{param.name}"
                    
                    triples.extend([
                        GraphTriple(
                            subject=impl_uri,
                            predicate=f"{self.WOC_NS}hasParameter",
                            object=param_uri
                        ),
                        GraphTriple(
                            subject=param_uri,
                            predicate=f"{self.RDF_NS}type",
                            object=f"{self.WOC_NS}Parameter"
                        ),
                        GraphTriple(
                            subject=param_uri,
                            predicate=f"{self.WOC_NS}hasName",
                            object=self._literal(param.name)
                        ),
                        GraphTriple(
                            subject=param_uri,
                            predicate=f"{self.WOC_NS}parameterOrder",
                            object=self._literal(str(i))
                        ),
                        GraphTriple(
                            subject=param_uri,
                            predicate=f"{self.WOC_NS}isRequired",
                            object=self._literal(str(param.is_required).lower())
                        )
                    ])
                    
                    if param.type_annotation:
                        triples.append(GraphTriple(
                            subject=param_uri,
                            predicate=f"{self.WOC_NS}hasType",
                            object=self._literal(param.type_annotation)
                        ))
                    
                    if param.default_value is not None:
                        triples.append(GraphTriple(
                            subject=param_uri,
                            predicate=f"{self.WOC_NS}hasDefault",
                            object=self._literal(param.default_value)
                        ))
                
                # Add return type if present
                if func.return_type:
                    triples.append(GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}returnsType",
                        object=self._literal(func.return_type)
                    ))
                
                # Add decorators
                for decorator in func.decorators:
                    decorator_uri = f"{impl_uri}/decorator/{self._sanitize_uri(decorator)}"
                    triples.extend([
                        GraphTriple(
                            subject=impl_uri,
                            predicate=f"{self.WOC_NS}hasDecorator",
                            object=decorator_uri
                        ),
                        GraphTriple(
                            subject=decorator_uri,
                            predicate=f"{self.WOC_NS}decoratorName",
                            object=self._literal(decorator)
                        )
                    ])
                
                # Add async flag
                if func.is_async:
                    triples.append(GraphTriple(
                        subject=impl_uri,
                        predicate=f"{self.WOC_NS}isAsync",
                        object=self._literal("true")
                    ))
        
        self.logger.info(f"💊 Built implementation graph: {len(triples)} triples")
        
        return BuiltGraph(
            uri=graph_uri,
            triples=triples,
            description=f"Implementation details for {org}/{repo} {release}"
        )
    
    async def _build_file_structure_graph(self, parsed_repo: ParsedRepository,
                                        org: str, repo: str, release: str) -> BuiltGraph:
        """
        📁 Build the file structure graph with GitHub links! 📁
        
        This maps out the maze structure - where each dot lives in the codebase!
        """
        graph_uri = GraphSchemas.get_files_uri(org, repo, release)
        triples = []
        
        for file in parsed_repo.files:
            file_uri = self._get_file_uri(org, repo, release, str(file.path))
            
            # Basic file info
            triples.extend([
                GraphTriple(
                    subject=file_uri,
                    predicate=f"{self.RDF_NS}type",
                    object=f"{self.WOC_NS}PythonFile"
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate=f"{self.WOC_NS}path",
                    object=self._literal(str(file.path))
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate=f"{self.WOC_NS}relativePath",
                    object=self._literal(file.path.name)
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate=f"{self.WOC_NS}githubUrl",
                    object=self._literal(f"https://github.com/{org}/{repo}/blob/{release}/{file.path}")
                ),
                GraphTriple(
                    subject=file_uri,
                    predicate=f"{self.WOC_NS}lineCount",
                    object=self._literal(str(file.line_count))
                )
            ])
            
            # Link functions to file
            for func in file.functions:
                impl_uri = self._get_implementation_uri(org, repo, func.name, release)
                triples.append(GraphTriple(
                    subject=file_uri,
                    predicate=f"{self.WOC_NS}containsFunction",
                    object=impl_uri
                ))
        
        self.logger.info(f"📁 Built file structure graph: {len(triples)} triples")
        
        return BuiltGraph(
            uri=graph_uri,
            triples=triples,
            description=f"File structure for {org}/{repo} {release}"
        )
    
    def map_python_ast_to_woc(self, parsed_file: ParsedFile) -> List[GraphTriple]:
        """
        🔮 Helper method: Map Python AST to Web of Code ontology 🔮
        
        Direct mapping helper for specific use cases.
        """
        triples = []
        
        # This is implemented in the main mapping methods above
        # Could be used for specific per-file mappings if needed
        
        return triples
    
    def generate_proper_rdf_triples(self, function_info: FunctionInfo, 
                                  base_uri: str) -> List[GraphTriple]:
        """
        🔮 Generate RDF triples for a single function 🔮
        
        Helper method for generating triples for individual functions.
        """
        triples = []
        func_uri = f"{base_uri}/{self._sanitize_uri(function_info.name)}"
        
        # Basic function triples
        triples.extend([
            GraphTriple(
                subject=func_uri,
                predicate=f"{self.RDF_NS}type",
                object=f"{self.WOC_NS}Function"
            ),
            GraphTriple(
                subject=func_uri,
                predicate=f"{self.WOC_NS}hasName",
                object=self._literal(function_info.name)
            ),
            GraphTriple(
                subject=func_uri,
                predicate=f"{self.WOC_NS}hasSignature",
                object=self._literal(function_info.signature)
            )
        ])
        
        return triples
    
    def handle_function_signatures_parameters_types(self, func: FunctionInfo) -> List[GraphTriple]:
        """
        🔧 Handle function signatures, parameters, and types 🔧
        
        Specialized method for detailed parameter and type handling.
        """
        triples = []
        
        # This functionality is implemented in _build_implementation_graph
        # This method provides the interface for specific parameter handling
        
        return triples
    
    # Helper methods for URI generation and formatting
    
    def _get_stable_function_uri(self, org: str, repo: str, func_name: str) -> str:
        """Generate stable function identity URI"""
        return f"function:{org}/{repo}/{func_name}"
    
    def _get_implementation_uri(self, org: str, repo: str, func_name: str, release: str) -> str:
        """Generate implementation-specific URI"""
        return f"function:{org}/{repo}/{func_name}#{release}"
    
    def _get_file_uri(self, org: str, repo: str, release: str, file_path: str) -> str:
        """Generate file URI"""
        sanitized_path = self._sanitize_uri(file_path)
        return f"file:{org}/{repo}/{release}/{sanitized_path}"
    
    def _literal(self, value: str) -> str:
        """Wrap value as RDF literal"""
        # Escape quotes and format as literal
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    
    def _sanitize_uri(self, value: str) -> str:
        """Sanitize string for use in URI"""
        # Replace problematic characters for URIs
        return value.replace('/', '_').replace(' ', '_').replace('.', '_')


# 🔮 PAC-MAN's Semantic Factory! 🔮
def create_ontology_mapper() -> OntologyMapper:
    """Factory function to create PAC-MAN's ontology mapper!"""
    return OntologyMapper()
