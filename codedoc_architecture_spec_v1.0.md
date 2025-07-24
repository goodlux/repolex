# CodeDoc Architecture Specification v1.0

*Hybrid semantic code intelligence system with stable identities and version-specific implementations*

## 🎯 Core Architecture Principles

### **Hybrid Identity Model**
- **Stable Function Identities**: Never deleted, safe for cross-graph references
- **Version-Specific Implementations**: Can be safely updated/nuked without breaking links
- **Git-Style Namespacing**: `org/repo` structure for multi-repository future

### **Nuclear Update Safety**
- Version implementations can be completely rebuilt without breaking cross-graph references
- All external links point to stable identities, not version-specific implementations
- ABC events and git intelligence survive version updates

## 🗂️ Complete Graph Structure

### **Ontology Graphs** (4)
```
http://codedoc.org/ontology/woc           # Web of Code ontology (functions, classes, methods)
http://codedoc.org/ontology/git           # Git concepts (commits, developers, branches)  
http://codedoc.org/ontology/evolution     # Evolution concepts (changes, analysis)
http://codedoc.org/ontology/files         # File system concepts
```

### **Function Graphs** (2)
```
http://codedoc.org/repo/goodlux/pixeltable/functions/stable          # Stable function identities
http://codedoc.org/repo/goodlux/pixeltable/functions/implementations # Version-specific implementations
```

### **File Structure Graphs** (per version)
```
http://codedoc.org/repo/goodlux/pixeltable/files/v0.2.30    # File paths, line numbers for GitHub linking
http://codedoc.org/repo/goodlux/pixeltable/files/v0.3.15    # File paths, line numbers for GitHub linking  
http://codedoc.org/repo/goodlux/pixeltable/files/v0.4.4     # File paths, line numbers for GitHub linking
```

### **Git Intelligence Graphs** (4)
```
http://codedoc.org/repo/goodlux/pixeltable/git/commits      # Commit history and metadata
http://codedoc.org/repo/goodlux/pixeltable/git/developers   # Developer profiles and stats
http://codedoc.org/repo/goodlux/pixeltable/git/branches     # Branch information
http://codedoc.org/repo/goodlux/pixeltable/git/tags         # Version tags and releases
```

### **ABC Events Graph** (1)
```
http://codedoc.org/repo/goodlux/pixeltable/abc/events       # Temporal change events (simple implementation)
```

### **Evolution Analysis Graphs** (3)  
```
http://codedoc.org/repo/goodlux/pixeltable/evolution/analysis     # Function change analysis
http://codedoc.org/repo/goodlux/pixeltable/evolution/statistics   # Stability metrics, change frequency
http://codedoc.org/repo/goodlux/pixeltable/evolution/patterns     # Co-change patterns
```

### **Processing Metadata Graphs** (per version)
```
http://codedoc.org/repo/goodlux/pixeltable/meta/v0.2.30     # Processing metadata, timestamps
http://codedoc.org/repo/goodlux/pixeltable/meta/v0.3.15     # Processing metadata, timestamps
http://codedoc.org/repo/goodlux/pixeltable/meta/v0.4.4      # Processing metadata, timestamps
```

**Total: 19 graphs per repository**

## 🏗️ Data Model Examples

### **Stable Function Identity**
```turtle
# Graph: http://codedoc.org/repo/goodlux/pixeltable/functions/stable
@prefix woc: <http://rdf.webofcode.org/woc/> .

<function:goodlux/pixeltable/create_table> a woc:Function ;
    woc:canonicalName "create_table" ;
    woc:firstAppearedIn "v0.2.30" ;
    woc:existsInVersion "v0.2.30", "v0.3.15", "v0.4.4" ;
    woc:module "pixeltable.core" ;
    woc:githubUrl "https://github.com/goodlux/pixeltable" .
```

### **Version-Specific Implementation**
```turtle
# Graph: http://codedoc.org/repo/goodlux/pixeltable/functions/implementations
<function:goodlux/pixeltable/create_table#v0.4.4> a woc:MethodImplementation ;
    woc:implementsFunction <function:goodlux/pixeltable/create_table> ;
    woc:hasSignature "create_table(name: str, schema: Dict[str, Any] = None) -> Table" ;
    woc:belongsToVersion "v0.4.4" ;
    rdfs:comment "Creates a new table with specified schema" ;
    woc:definedInFile "pixeltable/core.py" ;
    woc:startLine 142 ;
    woc:endLine 187 ;
    woc:githubLink "https://github.com/goodlux/pixeltable/blob/v0.4.4/pixeltable/core.py#L142-L187" .
```

