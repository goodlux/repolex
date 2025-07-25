"""
🟡 Repolex Storage System - PAC-MAN chomps through semantic data!

WAKA WAKA WAKA! This module manages our semantic maze where:
- Oxigraph is the game board (database)
- Graphs are the levels in our maze
- Triples are the dots PAC-MAN eats
- Nuclear updates are power pellets that clear ghosts!

The storage system implements the 19-graph architecture:
- 4 Ontology graphs (the maze walls)
- 2 Function graphs (stable identities + implementations)  
- File structure graphs (the maze layout)
- 4 Git intelligence graphs (ghost intelligence)
- 1 ABC events graph (score tracking)
- 3 Evolution analysis graphs (game statistics)
- Processing metadata (game state)

🌟 Ready to chomp some semantic dots! 🟡
"""

# The storage system exports
__all__ = [
    "OxigraphClient",
    "GraphBuilder", 
    "RepositoryStore",
    "GraphSchemas"
]
