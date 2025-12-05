#!/usr/bin/env python3
"""
Test suite for Echo Service (Async Native) - Fixed imports
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add src to path before any other imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now we can import our modules
pytest_plugins = ["pytest_asyncio"]


class TestBasicImports:
    """Test that we can import everything we need."""

    def test_chuk_mcp_server_import(self):
        """Test chuk_mcp_server import."""
        try:
            import chuk_mcp_server  # noqa: F401
            from chuk_mcp_server import ChukMCPServer

            assert ChukMCPServer is not None
        except ImportError as e:
            pytest.fail(f"Cannot import chuk_mcp_server: {e}")

    def test_echo_service_import(self):
        """Test echo service import."""
        try:
            from chuk_mcp_echo import echo_service

            assert echo_service is not None
        except ImportError as e:
            pytest.fail(f"Cannot import echo_service: {e}")


class TestEchoTools:
    """Test all async echo tools."""

    @pytest.mark.asyncio
    async def test_echo_text_basic(self):
        """Test basic text echoing."""
        from chuk_mcp_echo.tools import echo_text
        from chuk_mcp_echo import echo_service

        # Get the tool handler
        tool = None
        for t in echo_service.get_tools():
            if t.name == "echo_text":
                tool = t
                break

        assert tool is not None, "echo_text tool should be registered"

        # Test the underlying async function
        result = await echo_text("Hello")
        assert result == "Hello"

        result = await echo_text("Hello", prefix=">>> ", suffix=" <<<")
        assert result == ">>> Hello <<<"

    @pytest.mark.asyncio
    async def test_echo_uppercase(self):
        """Test uppercase conversion."""
        from chuk_mcp_echo.tools import echo_uppercase

        result = await echo_uppercase("hello world")
        assert result == "HELLO WORLD"

    @pytest.mark.asyncio
    async def test_echo_reverse(self):
        """Test text reversal."""
        from chuk_mcp_echo.tools import echo_reverse

        result = await echo_reverse("hello")
        assert result == "olleh"

    @pytest.mark.asyncio
    async def test_echo_json(self):
        """Test JSON echoing."""
        from chuk_mcp_echo.tools import echo_json

        test_data = {"name": "John", "age": 30}
        result = await echo_json(test_data)

        assert "echoed_data" in result
        assert result["echoed_data"] == test_data
        assert "timestamp" in result
        assert "keys_count" in result
        assert result["keys_count"] == 2

    @pytest.mark.asyncio
    async def test_echo_list(self):
        """Test list processing."""
        from chuk_mcp_echo.tools import echo_list

        # Basic list
        result = await echo_list([1, 2, 3])
        assert result["original"] == [1, 2, 3]
        assert result["processed"] == [1, 2, 3]
        assert result["count"] == 3

        # Sorted list
        result = await echo_list([3, 1, 2], sort=True)
        assert result["processed"] == [1, 2, 3]

        # Reversed list
        result = await echo_list([1, 2, 3], reverse=True)
        assert result["processed"] == [3, 2, 1]

    @pytest.mark.asyncio
    async def test_echo_delay(self):
        """Test async delay functionality."""
        from chuk_mcp_echo.tools import echo_delay
        import time

        start_time = time.time()
        result = await echo_delay("Test message", delay_seconds=0.1)
        end_time = time.time()

        # Should have actually delayed
        actual_duration = end_time - start_time
        assert actual_duration >= 0.1
        assert result["message"] == "Test message"
        assert result["requested_delay"] == 0.1
        assert result["actual_delay"] >= 0.1

    @pytest.mark.asyncio
    async def test_echo_number(self):
        """Test number operations."""
        from chuk_mcp_echo.tools import echo_number

        # Test with defaults
        result = await echo_number(10)
        assert result["original"] == 10
        assert result["result"] == 10  # 10 * 1 + 0

        # Test with multiply
        result = await echo_number(10, multiply=2)
        assert result["result"] == 20  # 10 * 2 + 0
        assert result["operations"]["multiplied_by"] == 2

        # Test with add
        result = await echo_number(10, add=5)
        assert result["result"] == 15  # 10 * 1 + 5
        assert result["operations"]["added"] == 5

        # Test with both
        result = await echo_number(10, multiply=3, add=7)
        assert result["result"] == 37  # 10 * 3 + 7

    @pytest.mark.asyncio
    async def test_echo_error(self):
        """Test error handling."""
        from chuk_mcp_echo.tools import echo_error

        # Test success case
        result = await echo_error(should_error=False)
        assert result["status"] == "success"
        assert "timestamp" in result

        # Test error case
        with pytest.raises(ValueError, match="Test error"):
            await echo_error(should_error=True, error_message="Test error")

    @pytest.mark.asyncio
    async def test_get_service_info(self):
        """Test service info retrieval."""
        from chuk_mcp_echo.tools import get_service_info

        result = await get_service_info()
        assert "service" in result
        assert result["service"]["name"] == "Echo Service"
        assert "capabilities" in result
        assert "tools_count" in result["capabilities"]
        assert "resources_count" in result["capabilities"]
        assert result["capabilities"]["tools_count"] > 0
        assert result["capabilities"]["resources_count"] > 0

    @pytest.mark.asyncio
    async def test_echo_list_sort_error(self):
        """Test list sorting with mixed types."""
        from chuk_mcp_echo.tools import echo_list

        # Test with mixed types that can't be sorted
        result = await echo_list([1, "two", 3], sort=True)
        # Should not crash, just skip sorting
        assert result["count"] == 3


class TestEchoResources:
    """Test all async echo resources."""

    @pytest.mark.asyncio
    async def test_get_echo_config(self):
        """Test configuration resource."""
        from chuk_mcp_echo.resources import get_echo_config

        config = await get_echo_config()
        assert config["service_name"] == "Echo Service"
        assert "features" in config
        assert "supported_operations" in config
        assert "limits" in config

    @pytest.mark.asyncio
    async def test_get_echo_status(self):
        """Test status resource."""
        from chuk_mcp_echo.resources import get_echo_status

        status = await get_echo_status()
        assert status["status"] == "running"
        assert "uptime_seconds" in status
        assert "service_info" in status
        assert status["service_info"]["ready"] is True

    @pytest.mark.asyncio
    async def test_get_echo_status_invalid_start_time(self):
        """Test status resource with invalid start_time."""
        from chuk_mcp_echo.resources import get_echo_status
        from chuk_mcp_echo import echo_service
        from unittest.mock import MagicMock

        # Mock session_manager to return invalid start_time
        original_sessions = echo_service.protocol.session_manager.sessions
        try:
            # Create a mock that returns invalid start_time
            mock_sessions = MagicMock()
            mock_sessions.get.return_value = "invalid"  # Not a number
            echo_service.protocol.session_manager.sessions = mock_sessions

            status = await get_echo_status()
            # Should still work, falling back to current time
            assert status["status"] == "running"
            assert "uptime_seconds" in status
        finally:
            # Restore original
            echo_service.protocol.session_manager.sessions = original_sessions

    @pytest.mark.asyncio
    async def test_get_usage_examples(self):
        """Test usage examples resource."""
        from chuk_mcp_echo.resources import get_usage_examples

        examples = await get_usage_examples()
        assert "description" in examples
        assert "examples" in examples
        assert "basic_text_echo" in examples["examples"]

    @pytest.mark.asyncio
    async def test_get_documentation(self):
        """Test documentation resource."""
        from chuk_mcp_echo.resources import get_documentation

        docs = await get_documentation()
        assert isinstance(docs, str)
        assert "Echo Service Documentation" in docs
        assert "## Overview" in docs


class TestAsyncConcurrency:
    """Test async concurrency features."""

    @pytest.mark.asyncio
    async def test_concurrent_tool_execution(self):
        """Test that multiple tools can run concurrently."""
        from chuk_mcp_echo.tools import echo_delay, echo_text
        import time

        # Run multiple async operations concurrently
        start_time = time.time()

        tasks = [
            echo_delay("Message 1", 0.1),
            echo_delay("Message 2", 0.1),
            echo_delay("Message 3", 0.1),
            echo_text("Quick message"),
        ]

        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Should complete in roughly 0.1 seconds (concurrent) not 0.3 (sequential)
        total_time = end_time - start_time
        assert total_time < 0.2  # Should be much faster than sequential execution
        assert len(results) == 4
        assert results[0]["message"] == "Message 1"
        assert results[3] == "Quick message"


class TestServiceIntegration:
    """Test service-level integration."""

    def test_service_registration(self):
        """Test that all tools and resources are registered."""
        from chuk_mcp_echo import echo_service

        tools = echo_service.get_tools()
        resources = echo_service.get_resources()

        # Check expected tools
        tool_names = [t.name for t in tools]
        expected_tools = [
            "echo_text",
            "echo_uppercase",
            "echo_reverse",
            "echo_json",
            "echo_list",
            "echo_number",
            "echo_delay",
            "echo_error",
            "get_service_info",
        ]

        for expected_tool in expected_tools:
            assert (
                expected_tool in tool_names
            ), f"Tool {expected_tool} should be registered"

        # Check expected resources
        resource_uris = [r.uri for r in resources]
        expected_resources = [
            "echo://config",
            "echo://status",
            "echo://examples",
            "echo://docs",
        ]

        for expected_resource in expected_resources:
            assert (
                expected_resource in resource_uris
            ), f"Resource {expected_resource} should be registered"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
