"""
Simple interactive menu for rlex command when no arguments provided.
"""

import sys


def show_interactive_menu():
    """Show simple numbered menu for basic operations."""
    
    while True:
        print("\nRepolex - Semantic Code Intelligence")
        print("=" * 35)
        print("1. List repositories")
        print("2. Add repository")
        print("3. List graphs")
        print("4. Add graph")
        print("5. Run query")
        print("6. Show help")
        print("7. Exit")
        print()
        
        try:
            choice = input("Select option (1-7): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            from repolex.cli.main import cli
            cli(["repo", "list"])
        elif choice == "2":
            repo = input("Enter repository (org/repo): ").strip()
            if repo:
                from repolex.cli.main import cli
                cli(["repo", "add", repo])
        elif choice == "3":
            from repolex.cli.main import cli
            cli(["graph", "list"])
        elif choice == "4":
            repo = input("Enter repository (org/repo): ").strip()
            if repo:
                release = input("Enter release (or press Enter for latest): ").strip()
                from repolex.cli.main import cli
                if release:
                    cli(["graph", "add", repo, release])
                else:
                    cli(["graph", "add", repo])
        elif choice == "5":
            query = input("Enter SPARQL query: ").strip()
            if query:
                from repolex.cli.main import cli
                cli(["query", "sparql", query])
        elif choice == "6":
            from repolex.cli.main import cli
            cli(["--help"])
        elif choice == "7":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1-7.")
