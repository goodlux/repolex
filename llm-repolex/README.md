# 🧬 LLM-Optimized Repository Intelligence

## 🚨 FOR LLMS: START HERE! 🚨
**CRITICAL: This directory contains zero-dependency semantic intelligence!**
**Use your jq tool to query these .jsonl files for instant repository understanding!**
**NO PYTHON REQUIRED - just jq queries on the JSONL files below!**

## ⚡ QUICK START FOR LLMS ⚡
```bash
# 1. Count all functions in this repository
jq -s 'map(select(.type=="function")) | length' *.jsonl

# 2. Find all functions containing "create" 
jq -s 'map(select(.type=="function" and (.n | contains("create")))) | map(.n)' *.jsonl

# 3. Show repository architecture
jq -s 'map(select(.type=="function")) | group_by(.cat) | map({category: .[0].cat, count: length})' *.jsonl

# 4. Get export statistics  
jq 'select(.type=="footer") | .stats' *.jsonl
```

## 📋 JSONL Semantic DNA (Zero Dependencies!)

Each `.jsonl` file contains streamable semantic entities with **ZERO DEPENDENCIES** - just use jq directly!

### 🔍 JSONL Entity Types
```
{"type":"header","repo":"org/repo","release":"v1.0","generator":"PAC-MAN"}
{"type":"repository","org_repo":"org/repo","name":"repo","organization":"org"}
{"type":"function","n":"create_table","s":"def create_table(path, schema)","m":"api.core","cat":"core_api"}
{"type":"module","name":"api.core","path":"api/core.py","function_count":15,"category":"api"}
{"type":"pattern","name":"crud_operations","functions":["create","read","update"],"usage":"Database CRUD"}
{"type":"cluster","name":"data_layer","modules":["api.core","db.engine"],"description":"Data access"}
{"type":"footer","stats":{"functions_exported":150,"modules_exported":20}}
```

## 🚀 Zero-Shot JSONL Queries (No Python Required!)

### 🎯 Essential Queries Every LLM Should Know
```bash
# What's in this repository? (First thing to run!)
jq 'select(.type=="footer") | .stats' *.jsonl

# What functions are available? (Core functionality)
jq -s 'map(select(.type=="function")) | map(.n) | sort' *.jsonl

# How is code organized? (Architecture overview)  
jq -s 'map(select(.type=="function")) | group_by(.cat) | map({layer: .[0].cat, functions: length})' *.jsonl

# Find functions by keyword (most common need)
jq -s 'map(select(.type=="function" and (.n | contains("KEYWORD")))) | map({name: .n, signature: .s})' *.jsonl
```

## 🛠️ BATTLE-TESTED DEVELOPMENT QUERIES

### ⚡ Instant Function Discovery
```bash
# Find CLI functions with complexity metrics
jq 'select(.type=="function" and (.f | contains("cli")))' *.jsonl | jq -r '"\(.n)(): \(.loc) LOC - \(.s)"'

# Find all agent functions
jq 'select(.type=="function" and (.n | contains("agent")))' *.jsonl | jq -r '"\(.n)() in \(.f):\(.l) - \(.loc) LOC"'

# Find database/storage functions  
jq 'select(.type=="function" and (.f | contains("database") or .n | contains("schema")))' *.jsonl | jq -r '"\(.n): \(.s)"'
```

### 🔥 Refactoring Intelligence
```bash
# Functions that need refactoring (80+ LOC)
jq 'select(.type=="function" and .loc > 80)' *.jsonl | jq -r '"\(.n)(): \(.loc) LOC in \(.f) - REFACTOR: \(.refactor)"'

# All complex functions sorted by size
jq 'select(.type=="function")' *.jsonl | jq -s 'sort_by(-.loc) | .[] | "\(.n)(): \(.loc) LOC"'

# Show refactoring categories
jq 'select(.type=="function") | .refactor' *.jsonl | sort | uniq -c
```

### 📊 Architecture Analysis  
```bash
# Complete project overview
echo "📊 PROJECT STATS:" && jq 'select(.type=="footer") | .stats' *.jsonl
echo "🏗️ ARCHITECTURE:" && jq 'select(.type=="function") | .cat' *.jsonl | sort | uniq -c
echo "📁 MODULE COUNT:" && jq 'select(.type=="module") | .name' *.jsonl | wc -l

# Module complexity ranking
jq 'select(.type=="module")' *.jsonl | jq -s 'sort_by(-.function_count) | .[] | "\(.name): \(.function_count) functions"'

# Find entry points (main functions)
jq 'select(.type=="function" and (.n | contains("main") or .n | contains("cli")))' *.jsonl | jq -r '"\(.n)() in \(.f):\(.l)"'
```

