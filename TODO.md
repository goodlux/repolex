# repolex TODO

## 🚨 CRITICAL ISSUES DISCOVERED (5:13 AM Session) 🚨

**Discovery Date**: 2025-01-30 @ 4:20-5:13 AM 🌿

### 1. **ALL FUNCTIONS SHOW AS UNREFERENCED** 
- **Issue**: SPARQL query shows 162 functions with 0 calls (100% unreferenced!)
- **Impact**: Call graph analysis completely broken
- **Root Cause**: Parser not tracking function calls in `woc:calls` relationships
- **Evidence**: 
  ```sparql
  SELECT (COUNT(?s) as ?total_calls) WHERE { 
    GRAPH <.../functions/implementations> { ?s woc:calls ?o } 
  }
  -- Result: 0
  ```

### 2. **rlex COMMAND NOT IN PATH**
- **Issue**: `rlex: command not found` - must use `uv run rlex`
- **Impact**: Not installed as global command, development mode only
- **Fix Options**:
  - Add installation instructions for global pip install
  - Create shell alias/script
  - Document uv-only workflow

### 3. **MINTLIFY PHANTOM NAVIGATION**
- **Issue**: docs.json references functions that don't exist as MDX files
- **Root Cause**: Template-based navigation vs actual discovered functions
- **Fixed**: ✅ Enhanced navigation to only include actual functions
- **Fixed**: ✅ Better docs.json merge logic to remove old SDK sections

### 4. **GLiNER INTEGRATION OPPORTUNITY**
- **Discovery**: GLiNER already in codebase for text parsing!
- **Potential**: Use NLP to discover semantic relationships between functions
- **Use Cases**:
  - Semantic call graph (where static analysis failed)
  - True dead code detection via meaning
  - Auto-categorization beyond name matching
  - Hidden relationship discovery

### 5. **INSTANT CLEANUP POTENTIAL**
- **With 100% unreferenced functions, we could**:
  - Build semantic relationships with GLiNER
  - Find true entry points (main, cli, etc)
  - Detect actually dead code vs parser issues
  - Create cleanup recommendations

## Action Items
1. **Fix function call tracking in parser** (HIGH PRIORITY)
2. **Add global install instructions** for rlex command
3. **Implement GLiNER semantic analysis** for functions
4. **Create dead code detection command** using semantic analysis
5. **Debug why woc:calls relationships aren't being created**

## Installation Instructions (TO BE ADDED TO README)

### Option 1: Development Mode (Current)
```bash
# Using uv (recommended for development)
uv run rlex <command>
```

### Option 2: Global Install (TO BE IMPLEMENTED)
```bash
# Install globally with pip
pip install -e .
# OR
pip install repolex

# Then use directly
rlex <command>
```

### Option 3: Shell Alias (Quick Fix)
```bash
# Add to ~/.bashrc or ~/.zshrc
alias rlex='uv run rlex'
```

## GLiNER Performance Issues (GLEEK Issue)

**Status**: Paused - GLiNER hangs during .phext consciousness file processing

**Problem**: 
- GLiNER entity extraction works but is extremely slow on large text files
- 17 .phext files in wbic16/human repository cause processing to hang
- Applied SLOPAT optimizations (threshold=0.3, text preprocessing) but still too slow
- Database corruption occurred during long-running GLiNER operations

**Applied Fixes**:
- ✅ Fixed --force flag propagation through CLI → manager → graph_manager
- ✅ Applied SLOPAT optimizations: threshold=0.3, markdown preprocessing
- ✅ Fixed entity label case mismatch (GLiNER uppercase vs graph builder lowercase)
- ✅ Added mood/emotion detection with custom labels
- ✅ Added .phext file support to text discovery pipeline

**Next Steps** (when we return to this):
1. Investigate file size limits and chunking strategies
2. Consider switching to spaCy for NLP processing (as suggested)
3. Add timeout handling and graceful degradation
4. Implement incremental processing for large text files
5. Add progress indicators for GLiNER operations

