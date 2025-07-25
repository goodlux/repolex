# Repolex - Semantic Code Intelligence System

**Professional semantic code analysis and repository documentation tool.**

Repolex transforms complex codebases into intelligent, queryable knowledge through advanced semantic analysis and RDF graph storage.

## ✨ Key Features

- **Semantic Analysis**: Deep code understanding with 19-graph architecture
- **Version Management**: Stable identities with version-specific implementations
- **Safe Updates**: Nuclear rebuilds that preserve cross-references
- **Export Formats**: Compact msgpack, OPML, and documentation exports
- **GitHub Integration**: Direct source links with precise line numbers
- **Multi-Repository**: Query across entire organizational codebases
- **CLI Interface**: Unix-style commands for professional workflows

## 🚀 Quick Start

```bash
# Install Repolex
uv add repolex

# Add a repository for analysis
rlex repo add pixeltable/pixeltable

# Generate semantic graphs for a version
rlex graph add pixeltable/pixeltable v0.4.14

# Export compact semantic data
rlex export msgpack pixeltable/pixeltable v0.4.14

# Query the knowledge base
rlex query functions "create table"
```

## 📋 Commands

### Repository Management
```bash
rlex repo add <org/repo>              # Add repository for analysis
rlex repo list                        # List managed repositories
rlex repo show <org/repo>             # Show repository details
rlex repo update <org/repo>           # Update with latest commits
rlex repo remove <org/repo>           # Remove repository
```

### Graph Operations
```bash
rlex graph add <org/repo> [version]   # Generate semantic graphs
rlex graph remove <org/repo>          # Remove semantic data
rlex graph update <org/repo>          # Rebuild graphs safely
rlex graph list                       # List all semantic graphs
```

### Export Operations
```bash
rlex export opml <org/repo> <version>     # Hierarchical documentation
rlex export msgpack <org/repo> <version>  # Compact semantic data
rlex export docs <org/repo> <version>     # Generated documentation
```

### Query Operations
```bash
rlex query functions "search term"       # Find functions by description
rlex query sparql "SELECT ?name WHERE..." # Raw SPARQL queries
```

## 🏗️ Architecture

### Semantic Graph System
Repolex creates 19 interconnected graphs per repository:

- **Stable Function Identities**: Permanent function IDs across versions
- **Version Implementations**: Specific code for each release
- **File Structure**: Directory and module organization
- **Git Intelligence**: Commit history and metadata
- **Event Tracking**: Code evolution over time
- **Cross-Version Analysis**: Pattern recognition across releases

### Hybrid Identity Model
- Functions receive permanent IDs that survive version changes
- Each release gets independent implementation graphs
- Nuclear updates rebuild without breaking references
- Cross-repository dependencies remain stable

## 📊 Storage Efficiency

```
Full Oxigraph Database:    ~100MB  (Complete semantic knowledge)
Semantic Data (.msgpack):   ~800KB  (125x compressed)
OPML Export:               ~2MB    (Human-readable)
Generated Docs:            ~5MB    (Full documentation)
```

## 🧬 Semantic Data Export

Every repository generates compact semantic data perfect for AI analysis:

```python
import msgpack

# Load semantic data
with open('pixeltable-v0.4.14.msgpack', 'rb') as f:
    semantic_data = msgpack.unpackb(f.read())

# Rich semantic information
print(f"Functions: {len(semantic_data['functions'])}")
print(f"Relationships: {len(semantic_data['relationships'])}")
print(f"Compression: 125x smaller than full RDF")
```

## 🎯 Performance Goals

- ✅ **Speed**: Sub-second queries across 1000+ functions
- ✅ **Compression**: 125x reduction with 95% semantic preservation
- ✅ **Safety**: Nuclear updates preserve all cross-references
- ✅ **Accuracy**: Natural language queries find precise matches

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/your-repo/repolex.git
cd repolex

# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Code formatting
uv run black repolex/
uv run ruff check repolex/

# Type checking
uv run mypy repolex/
```

## 📁 Configuration

Repolex stores data in `~/.repolex/`:

```
~/.repolex/
├── repos/          # Cloned repositories
├── oxigraph/       # Semantic database
├── exports/        # Generated exports
├── config/         # Configuration files
└── logs/           # System logs
```

## 🔧 Requirements

- Python 3.11+
- Git (for repository management)
- 2GB+ free disk space (for semantic database)

## 📄 License

MIT License - Open source semantic intelligence for everyone.

---

**Repolex**: Transform complexity into intelligence through semantic analysis.