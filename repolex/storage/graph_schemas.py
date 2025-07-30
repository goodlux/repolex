"""
🟡 PAC-MAN Graph Schema System 🟡
The master blueprint for our 19-graph semantic maze!

WAKA WAKA WAKA! 🟡 Chomp through all 19 graph types per repository!

This module generates consistent URIs and schemas for our semantic maze:
- 4 Ontology graphs (the game rules)
- 2 Function graphs (stable identities + implementations) 
- 1 File structure graph per version (the maze layout)
- 4 Git intelligence graphs (player statistics)
- 1 ABC events graph (temporal dots)
- 3 Evolution analysis graphs (strategy analysis)
- 4 Processing metadata graphs (game state)

Total: 19 beautiful graphs per repository! 🎮
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
import urllib.parse


def _sanitize_uri_component(component: str) -> str:
    """
    Sanitize a component for use in URIs.
    
    Replaces invalid URI characters with underscores to prevent IRI encoding errors.
    """
    # Replace brackets and other problematic characters
    sanitized = component.replace('[', '_').replace(']', '_')
    sanitized = sanitized.replace('<', '_').replace('>', '_')
    sanitized = sanitized.replace('"', '_').replace("'", '_')
    sanitized = sanitized.replace(' ', '_').replace('\t', '_').replace('\n', '_')
    sanitized = sanitized.replace('?', '_').replace('#', '_').replace('&', '_')
    sanitized = sanitized.replace('%', '_').replace('+', '_').replace('=', '_')
    
    # URL encode any remaining special characters as a fallback
    return urllib.parse.quote(sanitized, safe='-_.~')


@dataclass
class GraphURISet:
    """
    🟡 Complete set of graph URIs for a repository
    Like PAC-MAN's complete maze blueprint!
    """
    # Ontology graphs (4) - The fundamental game rules
    ontology_woc: str           # Web of Code ontology 
    ontology_git: str           # Git concepts
    ontology_evolution: str     # Evolution concepts  
    ontology_files: str         # File system concepts
    
    # Function graphs (2) - The players and their moves
    functions_stable: str       # Stable function identities (never deleted!)
    functions_implementations: str  # Version-specific implementations (can be nuked)
    
    # File structure graphs (per version) - The maze layout  
    files_structure: str        # File paths and GitHub links
    
    # Git intelligence graphs (4) - Player statistics and history
    git_commits: str           # Commit history
    git_developers: str        # Developer profiles  
    git_branches: str          # Branch information
    git_tags: str              # Version tags
    
    # ABC events graph (1) - Temporal dots chomped over time
    abc_events: str            # Change events between versions
    
    # Evolution analysis graphs (3) - Strategy analysis
    evolution_analysis: str    # Function change analysis
    evolution_statistics: str  # Stability metrics
    evolution_patterns: str    # Co-change patterns
    
    # Processing metadata graphs (per version) - Game state
    processing_metadata: str   # Timestamps, processing info


class GraphSchemas:
    """
    🟡 PAC-MAN Graph Schema Generator 🟡
    
    Generates consistent URIs for our 19-graph semantic maze!
    Each repository gets its own complete maze with all graph types.
    
    WAKA WAKA WAKA! 🟡 Chomp through all the URI generation!
    """
    
    # Base URI for all repolex graphs - the game world!
    BASE_URI = "http://repolex.org"
    
    @staticmethod 
    def get_ontology_graph_uris() -> Dict[str, str]:
        """
        🟡 Generate the 4 ontology graph URIs
        These are the fundamental game rules that all repositories share!
        """
        return {
            "woc": f"{GraphSchemas.BASE_URI}/ontology/woc",
            "git": f"{GraphSchemas.BASE_URI}/ontology/git", 
            "evolution": f"{GraphSchemas.BASE_URI}/ontology/evolution",
            "files": f"{GraphSchemas.BASE_URI}/ontology/files"
        }
    
    @staticmethod
    def get_woc_ontology_uri() -> str:
        """
        🟡 Get the Web of Code ontology URI specifically
        PAC-MAN's core game rules!
        """
        return GraphSchemas.get_ontology_graph_uris()["woc"]
    
    @staticmethod
    def get_git_ontology_uri() -> str:
        """
        🟡 Get the Git ontology URI specifically
        PAC-MAN's ghost behavior rules!
        """
        return GraphSchemas.get_ontology_graph_uris()["git"]
    
    @staticmethod
    def get_evolution_ontology_uri() -> str:
        """
        🟡 Get the Evolution ontology URI specifically
        PAC-MAN's game progression rules!
        """
        return GraphSchemas.get_ontology_graph_uris()["evolution"]
    
    @staticmethod
    def get_files_ontology_uri() -> str:
        """
        🟡 Get the Files ontology URI specifically
        PAC-MAN's maze layout rules!
        """
        return GraphSchemas.get_ontology_graph_uris()["files"]
    
    @staticmethod
    def get_repository_base_uri(org: str, repo: str) -> str:
        """
        🟡 Get base URI for a specific repository
        This is the entrance to each repository's maze!
        """
        return f"{GraphSchemas.BASE_URI}/repo/{org}/{repo}"
    
    @staticmethod
    def get_function_graph_uris(org: str, repo: str) -> Dict[str, str]:
        """
        🟡 Generate the 2 function graph URIs
        Stable identities (never deleted) + implementations (can be nuked safely)
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        return {
            "stable": f"{base}/functions/stable",
            "implementations": f"{base}/functions/implementations"
        }
    
    @staticmethod
    def get_stable_functions_uri(org: str, repo: str) -> str:
        """
        🟡 Get stable functions graph URI
        """
        return GraphSchemas.get_function_graph_uris(org, repo)["stable"]
    
    @staticmethod
    def get_implementation_uri(org: str, repo: str) -> str:
        """
        🟡 Get implementations graph URI
        """
        return GraphSchemas.get_function_graph_uris(org, repo)["implementations"]
    
    @staticmethod
    def get_file_structure_uri(org: str, repo: str, version: str) -> str:
        """
        🟡 Generate file structure graph URI for specific version
        Each version gets its own maze layout!
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        safe_version = _sanitize_uri_component(version)
        return f"{base}/files/{safe_version}"
    
    @staticmethod
    def get_git_intelligence_uris(org: str, repo: str) -> Dict[str, str]:
        """
        🟡 Generate the 4 git intelligence graph URIs
        Player statistics and game history!
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        return {
            "commits": f"{base}/git/commits",
            "developers": f"{base}/git/developers", 
            "branches": f"{base}/git/branches",
            "tags": f"{base}/git/tags"
        }
    
    @staticmethod
    def get_git_commits_uri(org: str, repo: str) -> str:
        """🟡 Get git commits graph URI"""
        return GraphSchemas.get_git_intelligence_uris(org, repo)["commits"]
    
    @staticmethod
    def get_git_developers_uri(org: str, repo: str) -> str:
        """🟡 Get git developers graph URI"""
        return GraphSchemas.get_git_intelligence_uris(org, repo)["developers"]
    
    @staticmethod
    def get_git_branches_uri(org: str, repo: str) -> str:
        """🟡 Get git branches graph URI"""
        return GraphSchemas.get_git_intelligence_uris(org, repo)["branches"]
    
    @staticmethod
    def get_git_tags_uri(org: str, repo: str) -> str:
        """🟡 Get git tags graph URI"""
        return GraphSchemas.get_git_intelligence_uris(org, repo)["tags"]
    
    @staticmethod
    def get_abc_events_uri(org: str, repo: str) -> str:
        """
        🟡 Generate ABC events graph URI
        Temporal dots chomped over time!
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        return f"{base}/abc/events"
    
    @staticmethod
    def get_evolution_analysis_uris(org: str, repo: str) -> Dict[str, str]:
        """
        🟡 Generate the 3 evolution analysis graph URIs  
        Strategy analysis for how the code maze evolves!
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        return {
            "analysis": f"{base}/evolution/analysis",
            "statistics": f"{base}/evolution/statistics",
            "patterns": f"{base}/evolution/patterns"
        }
    
    @staticmethod
    def get_evolution_analysis_uri(org: str, repo: str) -> str:
        """🟡 Get evolution analysis graph URI"""
        return GraphSchemas.get_evolution_analysis_uris(org, repo)["analysis"]
    
    @staticmethod
    def get_evolution_statistics_uri(org: str, repo: str) -> str:
        """🟡 Get evolution statistics graph URI"""
        return GraphSchemas.get_evolution_analysis_uris(org, repo)["statistics"]
    
    @staticmethod
    def get_evolution_patterns_uri(org: str, repo: str) -> str:
        """🟡 Get evolution patterns graph URI"""
        return GraphSchemas.get_evolution_analysis_uris(org, repo)["patterns"]
    
    @staticmethod
    def get_processing_metadata_uri(org: str, repo: str, version: str) -> str:
        """
        🟡 Generate processing metadata graph URI for specific version
        Game state and processing information!
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        safe_version = _sanitize_uri_component(version)
        return f"{base}/meta/{safe_version}"
    
    @staticmethod
    def get_all_graph_uris(org: str, repo: str, version: str) -> GraphURISet:
        """
        🟡 Generate ALL 19 graph URIs for a repository version!
        
        This is the COMPLETE PAC-MAN maze blueprint! WAKA WAKA WAKA! 🟡
        
        Args:
            org: Organization name (e.g., "goodlux")
            repo: Repository name (e.g., "pixeltable") 
            version: Version tag (e.g., "v0.4.14")
            
        Returns:
            GraphURISet: Complete set of all 19 graph URIs
        """
        ontology_uris = GraphSchemas.get_ontology_graph_uris()
        function_uris = GraphSchemas.get_function_graph_uris(org, repo)
        git_uris = GraphSchemas.get_git_intelligence_uris(org, repo)
        evolution_uris = GraphSchemas.get_evolution_analysis_uris(org, repo)
        
        return GraphURISet(
            # Ontology graphs (4)
            ontology_woc=ontology_uris["woc"],
            ontology_git=ontology_uris["git"],
            ontology_evolution=ontology_uris["evolution"],
            ontology_files=ontology_uris["files"],
            
            # Function graphs (2)
            functions_stable=function_uris["stable"],
            functions_implementations=function_uris["implementations"],
            
            # File structure graph (1 per version)
            files_structure=GraphSchemas.get_file_structure_uri(org, repo, version),
            
            # Git intelligence graphs (4)
            git_commits=git_uris["commits"],
            git_developers=git_uris["developers"],
            git_branches=git_uris["branches"],
            git_tags=git_uris["tags"],
            
            # ABC events graph (1)
            abc_events=GraphSchemas.get_abc_events_uri(org, repo),
            
            # Evolution analysis graphs (3)
            evolution_analysis=evolution_uris["analysis"],
            evolution_statistics=evolution_uris["statistics"],
            evolution_patterns=evolution_uris["patterns"],
            
            # Processing metadata graph (1 per version)
            processing_metadata=GraphSchemas.get_processing_metadata_uri(org, repo, version)
        )
    
    @staticmethod
    def get_stable_function_uri(org: str, repo: str, function_name: str) -> str:
        """
        🟡 Generate stable function identity URI
        
        These URIs NEVER get deleted - they're permanent identities!
        Safe for cross-graph references and ABC events.
        
        Example: function:goodlux/pixeltable/create_table
        """
        safe_function_name = _sanitize_uri_component(function_name)
        return f"function:{org}/{repo}/{safe_function_name}"
    
    @staticmethod
    def get_implementation_uri(org: str, repo: str, function_name: str, version: str) -> str:
        """
        🟡 Generate version-specific implementation URI
        
        These URIs CAN be safely deleted during nuclear updates!
        They point back to stable identities.
        
        Example: function:goodlux/pixeltable/create_table#v0.4.14
        """
        stable_uri = GraphSchemas.get_stable_function_uri(org, repo, function_name)
        safe_version = _sanitize_uri_component(version)
        return f"{stable_uri}#{safe_version}"
    
    @staticmethod
    def get_commit_uri(org: str, repo: str, commit_sha: str) -> str:
        """🟡 Generate commit URI"""
        base = GraphSchemas.get_repository_base_uri(org, repo)
        return f"{base}/commit/{commit_sha}"
    
    @staticmethod
    def get_developer_uri(org: str, repo: str, email: str) -> str:
        """🟡 Generate developer URI"""
        base = GraphSchemas.get_repository_base_uri(org, repo)
        # Replace @ and . with underscores for URI safety
        safe_email = email.replace('@', '_at_').replace('.', '_')
        return f"{base}/developer/{safe_email}"
    
    @staticmethod
    def get_file_uri(org: str, repo: str, version: str, file_path: str) -> str:
        """🟡 Generate file URI"""
        base = GraphSchemas.get_repository_base_uri(org, repo)
        # Replace path separators for URI safety
        safe_path = _sanitize_uri_component(str(file_path).replace('/', '_'))
        safe_version = _sanitize_uri_component(version)
        return f"{base}/file/{safe_version}/{safe_path}"
    
    @staticmethod
    def generate_github_link(org: str, repo: str, version: str, 
                           file_path: str, start_line: Optional[int] = None, 
                           end_line: Optional[int] = None) -> str:
        """
        🟡 Generate GitHub source links on demand
        
        We don't store these - we generate them when needed!
        This keeps our database lean and flexible.
        
        Args:
            org: GitHub organization
            repo: GitHub repository
            version: Git tag/version
            file_path: Relative file path
            start_line: Optional start line number
            end_line: Optional end line number
        
        Returns:
            Complete GitHub URL with line numbers
        """
        base_url = f"https://github.com/{org}/{repo}/blob/{version}/{file_path}"
        
        if start_line and end_line:
            return f"{base_url}#L{start_line}-L{end_line}"
        elif start_line:
            return f"{base_url}#L{start_line}"
        else:
            return base_url
    
    @staticmethod  
    def list_all_graph_types() -> List[str]:
        """
        🟡 List all 19 graph types in our semantic maze!
        Perfect for documentation and validation.
        """
        return [
            # Ontology graphs (4)
            "ontology_woc",
            "ontology_git", 
            "ontology_evolution",
            "ontology_files",
            
            # Function graphs (2)
            "functions_stable",
            "functions_implementations",
            
            # File structure graphs (1 per version)
            "files_structure",
            
            # Git intelligence graphs (4)
            "git_commits",
            "git_developers",
            "git_branches", 
            "git_tags",
            
            # ABC events graph (1)
            "abc_events",
            
            # Evolution analysis graphs (3)
            "evolution_analysis",
            "evolution_statistics",
            "evolution_patterns",
            
            # Processing metadata graphs (1 per version)
            "processing_metadata"
        ]
    
    @staticmethod
    def validate_org_repo_format(org: str, repo: str) -> bool:
        """
        🟡 Validate org/repo format for URI generation
        Keep those ghosts out of our clean maze!
        """
        import re
        
        # Basic format validation
        if not org or not repo:
            return False
            
        # Allow alphanumeric, dots, dashes, underscores
        valid_pattern = re.compile(r'^[a-zA-Z0-9._-]+$')
        
        return bool(valid_pattern.match(org) and valid_pattern.match(repo))
    
    # 🛸 TEXT ANALYSIS GRAPH SCHEMAS - Where No LLM Has Gone Before! 🛸
    
    @staticmethod
    def get_text_analysis_uris(org: str, repo: str) -> Dict[str, str]:
        """
        🛸 Generate text analysis graph URIs for NLP semantic intelligence
        Boldly going where no semantic analyzer has gone before!
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        return {
            "entities_people": f"{base}/entities/people",
            "entities_organizations": f"{base}/entities/organizations", 
            "entities_concepts": f"{base}/entities/concepts",
            "entities_technologies": f"{base}/entities/technologies",
            "entities_locations": f"{base}/entities/locations",
            "entities_moods": f"{base}/entities/moods",  # 🧠 Mood/emotion entities
            "relationships_mentions": f"{base}/relationships/mentions",
            "relationships_references": f"{base}/relationships/references",
            "relationships_cooccurs": f"{base}/relationships/cooccurs",
            "content_structure": f"{base}/content/structure",
            "content_topics": f"{base}/content/topics"
        }
    
    @staticmethod
    def get_entities_people_uri(org: str, repo: str) -> str:
        """🛸 Get people entities graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["entities_people"]
    
    @staticmethod
    def get_entities_organizations_uri(org: str, repo: str) -> str:
        """🛸 Get organization entities graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["entities_organizations"]
    
    @staticmethod
    def get_entities_concepts_uri(org: str, repo: str) -> str:
        """🛸 Get concept entities graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["entities_concepts"]
    
    @staticmethod
    def get_entities_technologies_uri(org: str, repo: str) -> str:
        """🛸 Get technology entities graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["entities_technologies"]
    
    @staticmethod
    def get_entities_locations_uri(org: str, repo: str) -> str:
        """🛸 Get location entities graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["entities_locations"]
    
    @staticmethod
    def get_entities_moods_uri(org: str, repo: str) -> str:
        """🧠 Get mood/emotion entities graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["entities_moods"]
    
    @staticmethod
    def get_relationships_mentions_uri(org: str, repo: str) -> str:
        """🛸 Get mention relationships graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["relationships_mentions"]
    
    @staticmethod
    def get_content_structure_uri(org: str, repo: str) -> str:
        """🛸 Get content structure graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["content_structure"]
    
    @staticmethod
    def get_content_topics_uri(org: str, repo: str) -> str:
        """🛸 Get content topics graph URI"""
        return GraphSchemas.get_text_analysis_uris(org, repo)["content_topics"]
    
    @staticmethod
    def get_entity_uri(org: str, repo: str, entity_type: str, entity_text: str) -> str:
        """
        🛸 Generate URI for a specific entity
        
        Args:
            org: Organization name
            repo: Repository name
            entity_type: Type of entity (PERSON, ORGANIZATION, etc.)
            entity_text: The entity text
            
        Returns:
            URI for the specific entity
        """
        base = GraphSchemas.get_repository_base_uri(org, repo)
        safe_entity = _sanitize_uri_component(entity_text)
        entity_type_lower = entity_type.lower()
        return f"{base}/entity/{entity_type_lower}/{safe_entity}"
    
    @staticmethod
    def get_document_uri(org: str, repo: str, version: str, doc_path: str) -> str:
        """🛸 Generate URI for a text document"""
        base = GraphSchemas.get_repository_base_uri(org, repo)
        safe_version = _sanitize_uri_component(version)
        safe_path = _sanitize_uri_component(str(doc_path).replace('/', '_'))
        return f"{base}/document/{safe_version}/{safe_path}"
    
    @staticmethod
    def get_relationship_uri(org: str, repo: str, source_entity: str, target_entity: str, rel_type: str) -> str:
        """🛸 Generate URI for a relationship between entities"""
        base = GraphSchemas.get_repository_base_uri(org, repo)
        safe_source = _sanitize_uri_component(source_entity)
        safe_target = _sanitize_uri_component(target_entity)
        safe_rel_type = _sanitize_uri_component(rel_type)
        return f"{base}/relationship/{safe_rel_type}/{safe_source}_to_{safe_target}"
    
    @staticmethod
    def list_all_text_graph_types() -> List[str]:
        """
        🛸 List all text analysis graph types in our semantic universe!
        Perfect for NLP pipeline documentation and validation.
        """
        return [
            # Entity graphs (6)
            "entities_people",
            "entities_organizations", 
            "entities_concepts",
            "entities_technologies",
            "entities_locations",
            "entities_moods",  # 🧠 Mood/emotion entities
            
            # Relationship graphs (3)
            "relationships_mentions",
            "relationships_references", 
            "relationships_cooccurs",
            
            # Content graphs (2)
            "content_structure",
            "content_topics"
        ]
    
    @staticmethod
    def get_extended_graph_uris(org: str, repo: str, version: str, include_nlp: bool = False) -> Dict[str, str]:
        """
        🛸 Generate ALL graph URIs - both code and text analysis!
        
        The complete semantic intelligence package for repositories.
        
        Args:
            org: Organization name
            repo: Repository name 
            version: Version tag
            include_nlp: Whether to include NLP text analysis graphs
            
        Returns:
            Dict with all graph URIs (19 code + 10 text = 29 total!)
        """
        # Get standard code analysis graphs
        code_uris = GraphSchemas.get_all_graph_uris(org, repo, version)
        
        # Convert to dict for easier manipulation
        all_uris = {
            # Code analysis graphs (19)
            "ontology_woc": code_uris.ontology_woc,
            "ontology_git": code_uris.ontology_git,
            "ontology_evolution": code_uris.ontology_evolution,
            "ontology_files": code_uris.ontology_files,
            "functions_stable": code_uris.functions_stable,
            "functions_implementations": code_uris.functions_implementations,
            "files_structure": code_uris.files_structure,
            "git_commits": code_uris.git_commits,
            "git_developers": code_uris.git_developers,
            "git_branches": code_uris.git_branches,
            "git_tags": code_uris.git_tags,
            "abc_events": code_uris.abc_events,
            "evolution_analysis": code_uris.evolution_analysis,
            "evolution_statistics": code_uris.evolution_statistics,
            "evolution_patterns": code_uris.evolution_patterns,
            "processing_metadata": code_uris.processing_metadata
        }
        
        # Add text analysis graphs if requested
        if include_nlp:
            text_uris = GraphSchemas.get_text_analysis_uris(org, repo)
            all_uris.update(text_uris)
        
        return all_uris


