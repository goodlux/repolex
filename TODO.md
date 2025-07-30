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

### Git Analysis Bug 🐛 
**The Eternal Numpy Problem**: Git intelligence fails parsing email addresses as integers
- Error: `invalid literal for int() with base 10: 'erfan.nariman@veneficus.nl'`
- Affects large repos like numpy during semantic analysis
- Need to fix git commit author parsing in intelligence pipeline

### Future Enhancements