"""
🏗️ PAC-MAN's Query Builder 🏗️

This is PAC-MAN's query construction workshop - building custom SPARQL
queries dynamically for semantic maze exploration!

WAKA WAKA! Building the perfect maze navigation routes!
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class QueryType(str, Enum):
    """🏗️ Types of queries PAC-MAN can build"""
    SELECT = "SELECT"
    CONSTRUCT = "CONSTRUCT"
    ASK = "ASK"
    DESCRIBE = "DESCRIBE"


class FilterOperator(str, Enum):
    """🏗️ Filter operators for query conditions"""
    EQUALS = "="
    NOT_EQUALS = "!="
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STRSTARTS"
    ENDS_WITH = "STRENDS"
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    REGEX = "REGEX"


@dataclass
class QueryVariable:
    """🏗️ A SPARQL variable in PAC-MAN's query"""
    name: str
    optional: bool = False
    description: str = ""


@dataclass
class QueryFilter:
    """🏗️ A filter condition in PAC-MAN's query"""
    variable: str
    operator: FilterOperator
    value: str
    case_sensitive: bool = True


@dataclass
class QueryTriple:
    """🏗️ A triple pattern in PAC-MAN's query"""
    subject: str
    predicate: str
    object: str
    optional: bool = False


class QueryBuilder:
    """🏗️ PAC-MAN's SPARQL Query Construction Workshop!"""
    
    def __init__(self):
        """🟡 Initialize PAC-MAN's query builder"""
        self.query_type = QueryType.SELECT
        self.prefixes: Dict[str, str] = {
            "woc": "http://rdf.webofcode.org/woc/",
            "git": "http://Repolex.org/ontology/git/",
            "abc": "http://Repolex.org/ontology/evolution/",
            "files": "http://Repolex.org/ontology/files/"
        }
        self.variables: List[QueryVariable] = []
        self.triples: List[QueryTriple] = []
        self.filters: List[QueryFilter] = []
        self.order_by: List[str] = []
        self.group_by: List[str] = []
        self.limit: Optional[int] = None
        self.offset: Optional[int] = None
        
        logger.debug("🟡 PAC-MAN Query Builder initialized - ready to build maze routes!")
    
    def select(self, *variables: str) -> 'QueryBuilder':
        """🟡 Add variables to SELECT clause"""
        self.query_type = QueryType.SELECT
        for var in variables:
            if not var.startswith('?'):
                var = f"?{var}"
            self.variables.append(QueryVariable(var))
        return self
    
    def add_prefix(self, prefix: str, uri: str) -> 'QueryBuilder':
        """🟡 Add a custom prefix"""
        self.prefixes[prefix] = uri
        return self
    
    def where(self, subject: str, predicate: str, obj: str, optional: bool = False) -> 'QueryBuilder':
        """🟡 Add a triple pattern to WHERE clause"""
        # Auto-add ? to variables if needed
        if not subject.startswith(('?', '<', '"') and ':' not in subject:
            subject = f"?{subject}"
        if not obj.startswith(('?', '<', '"') and ':' not in obj and not obj.isdigit():
            obj = f"?{obj}"
            
        self.triples.append(QueryTriple(subject, predicate, obj, optional))
        return self
    
    def optional_where(self, subject: str, predicate: str, obj: str) -> 'QueryBuilder':
        """🟡 Add an optional triple pattern"""
        return self.where(subject, predicate, obj, optional=True)
    
    def filter(self, variable: str, operator: FilterOperator, value: str, case_sensitive: bool = True) -> 'QueryBuilder':
        """🟡 Add a filter condition"""
        if not variable.startswith('?'):
            variable = f"?{variable}"
        self.filters.append(QueryFilter(variable, operator, value, case_sensitive))
        return self
    
    def filter_contains(self, variable: str, value: str, case_sensitive: bool = False) -> 'QueryBuilder':
        """🟡 Convenient filter for contains"""
        return self.filter(variable, FilterOperator.CONTAINS, value, case_sensitive)
    
    def filter_equals(self, variable: str, value: str) -> 'QueryBuilder':
        """🟡 Convenient filter for equals"""
        return self.filter(variable, FilterOperator.EQUALS, value)
    
    def filter_regex(self, variable: str, pattern: str, case_sensitive: bool = False) -> 'QueryBuilder':
        """🟡 Convenient filter for regex"""
        return self.filter(variable, FilterOperator.REGEX, pattern, case_sensitive)
    
    def order_by_asc(self, variable: str) -> 'QueryBuilder':
        """🟡 Order results ascending"""
        if not variable.startswith('?'):
            variable = f"?{variable}"
        self.order_by.append(variable)
        return self
    
    def order_by_desc(self, variable: str) -> 'QueryBuilder':
        """🟡 Order results descending"""
        if not variable.startswith('?'):
            variable = f"?{variable}"
        self.order_by.append(f"DESC({variable})")
        return self
    
    def limit_results(self, limit: int) -> 'QueryBuilder':
        """🟡 Limit number of results"""
        self.limit = limit
        return self
    
    def offset_results(self, offset: int) -> 'QueryBuilder':
        """🟡 Skip results"""
        self.offset = offset
        return self
    
    def group_by_variable(self, variable: str) -> 'QueryBuilder':
        """🟡 Group results by variable"""
        if not variable.startswith('?'):
            variable = f"?{variable}"
        self.group_by.append(variable)
        return self
    
    def build(self) -> str:
        """🟡 Build the final SPARQL query - PAC-MAN's masterpiece!"""
        query_parts = []
        
        # Add prefixes
        for prefix, uri in self.prefixes.items():
            query_parts.append(f"PREFIX {prefix}: <{uri}>")
        
        query_parts.append("")  # Empty line after prefixes
        
        # Add SELECT clause
        if self.query_type == QueryType.SELECT:
            if self.variables:
                vars_str = " ".join(var.name for var in self.variables)
            else:
                vars_str = "*"
            query_parts.append(f"SELECT {vars_str} WHERE {{")
        
        # Add WHERE clause triples
        optional_triples = []
        regular_triples = []
        
        for triple in self.triples:
            triple_str = f"    {triple.subject} {triple.predicate} {triple.object} ."
            if triple.optional:
                optional_triples.append(triple_str)
            else:
                regular_triples.append(triple_str)
        
        # Add regular triples first
        query_parts.extend(regular_triples)
        
        # Add optional triples in OPTIONAL blocks
        for opt_triple in optional_triples:
            query_parts.append("    OPTIONAL {")
            query_parts.append(f"        {opt_triple.strip()}")
            query_parts.append("    }")
        
        # Add filters
        if self.filters:
            for filter_cond in self.filters:
                filter_str = self._build_filter(filter_cond)
                query_parts.append(f"    FILTER({filter_str})")
        
        query_parts.append("}")
        
        # Add GROUP BY
        if self.group_by:
            group_vars = " ".join(self.group_by)
            query_parts.append(f"GROUP BY {group_vars}")
        
        # Add ORDER BY
        if self.order_by:
            order_vars = " ".join(self.order_by)
            query_parts.append(f"ORDER BY {order_vars}")
        
        # Add LIMIT
        if self.limit:
            query_parts.append(f"LIMIT {self.limit}")
        
        # Add OFFSET
        if self.offset:
            query_parts.append(f"OFFSET {self.offset}")
        
        query = "\n".join(query_parts)
        logger.debug(f"🟡 PAC-MAN built query:\n{query}")
        return query
    
    def _build_filter(self, filter_cond: QueryFilter) -> str:
        """🟡 Build a filter condition string"""
        var = filter_cond.variable
        op = filter_cond.operator
        val = filter_cond.value
        
        # Handle string values
        if not val.startswith(('"', "'", "?")) and not val.isdigit():
            val = f'"{val}"'
        
        if op == FilterOperator.CONTAINS:
            if filter_cond.case_sensitive:
                return f"CONTAINS({var}, {val})"
            else:
                return f"CONTAINS(LCASE({var}), LCASE({val}))"
        elif op == FilterOperator.STARTS_WITH:
            return f"STRSTARTS({var}, {val})"
        elif op == FilterOperator.ENDS_WITH:
            return f"STRENDS({var}, {val})"
        elif op == FilterOperator.REGEX:
            flags = "" if filter_cond.case_sensitive else ", \"i\""
            return f"REGEX({var}, {val}{flags})"
        else:
            return f"{var} {op.value} {val}"


class FunctionQueryBuilder(QueryBuilder):
    """🟡 Specialized query builder for function queries"""
    
    def __init__(self):
        super().__init__()
        # Start with common function variables
        self.select("function", "name", "module")
        self.where("function", "a", "woc:Function")
        self.where("function", "woc:canonicalName", "name")
        self.where("function", "woc:module", "module")
    
    def with_signature(self) -> 'FunctionQueryBuilder':
        """🟡 Include function signature"""
        self.select("signature")
        self.where("function", "woc:signature", "signature")
        return self
    
    def with_parameters(self) -> 'FunctionQueryBuilder':
        """🟡 Include parameter information"""
        self.select("paramCount")
        self.optional_where("function", "woc:parameterCount", "paramCount")
        return self
    
    def with_complexity(self) -> 'FunctionQueryBuilder':
        """🟡 Include complexity metrics"""
        self.select("complexity")
        self.optional_where("function", "woc:cyclomaticComplexity", "complexity")
        return self
    
    def in_module(self, module_pattern: str) -> 'FunctionQueryBuilder':
        """🟡 Filter by module pattern"""
        self.filter_contains("module", module_pattern)
        return self
    
    def with_name_pattern(self, pattern: str) -> 'FunctionQueryBuilder':
        """🟡 Filter by name pattern"""
        self.filter_contains("name", pattern)
        return self


class GitQueryBuilder(QueryBuilder):
    """👻 Specialized query builder for git intelligence queries"""
    
    def __init__(self):
        super().__init__()
        self.select("commit", "author", "timestamp")
        self.where("commit", "git:author", "author")
        self.where("commit", "git:timestamp", "timestamp")
    
    def by_author(self, author_email: str) -> 'GitQueryBuilder':
        """👻 Filter commits by author"""
        self.filter_equals("author", author_email)
        return self
    
    def affecting_function(self, function_name: str) -> 'GitQueryBuilder':
        """👻 Find commits affecting a specific function"""
        self.where("commit", "git:modifies", "function")
        self.where("function", "woc:canonicalName", f'"{function_name}"')
        return self
    
    def in_date_range(self, start_date: str, end_date: str) -> 'GitQueryBuilder':
        """👻 Filter by date range"""
        self.filter("timestamp", FilterOperator.GREATER_EQUAL, f'"{start_date}"')
        self.filter("timestamp", FilterOperator.LESS_EQUAL, f'"{end_date}"')
        return self


# Convenience functions for common query patterns

def find_functions_by_name(name_pattern: str, limit: int = 20) -> str:
    """🟡 Quick function name search"""
    return (FunctionQueryBuilder()
            .with_name_pattern(name_pattern)
            .with_signature()
            .order_by_asc("name")
            .limit_results(limit)
            .build())


def find_functions_in_module(module_pattern: str, limit: int = 50) -> str:
    """🟡 Quick module function search"""
    return (FunctionQueryBuilder()
            .in_module(module_pattern)
            .with_signature()
            .with_complexity()
            .order_by_asc("name")
            .limit_results(limit)
            .build())


def find_commits_by_author(author_email: str, limit: int = 100) -> str:
    """👻 Quick author commit search"""
    return (GitQueryBuilder()
            .by_author(author_email)
            .order_by_desc("timestamp")
            .limit_results(limit)
            .build())


def find_complex_functions(min_complexity: int = 10, limit: int = 20) -> str:
    """🧠 Quick complexity search"""
    return (FunctionQueryBuilder()
            .with_complexity()
            .filter("complexity", FilterOperator.GREATER_THAN, str(min_complexity))
            .order_by_desc("complexity")
            .limit_results(limit)
            .build())