**Architecture Completed**:
- ✅ Text analysis pipeline with 10 new graph types
- ✅ NLP integration with --nlp flag
- ✅ Graph schemas for entities, relationships, content, topics
- ✅ UFO/alien theming in stdout (not function names)

---

## LLM-Optimized Export System ✅ COMPLETED!

**Goal**: Create msgpack exports optimized for LLM consumption via jq queries ✅

**Use Case**: Pixeltable documentation and repo understanding for LLMs ✅

**Requirements**:
- ✅ `rlex lexify` command for intelligent one-click semantic lexicon building
- ✅ Output: `llm-repolex/org~repo~version.msgpack` with tilde separator
- ✅ Include repo + ALL dependencies with PyPI → GitHub resolution
- ✅ Queryable with jq only (no graph tools needed)
- ✅ README.md integration with LLM instructions
- ✅ Two-tier filtering: dependencies get public functions, current repo gets all
- ✅ Real-world tested on Pixeltable (379 functions, 95KB semantic DNA)

**Status**: ✅ PRODUCTION READY! Successfully lexified Pixeltable with 30 dependencies

---

## Current Issues & Next Steps

### 🚨 URGENT: Local Repo Lexify Performance Issues 🚨
**The Local Repo Git Pull Problem**: `rlex lexify` hangs during update phase
- **Root Cause**: lexify treats local repo like remote repo, tries to `git pull` during update
- **Impact**: 2+ minute hangs, requires commits before running
- **Fix Options**:
  - Skip repo_update/graph_update for local repositories during lexify
  - Add `--allow-uncommitted` flag for development workflow  
  - Detect if we're processing the current working directory and use filesystem directly

### Nuclear Development Options Needed 💥
**For rapid development iterations we need easy ways to nuke data:**
- `rlex graph remove all` - Remove all graphs from database
- `rlex repo remove all` - Remove all repositories (but confirm first!)
- Maybe: `rlex nuke --graphs` / `rlex nuke --repos` / `rlex nuke --all`

### Git Analysis Bug 🐛 
**The Eternal Numpy Problem**: Git intelligence fails parsing email addresses as integers
- Error: `invalid literal for int() with base 10: 'erfan.nariman@veneficus.nl'`
- Affects large repos like numpy during semantic analysis
- Need to fix git commit author parsing in intelligence pipeline

## JQ Query Ergonomics Improvements 🔍

### Helper Scripts Needed
**Status**: Pending - Identified during semantic DNA demo
**Problem**: Complex JQ queries with shell quoting issues causing syntax errors
**Solutions**:
1. **Create helper scripts for common development queries**:
   - `find-functions.sh <keyword>` - Find functions by name/keyword
   - `complexity-analysis.sh` - Show refactoring hotspots  
   - `architecture-overview.sh` - Complete project structure
   - `pattern-analysis.sh <pattern>` - Find usage patterns

2. **Add query validation** to catch JQ syntax errors early:
   - Pre-validate JQ expressions before execution
   - Better error messages for common mistakes
   - Safe query patterns that handle missing fields gracefully

### Future Enhancements

---

## 🎉 CLASS SUPPORT COMPLETED! (2025-08-04 Session)

**Achievement**: Full class extraction and JSONL export now working!

### What Was Fixed:
1. **Python Parser Enhanced** ✅
   - Now extracts classes with inheritance, methods, docstrings
   - Creates ClassNode objects with full metadata
   
2. **Graph Builder Updated** ✅  
   - Stores classes as both stable identities and version-specific implementations
   - Proper RDF triples with woc:Class and woc:ClassImplementation types
   
3. **JSONL Exporter Extended** ✅
   - Added `_gather_class_data()` method with SPARQL queries
   - New `"type": "class"` entities in JSONL output
   - Smart categorization (model, service, config, exception, etc.)
   - Refactor scoring based on method count (god_class, large_class, etc.)

