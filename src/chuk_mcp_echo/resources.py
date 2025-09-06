#!/usr/bin/env python3
# src/chuk_mcp_echo/resources.py
"""
Echo Service Resources - Async native resource implementations
"""

import asyncio
import time
from datetime import datetime

from .server import echo_service

# ============================================================================
# Configuration Resource
# ============================================================================


@echo_service.resource("echo://config", mime_type="application/json")
async def get_echo_config() -> dict:
    """Get the echo service configuration."""
    await asyncio.sleep(0.001)  # Simulate async I/O
    return {
        "service_name": "Echo Service",
        "version": "0.1.0",
        "features": [
            "Text echoing with transformations",
            "JSON data echoing with metadata",
            "List processing and manipulation",
            "Number operations",
            "Delayed responses for async testing",
            "Error simulation for testing",
        ],
        "supported_operations": {
            "text": ["echo", "uppercase", "reverse"],
            "data": ["json_echo", "list_processing", "number_operations"],
            "testing": ["delayed_response", "error_simulation"],
        },
        "limits": {
            "max_delay_seconds": 10.0,
            "max_list_size": 1000,
            "max_string_length": 10000,
        },
        "created_at": datetime.now().isoformat(),
    }


# ============================================================================
# Status Resource
# ============================================================================


@echo_service.resource("echo://status", mime_type="application/json")
async def get_echo_status() -> dict:
    """Get the current status of the echo service."""
    await asyncio.sleep(0.001)
    start_time = echo_service.protocol.session_manager.sessions.get(
        "start_time", time.time()
    )
    # Ensure start_time is a float for type checking
    if not isinstance(start_time, (int, float)):
        start_time = time.time()
    return {
        "status": "running",
        "uptime_seconds": time.time() - start_time,
        "service_info": {"name": "Echo Service", "version": "0.1.0", "ready": True},
        "capabilities": {
            "tools_available": len(echo_service.get_tools()),
            "resources_available": len(echo_service.get_resources()),
        },
        "health": {
            "database": "not_applicable",
            "external_services": "not_applicable",
            "memory_usage": "normal",
        },
        "last_check": datetime.now().isoformat(),
    }


# ============================================================================
# Examples Resource
# ============================================================================


@echo_service.resource("echo://examples", mime_type="application/json")
async def get_usage_examples() -> dict:
    """Get comprehensive usage examples for the echo service."""
    await asyncio.sleep(0.001)
    return {
        "description": "Echo Service Usage Examples",
        "examples": {
            "basic_text_echo": {
                "tool": "echo_text",
                "arguments": {"message": "Hello, World!"},
                "description": "Basic text echoing",
            },
            "text_with_formatting": {
                "tool": "echo_text",
                "arguments": {"message": "Echo", "prefix": ">>> ", "suffix": " <<<"},
                "description": "Text echo with prefix and suffix",
            },
            "text_transformations": [
                {
                    "tool": "echo_uppercase",
                    "arguments": {"text": "make me loud"},
                    "description": "Convert to uppercase",
                },
                {
                    "tool": "echo_reverse",
                    "arguments": {"text": "reverse this"},
                    "description": "Reverse the text",
                },
            ],
            "json_processing": {
                "tool": "echo_json",
                "arguments": {
                    "data": {"name": "John Doe", "age": 30, "city": "New York"}
                },
                "description": "Echo JSON with metadata",
            },
            "list_operations": [
                {
                    "tool": "echo_list",
                    "arguments": {"items": [3, 1, 4, 1, 5, 9]},
                    "description": "Basic list echo",
                },
                {
                    "tool": "echo_list",
                    "arguments": {"items": ["banana", "apple", "cherry"], "sort": True},
                    "description": "Sort a list",
                },
                {
                    "tool": "echo_list",
                    "arguments": {"items": [1, 2, 3, 4, 5], "reverse": True},
                    "description": "Reverse a list",
                },
            ],
            "number_operations": [
                {
                    "tool": "echo_number",
                    "arguments": {"number": 10},
                    "description": "Basic number echo",
                },
                {
                    "tool": "echo_number",
                    "arguments": {"number": 5, "multiply": 2, "add": 3},
                    "description": "Number with operations: (5 * 2) + 3 = 13",
                },
            ],
            "testing_features": [
                {
                    "tool": "echo_delay",
                    "arguments": {"message": "Delayed response", "delay_seconds": 2.0},
                    "description": "Test delayed response",
                },
                {
                    "tool": "echo_error",
                    "arguments": {"should_error": False},
                    "description": "Test successful response",
                },
                {
                    "tool": "echo_error",
                    "arguments": {
                        "should_error": True,
                        "error_message": "This is a test error",
                    },
                    "description": "Test error handling",
                },
            ],
            "service_introspection": {
                "tool": "get_service_info",
                "arguments": {},
                "description": "Get service information",
            },
        },
        "resource_examples": {
            "configuration": {
                "uri": "echo://config",
                "description": "Service configuration and features",
            },
            "status": {"uri": "echo://status", "description": "Current service status"},
            "examples": {
                "uri": "echo://examples",
                "description": "This examples resource",
            },
            "documentation": {
                "uri": "echo://docs",
                "description": "Comprehensive documentation",
            },
        },
    }


# ============================================================================
# Documentation Resource
# ============================================================================