### **Git Intelligence**
```turtle
# Graph: http://codedoc.org/repo/goodlux/pixeltable/git/commits
@prefix git: <http://codedoc.org/git/> .

<commit:goodlux/pixeltable/abc123def456> a git:Commit ;
    git:sha "abc123def456" ;
    git:author <developer:goodlux/pixeltable/alice> ;
    git:date "2025-01-20T14:30:00Z" ;
    git:message "Add optional schema parameter to create_table" ;
    git:affectsVersion "v0.4.4" ;
    git:modifies <function:goodlux/pixeltable/create_table> ;  # Points to stable identity
    git:githubUrl "https://github.com/goodlux/pixeltable/commit/abc123def456" .
```

### **ABC Events (Simple Implementation)**
```turtle
# Graph: http://codedoc.org/repo/goodlux/pixeltable/abc/events
@prefix abc: <http://codedoc.org/abc/> .

<abc_event:goodlux/pixeltable/create_table_v034_to_v044> a abc:FunctionChange ;
    abc:function <function:goodlux/pixeltable/create_table> ;  # Points to stable identity
    abc:fromVersion "v0.3.15" ;
    abc:toVersion "v0.4.4" ;
    abc:changeType "parameter_added" ;
    abc:timestamp "2025-01-15T10:30:00Z" ;
    abc:commitSha "abc123def456" .
```

### **File Structure with GitHub Links**
```turtle
# Graph: http://codedoc.org/repo/goodlux/pixeltable/files/v0.4.4
@prefix files: <http://codedoc.org/files/> .

<file:goodlux/pixeltable/v0.4.4/pixeltable/core.py> a files:PythonFile ;
    files:path "pixeltable/core.py" ;
    files:relativePath "pixeltable/core.py" ;
    files:githubUrl "https://github.com/goodlux/pixeltable/blob/v0.4.4/pixeltable/core.py" ;
    files:containsFunction <function:goodlux/pixeltable/create_table#v0.4.4> ;
    files:lineCount 500 .
```

## 💾 Local Storage Structure

### **Repository Storage**
```
~/.codedoc/repos/goodlux/pixeltable/
├── .git/                           # Full git history
├── v0.2.30/                        # Checkout of v0.2.30 tag
├── v0.3.15/                        # Checkout of v0.3.15 tag  
├── v0.4.4/                         # Checkout of v0.4.4 tag
└── .codedoc/
    ├── parsed_versions.json        # Track what's been parsed
    └── last_updated.json           # Update timestamps
```

### **Database Storage**
```
~/.codedoc/oxigraph/
├── codedoc.db                      # Single Oxigraph instance for ALL repositories
├── exports/
│   ├── goodlux/pixeltable/
│   │   ├── v0.4.4.opml            # OPML export for human browsing
│   │   ├── v0.4.4.msgpack         # Compact format for LLM consumption
│   │   └── docs/                  # Generated documentation
│   └── microsoft/typescript/
│       └── ...
└── logs/
    ├── parsing.log                # Processing logs
    └── updates.log                # Update history
```

## 🗄️ Oxigraph Performance & Scaling

### **Single Instance Architecture**
**Yes, we can use one Oxigraph instance for everything!**

### **Performance Characteristics**
- **Named graphs**: Essentially unlimited (millions supported)
- **19 graphs per repo**: No performance impact
- **1,000 repos = 19,000 graphs**: Still excellent performance
- **Performance degrades**: Around 100K+ graphs with complex cross-graph queries
- **Sweet spot**: 10K-50K graphs with sub-second query response

### **Scaling Strategy**
```
Single Oxigraph Database (~/.codedoc/oxigraph/codedoc.db):
├── 1,000 repositories supported
├── 19,000 total named graphs  
├── ~50M triples estimated
├── <1 second query performance
└── Multi-GB database size (acceptable)

Future Scaling (if needed):
├── Shard by organization (goodlux.db, microsoft.db)
├── Separate "hot" vs "cold" repositories
└── Cloud deployment with clustering
```

