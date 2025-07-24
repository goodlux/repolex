#!/usr/bin/env python3
"""
🟡 CodeDoc - Semantic Code Intelligence System 🟡
Entry point that routes between CLI and TUI based on arguments.

WAKA WAKA! Welcome to the semantic PAC-MAN maze!
"""

import sys
import asyncio
from pathlib import Path

def setup_environment():
    """Set up the CodeDoc environment and paths."""
    # Ensure storage directory exists
    storage_path = Path.home() / ".codedoc"
    storage_path.mkdir(exist_ok=True)
    
    # Create subdirectories
    (storage_path / "repos").mkdir(exist_ok=True)
    (storage_path / "graph").mkdir(exist_ok=True)
    (storage_path / "exports").mkdir(exist_ok=True)
    (storage_path / "config").mkdir(exist_ok=True)
    (storage_path / "logs").mkdir(exist_ok=True)
    
    return storage_path

def main():
    """
    🟡 Main entry point - route to CLI or TUI based on arguments.
    
    If no arguments: Launch TUI (interactive PAC-MAN mode)
    If arguments: Use CLI (command mode)
    """
    
    # Set up environment first
    setup_environment()
    
    if len(sys.argv) == 1:
        # No arguments - launch TUI (PAC-MAN interactive mode!)
        print("🟡 WAKA WAKA! Launching CodeDoc TUI...")
        print("👻 Welcome to the semantic maze!")
        
        try:
            from codedoc.tui.app import CodeDocTUI
            app = CodeDocTUI()
            app.run()
        except ImportError:
            print("⚠️  TUI not available, falling back to CLI help")
            from codedoc.cli.main import cli
            cli(['--help'])
        except Exception as e:
            print(f"💥 TUI Error: {e}")
            print("🔧 Try using CLI commands instead: codedoc --help")
            sys.exit(1)
    else:
        # Arguments provided - use CLI (command mode)
        try:
            from codedoc.cli.main import cli
            cli()
        except Exception as e:
            print(f"💥 CLI Error: {e}")
            print("🔧 Check 'codedoc --help' for usage")
            sys.exit(1)

if __name__ == "__main__":
    main()
