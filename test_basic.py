#!/usr/bin/env python3
"""Basic test to verify Repolex module loading."""

print("Testing Repolex module loading...")

try:
    print("Importing core modules...")
    import repolex
    print("✓ Core repolex package loaded")
    
    from repolex.models.exceptions import RepolexError
    print("✓ Exception models loaded")
    
    from repolex.utils.validation import validate_org_repo
    print("✓ Validation utilities loaded")
    
    from repolex.utils.file_utils import ensure_directory
    print("✓ File utilities loaded")
    
    print("✓ All basic imports successful!")

except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()