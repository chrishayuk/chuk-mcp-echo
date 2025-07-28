#!/usr/bin/env python3
# src/chuk_mcp_echo/tools.py
"""
Echo Service Tools - Async native tool implementations
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List

from .server import echo_service

# ============================================================================
# Text Processing Tools
# ============================================================================

@echo_service.tool
async def echo_text(message: str, prefix: str = "", suffix: str = "") -> str:
    """
    Echo a text message with optional prefix and suffix.
    
    Args:
        message: The message to echo
        prefix: Optional prefix to add
        suffix: Optional suffix to add
    """
    # Simulate async I/O for demonstration
    await asyncio.sleep(0.001)  # 1ms delay to show async nature
    result = f"{prefix}{message}{suffix}"
    return result

@echo_service.tool
async def echo_uppercase(text: str) -> str:
    """Convert text to uppercase and echo it back."""
    await asyncio.sleep(0.001)
    return text.upper()

@echo_service.tool
async def echo_reverse(text: str) -> str:
    """Reverse the text and echo it back."""
    await asyncio.sleep(0.001)
    return text[::-1]

# ============================================================================
# Data Processing Tools
# ============================================================================

@echo_service.tool
async def echo_json(data: dict) -> dict:
    """
    Echo JSON data back with metadata.
    
    Args:
        data: JSON object to echo
    """
    await asyncio.sleep(0.001)
    return {
        "echoed_data": data,
        "data_type": type(data).__name__,
        "timestamp": time.time(),
        "iso_timestamp": datetime.now().isoformat(),
        "keys_count": len(data) if isinstance(data, dict) else None
    }

@echo_service.tool
async def echo_list(items: list, sort: bool = False, reverse: bool = False) -> dict:
    """
    Echo a list back with processing options.
    
    Args:
        items: List of items to echo
        sort: Whether to sort the list
        reverse: Whether to reverse the list
    """
    await asyncio.sleep(0.001)
    processed_items = items.copy()
    
    if sort:
        try:
            processed_items = sorted(processed_items)
        except TypeError:
            # Can't sort mixed types
            pass
    
    if reverse:
        processed_items = processed_items[::-1]
    
    return {
        "original": items,
        "processed": processed_items,
        "operations": {
            "sorted": sort,
            "reversed": reverse
        },
        "count": len(items),
        "timestamp": datetime.now().isoformat()
    }

@echo_service.tool
async def echo_number(number: float, multiply: float = 1.0, add: float = 0.0) -> dict:
    """
    Echo a number back with optional mathematical operations.
    
    Args:
        number: The number to process
        multiply: Factor to multiply by
        add: Amount to add
    """
    await asyncio.sleep(0.001)
    result = (number * multiply) + add
    
    return {
        "original": number,
        "result": result,
        "operations": {
            "multiplied_by": multiply,
            "added": add
        },
        "is_integer": isinstance(result, int) or result.is_integer(),
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# Testing and Utility Tools
# ============================================================================

@echo_service.tool
async def echo_delay(message: str, delay_seconds: float = 1.0) -> dict:
    """
    Echo a message after a specified delay (for testing async behavior).
    
    Args:
        message: Message to echo
        delay_seconds: Delay in seconds before responding
    """
    start_time = time.time()
    await asyncio.sleep(delay_seconds)  # Use async sleep instead of blocking sleep
    end_time = time.time()
    
    return {
        "message": message,
        "requested_delay": delay_seconds,
        "actual_delay": round(end_time - start_time, 3),
        "timestamp": datetime.now().isoformat()
    }

@echo_service.tool
async def echo_error(should_error: bool = False, error_message: str = "Test error") -> dict:
    """
    Tool for testing error handling.
    
    Args:
        should_error: Whether to raise an error
        error_message: Error message to use if raising an error
    """
    await asyncio.sleep(0.001)
    if should_error:
        raise ValueError(error_message)
    
    return {
        "status": "success",
        "message": "No error requested",
        "timestamp": datetime.now().isoformat()
    }

@echo_service.tool
async def get_service_info() -> dict:
    """Get information about this echo service."""
    await asyncio.sleep(0.001)
    tools = echo_service.get_tools()
    resources = echo_service.get_resources()
    
    return {
        "service": {
            "name": "Echo Service",
            "version": "0.1.0",
            "description": "Simple echo service for testing ChukMCP Server",
            "framework": "ChukMCP Server"
        },
        "capabilities": {
            "tools_count": len(tools),
            "resources_count": len(resources),
            "tool_names": [tool.name for tool in tools],
            "resource_uris": [resource.uri for resource in resources]
        },
        "timestamp": datetime.now().isoformat()
    }