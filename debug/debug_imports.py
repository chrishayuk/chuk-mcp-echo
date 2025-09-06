#!/usr/bin/env python3
"""
Debug script to check import issues
"""

import sys
import subprocess

print("🔍 Debugging Import Issues")
print("=" * 50)

# Check Python version and path
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Check if chuk_mcp_server is importable
print("Testing chuk_mcp_server import:")
try:
    import chuk_mcp_server

    print("✅ chuk_mcp_server imported successfully")
    print(f"   Location: {chuk_mcp_server.__file__}")
    print(f"   Version: {getattr(chuk_mcp_server, '__version__', 'unknown')}")

    # Check specific imports
    try:
        from chuk_mcp_server import ChukMCPServer  # noqa: F401

        print("✅ ChukMCPServer imported successfully")
    except ImportError as e:
        print(f"❌ ChukMCPServer import failed: {e}")

except ImportError as e:
    print(f"❌ chuk_mcp_server import failed: {e}")

print()

# Check installed packages
print("Checking installed packages:")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
    )
    lines = result.stdout.split("\n")
    chuk_packages = [line for line in lines if "chuk" in line.lower()]
    if chuk_packages:
        print("Found chuk-related packages:")
        for pkg in chuk_packages:
            print(f"  {pkg}")
    else:
        print("❌ No chuk-related packages found")
except Exception as e:
    print(f"Error checking packages: {e}")

print()

# Check sys.path
print("Python path (first 5 entries):")
for i, path in enumerate(sys.path[:5]):
    print(f"  {i}: {path}")

print()

# Try to import the echo service components
print("Testing echo service imports:")
try:
    sys.path.insert(0, "src")
    import chuk_mcp_echo  # noqa: F401

    print("✅ chuk_mcp_echo imported successfully")

    try:
        from chuk_mcp_echo import echo_service  # noqa: F401

        print("✅ echo_service imported successfully")
    except ImportError as e:
        print(f"❌ echo_service import failed: {e}")

except ImportError as e:
    print(f"❌ chuk_mcp_echo import failed: {e}")
