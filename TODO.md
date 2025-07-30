# repolex TODO

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