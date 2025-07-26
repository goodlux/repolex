#!/usr/bin/env python3
"""
Debug script to see what the parser actually returns
"""

import sys
from pathlib import Path

# Add the repolex module to the path
sys.path.insert(0, str(Path(__file__).parent))

from repolex.parsers.python_parser import PythonParser

def main():
    parser = PythonParser()
    
    # Get the pixeltable repo path
    repo_path = Path.home() / ".repolex" / "repos" / "pixeltable" / "pixeltable"
    
    print(f"🔍 Testing parser on: {repo_path}")
    print(f"Repo exists: {repo_path.exists()}")
    
    if not repo_path.exists():
        print("❌ Repository not found!")
        return
    
    # Check what Python files the parser finds
    python_files = list(repo_path.rglob("*.py"))
    print(f"\n🔍 Python files found by rglob:")
    print(f"  Count: {len(python_files)}")
    if len(python_files) > 0:
        print(f"  First few: {[str(f) for f in python_files[:5]]}")
        
        # Check the filtering logic
        first_file = python_files[0]
        print(f"\n🔍 Testing filter on first file: {first_file}")
        print(f"  Parts: {first_file.parts}")
        print(f"  Has dot-prefix parts: {any(part.startswith('.') for part in first_file.parts)}")
        print(f"  Test filter: {'test' in first_file.name.lower() and not first_file.name.startswith('test_')}")
    
    # Try to parse the repository
    try:
        result = parser.parse_repository(repo_path, "latest", "pixeltable/pixeltable")
        
        print(f"\n📊 Parser Results:")
        print(f"  Org/Repo: {result.org_repo}")
        print(f"  Release: {result.release}")
        print(f"  Total functions: {result.total_functions}")
        print(f"  Total classes: {result.total_classes}")
        print(f"  Files processed: {len(result.files)}")
        
        print(f"\n🔍 Examining all_functions property:")
        all_funcs = result.all_functions
        print(f"  Type: {type(all_funcs)}")
        print(f"  Length: {len(all_funcs)}")
        
        if len(all_funcs) > 0:
            print(f"\n🔍 First function details:")
            first_func = all_funcs[0]
            print(f"  Type: {type(first_func)}")
            print(f"  Content: {first_func}")
            
            if isinstance(first_func, dict):
                print(f"  Keys: {list(first_func.keys())}")
        
        print(f"\n🔍 Examining first file:")
        if len(result.files) > 0:
            first_file = result.files[0]
            print(f"  File path: {first_file.file_path}")
            print(f"  Functions count: {len(first_file.functions)}")
            print(f"  Classes count: {len(first_file.classes)}")
            
            if len(first_file.functions) > 0:
                print(f"  First function type: {type(first_file.functions[0])}")
                print(f"  First function: {first_file.functions[0]}")
        
    except Exception as e:
        print(f"❌ Parser failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()