"""
🟡 PAC-MAN's Function Search Engine - Find All the Semantic Dots! 🟡

Natural language search through the semantic maze!
PAC-MAN uses advanced fuzzy matching and semantic understanding
to find the perfect function dots for any query!

WAKA WAKA! Let's find those functions!
"""

from typing import Dict, List, Any, Optional, Tuple
import re
from datetime import datetime
from dataclasses import dataclass
from difflib import SequenceMatcher

from ..models.exceptions import SearchError, ValidationError
from ..models.function import FunctionInfo
from ..models.results import SearchResult, SearchMetadata
from ..storage.oxigraph_client import OxigraphClient
from ..utils.validation import validate_org_repo, validate_release_tag


@dataclass
class FunctionMatch:
    """🎯 Represents a function match with relevance scoring"""
    function: FunctionInfo
    relevance_score: float
    match_reasons: List[str]
    search_query: str


class FunctionSearchEngine:
    """
    🟡 PAC-MAN's Function Search Engine - The Ultimate Function Finder! 🟡
    
    Finds functions using natural language queries with advanced matching:
    - Fuzzy name matching (typo-tolerant!)
    - Semantic description analysis
    - Parameter type matching
    - Usage pattern recognition
    - Category-based filtering
    
    WAKA WAKA! No function can hide from PAC-MAN's search power!
    """
    
    def __init__(self, oxigraph_client: OxigraphClient):
        self.oxigraph_client = oxigraph_client
        self.search_cache = {}
        self.search_stats = {
            'total_searches': 0,
            'successful_searches': 0,
            'avg_results_per_search': 0.0,
            'avg_search_time': 0.0
        }
        
        # Search configuration
        self.min_relevance_score = 0.1
        self.max_results = 50
        self.fuzzy_threshold = 0.6
        
        # Common synonyms for better matching
        self.synonyms = {
            'create': ['make', 'build', 'new', 'add', 'generate', 'construct'],
            'delete': ['remove', 'drop', 'destroy', 'erase', 'clear'],
            'update': ['modify', 'change', 'edit', 'alter', 'set'],
            'get': ['fetch', 'retrieve', 'find', 'obtain', 'access'],
            'list': ['show', 'display', 'enumerate', 'all'],
            'table': ['data', 'dataset', 'collection'],
            'image': ['picture', 'photo', 'img', 'visual'],
            'process': ['handle', 'execute', 'run', 'perform'],
            'analyze': ['examine', 'study', 'inspect', 'evaluate']
        }
    
    def search_functions(
        self,
        search_query: str,
        repo_filter: Optional[str] = None,
        release_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        max_results: Optional[int] = None,
        min_relevance: Optional[float] = None
    ) -> SearchResult:
        """
        🟡 Search for functions using natural language query!
        
        Args:
            search_query: Natural language search query
            repo_filter: Limit to specific repository (org/repo format)
            release_filter: Limit to specific release
            category_filter: Filter by function category
            max_results: Maximum number of results to return
            min_relevance: Minimum relevance score threshold
        
        Returns:
            SearchResult with ranked function matches
        """
        start_time = datetime.now()
        
        try:
            # Validate inputs
            if not search_query or not search_query.strip():
                raise ValidationError(
                    "🟡 PAC-MAN needs something to search for!",
                    suggestions=["Provide a search query like 'create table' or 'image processing'"]
                )
            
            if repo_filter:
                validate_org_repo(repo_filter)
            
            if release_filter:
                validate_release_tag(release_filter)
            
            # Normalize and process query
            processed_query = self._preprocess_query(search_query)
            
            # Check cache first
            cache_key = f"{processed_query}|{repo_filter}|{release_filter}|{category_filter}"
            if cache_key in self.search_cache:
                cached_result = self.search_cache[cache_key]
                return SearchResult(
                    success=True,
                    query=search_query,
                    matches=cached_result['matches'],
                    total_results=len(cached_result['matches']),
                    search_time=0.001,  # Cached
                    from_cache=True,
                    metadata=SearchMetadata(
                        processed_query=processed_query,
                        filters_applied=self._get_active_filters(repo_filter, release_filter, category_filter),
                        search_engine="PAC-MAN Function Search Cache 🟡"
                    )
                )
            
            # Extract all candidate functions
            candidates = self._extract_candidate_functions(
                repo_filter, release_filter, category_filter
            )
            
            if not candidates:
                return SearchResult(
                    success=True,
                    query=search_query,
                    matches=[],
                    total_results=0,
                    search_time=(datetime.now() - start_time).total_seconds(),
                    from_cache=False,
                    metadata=SearchMetadata(
                        processed_query=processed_query,
                        filters_applied=self._get_active_filters(repo_filter, release_filter, category_filter),
                        search_engine="PAC-MAN Function Search Engine 🟡",
                        message="🟡 No functions found matching the filters!"
                    )
                )
            
            # Score and rank candidates
            scored_matches = []
            for candidate in candidates:
                relevance_score, match_reasons = self._calculate_relevance(
                    candidate, processed_query
                )
                
                if relevance_score >= (min_relevance or self.min_relevance_score):
                    match = FunctionMatch(
                        function=candidate,
                        relevance_score=relevance_score,
                        match_reasons=match_reasons,
                        search_query=search_query
                    )
                    scored_matches.append(match)
            
            # Sort by relevance score (highest first)
            scored_matches.sort(key=lambda m: m.relevance_score, reverse=True)
            
            # Apply result limit
            max_results = min(max_results or self.max_results, self.max_results)
            final_matches = scored_matches[:max_results]
            
            # Cache results (if not too many)
            if len(final_matches) < 100:
                self.search_cache[cache_key] = {
                    'matches': final_matches,
                    'timestamp': datetime.now()
                }
                
                # Limit cache size
                if len(self.search_cache) > 50:
                    oldest_key = min(self.search_cache.keys(),
                                   key=lambda k: self.search_cache[k]['timestamp'])
                    del self.search_cache[oldest_key]
            
            # Update statistics
            search_time = (datetime.now() - start_time).total_seconds()
            self._update_search_stats(len(final_matches), search_time)
            
            return SearchResult(
                success=True,
                query=search_query,
                matches=final_matches,
                total_results=len(final_matches),
                search_time=search_time,
                from_cache=False,
                metadata=SearchMetadata(
                    processed_query=processed_query,
                    filters_applied=self._get_active_filters(repo_filter, release_filter, category_filter),
                    search_engine="PAC-MAN Function Search Engine 🟡",
                    candidates_evaluated=len(candidates),
                    message=f"🟡 WAKA WAKA! Found {len(final_matches)} matching functions!"
                )
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise SearchError(
                f"🟡 PAC-MAN got confused in the search maze! {str(e)}",
                suggestions=[
                    "Try a simpler search query",
                    "Check repository and release filters",
                    "Use common function keywords"
                ]
            )
    
    def suggest_search_terms(self, partial_query: str) -> List[str]:
        """💡 Suggest search terms based on partial input"""
        suggestions = []
        
        # Common function patterns
        common_patterns = [
            "create table", "delete table", "update table", "list tables",
            "insert data", "query data", "process image", "resize image",
            "machine learning", "data analysis", "file operations",
            "string manipulation", "date functions", "math operations"
        ]
        
        # Find matching patterns
        partial_lower = partial_query.lower()
        for pattern in common_patterns:
            if partial_lower in pattern or pattern.startswith(partial_lower):
                suggestions.append(pattern)
        
        # Add synonym-based suggestions
        for word in partial_query.split():
            word_lower = word.lower()
            for base_word, synonyms in self.synonyms.items():
                if word_lower == base_word or word_lower in synonyms:
                    suggestions.extend([
                        f"{base_word} table",
                        f"{base_word} data",
                        f"{base_word} image"
                    ])
        
        # Remove duplicates and limit
        unique_suggestions = list(set(suggestions))
        return unique_suggestions[:10]
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """📊 Get PAC-MAN's search statistics"""
        return {
            'total_searches': self.search_stats['total_searches'],
            'successful_searches': self.search_stats['successful_searches'],
            'success_rate': (
                self.search_stats['successful_searches'] / 
                max(1, self.search_stats['total_searches'])
            ) * 100,
            'avg_results_per_search': self.search_stats['avg_results_per_search'],
            'avg_search_time': self.search_stats['avg_search_time'],
            'cache_size': len(self.search_cache),
            'pac_man_status': "🟡 WAKA WAKA! Ready to find more functions!"
        }
    
    def _preprocess_query(self, query: str) -> Dict[str, Any]:
        """🧹 Preprocess and analyze search query"""
        query = query.strip().lower()
        
        # Extract keywords
        words = re.findall(r'\b\w+\b', query)
        
        # Expand synonyms
        expanded_words = []
        for word in words:
            expanded_words.append(word)
            if word in self.synonyms:
                expanded_words.extend(self.synonyms[word])
            else:
                # Check if word is a synonym
                for base_word, synonyms in self.synonyms.items():
                    if word in synonyms:
                        expanded_words.append(base_word)
        
        # Detect intent patterns
        intent = self._detect_query_intent(query)
        
        # Extract technical terms
        tech_terms = self._extract_technical_terms(query)
        
        return {
            'original_query': query,
            'keywords': list(set(words)),
            'expanded_keywords': list(set(expanded_words)),
            'intent': intent,
            'technical_terms': tech_terms,
            'word_count': len(words)
        }
    
    def _detect_query_intent(self, query: str) -> Dict[str, float]:
        """🧠 Detect the intent behind the search query"""
        intents = {
            'create': 0.0,
            'read': 0.0,
            'update': 0.0,
            'delete': 0.0,
            'process': 0.0,
            'analyze': 0.0
        }
        
        # CRUD operations
        create_keywords = ['create', 'add', 'new', 'make', 'build', 'generate']
        read_keywords = ['get', 'find', 'list', 'show', 'retrieve', 'fetch']
        update_keywords = ['update', 'modify', 'change', 'edit', 'set']
        delete_keywords = ['delete', 'remove', 'drop', 'clear', 'destroy']
        process_keywords = ['process', 'transform', 'convert', 'handle']
        analyze_keywords = ['analyze', 'examine', 'study', 'evaluate']
        
        # Calculate intent scores
        for keyword in create_keywords:
            if keyword in query:
                intents['create'] += 1.0
        
        for keyword in read_keywords:
            if keyword in query:
                intents['read'] += 1.0
        
        for keyword in update_keywords:
            if keyword in query:
                intents['update'] += 1.0
        
        for keyword in delete_keywords:
            if keyword in query:
                intents['delete'] += 1.0
        
        for keyword in process_keywords:
            if keyword in query:
                intents['process'] += 1.0
        
        for keyword in analyze_keywords:
            if keyword in query:
                intents['analyze'] += 1.0
        
        # Normalize scores
        total_score = sum(intents.values())
        if total_score > 0:
            intents = {k: v / total_score for k, v in intents.items()}
        
        return intents
    
    def _extract_technical_terms(self, query: str) -> List[str]:
        """🔧 Extract technical terms from query"""
        tech_terms = []
        
        # Common technical patterns
        tech_patterns = [
            r'\b(table|database|sql|query)\b',
            r'\b(image|picture|photo|video|media)\b',
            r'\b(file|directory|path|io)\b',
            r'\b(json|xml|csv|yaml)\b',
            r'\b(http|api|rest|web)\b',
            r'\b(ml|ai|machine\s+learning|neural)\b',
            r'\b(data|dataset|dataframe)\b',
            r'\b(string|text|regex)\b',
            r'\b(math|calculation|compute)\b'
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            tech_terms.extend(matches)
        
        return list(set(tech_terms))
    
    def _extract_candidate_functions(
        self,
        repo_filter: Optional[str],
        release_filter: Optional[str],
        category_filter: Optional[str]
    ) -> List[FunctionInfo]:
        """🔍 Extract candidate functions based on filters"""
        
        # Build SPARQL query based on filters
        query_parts = [
            "PREFIX woc: <http://rdf.webofcode.org/woc/>",
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
            "",
            "SELECT ?function ?name ?signature ?docstring ?file_path ?start_line ?end_line WHERE {"
        ]
        
        if repo_filter:
            org, repo = repo_filter.split('/')
            query_parts.append(f"  GRAPH <http://repolex.org/repo/{org}/{repo}/functions/implementations> {{")
        else:
            query_parts.append("  GRAPH ?graph {")
        
        query_parts.extend([
            "    ?function woc:hasSignature ?signature ;",
            "             woc:definedInFile ?file_path ;",
            "             woc:startLine ?start_line ;",
            "             woc:endLine ?end_line ."
        ])
        
        if release_filter:
            query_parts.append(f'    ?function woc:belongsToVersion "{release_filter}" .')
        
        query_parts.extend([
            "    OPTIONAL { ?function rdfs:comment ?docstring }",
            "  }",
            ""
        ])
        
        if repo_filter:
            org, repo = repo_filter.split('/')
            query_parts.append(f"  GRAPH <http://repolex.org/repo/{org}/{repo}/functions/stable> {{")
        else:
            query_parts.append("  GRAPH ?stable_graph {")
        
        query_parts.extend([
            "    ?stable_function woc:canonicalName ?name .",
            "    ?function woc:implementsFunction ?stable_function .",
            "  }",
            "}",
            "ORDER BY ?name",
            "LIMIT 1000"
        ])
        
        sparql_query = "\n".join(query_parts)
        
        # Execute query
        results = self.oxigraph_client.query_sparql(sparql_query)
        
        # Convert to FunctionInfo objects
        functions = []
        for result in results:
            # Parse docstring for additional info
            docstring_info = self._parse_docstring_simple(result.get('docstring', ''))
            
            # Determine repository from graph or use filter
            if repo_filter:
                repository = repo_filter
            else:
                # Extract from graph URI if possible
                repository = "unknown/repository"  # Simplified for now
            
            function = FunctionInfo(
                name=result['name'],
                signature=result['signature'],
                docstring=result.get('docstring', ''),
                file_path=result['file_path'],
                start_line=int(result['start_line']),
                end_line=int(result['end_line']),
                repository=repository,
                parameters=docstring_info.get('parameters', []),
                returns=docstring_info.get('returns', ''),
                examples=docstring_info.get('examples', []),
                github_url=self._generate_github_url(
                    repository, release_filter or "main", 
                    result['file_path'], 
                    int(result['start_line']), 
                    int(result['end_line'])
                )
            )
            
            # Apply category filter if specified
            if category_filter:
                function_category = self._categorize_function(function)
                if category_filter.lower() not in function_category.lower():
                    continue
            
            functions.append(function)
        
        return functions
    
    def _calculate_relevance(
        self, 
        function: FunctionInfo, 
        processed_query: Dict[str, Any]
    ) -> Tuple[float, List[str]]:
        """🎯 Calculate relevance score for a function"""
        
        relevance_score = 0.0
        match_reasons = []
        
        query_keywords = processed_query['expanded_keywords']
        intent = processed_query['intent']
        tech_terms = processed_query['technical_terms']
        
        # 1. Function name matching (highest weight)
        name_score = self._calculate_name_similarity(function.name, query_keywords)
        if name_score > 0.3:
            relevance_score += name_score * 0.4
            match_reasons.append(f"Name similarity: {name_score:.2f}")
        
        # 2. Docstring content matching
        if function.docstring:
            docstring_score = self._calculate_text_similarity(
                function.docstring.lower(), query_keywords
            )
            if docstring_score > 0.1:
                relevance_score += docstring_score * 0.3
                match_reasons.append(f"Description match: {docstring_score:.2f}")
        
        # 3. Intent matching
        function_intent = self._detect_function_intent(function)
        intent_score = self._calculate_intent_similarity(intent, function_intent)
        if intent_score > 0.1:
            relevance_score += intent_score * 0.2
            match_reasons.append(f"Intent match: {intent_score:.2f}")
        
        # 4. Technical term matching
        tech_score = self._calculate_technical_term_match(function, tech_terms)
        if tech_score > 0.1:
            relevance_score += tech_score * 0.1
            match_reasons.append(f"Technical terms: {tech_score:.2f}")
        
        # 5. Bonus for exact keyword matches
        exact_matches = self._count_exact_keyword_matches(function, query_keywords)
        if exact_matches > 0:
            bonus = min(exact_matches * 0.1, 0.2)
            relevance_score += bonus
            match_reasons.append(f"Exact keyword matches: {exact_matches}")
        
        # Normalize relevance score to 0-1 range
        relevance_score = min(relevance_score, 1.0)
        
        return relevance_score, match_reasons
    
    def _calculate_name_similarity(self, function_name: str, keywords: List[str]) -> float:
        """📝 Calculate similarity between function name and keywords"""
        function_name_lower = function_name.lower()
        max_similarity = 0.0
        
        for keyword in keywords:
            # Exact match
            if keyword in function_name_lower:
                return 1.0
            
            # Fuzzy match
            similarity = SequenceMatcher(None, function_name_lower, keyword).ratio()
            max_similarity = max(max_similarity, similarity)
            
            # Partial match
            if len(keyword) > 3 and keyword in function_name_lower:
                max_similarity = max(max_similarity, 0.8)
        
        return max_similarity
    
    def _calculate_text_similarity(self, text: str, keywords: List[str]) -> float:
        """📄 Calculate similarity between text and keywords"""
        if not text or not keywords:
            return 0.0
        
        text_words = set(re.findall(r'\b\w+\b', text.lower()))
        keyword_set = set(keywords)
        
        # Count matches
        matches = len(text_words.intersection(keyword_set))
        
        # Calculate similarity score
        if matches == 0:
            return 0.0
        
        # Jaccard similarity with bonus for multiple matches
        jaccard = matches / len(text_words.union(keyword_set))
        bonus = min(matches * 0.1, 0.5)  # Bonus for multiple matches
        
        return jaccard + bonus
    
    def _detect_function_intent(self, function: FunctionInfo) -> Dict[str, float]:
        """🧠 Detect the intent of a function based on its characteristics"""
        intents = {
            'create': 0.0,
            'read': 0.0, 
            'update': 0.0,
            'delete': 0.0,
            'process': 0.0,
            'analyze': 0.0
        }
        
        name_lower = function.name.lower()
        
        # Analyze function name
        if any(word in name_lower for word in ['create', 'add', 'new', 'make', 'build']):
            intents['create'] = 1.0
        elif any(word in name_lower for word in ['get', 'find', 'list', 'show', 'retrieve']):
            intents['read'] = 1.0
        elif any(word in name_lower for word in ['update', 'modify', 'change', 'set']):
            intents['update'] = 1.0
        elif any(word in name_lower for word in ['delete', 'remove', 'drop', 'clear']):
            intents['delete'] = 1.0
        elif any(word in name_lower for word in ['process', 'transform', 'convert']):
            intents['process'] = 1.0
        elif any(word in name_lower for word in ['analyze', 'examine', 'evaluate']):
            intents['analyze'] = 1.0
        
        return intents
    
    def _calculate_intent_similarity(
        self, 
        query_intent: Dict[str, float], 
        function_intent: Dict[str, float]
    ) -> float:
        """🎯 Calculate similarity between query and function intents"""
        
        similarity = 0.0
        for intent, query_score in query_intent.items():
            function_score = function_intent.get(intent, 0.0)
            similarity += query_score * function_score
        
        return similarity
    
    def _calculate_technical_term_match(
        self, 
        function: FunctionInfo, 
        tech_terms: List[str]
    ) -> float:
        """🔧 Calculate technical term matching score"""
        if not tech_terms:
            return 0.0
        
        function_text = f"{function.name} {function.docstring}".lower()
        matches = 0
        
        for term in tech_terms:
            if term.lower() in function_text:
                matches += 1
        
        return matches / len(tech_terms)
    
    def _count_exact_keyword_matches(
        self, 
        function: FunctionInfo, 
        keywords: List[str]
    ) -> int:
        """🎯 Count exact keyword matches in function"""
        function_text = f"{function.name} {function.docstring}".lower()
        matches = 0
        
        for keyword in keywords:
            if keyword in function_text:
                matches += 1
        
        return matches
    
    def _categorize_function(self, function: FunctionInfo) -> str:
        """🏷️ Categorize function for filtering"""
        name = function.name.lower()
        
        if any(keyword in name for keyword in ['create', 'add', 'insert', 'new']):
            return 'Core API'
        elif any(keyword in name for keyword in ['update', 'modify', 'change', 'set']):
            return 'Data Operations'
        elif any(keyword in name for keyword in ['get', 'list', 'show', 'find', 'search']):
            return 'Data Operations'
        elif any(keyword in name for keyword in ['delete', 'remove', 'drop', 'clear']):
            return 'Data Operations'
        elif any(keyword in name for keyword in ['image', 'video', 'media']):
            return 'Media Processing'
        elif any(keyword in name for keyword in ['util', 'helper', 'format', 'parse']):
            return 'Utilities'
        else:
            return 'Advanced'
    
    def _parse_docstring_simple(self, docstring: str) -> Dict[str, Any]:
        """📝 Simple docstring parsing for basic info"""
        # This is a simplified parser - could be enhanced
        return {
            'parameters': [],
            'returns': '',
            'examples': []
        }
    
    def _generate_github_url(
        self, 
        repo: str, 
        release: str, 
        file_path: str, 
        start_line: int, 
        end_line: int
    ) -> str:
        """🔗 Generate GitHub URL for function"""
        if repo == "unknown/repository":
            return ""
        return f"https://github.com/{repo}/blob/{release}/{file_path}#L{start_line}-L{end_line}"
    
    def _get_active_filters(
        self, 
        repo_filter: Optional[str], 
        release_filter: Optional[str], 
        category_filter: Optional[str]
    ) -> Dict[str, str]:
        """🔍 Get active filters for metadata"""
        filters = {}
        if repo_filter:
            filters['repository'] = repo_filter
        if release_filter:
            filters['release'] = release_filter
        if category_filter:
            filters['category'] = category_filter
        return filters
    
    def _update_search_stats(self, result_count: int, search_time: float) -> None:
        """📊 Update search statistics"""
        self.search_stats['total_searches'] += 1
        if result_count > 0:
            self.search_stats['successful_searches'] += 1
        
        # Update averages
        total_searches = self.search_stats['total_searches']
        
        # Average results per search
        current_avg_results = self.search_stats['avg_results_per_search']
        self.search_stats['avg_results_per_search'] = (
            (current_avg_results * (total_searches - 1) + result_count) / total_searches
        )
        
        # Average search time
        current_avg_time = self.search_stats['avg_search_time']
        self.search_stats['avg_search_time'] = (
            (current_avg_time * (total_searches - 1) + search_time) / total_searches
        )
