# ChukMCP Echo Service

An async-native demonstration MCP (Model Context Protocol) service built using the ChukMCP Server framework. This service showcases various MCP capabilities including text processing, data manipulation, and testing features with full async/await support.

> This is a demonstration project provided as-is for learning and testing purposes.

## Features

- **Async-Native Architecture**: All tools and resources implemented with async/await
- **Text Processing**: Echo, uppercase, reverse text operations
- **Data Manipulation**: JSON echoing with metadata, list processing, number operations
- **Testing Utilities**: Delayed responses for async testing, error simulation
- **Resource Management**: Configuration, status, examples, and documentation resources
- **Non-blocking I/O**: Handles concurrent requests efficiently

## Installation

### Using pip

```bash
pip install chuk-mcp-echo
```

### Using uv

```bash
uv pip install chuk-mcp-echo
```

### Using uvx (for running directly)

```bash
uvx chuk-mcp-echo
```

### Development Installation

```bash
git clone https://github.com/yourusername/chuk-mcp-echo.git
cd chuk-mcp-echo
make dev-install
```

## Quick Start

### Running the Service

The echo service can run in two modes: HTTP mode (default) and stdio mode (for MCP clients).

#### HTTP Mode (Default)

```bash
# Using the installed command
chuk-mcp-echo

# Or explicitly specify HTTP mode
chuk-mcp-echo http

# With custom host and port
chuk-mcp-echo http --host 0.0.0.0 --port 9000

# Or using make
make run

# Or using uvx
uvx chuk-mcp-echo
```

The service will start on `http://localhost:8000` with the MCP endpoint at `http://localhost:8000/mcp`.

#### Stdio Mode (For MCP Clients)

```bash
# Run in stdio mode for MCP clients
chuk-mcp-echo stdio

# With debug logging (sent to stderr)
chuk-mcp-echo stdio --debug

# Using uvx
uvx chuk-mcp-echo stdio
```

### MCP Client Configuration

To use this service with an MCP client (like Claude Desktop or mcp-cli), add the following to your MCP client configuration:

```json
{
  "mcpServers": {
    "echo": {
      "command": "uvx",
      "args": ["chuk-mcp-echo", "stdio"]
    }
  }
}
```

Or if you have it installed locally:

```json
{
  "mcpServers": {
    "echo": {
      "command": "chuk-mcp-echo",
      "args": ["stdio"]
    }
  }
}
```

Or if you want to run it from source:

```json
{
  "mcpServers": {
    "echo": {
      "command": "python",
      "args": ["-m", "chuk_mcp_echo.main", "stdio"],
      "env": {
        "PYTHONPATH": "/path/to/chuk-mcp-echo/src"
      }
    }
  }
}
```

### Testing with MCP Inspector

1. Open MCP Inspector
2. Set Transport Type to "Streamable HTTP"
3. Enter URL: `http://localhost:8000/mcp`
4. Connect and explore available tools and resources

## Available Tools

### Text Processing
- `echo_text(message, prefix="", suffix="")` - Echo text with optional formatting
- `echo_uppercase(text)` - Convert text to uppercase
- `echo_reverse(text)` - Reverse the text

### Data Processing
- `echo_json(data)` - Echo JSON data with metadata
- `echo_list(items, sort=False, reverse=False)` - Process and echo lists
- `echo_number(number, multiply=1.0, add=0.0)` - Perform number operations

### Testing & Utility
- `echo_delay(message, delay_seconds=1.0)` - Test async delayed responses
- `echo_error(should_error=False, error_message="Test error")` - Test error handling
- `get_service_info()` - Get service information

## Available Resources

- `echo://config` - Service configuration and features (JSON)
- `echo://status` - Current service status and health (JSON)
- `echo://examples` - Comprehensive usage examples (JSON)
- `echo://docs` - Complete service documentation (Markdown)

## Development

### Project Structure

```
chuk-mcp-echo/
├── src/
│   └── chuk_mcp_echo/
│       ├── __init__.py
│       ├── main.py          # Entry point
│       ├── server.py        # Server configuration
│       ├── tools.py         # Async tool implementations
│       └── resources.py     # Async resource handlers
├── tests/
│   ├── test_echo_service.py
│   └── test_simple.py
├── examples/
│   └── api_test_script.py
├── debug/
│   ├── debug_failing_tests.py
│   └── debug_imports.py
├── Makefile
├── pyproject.toml
└── README.md
```


### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
uv run pytest tests/test_echo_service.py::test_echo_text
```

### Code Quality

```bash
# Run all checks (lint, typecheck, tests)
make check

# Format code
make format

# Run linter
make lint

# Type checking
make typecheck
```

### Building and Publishing

```bash
# Build the package
make build

# Publish to PyPI
make publish

# Publish to Test PyPI
make publish-test
```

## Usage Examples

### Using with Python Client

```python
import asyncio
from chuk_mcp_client import ChukMCPClient

async def main():
    client = ChukMCPClient("http://localhost:8000/mcp")
    
    # Echo text
    result = await client.call_tool("echo_text", {
        "message": "Hello, World!",
        "prefix": ">>> ",
        "suffix": " <<<"
    })
    print(result)  # >>> Hello, World! <<<
    
    # Process a list
    result = await client.call_tool("echo_list", {
        "items": [3, 1, 4, 1, 5],
        "sort": True
    })
    print(result["processed"])  # [1, 1, 3, 4, 5]
    
    # Test async behavior with delay
    result = await client.call_tool("echo_delay", {
        "message": "Delayed message",
        "delay_seconds": 2.0
    })
    print(result["actual_delay"])  # ~2.0

asyncio.run(main())
```

### Concurrent Execution Example

```python
async def test_concurrent_requests():
    # Multiple requests execute concurrently
    tasks = [
        client.call_tool("echo_delay", {"message": f"Message {i}", "delay_seconds": 2.0})
        for i in range(3)
    ]
    
    # All complete in ~2 seconds (concurrent) not 6 seconds (sequential)
    results = await asyncio.gather(*tasks)
    return results
```

## Requirements

- Python 3.11+
- ChukMCP Server >= 0.2.3
- Pydantic >= 2.11.7
- Uvicorn >= 0.35.0

## License

Apache License 2.0 - See LICENSE.md for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with the ChukMCP Server framework for creating async-native MCP services.