@echo_service.resource("echo://docs", mime_type="text/markdown")
async def get_documentation() -> str:
    """Get comprehensive documentation for the echo service."""
    await asyncio.sleep(0.001)
    return """# Echo Service Documentation

## Overview

The Echo Service is a simple MCP (Model Context Protocol) service built using the ChukMCP Server framework. It demonstrates various capabilities including text processing, data manipulation, and testing features with full async/await support.

## Async Native Architecture

All tools and resources in this service are implemented using async/await:

- **Non-blocking I/O**: All operations use `asyncio.sleep()` instead of blocking calls
- **Concurrent Execution**: Multiple tools can run simultaneously
- **Scalable Performance**: Handles many concurrent requests efficiently
- **Type Safety**: Automatic schema generation works with async functions

## Tools Available

### Text Processing Tools

#### `echo_text(message, prefix="", suffix="")`
- **Purpose**: Echo text with optional formatting (async)
- **Parameters**:
  - `message` (string, required): Text to echo
  - `prefix` (string, optional): Text to prepend
  - `suffix` (string, optional): Text to append
- **Example**: `await echo_text("Hello", ">>> ", " <<<")` → `">>> Hello <<<"`

#### `echo_uppercase(text)`
- **Purpose**: Convert text to uppercase (async)
- **Parameters**:
  - `text` (string, required): Text to convert
- **Example**: `await echo_uppercase("hello world")` → `"HELLO WORLD"`

#### `echo_reverse(text)`
- **Purpose**: Reverse the text (async)
- **Parameters**:
  - `text` (string, required): Text to reverse
- **Example**: `await echo_reverse("hello")` → `"olleh"`

### Data Processing Tools

#### `echo_json(data)`
- **Purpose**: Echo JSON data with metadata (async)
- **Parameters**:
  - `data` (object, required): JSON object to process
- **Returns**: Object with echoed data, type info, and timestamp

#### `echo_list(items, sort=False, reverse=False)`
- **Purpose**: Process and echo list data (async)
- **Parameters**:
  - `items` (array, required): List of items
  - `sort` (boolean, optional): Whether to sort the list
  - `reverse` (boolean, optional): Whether to reverse the list
- **Returns**: Object with original and processed lists

#### `echo_number(number, multiply=1.0, add=0.0)`
- **Purpose**: Process numerical data with operations (async)
- **Parameters**:
  - `number` (number, required): Number to process
  - `multiply` (number, optional): Multiplication factor
  - `add` (number, optional): Addition amount
- **Returns**: Object with original, result, and operation details

### Testing and Utility Tools

#### `echo_delay(message, delay_seconds=1.0)`
- **Purpose**: Test delayed responses for async behavior
- **Parameters**:
  - `message` (string, required): Message to echo after delay
  - `delay_seconds` (number, optional): Delay duration
- **Returns**: Message with timing information
- **Note**: Uses `asyncio.sleep()` for true async delays

#### `echo_error(should_error=False, error_message="Test error")`
- **Purpose**: Test error handling mechanisms (async)
- **Parameters**:
  - `should_error` (boolean, optional): Whether to raise an error
  - `error_message` (string, optional): Error message if raising
- **Returns**: Success status or raises specified error

#### `get_service_info()`
- **Purpose**: Get service introspection information (async)
- **Parameters**: None
- **Returns**: Comprehensive service information

## Resources Available

### `echo://config` (Async)
- **Type**: JSON
- **Purpose**: Service configuration and feature list
- **Content**: Service metadata, supported operations, and limits

### `echo://status` (Async)
- **Type**: JSON  
- **Purpose**: Current service status and health
- **Content**: Runtime status, uptime, and capability information

### `echo://examples` (Async)
- **Type**: JSON
- **Purpose**: Comprehensive usage examples
- **Content**: Example tool calls and resource reads

### `echo://docs` (Async)
- **Type**: Markdown
- **Purpose**: This documentation
- **Content**: Complete service documentation

## Async Usage Patterns

### Concurrent Tool Execution
```python
import asyncio

# Execute multiple tools concurrently
async def test_concurrency():
    tasks = [
        echo_delay("Message 1", 2.0),
        echo_delay("Message 2", 2.0),
        echo_delay("Message 3", 2.0),
    ]
    
    # All complete in ~2 seconds (concurrent) not 6 seconds (sequential)
    results = await asyncio.gather(*tasks)
    return results
```

### Non-blocking Resource Reads
```python
# Read multiple resources concurrently
async def read_all_resources():
    config_task = get_echo_config()
    status_task = get_echo_status()
    examples_task = get_usage_examples()
    
    config, status, examples = await asyncio.gather(
        config_task, status_task, examples_task
    )
    return config, status, examples
```

## MCP Inspector Integration

This service is fully compatible with the MCP Inspector:

1. **Transport Type**: Streamable HTTP
2. **URL**: Point to the running service endpoint
3. **Features**: All async tools and resources are available
4. **Testing**: Use the `echo_delay` tool to test concurrent execution
5. **Performance**: Multiple requests don't block each other

## Development Notes

This async-native echo service serves as a reference implementation for:
- Clean async tool and resource definition
- Proper async error handling
- Type safety with automatic schema generation from async functions
- Comprehensive async documentation
- Concurrent execution testing utilities

Built with ❤️ using ChukMCP Server framework with full async/await support.
"""