### Test Results:
- **GLiNER Repository**: Successfully extracted 70 classes and 42 functions
- **JSONL Export**: 69 classes exported with full metadata
- **Entity Structure**:
  ```json
  {
    "type": "class",
    "n": "TrainingArguments",
    "m": "gliner.training.trainer", 
    "f": "",
    "inherits": "transformers.TrainingArguments",
    "methods": 0,
    "cat": "domain",
    "refactor": "unknown"
  }
  ```

---

## 🚀 Next Major Task: Intelligent Agent Tool

### Architecture Decision:
Keep repolex as pure semantic graph extractor following CodeOntology standards. Build intelligence and heuristics in a separate agent tool that reads JSONL and enhances it.

### Refactoring Intelligence (Currently Implemented):

**Automated Refactor Scoring System** ✅
The JSONL export now includes intelligent refactoring recommendations based on code complexity:

#### Function Refactor Scores (based on lines of code):
- **"small"**: < 50 lines - ideal, well-scoped functions
- **"good"**: 50-99 lines - reasonable size
- **"medium_function"**: 100-199 lines - could be reviewed
- **"large_function"**: 200-399 lines - should be broken down
- **"monster_function"**: 400+ lines - needs immediate attention

#### Class Refactor Scores (based on method count):
- **"simple"**: < 10 methods - clean, focused classes
- **"good"**: 10-19 methods - reasonable complexity
- **"medium_class"**: 20-29 methods - could be reviewed
- **"large_class"**: 30-49 methods - should be broken down  
- **"god_class"**: 50+ methods - needs immediate refactoring

#### Module/File Refactor Scores (based on function count):
- **"simple"**: < 3 functions - minimal files
- **"good"**: 3-9 functions - well organized
- **"moderate_functions"**: 10-19 functions - reasonable
- **"many_functions"**: 20-29 functions - should be reviewed
- **"excessive_functions"**: 30+ functions - needs restructuring

These scores help identify:
- Technical debt hotspots
- Refactoring priorities
- Code review focus areas
- Architecture improvement opportunities

### Agent Tool Design (To Be Built):

#### High Priority
1. **Create new agent tool for JSONL enrichment/validation**
   - Read JSONL exports from repolex
   - Analyze README/docs for API conventions
   - Apply heuristics for public/private API detection
   - Output enriched JSONL with confidence scores
   - **Enhance refactor recommendations with context** (e.g., a 400-line function might be OK if it's a state machine)

#### Medium Priority  
2. **Agent should read JSONL + docs + query repolex for context**
   - Connect to repolex graph for additional queries
   - Parse documentation files for API patterns
   - Check test coverage patterns
   
3. **Agent makes intelligent decisions about public/private APIs**
   - Use `__all__` exports when available
   - Analyze import patterns across codebase
   - Check docstring quality (public APIs often better documented)
   - Look for decorator patterns (@api, @public, etc.)
   - Consider test coverage (public functions more likely tested)

### Python Public/Private Challenge:
- Python lacks explicit visibility modifiers
- Must rely on naming conventions (underscore prefixes)
- Need ML-based inference or manual configuration per repo
- Agent tool can apply repo-specific heuristics

---

## 📊 Current System Status

### What's Working:
- ✅ Function extraction and JSONL export
- ✅ Class extraction and JSONL export  
- ✅ Module analysis with refactor recommendations
- ✅ Pattern detection (CRUD, export operations)
- ✅ Semantic clustering
- ✅ Code quality metrics

### JSONL Stats (GLiNER v0.2.20):
- 51 functions exported
- 69 classes exported
- 15 modules analyzed
- 1 pattern detected
- 4 semantic clusters
- Total: 143 entities

### Code Quality Insights in JSONL:
The JSONL also includes a `"type": "code_quality"` entity with:
- Monster functions (400+ lines) with examples
- Large functions (200+ lines) with examples
- Files with excessive functions (30+) with examples
- Overall refactoring priority: critical/high/medium/low
- Average function size metrics
- Total lines of code statistics

### Important Note:
**Remember to rebuild graphs** after code changes! Old graphs won't have new features:
```bash
rlex graph remove org/repo
rlex graph add org/repo version
```

---
*Last updated: 2025-08-04 @ 1:00 AM after successful class implementation*