## 🔗 GitHub Link Strategy

### **Minimal Metadata Storage**
Store repository metadata once, generate links on demand:

```turtle
# Repository metadata (stored once per repo)
<repo:goodlux/pixeltable> a repo:Repository ;
    repo:githubOrg "goodlux" ;
    repo:githubRepo "pixeltable" ;
    repo:githubUrl "https://github.com/goodlux/pixeltable" .

# Function implementation (minimal file info)
<function:goodlux/pixeltable/create_table#v0.4.4> a woc:MethodImplementation ;
    woc:implementsFunction <function:goodlux/pixeltable/create_table> ;
    woc:hasSignature "create_table(name: str, schema: Dict[str, Any] = None) -> Table" ;
    woc:belongsToVersion "v0.4.4" ;
    rdfs:comment "Creates a new table with specified schema" ;
    woc:definedInFile "pixeltable/core.py" ;  # Relative path only
    woc:startLine 142 ;                       # Line numbers only
    woc:endLine 187 .                        # No full GitHub URLs stored
```

### **Generate Links at Query Time**
```python
def generate_github_link(org: str, repo: str, version: str, file_path: str, 
                        start_line: int = None, end_line: int = None) -> str:
    """Generate GitHub source links on demand"""
    base = f"https://github.com/{org}/{repo}/blob/{version}/{file_path}"
    if start_line and end_line:
        return f"{base}#L{start_line}-L{end_line}"
    elif start_line:
        return f"{base}#L{start_line}"
    return base

# Example usage:
# github_link = generate_github_link("goodlux", "pixeltable", "v0.4.4", 
#                                   "pixeltable/core.py", 142, 187)
# Result: "https://github.com/goodlux/pixeltable/blob/v0.4.4/pixeltable/core.py#L142-L187"
```

### **Benefits of Generated Links**
- ✅ **Reduced storage**: No duplicate URL strings throughout database
- ✅ **Flexibility**: Easy to change GitHub URL format globally  
- ✅ **Consistency**: All links guaranteed to follow same pattern
- ✅ **Clean data model**: Focus on semantic relationships, not presentation

### **Nuclear Update (Recommended)**
```python
async def nuclear_update_version(org: str, repo: str, version: str):
    """Safely rebuild single version without breaking cross-graph references"""
    
    # Step 1: Clear version-specific graphs (safe to delete)
    await clear_graphs([
        f"repo/{org}/{repo}/functions/implementations",  # Only this version's implementations
        f"repo/{org}/{repo}/files/{version}",
        f"repo/{org}/{repo}/meta/{version}"
    ])
    
    # Step 2: Reparse repository for this version
    repo_path = f"~/.codedoc/repos/{org}/{repo}/{version}"
    await parse_repository_for_version(repo_path, version)
    
    # Step 3: Update evolution analysis (derived data)
    await recalculate_evolution_for_version(org, repo, version)
    
    # Cross-graph references remain intact:
    # ✅ Git commits still point to stable function identities
    # ✅ ABC events still reference stable identities
    # ✅ Other versions unaffected
```

### **Adding New Version**
```python
async def add_new_version(org: str, repo: str, version: str):
    """Add new version - purely additive operation"""
    
    # Step 1: Checkout new version
    repo_path = f"~/.codedoc/repos/{org}/{repo}"
    await git_checkout_tag(repo_path, version)
    
    # Step 2: Create new version-specific graphs
    await create_graphs([
        f"repo/{org}/{repo}/files/{version}",
        f"repo/{org}/{repo}/meta/{version}"
    ])
    
    # Step 3: Parse and add implementations
    await parse_and_add_implementations(org, repo, version)
    
    # Step 4: Update stable function metadata
    await update_stable_functions_with_new_version(org, repo, version)
    
    # Step 5: Generate new ABC events for changes
    await generate_abc_events_for_version(org, repo, version)
```

## 🎯 Primary Use Cases

