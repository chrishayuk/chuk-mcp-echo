#!/usr/bin/env python3
"""
Simple test that checks basic functionality without complex imports
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_python_path():
    """Test that we can access the source directory."""
    assert src_path.exists()
    assert (src_path / "chuk_mcp_echo").exists()
    assert (src_path / "chuk_mcp_echo" / "__init__.py").exists()


def test_chuk_mcp_server_available():
    """Test if chuk_mcp_server is available."""
    try:
        import chuk_mcp_server  # noqa: F401

        assert True, "chuk_mcp_server is available"
    except ImportError as e:
        pytest.fail(f"chuk_mcp_server not available: {e}")


def test_chuk_mcp_server_components():
    """Test specific components we need."""
    try:
        from chuk_mcp_server import ChukMCPServer

        assert ChukMCPServer is not None
    except ImportError as e:
        pytest.fail(f"ChukMCPServer not available: {e}")


@pytest.mark.asyncio
async def test_async_functionality():
    """Test basic async functionality."""
    import asyncio

    async def simple_async_func():
        await asyncio.sleep(0.001)
        return "async works"

    result = await simple_async_func()
    assert result == "async works"


def test_package_importable():
    """Test that our package can be imported."""
    try:
        import chuk_mcp_echo

        assert hasattr(chuk_mcp_echo, "echo_service")
    except ImportError as e:
        pytest.fail(f"chuk_mcp_echo package not importable: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
