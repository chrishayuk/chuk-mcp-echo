#!/usr/bin/env python3
"""
Test suite for Echo Service (Async Native) - Fixed imports
"""

import pytest
import asyncio
import json
import sys
from pathlib import Path

# Add src to path before any other imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Now we can import our modules
pytest_plugins = ['pytest_asyncio']

class TestBasicImports:
    """Test that we can import everything we need."""
    
    def test_chuk_mcp_server_import(self):
        """Test chuk_mcp_server import."""
        try:
            import chuk_mcp_server
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
            echo_text("Quick message")
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
            "echo_text", "echo_uppercase", "echo_reverse",
            "echo_json", "echo_list", "echo_number", 
            "echo_delay", "echo_error", "get_service_info"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Tool {expected_tool} should be registered"
        
        # Check expected resources
        resource_uris = [r.uri for r in resources]
        expected_resources = [
            "echo://config", "echo://status", 
            "echo://examples", "echo://docs"
        ]
        
        for expected_resource in expected_resources:
            assert expected_resource in resource_uris, f"Resource {expected_resource} should be registered"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])