### **1. Auto Documentation Generation**
```sparql
# Get all public functions for v0.4.4 with file locations
PREFIX woc: <http://rdf.webofcode.org/woc/>
SELECT ?name ?signature ?docstring ?githubLink WHERE {
  GRAPH <http://codedoc.org/repo/goodlux/pixeltable/functions/implementations> {
    ?impl woc:belongsToVersion "v0.4.4" ;
          woc:hasSignature ?signature ;
          rdfs:comment ?docstring ;
          woc:githubLink ?githubLink .
  }
  GRAPH <http://codedoc.org/repo/goodlux/pixeltable/functions/stable> {
    ?function woc:canonicalName ?name .
    ?impl woc:implementsFunction ?function .
  }
}
```

### **2. Intelligent Function Discovery with Claude**
```sparql
# Find functions related to "record" and "database"
PREFIX woc: <http://rdf.webofcode.org/woc/>
SELECT ?name ?signature ?docstring WHERE {
  GRAPH <http://codedoc.org/repo/goodlux/pixeltable/functions/implementations> {
    ?impl woc:belongsToVersion "v0.4.4" ;
          woc:hasSignature ?signature ;
          rdfs:comment ?docstring .
  }
  GRAPH <http://codedoc.org/repo/goodlux/pixeltable/functions/stable> {
    ?function woc:canonicalName ?name .
    ?impl woc:implementsFunction ?function .
  }
  FILTER(CONTAINS(LCASE(?docstring), "record") && CONTAINS(LCASE(?docstring), "database"))
}
```

### **3. Version Evolution Analysis**
```sparql
# Show how create_table evolved across versions
PREFIX woc: <http://rdf.webofcode.org/woc/>
SELECT ?version ?signature WHERE {
  GRAPH <http://codedoc.org/repo/goodlux/pixeltable/functions/implementations> {
    ?impl woc:implementsFunction <function:goodlux/pixeltable/create_table> ;
          woc:belongsToVersion ?version ;
          woc:hasSignature ?signature .
  }
}
ORDER BY ?version
```

## ☁️ Cloud Architecture Strategy

### **User-Centric Database Model**
```
Local Processing:
~/.codedoc/oxigraph/codedoc.db          # User's local database (all their repos)

Cloud Deployment:
├── user-databases/
│   ├── alice123.oxigraph               # Alice's repos (pixeltable, scramble, etc.)
│   ├── bob456.oxigraph                 # Bob's repos (react-utils, typescript-lib)
│   └── company789.oxigraph             # Company's repos (internal tools)
└── uber-graph/
    ├── aggregated.oxigraph             # Reads from all user databases
    ├── public-repos/                   # Crowdsourced public repository data
    └── ecosystem-intelligence/         # Cross-user, cross-repo analytics
```

### **Local → Cloud Sync Process**
```python
class CodeDocCloudSync:
    async def sync_user_database(self, user_id: str):
        """Sync local database to user's cloud instance"""
        
        # Step 1: Process repos locally (full control, privacy)
        local_db = f"~/.codedoc/oxigraph/codedoc.db"
        
        # Step 2: Upload/sync to user's cloud database
        cloud_db = f"cloud://user-databases/{user_id}.oxigraph"
        await self.sync_database(local_db, cloud_db)
        
        # Step 3: User's data feeds into uber-graph (if consented)
        if user.allows_ecosystem_contribution:
            await self.contribute_to_uber_graph(user_id)
```

### **Uber-Graph Intelligence**
```sparql
# Query across ALL users' repositories for ecosystem insights
PREFIX woc: <http://rdf.webofcode.org/woc/>
SELECT ?repoOwner ?functionName ?popularity WHERE {
  # Federated query across all user databases
  SERVICE <user-database:*> {
    GRAPH ?userGraph {
      ?impl woc:hasSignature ?signature ;
            woc:implementsFunction ?function .
      ?function woc:canonicalName ?functionName .
    }
  }
  # Aggregate popularity across ecosystem
}
GROUP BY ?functionName
ORDER BY DESC(COUNT(?impl))
```

### **Architecture Benefits**
- ✅ **Privacy**: Users control their own data
- ✅ **Scalability**: Each user database scales independently  
- ✅ **Ecosystem Intelligence**: Uber-graph provides cross-user insights
- ✅ **Hybrid Deployment**: Local processing + cloud sync
- ✅ **Crowdsourcing**: Public repos contribute to shared knowledge

