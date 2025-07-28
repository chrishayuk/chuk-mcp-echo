#!/usr/bin/env python3
"""
Debug script to identify the specific issues with failing tests
"""

import asyncio
import httpx
import json
import time
import traceback

async def debug_echo_list():
    """Debug the echo_list tool that's failing."""
    print("🔍 Debugging echo_list tool...")
    
    mcp_url = "http://localhost:8000/mcp"
    
    # Initialize session first
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "clientInfo": {"name": "Debug Client", "version": "1.0.0"}
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Initialize
            response = await client.post(mcp_url, json=init_request)
            init_result = response.json()
            session_id = response.headers.get("Mcp-Session-Id")
            
            print(f"✅ Initialized with session: {session_id}")
            
            # Test echo_list tool
            list_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "echo_list",
                    "arguments": {"items": [3, 1, 4, 1, 5], "sort": True}
                }
            }
            
            headers = {"Mcp-Session-Id": session_id} if session_id else {}
            response = await client.post(mcp_url, json=list_request, headers=headers)
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            result = response.json()
            print(f"Response body:")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"❌ Error testing echo_list: {e}")
        traceback.print_exc()

async def debug_echo_delay():
    """Debug the echo_delay tool for async concurrency."""
    print("\n🔍 Debugging echo_delay tool...")
    
    mcp_url = "http://localhost:8000/mcp"
    
    # Initialize session first
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize", 
        "params": {
            "protocolVersion": "2025-03-26",
            "clientInfo": {"name": "Debug Client", "version": "1.0.0"}
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Initialize
            response = await client.post(mcp_url, json=init_request)
            session_id = response.headers.get("Mcp-Session-Id")
            
            print(f"✅ Initialized with session: {session_id}")
            
            # Test single echo_delay first
            print("Testing single echo_delay...")
            start_time = time.time()
            
            delay_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "echo_delay",
                    "arguments": {"message": "Test delay", "delay_seconds": 0.5}
                }
            }
            
            headers = {"Mcp-Session-Id": session_id} if session_id else {}
            response = await client.post(mcp_url, json=delay_request, headers=headers)
            
            end_time = time.time()
            actual_duration = end_time - start_time
            
            print(f"Single delay took: {actual_duration:.3f}s")
            print(f"Response status: {response.status_code}")
            
            result = response.json()
            print(f"Response:")
            print(json.dumps(result, indent=2))
            
            # Test concurrent delays
            print("\nTesting concurrent echo_delay...")
            start_time = time.time()
            
            delay_requests = [
                {
                    "jsonrpc": "2.0",
                    "id": 3 + i,
                    "method": "tools/call",
                    "params": {
                        "name": "echo_delay",
                        "arguments": {"message": f"Concurrent {i}", "delay_seconds": 0.5}
                    }
                }
                for i in range(3)
            ]
            
            # Send all requests concurrently
            tasks = [
                client.post(mcp_url, json=req, headers=headers)
                for req in delay_requests
            ]
            
            responses = await asyncio.gather(*tasks)
            end_time = time.time()
            concurrent_duration = end_time - start_time
            
            print(f"Concurrent delays took: {concurrent_duration:.3f}s")
            print(f"Expected: ~0.5s, Actual: {concurrent_duration:.3f}s")
            
            for i, response in enumerate(responses):
                result = response.json()
                print(f"Response {i}: {response.status_code}")
                if "error" in result:
                    print(f"  Error: {result['error']}")
                elif "result" in result:
                    content = result["result"].get("content", [])
                    if content:
                        print(f"  Success: {len(content)} content items")
                    else:
                        print(f"  Empty content")
                        
    except Exception as e:
        print(f"❌ Error testing echo_delay: {e}")
        traceback.print_exc()

async def debug_tools_list():
    """Check what tools are actually registered."""
    print("\n🔍 Checking registered tools...")
    
    mcp_url = "http://localhost:8000/mcp"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Initialize
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "clientInfo": {"name": "Debug Client", "version": "1.0.0"}
                }
            }
            
            response = await client.post(mcp_url, json=init_request)
            session_id = response.headers.get("Mcp-Session-Id")
            
            # List tools
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            headers = {"Mcp-Session-Id": session_id} if session_id else {}
            response = await client.post(mcp_url, json=tools_request, headers=headers)
            
            result = response.json()
            if "result" in result and "tools" in result["result"]:
                tools = result["result"]["tools"]
                print(f"✅ Found {len(tools)} tools:")
                
                for tool in tools:
                    print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
                    if tool['name'] in ['echo_list', 'echo_delay']:
                        print(f"    Schema: {json.dumps(tool.get('inputSchema', {}), indent=6)}")
            else:
                print(f"❌ Failed to list tools: {result}")
                
    except Exception as e:
        print(f"❌ Error listing tools: {e}")
        traceback.print_exc()

async def main():
    """Run all debug tests."""
    print("🐛 ChukMCP Server Debug - Investigating Failing Tests")
    print("=" * 60)
    
    await debug_tools_list()
    await debug_echo_list()
    await debug_echo_delay()
    
    print("\n" + "=" * 60)
    print("🔍 Debug complete. Check the output above for:")
    print("   1. JSONRPCError issues in echo_list")
    print("   2. Timing issues in echo_delay")
    print("   3. Tool registration problems")

if __name__ == "__main__":
    asyncio.run(main())