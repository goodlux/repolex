# Repolex Architecture & Multi-Format Vision

## 🛸 The Semantic Intelligence Ecosystem

Repolex is evolving into a complete semantic intelligence platform that serves multiple stakeholders through different output formats.

## 🎯 Multi-Format Vision

### Current State
- **SPARQL Queries**: Interactive semantic exploration  
- **19-Graph Architecture**: Complete code semantic analysis
- **Enhanced Metadata**: 30+ docstring fields with RDF serialization

### Expansion: Text + NLP Analysis

#### New Analysis Modes
```bash
# Current (auto-detects code)
uv run rlex graph add pixeltable/pixeltable

# New modes
uv run rlex graph add my-docs/blog --mode=text
uv run rlex graph add mixed-repo/project --mode=hybrid
uv run rlex graph add repo/project --nlp    # Enhanced NLP analysis
```

#### Text Analysis Graphs (New Namespace)
```
# Code Analysis (current)
http://Repolex.org/repo/org/repo/functions/implementations
http://Repolex.org/repo/org/repo/git/commits

# Text Analysis (new)  
http://Repolex.org/repo/org/repo/entities/people
http://Repolex.org/repo/org/repo/entities/concepts
http://Repolex.org/repo/org/repo/relationships/mentions
http://Repolex.org/repo/org/repo/content/structure
```

## 🚀 Multi-Format Output Strategy

### 1. Developer Workflow
```bash
# Fast development cycles
uv run rlex export msgpack --profile=compact  # Core API only

# Comprehensive analysis
uv run rlex export msgpack --profile=complete  # Everything + NLP
```

### 2. Documentation Generation
```bash
# Auto-generated documentation sites
uv run rlex export docs --target=mintlify     # Mintlify integration
uv run rlex export docs --target=sphinx       # Sphinx integration

# Human review formats
uv run rlex export opml --include=entities    # OPML with NLP entities
uv run rlex export audit --format=json        # Documentation gap analysis
```

### 3. Export Profiles
- **compact**: Core functions + summaries (fast dev cycles)
- **complete**: Everything including NLP entities (comprehensive docs)
- **api-only**: Just public functions + documentation
- **audit**: Documentation gaps and quality metrics

## 🏗️ Implementation Strategy

### Phase 1: NLP Extension (Optional)
- Add `--nlp` flag to `graph add`
- Implement GLiNER entity extraction
- Add relationship discovery models
- Test performance impact

### Phase 2: Export System
- Implement msgpack export with profiles
- Add OPML generation for human review
- Create documentation site generators

### Phase 3: Auto-Documentation 
- Mintlify integration (target: Anthropic SDK)
- Pixeltable dogfooding as Employee #7
- Performance optimization → make NLP default

## 🎯 Market Positioning

### Current Gap in Market
- **Mintlify**: Beautiful design, zero semantic understanding
- **Anthropic**: Manual SDK docs, no auto-generation
- **Most Companies**: Reactive documentation, manual maintenance

### Repolex Advantage
- **Semantic Understanding**: AST + NLP analysis
- **Always Current**: Auto-sync with code changes  
- **Multi-Format**: Serve all stakeholders
- **AI-Enhanced**: Perfect LLM context via msgpack exports

## 🛠️ Technical Architecture

### Shared Infrastructure
- ✅ Git intelligence (commits, authors, changes)
- ✅ File structure analysis  
- ✅ Storage & querying systems
- 🆕 NLP analysis pipeline
- 🆕 Text-specific ontologies
- 🆕 Multi-format export system

### Mode Detection
```python
def detect_repo_type(repo_path):
    code_files = count_files("*.py", "*.js", "*.java")
    text_files = count_files("*.md", "*.txt", "*.rst") 
    
    if code_files > text_files * 2:
        return "code"
    elif text_files > code_files * 2:
        return "text"  
    else:
        return "hybrid"
```

## 🎮 The MOTHERSHIP Prophecy

> "Within 6 months, every Pixeltable release will include auto-generated documentation audits, and other companies will be asking 'How does Pixeltable have such perfect docs?'"

**This is the future of documentation tooling.** 🚀