## 🌐 Multi-Repository Future

### **Cross-Repository Intelligence**
```sparql
# Find all table creation functions across entire ecosystem
PREFIX woc: <http://rdf.webofcode.org/woc/>
SELECT ?repo ?name ?signature WHERE {
  GRAPH ?g {
    ?impl woc:hasSignature ?signature .
    ?function woc:canonicalName ?name .
    ?impl woc:implementsFunction ?function .
  }
  FILTER(STRSTARTS(STR(?g), "http://codedoc.org/repo/"))
  FILTER(CONTAINS(LCASE(?name), "table") && CONTAINS(LCASE(?name), "create"))
  BIND(REPLACE(STR(?g), "^.*/repo/([^/]+/[^/]+)/.*$", "$1") AS ?repo)
}
```

### **Storage Scaling**
```
~/.codedoc/repos/           # All repositories in single directory tree
├── goodlux/
│   ├── pixeltable/
│   └── scramble/
├── microsoft/
│   └── typescript/
└── facebook/
    └── react/

~/.codedoc/oxigraph/        # Single database for everything
├── codedoc.db              # One Oxigraph instance, all repos
├── exports/                # Organized by org/repo
└── logs/
```

## 🔧 Implementation Guidelines

### **Graph URI Generation**
```python
def get_graph_uri(graph_type: str, org: str, repo: str, version: str = None) -> str:
    """Generate consistent graph URIs"""
    base = f"http://codedoc.org/repo/{org}/{repo}/{graph_type}"
    return f"{base}/{version}" if version else base

# Examples:
stable_functions = get_graph_uri("functions/stable", "goodlux", "pixeltable")
v044_files = get_graph_uri("files", "goodlux", "pixeltable", "v0.4.4")
```

### **Function URI Generation**
```python
def get_function_uri(function_name: str, org: str, repo: str, version: str = None) -> str:
    """Generate consistent function URIs"""
    base = f"function:{org}/{repo}/{function_name}"
    return f"{base}#{version}" if version else base

# Examples:
stable_id = get_function_uri("create_table", "goodlux", "pixeltable")
v044_impl = get_function_uri("create_table", "goodlux", "pixeltable", "v0.4.4")
```

### **GitHub Link Generation**
```python
def generate_github_link(org: str, repo: str, version: str, file_path: str, 
                        start_line: int = None, end_line: int = None) -> str:
    """Generate GitHub source links"""
    base = f"https://github.com/{org}/{repo}/blob/{version}/{file_path}"
    if start_line and end_line:
        return f"{base}#L{start_line}-L{end_line}"
    elif start_line:
        return f"{base}#L{start_line}"
    return base
```

## 🎯 Success Metrics

### **Architecture Validation**
- ✅ Nuclear updates complete without breaking cross-graph references
- ✅ New versions can be added without affecting existing data
- ✅ Cross-repository queries execute efficiently
- ✅ Function discovery queries return accurate results in <1 second

### **Use Case Validation** 
- ✅ Documentation generation produces complete, accurate API docs
- ✅ OPML/msgpack exports enable human browsing and LLM consumption
- ✅ Claude can instantly find obscure functions through semantic queries
- ✅ Evolution analysis reveals meaningful patterns in code changes

### **Scalability Validation**
- ✅ System handles repositories with 1000+ functions
- ✅ Version updates complete in <2 minutes for typical changes
- ✅ Storage overhead <100MB per repository version
- ✅ Multi-repository expansion requires no architectural changes

---

## 🚀 Implementation Phases

### **Phase 1**: Single Repository Foundation
- Implement hybrid architecture for goodlux/pixeltable
- Nuclear update capability for single versions
- Basic documentation generation
- File structure with GitHub linking

### **Phase 2**: Intelligence Layer  
- SPARQL query interface for Claude
- Function discovery and semantic search
- OPML/msgpack export capabilities
- Simple ABC event tracking

### **Phase 3**: Multi-Repository Expansion
- Extend to multiple org/repo combinations
- Cross-repository intelligence queries
- Crowdsourced update mechanisms
- Cloud deployment architecture

**This architecture provides a solid foundation for semantic code intelligence that scales from single repositories to entire ecosystems while maintaining data consistency and query performance.**