# 🟡 PAC-MAN Example Usage 🟡
if __name__ == "__main__":
    print("🟡 PAC-MAN Graph Schema Demo! 🟡")
    print("WAKA WAKA WAKA! Let's generate some graph URIs!")
    
    # Generate complete graph set for Pixeltable
    uris = GraphSchemas.get_all_graph_uris("goodlux", "pixeltable", "v0.4.14")
    
    print(f"\n🎮 Complete 19-graph maze for goodlux/pixeltable v0.4.14:")
    print(f"📚 Stable Functions: {uris.functions_stable}")
    print(f"🔄 Implementations: {uris.functions_implementations}")
    print(f"📁 Files: {uris.files_structure}")
    print(f"🏆 Git Commits: {uris.git_commits}")
    print(f"⚡ ABC Events: {uris.abc_events}")
    
    # Generate function URIs
    stable_func = GraphSchemas.get_stable_function_uri("goodlux", "pixeltable", "create_table")
    impl_func = GraphSchemas.get_implementation_uri("goodlux", "pixeltable", "create_table", "v0.4.14")
    
    print(f"\n🟡 Function URI Examples:")
    print(f"Stable Identity: {stable_func}")
    print(f"Implementation: {impl_func}")
    
    # Generate GitHub link
    github_link = GraphSchemas.generate_github_link(
        "goodlux", "pixeltable", "v0.4.14", 
        "pixeltable/core.py", 142, 187
    )
    print(f"GitHub Link: {github_link}")
    
    print(f"\n🎯 Total graph types: {len(GraphSchemas.list_all_graph_types())}")
    print("🟡 CHOMP CHOMP CHOMP! Graph schema system ready! 🟡")