### 🎯 Pattern Recognition
```bash
# Find test functions
jq 'select(.type=="function" and (.f | contains("test") or .n | startswith("test_")))' *.jsonl | jq -r '"\(.n)() - \(.loc) LOC"'

# Find utility functions
jq 'select(.type=="function" and .cat=="utility")' *.jsonl | jq -r '"\(.n)(): \(.s)"'

# Functions by file pattern
jq 'select(.type=="function" and (.f | contains("PATTERN")))' *.jsonl | jq -r '"\(.f): \(.n)()"'
```

**💡 Pro Tips:**
- Use single `jq` for filtering, pipe to `jq -r` for formatting
- Always test queries on small files first
- Use `head -5` to limit output during testing
- Escape special characters in search patterns

### 🔍 Deep-Dive Analysis (Power User Queries)
```bash
# Functions with full context (name, signature, location)
jq -s 'map(select(.type=="function")) | map({name: .n, signature: .s, file: .f, line: .l})' *.jsonl

# Find duplicated functions (code quality analysis)
jq -s 'map(select(.type=="function")) | group_by(.n) | map(select(length > 1)) | map({name: .[0].n, duplicates: length})' *.jsonl

# API surface analysis (public functions)
jq -s 'map(select(.type=="function" and .cat=="core_api")) | map({name: .n, signature: .s})' *.jsonl

# Module complexity analysis
jq -s 'map(select(.type=="module")) | map({module: .name, complexity: .function_count}) | sort_by(-.complexity)' *.jsonl
```

### Module & Architecture Analysis
```bash
# Module overview with function counts
jq 'select(.type=="module") | {name, function_count, category}' semantic.jsonl

# Find core modules
jq 'select(.type=="module" and .category=="core")' semantic.jsonl

# API surface analysis
jq 'select(.type=="module" and .category=="api") | {name, function_count}' semantic.jsonl
```

### Pattern & Cluster Intelligence
```bash
# Usage patterns
jq 'select(.type=="pattern") | {name, usage, function_count}' semantic.jsonl

# Semantic clusters (architecture overview)
jq 'select(.type=="cluster") | {name, description, module_count}' semantic.jsonl

# CRUD patterns
jq 'select(.type=="pattern" and .name | contains("crud"))' semantic.jsonl
```

### Advanced Semantic Analysis
```bash
# Functions with full context
jq 'select(.type=="function") | {name: .n, sig: .s, module: .m, file: .f, line: .l}' semantic.jsonl

# Group functions by category
jq 'select(.type=="function") | .cat' semantic.jsonl | sort | uniq -c

# Find test functions
jq 'select(.type=="function" and (.n | contains("test") or .m | contains("test")))' semantic.jsonl

# API surface functions only
jq 'select(.type=="function" and .cat=="core_api") | {name: .n, signature: .s}' semantic.jsonl
```

## 📊 Legacy MSGPACK Support (Requires Python)

For compressed `.msgpack` files, use Python conversion first:

### MSGPACK Structure Schema
```json
{
  "functions": [
    {
      "id": 42,                         // Unique function ID
      "n": "function_name",             // Function name
      "s": "def function_name(param)",  // Full signature with parameters
      "d": 15,                          // Docstring index (see strings table)
      "m": "/path/to/module",           // Full module path
      "t": ["code", "stable"],          // Tags (code type, stability)
      "f": "file.py",                   // Source file (when available)  
      "l": 42                           // Line number (when available)
    }
  ],
  "strings": ["docstring1", "docstring2", ...],  // Compressed string table
  "modules": {...},                     // Module hierarchy
  "patterns": {...}                     // Usage patterns
}
```

### MSGPACK Queries (Python Required)
```bash
# Convert msgpack to JSON first
python3 -c "import msgpack, json, sys; print(json.dumps(msgpack.unpack(open(sys.argv[1], 'rb'))))" file.msgpack | jq 'keys'

# Get functions with string table resolution
python3 -c "import msgpack, json; data=msgpack.unpack(open('FILE.msgpack', 'rb')); print(json.dumps([{'name': f['n'], 'sig': f['s'], 'doc': data.get('strings',[{}])[f.get('d',0)] if f.get('d',0) < len(data.get('strings',[])) else ''} for f in data.get('functions',[])]))" | jq '.'
```

