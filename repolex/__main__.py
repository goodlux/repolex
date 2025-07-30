#!/usr/bin/env python3
"""
repolex - Semantic Code Intelligence System
Entry point for the rlex command.
"""

import sys
from pathlib import Path

def setup_environment():
    """Set up the repolex environment and paths."""
    # Ensure storage directory exists
    storage_path = Path.home() / ".repolex"
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
    Main entry point for rlex command.
    
    If no arguments: Show interactive menu
    If arguments: Use CLI commands
    """
    
    # Set up environment first
    setup_environment()
    
    if len(sys.argv) == 1:
        # No arguments - show interactive menu
        from repolex.cli.interactive import show_interactive_menu
        show_interactive_menu()
    else:
        # Arguments provided - use CLI (command mode)
        from repolex.cli.main import cli
        cli()

if __name__ == "__main__":
    main()
