#!/usr/bin/env python3
"""
API Test Script - ChukMCP Server Async-Native API Validation

This script tests the ChukMCP Server API by making actual HTTP requests
to the running echo service, validating the async-native developer experience.
"""

import asyncio
import httpx
import time
from typing import Dict, Any


class MCPTestClient:
    """Simple MCP test client for API validation."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.mcp_url = f"{base_url}/mcp"
        self.session_id = None
        self.request_id = 0

    def next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id

    async def initialize(self) -> Dict[str, Any]:
        """Initialize MCP connection."""
        request = {
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "clientInfo": {"name": "API Test Client", "version": "1.0.0"},
            },
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.mcp_url, json=request)
            response.raise_for_status()

            # Extract session ID from headers
            self.session_id = response.headers.get("Mcp-Session-Id")

            data = response.json()
            return data

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool."""
        request = {
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }

        headers = {}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.mcp_url, json=request, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data

    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read an MCP resource."""
        request = {
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": "resources/read",
            "params": {"uri": uri},
        }

        headers = {}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.mcp_url, json=request, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data


class AsyncAPIValidator:
    """Validate the async-native ChukMCP Server API experience."""

    def __init__(self):
        self.client = MCPTestClient()
        self.results = []

    def log_result(
        self, test_name: str, success: bool, message: str, details: Any = None
    ):
        """Log a test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")

        self.results.append(
            {
                "test": test_name,
                "success": success,
                "message": message,
                "details": details,
            }
        )

    async def test_server_availability(self) -> bool:
        """Test if the echo service is running."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.client.base_url}/health")
                if response.status_code == 200:
                    data = response.json()
                    server_name = data.get("server", {}).get("name", "Unknown")
                    self.log_result(
                        "Server Availability",
                        True,
                        f"Echo service running: {server_name}",
                    )
                    return True
                else:
                    self.log_result(
                        "Server Availability",
                        False,
                        f"Health check failed: HTTP {response.status_code}",
                    )
                    return False
        except Exception as e:
            self.log_result(
                "Server Availability", False, f"Cannot connect to server: {e}"
            )
            return False

    async def test_mcp_initialization(self) -> bool:
        """Test MCP protocol initialization."""
        try:
            result = await self.client.initialize()

            if "result" in result:
                server_info = result["result"]["serverInfo"]
                self.log_result(
                    "MCP Initialization",
                    True,
                    f"Connected to {server_info['name']} v{server_info['version']}",
                )
                return True
            else:
                self.log_result(
                    "MCP Initialization", False, f"Initialization failed: {result}"
                )
                return False
        except Exception as e:
            self.log_result("MCP Initialization", False, f"Initialization error: {e}")
            return False

    async def test_async_concurrency(self) -> bool:
        """Test async concurrency with delay tools."""
        try:
            print("   Testing concurrent execution of 3 delay tools...")
            start_time = time.time()

            # Execute 3 delay tools concurrently (each with 0.5s delay)
            tasks = [
                self.client.call_tool(
                    "echo_delay",
                    {"message": f"Concurrent request {i}", "delay_seconds": 0.5},
                )
                for i in range(1, 4)
            ]

            results = await asyncio.gather(*tasks)
            end_time = time.time()
            total_time = end_time - start_time

            # Verify all tools executed successfully
            all_successful = all(
                "result" in result and "content" in result["result"]
                for result in results
            )

            # Should complete in ~0.5 seconds (concurrent) not ~1.5 seconds (sequential)
            is_concurrent = total_time < 1.0

            if all_successful and is_concurrent:
                self.log_result(
                    "Async Concurrency",
                    True,
                    f"3 concurrent 0.5s delays completed in {total_time:.2f}s (async working!)",
                )
                return True
            else:
                self.log_result(
                    "Async Concurrency",
                    False,
                    f"Concurrency test failed: {total_time:.2f}s duration, success: {all_successful}",
                )
                return False

        except Exception as e:
            self.log_result("Async Concurrency", False, f"Concurrency test error: {e}")
            return False

    async def test_basic_tools(self) -> bool:
        """Test basic async tool execution."""
        test_cases = [
            {
                "name": "echo_text",
                "arguments": {"message": "Hello Async World!"},
                "description": "Basic text echo",
            },
            {
                "name": "echo_json",
                "arguments": {"data": {"async": True, "test": "validation"}},
                "description": "JSON echo with metadata",
            },
            {
                "name": "echo_list",
                "arguments": {"items": [3, 1, 4, 1, 5], "sort": True},
                "description": "List processing",
            },
            {
                "name": "echo_uppercase",
                "arguments": {"text": "async is awesome"},
                "description": "Text transformation",
            },
        ]

        all_passed = True

        for test_case in test_cases:
            try:
                result = await self.client.call_tool(
                    test_case["name"], test_case["arguments"]
                )

                if "result" in result and "content" in result["result"]:
                    content = result["result"]["content"]
                    if content and len(content) > 0:
                        self.log_result(
                            f"Tool: {test_case['name']}",
                            True,
                            f"{test_case['description']} - executed successfully",
                        )
                    else:
                        self.log_result(
                            f"Tool: {test_case['name']}",
                            False,
                            "Empty content in response",
                        )
                        all_passed = False
                else:
                    self.log_result(
                        f"Tool: {test_case['name']}",
                        False,
                        f"Invalid response format: {result}",
                    )
                    all_passed = False
            except Exception as e:
                self.log_result(
                    f"Tool: {test_case['name']}", False, f"Execution error: {e}"
                )
                all_passed = False

        return all_passed

    async def test_async_resources(self) -> bool:
        """Test async resource access."""
        resources_to_test = [
            ("echo://config", "Service configuration"),
            ("echo://status", "Service status"),
            ("echo://examples", "Usage examples"),
        ]

        try:
            # Test concurrent resource reads
            print("   Testing concurrent resource reads...")
            start_time = time.time()

            tasks = [self.client.read_resource(uri) for uri, _ in resources_to_test]

            results = await asyncio.gather(*tasks)
            end_time = time.time()
            total_time = end_time - start_time

            # Verify all resources read successfully
            all_successful = True
            for i, result in enumerate(results):
                uri, description = resources_to_test[i]
                if "result" in result and "contents" in result["result"]:
                    contents = result["result"]["contents"]
                    if contents and len(contents) > 0:
                        self.log_result(
                            f"Resource: {uri}",
                            True,
                            f"{description} - read successfully",
                        )
                    else:
                        self.log_result(
                            f"Resource: {uri}", False, "Empty contents in response"
                        )
                        all_successful = False
                else:
                    self.log_result(
                        f"Resource: {uri}", False, f"Invalid response format: {result}"
                    )
                    all_successful = False

            if all_successful:
                self.log_result(
                    "Async Resources",
                    True,
                    f"3 concurrent resources read in {total_time:.2f}s",
                )

            return all_successful

        except Exception as e:
            self.log_result("Async Resources", False, f"Resource access error: {e}")
            return False

    async def test_error_handling(self) -> bool:
        """Test async error handling."""
        try:
            result = await self.client.call_tool(
                "echo_error",
                {"should_error": True, "error_message": "Test async error"},
            )

            # This should return an error response
            if "error" in result:
                self.log_result(
                    "Error Handling",
                    True,
                    f"Async error properly handled: {result['error']['message']}",
                )
                return True
            else:
                self.log_result(
                    "Error Handling",
                    False,
                    f"Expected error response but got: {result}",
                )
                return False
        except Exception as e:
            # HTTP-level errors are also acceptable
            if "Test async error" in str(e):
                self.log_result(
                    "Error Handling", True, f"Async error properly propagated: {e}"
                )
                return True
            else:
                self.log_result("Error Handling", False, f"Unexpected error: {e}")
                return False

    async def test_performance(self) -> bool:
        """Test async performance characteristics."""
        try:
            print("   Testing async performance with 10 rapid calls...")
            start_time = time.time()
            iterations = 10

            # Execute multiple fast tools concurrently
            tasks = [
                self.client.call_tool("echo_text", {"message": f"Performance test {i}"})
                for i in range(iterations)
            ]

            results = await asyncio.gather(*tasks)
            end_time = time.time()

            total_time = end_time - start_time
            avg_time = (total_time / iterations) * 1000  # ms per call

            # All should succeed
            all_successful = all(
                "result" in result and "content" in result["result"]
                for result in results
            )

            # Should be reasonably fast
            acceptable_performance = (
                avg_time < 200
            )  # Less than 200ms per call on average

            if all_successful and acceptable_performance:
                self.log_result(
                    "Performance",
                    True,
                    f"10 concurrent calls: {avg_time:.1f}ms avg, {total_time:.2f}s total",
                )
                return True
            else:
                self.log_result(
                    "Performance",
                    False,
                    f"Performance test failed: {avg_time:.1f}ms avg, success: {all_successful}",
                )
                return False

        except Exception as e:
            self.log_result("Performance", False, f"Performance test error: {e}")
            return False

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all async API validation tests."""
        print("🧪 ChukMCP Server Async-Native API Validation")
        print("=" * 70)
        print("Testing Echo Service async capabilities...")
        print()

        tests = [
            ("Server Availability", self.test_server_availability),
            ("MCP Initialization", self.test_mcp_initialization),
            ("Basic Tools", self.test_basic_tools),
            ("Async Concurrency", self.test_async_concurrency),
            ("Async Resources", self.test_async_resources),
            ("Error Handling", self.test_error_handling),
            ("Performance", self.test_performance),
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            try:
                success = await test_func()
                if success:
                    passed += 1
            except Exception as e:
                self.log_result(test_name, False, f"Test failed with exception: {e}")

        print("\n" + "=" * 70)
        print(f"📊 Test Results: {passed}/{total} tests passed")

        success_rate = (passed / total) * 100

        if passed == total:
            print("🎉 All tests passed! ChukMCP Server async-native API is excellent!")
            print("\n🎯 Validation Summary:")
            print("   ✅ Async tools work perfectly")
            print("   ✅ Concurrent execution confirmed")
            print("   ✅ Non-blocking I/O throughout")
            print("   ✅ MCP protocol compliance")
            print("   ✅ Error handling works correctly")
            print("   ✅ Performance is acceptable")
        elif success_rate >= 80:
            print(f"👍 Most tests passed ({success_rate:.1f}% success rate)")
            print("   Minor issues to address, but overall good async support")
        else:
            print(f"⚠️  Several tests failed ({success_rate:.1f}% success rate)")
            print("   Review failed tests above for async issues")

        return {
            "total_tests": total,
            "passed_tests": passed,
            "success_rate": success_rate,
            "results": self.results,
        }


async def main():
    """Main function to run async API validation."""
    print("🚀 ChukMCP Server Async-Native API Test Suite")
    print()
    print("Prerequisites:")
    print("  • Echo service should be running on http://localhost:8000")
    print("  • Start with: uv run chuk-mcp-echo")
    print()

    # Check if user wants to continue
    try:
        input("Press Enter to start testing (Ctrl+C to cancel)...")
    except KeyboardInterrupt:
        print("\n👋 Test cancelled.")
        return

    print()

    validator = AsyncAPIValidator()
    results = await validator.run_all_tests()

    # Final summary
    print("\n📋 Final Summary:")
    print(f"   Tests Passed: {results['passed_tests']}/{results['total_tests']}")
    print(f"   Success Rate: {results['success_rate']:.1f}%")

    if results["success_rate"] == 100:
        print("\n🎯 ChukMCP Server Async API: EXCELLENT ⭐⭐⭐⭐⭐")
        print(
            "   Your framework provides outstanding async-native developer experience!"
        )
    elif results["success_rate"] >= 80:
        print("\n👍 ChukMCP Server Async API: GOOD ⭐⭐⭐⭐")
        print("   Strong async support with minor areas for improvement")
    else:
        print("\n⚠️  ChukMCP Server Async API: NEEDS WORK ⭐⭐")
        print("   Async functionality needs attention")

    print("\n💡 Next Steps:")
    if results["success_rate"] == 100:
        print("   • Test with MCP Inspector for full validation")
        print("   • Try building more complex async services")
        print("   • Share your framework - it's ready for production!")
    else:
        print("   • Review failed tests above")
        print("   • Fix async-related issues")
        print("   • Re-run tests to validate fixes")


if __name__ == "__main__":
    asyncio.run(main())
