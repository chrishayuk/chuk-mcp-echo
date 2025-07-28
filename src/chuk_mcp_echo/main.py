#!/usr/bin/env python3
# src/chuk_mcp_echo/main.py
"""
Echo Service Main - Entry point for the async native echo service
"""

from .server import echo_service
from . import tools  # Import to register tools
from . import resources  # Import to register resources

def main():
    """Main function to run the echo service."""
    
    print("🔄 Echo Service - ChukMCP Server Test (Async Native)")
    print("=" * 50)
    
    # Show what we've registered
    registered_tools = echo_service.get_tools()
    registered_resources = echo_service.get_resources()
    
    print(f"📝 Registered Async Tools ({len(registered_tools)}):")
    for tool in registered_tools:
        print(f"   - {tool.name}: {tool.description}")
    
    print(f"\n📂 Registered Async Resources ({len(registered_resources)}):")
    for resource in registered_resources:
        print(f"   - {resource.uri}: {resource.description}")
    
    print(f"\n🔍 Developer Experience Test (Async Native):")
    print(f"   - All tools are async/await native")
    print(f"   - All resources use async handlers")
    print(f"   - Non-blocking I/O throughout")
    print(f"   - Proper asyncio.sleep() for delays")
    print(f"   - Async-first architecture")
    
    print(f"\n🌐 Testing Instructions:")
    print(f"   1. Run this service: chuk-mcp-echo")
    print(f"   2. Server will start on: http://localhost:8000")
    print(f"   3. MCP endpoint: http://localhost:8000/mcp")
    print(f"   4. All operations are non-blocking async")
    print(f"   5. Test 'echo_delay' to see async behavior")
    print(f"   6. Multiple concurrent requests work perfectly")
    
    print("=" * 50)
    
    # Run the service
    try:
        echo_service.run(
            host="localhost",
            port=8000,
            debug=True  # Enable debug mode for development
        )
    except KeyboardInterrupt:
        print("\n👋 Echo service shutting down...")
    except Exception as e:
        print(f"❌ Service error: {e}")

if __name__ == "__main__":
    main()