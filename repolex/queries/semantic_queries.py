"""
🔮 PAC-MAN's Pre-built Semantic Queries 🔮

This is PAC-MAN's collection of favorite maze navigation routes!
Pre-built SPARQL queries for common semantic code intelligence tasks.

WAKA WAKA! The greatest hits of semantic exploration!
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SemanticQuery:
    """🔮 A pre-built semantic query with PAC-MAN power!"""
    name: str
    description: str
    sparql: str
    parameters: List[str]
    example_params: Dict[str, str]


class SemanticQueries:
    """🔮 PAC-MAN's library of semantic maze navigation queries!"""
    
    # Function discovery queries
    FIND_FUNCTIONS_BY_NAME = SemanticQuery(
        name="find_functions_by_name",
        description="🟡 Find functions by name pattern",
        sparql="""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?function ?name ?module ?signature WHERE {
            ?function a woc:Function ;
                     woc:canonicalName ?name ;
                     woc:module ?module ;
                     woc:signature ?signature .
            FILTER(CONTAINS(LCASE(?name), LCASE("{name_pattern}")))
        }
        ORDER BY ?name
        """,
        parameters=["name_pattern"],
        example_params={"name_pattern": "create"}
    )
    
    FIND_FUNCTIONS_BY_MODULE = SemanticQuery(
        name="find_functions_by_module",
        description="🟡 Find all functions in a specific module",
        sparql="""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?function ?name ?signature ?line_start WHERE {
            ?function a woc:Function ;
                     woc:canonicalName ?name ;
                     woc:module "{module_name}" ;
                     woc:signature ?signature ;
                     woc:lineStart ?line_start .
        }
        ORDER BY ?line_start
        """,
        parameters=["module_name"],
        example_params={"module_name": "pixeltable.core"}
    )
    
    # Class and inheritance queries
    FIND_CLASS_HIERARCHY = SemanticQuery(
        name="find_class_hierarchy",
        description="🟡 Find class inheritance hierarchy",
        sparql="""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?class ?className ?parent ?parentName WHERE {
            ?class a woc:Class ;
                  woc:canonicalName ?className .
            OPTIONAL {
                ?class woc:inheritsFrom ?parent .
                ?parent woc:canonicalName ?parentName .
            }
            FILTER(CONTAINS(LCASE(?className), LCASE("{class_pattern}")))
        }
        ORDER BY ?className
        """,
        parameters=["class_pattern"],
        example_params={"class_pattern": "Table"}
    )
    
    # Git intelligence queries
    FIND_MOST_CHANGED_FUNCTIONS = SemanticQuery(
        name="find_most_changed_functions",
        description="👻 Find functions that change most frequently",
        sparql="""
        PREFIX git: <http://repolex.org/ontology/git/>
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?function ?name ?changeCount WHERE {
            ?function a woc:Function ;
                     woc:canonicalName ?name .
            {
                SELECT ?function (COUNT(?commit) as ?changeCount) WHERE {
                    ?commit git:modifies ?function .
                }
                GROUP BY ?function
            }
        }
        ORDER BY DESC(?changeCount)
        LIMIT 20
        """,
        parameters=[],
        example_params={}
    )
    
    FIND_DEVELOPER_EXPERTISE = SemanticQuery(
        name="find_developer_expertise",
        description="👻 Find what areas a developer specializes in",
        sparql="""
        PREFIX git: <http://repolex.org/ontology/git/>
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?module (COUNT(?commit) as ?commitCount) WHERE {
            ?commit git:author "{developer_email}" ;
                   git:modifies ?function .
            ?function woc:module ?module .
        }
        GROUP BY ?module
        ORDER BY DESC(?commitCount)
        """,
        parameters=["developer_email"],
        example_params={"developer_email": "developer@example.com"}
    )
    
    # Evolution and change analysis
    FIND_FUNCTION_EVOLUTION = SemanticQuery(
        name="find_function_evolution",
        description="⏰ Track how a function has evolved over time",
        sparql="""
        PREFIX abc: <http://repolex.org/ontology/evolution/>
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?event ?eventType ?timestamp ?release WHERE {
            ?function woc:canonicalName "{function_name}" .
            ?event abc:affects ?function ;
                  abc:changeType ?eventType ;
                  abc:timestamp ?timestamp ;
                  abc:releaseTo ?release .
        }
        ORDER BY ?timestamp
        """,
        parameters=["function_name"],
        example_params={"function_name": "create_table"}
    )
    
    # Complexity and quality queries
    FIND_COMPLEX_FUNCTIONS = SemanticQuery(
        name="find_complex_functions",
        description="🧠 Find functions with high complexity",
        sparql="""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?function ?name ?module ?complexity WHERE {
            ?function a woc:Function ;
                     woc:canonicalName ?name ;
                     woc:module ?module ;
                     woc:cyclomaticComplexity ?complexity .
            FILTER(?complexity > {min_complexity})
        }
        ORDER BY DESC(?complexity)
        """,
        parameters=["min_complexity"],
        example_params={"min_complexity": "10"}
    )
    
    # Cross-repository queries
    FIND_SIMILAR_FUNCTIONS = SemanticQuery(
        name="find_similar_functions",
        description="🔍 Find functions with similar signatures",
        sparql="""
        PREFIX woc: <http://rdf.webofcode.org/woc/>
        SELECT ?function1 ?name1 ?function2 ?name2 ?signature WHERE {
            ?function1 woc:canonicalName ?name1 ;
                      woc:signature ?signature .
            ?function2 woc:canonicalName ?name2 ;
                      woc:signature ?signature .
            FILTER(?function1 != ?function2)
            FILTER(CONTAINS(?signature, "{signature_pattern}"))
        }
        ORDER BY ?signature
        """,
        parameters=["signature_pattern"],
        example_params={"signature_pattern": "def create_"}
    )
    
    @classmethod
    def get_all_queries(cls) -> List[SemanticQuery]:
        """🟡 Get all pre-built queries"""
        queries = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, SemanticQuery):
                queries.append(attr)
        return queries
    
    @classmethod
    def get_query_by_name(cls, name: str) -> Optional[SemanticQuery]:
        """🟡 Get a specific query by name"""
        for query in cls.get_all_queries():
            if query.name == name:
                return query
        return None
    
    @classmethod
    def list_query_names(cls) -> List[str]:
        """🟡 List all available query names"""
        return [query.name for query in cls.get_all_queries()]


def format_query(query: SemanticQuery, params: Dict[str, str]) -> str:
    """🟡 Format a query with parameters - PAC-MAN's query formatter!"""
    sparql = query.sparql
    for param_name, param_value in params.items():
        if param_name in query.parameters:
            sparql = sparql.replace(f"{{{param_name}}}", param_value)
        else:
            logger.warning(f"🟠 Parameter {param_name} not found in query {query.name}")
    
    return sparql


def validate_query_params(query: SemanticQuery, params: Dict[str, str]) -> List[str]:
    """🟡 Validate query parameters - PAC-MAN's param checker!"""
    errors = []
    
    for required_param in query.parameters:
        if required_param not in params:
            errors.append(f"Missing required parameter: {required_param}")
    
    for provided_param in params.keys():
        if provided_param not in query.parameters:
            errors.append(f"Unknown parameter: {provided_param}")
    
    return errors