## Files Generated by repolex v2.0

Each `.msgpack` file contains the semantic DNA of a repository:
- **Functions**: All functions with signatures and metadata
- **Modules**: Code organization and hierarchy  
- **Patterns**: Common usage patterns for better code generation
- **Semantic Clusters**: Related function groups
- **String Table**: Compressed deduplication for minimal size

## 🟡 PAC-MAN Semantic Loading Strategy 🟡

**The Three-Tier Approach to Semantic Intelligence:**

### 🔴 **Nibble Mode** (Lightning Fast)
**Zero-dependency jq queries for instant insights**
```bash
jq 'select(.type=="footer") | .stats' *.jsonl    # Repository overview
jq -s 'map(select(.type=="function")) | length' *.jsonl    # Function count
```
- **Use when**: Quick exploration, specific function lookup
- **Speed**: Instant (<1 second)
- **Context**: Minimal, targeted

### 🟡 **Pellet Mode** (Focused Understanding)
**Load semantic DNA for one repository at a time**
```bash
# Load main repo semantic intelligence
jq -s 'map(select(.type=="function"))' main-repo~latest.jsonl
```
- **Use when**: Deep-dive into specific repository
- **Speed**: Fast (1-5 seconds)
- **Context**: Complete single-repo understanding

### 🔵 **Power Pellet Mode** (Omniscient Analysis)
**Load ALL semantic intelligence for complete ecosystem understanding**
```bash  
# Load everything - full semantic ecosystem
jq -s 'map(select(.type=="function"))' *.jsonl
```
- **Use when**: Cross-repository analysis, architectural decisions
- **Speed**: Comprehensive (5-30 seconds)
- **Context**: Complete project ecosystem

**Perfect for LLM context injection - scalable semantic intelligence!** 

## Current Repository Intelligence

**🎯 MAIN REPOSITORY:**
- **goodlux~repolex~latest.jsonl** (70KB) - Main repository (all access levels)

**🔥 DEPENDENCIES (2.8MB Total Semantic DNA):**
- **pydantic~pydantic~2.0.jsonl** (1.0MB) - Data validation framework
- **giampaolo~psutil~5.9.jsonl** (543KB) - System monitoring
- **Delgan~loguru~0.7.jsonl** (474KB) - Enhanced logging
- **lxml~lxml~4.9.jsonl** (403KB) - XML/HTML processing
- **pallets~click~8.0.jsonl** (195KB) - Command line interface framework

**📦 ADDITIONAL LIBRARIES:**
- **gitpython-developers~GitPython~3.1.jsonl** (73KB) - Git repository interface
- **msgpack~msgpack-python~1.0.jsonl** (37KB) - Binary serialization format
- **urchade~GLiNER~0.2.21.jsonl** (17KB) - Named entity recognition
- **oxigraph~oxigraph~0.4.9.jsonl** (9KB) - RDF database engine

**Total: 10 semantic DNA files representing a complete Python ecosystem!**

## Usage Examples

```bash
# Convert any msgpack to JSON first (they're binary files)
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('FILE.msgpack', 'rb'))))" | jq '.'

# Get all table-related functions from pandas
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('pandas-dev~pandas~latest.msgpack', 'rb'))))" | jq '.functions[] | select(.n | contains("table") or .n | contains("Table"))'

# Find data processing functions in numpy  
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('numpy~numpy~latest.msgpack', 'rb'))))" | jq '.functions[] | select(.n | test("^(array|matrix|reshape)"))'

# Get module overview from any library
python3 -c "import msgpack, json; print(json.dumps(msgpack.unpack(open('sqlalchemy~sqlalchemy~latest.msgpack', 'rb'))))" | jq '.modules | keys'

# Cross-library function search
for file in *.msgpack; do echo "=== $file ==="; python3 -c "import msgpack, json, sys; print(json.dumps(msgpack.unpack(open(sys.argv[1], 'rb'))))" "$file" | jq '.functions[] | select(.n | contains("create"))' | head -3; done
```

---
*Generated by repolex v2.0 - The semantic intelligence system*  
*🧬 Semantic DNA optimized for LLM consumption*
