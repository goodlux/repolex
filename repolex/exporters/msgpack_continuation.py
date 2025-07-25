#!/usr/bin/env python3
"""
🚀 PAC-MAN's MsgPack Export POWERHOUSE! 🚀 - CONTINUED
Ultra-compact semantic packages with 125x compression for LLM consumption!
"""

# [Previous content would be here - this is the continuation of the _get_type_id method]

    def _get_type_id(self, type_string: str) -> int:
        """Get type ID from type mapping cache"""
        if not type_string or not isinstance(type_string, str):
            return 0  # "Any" type at index 0
        
        # Check cache first
        if type_string in self.type_mapping_cache:
            return self.type_mapping_cache[type_string]
        
        # Add new type to cache
        type_id = len(self.type_mapping_cache)
        self.type_mapping_cache[type_string] = type_id
        return type_id

# Continue with the rest of the methods...

if __name__ == "__main__":
    print("🚀 PAC-MAN MsgPack Export Powerhouse - WAKA WAKA!")
