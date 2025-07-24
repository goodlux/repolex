#!/usr/bin/env python3
"""Quick test to see if our PAC-MAN system loads without errors!"""

print("🟡 Testing PAC-MAN CodeDoc loading...")

try:
    print("🔄 Importing PAC-MAN's core systems...")
    from codedoc.core.interface import CodeDocCore
    print("✅ PAC-MAN interface loaded!")
    
    from codedoc.models.results import ProcessingResult
    print("✅ PAC-MAN results loaded!")
    
    from codedoc.models.graph import GraphInfo
    print("✅ PAC-MAN graph models loaded!")
    
    print("🟡 WAKA WAKA! All systems operational!")

except Exception as e:
    print(f"💥 Ghost encounter! Error: {e}")
    import traceback
    traceback.print_exc()
