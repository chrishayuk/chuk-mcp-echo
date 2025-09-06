# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ChukMCP Echo Service - A demonstration MCP (Model Context Protocol) service built using the ChukMCP Server framework. This is an async-native echo service that demonstrates various MCP capabilities including text processing, data manipulation, and testing features.

## Architecture

This service follows an async-first architecture using the ChukMCP Server framework:

- **Server Configuration**: `src/chuk_mcp_echo/server.py` - Creates the ChukMCPServer instance
- **Tools Implementation**: `src/chuk_mcp_echo/tools.py` - Async tool definitions using decorators
- **Resources Implementation**: `src/chuk_mcp_echo/resources.py` - Async resource handlers  
- **Entry Point**: `src/chuk_mcp_echo/main.py` - Service initialization and runtime

All tools and resources are implemented as async functions using `async/await` patterns. The service uses `asyncio.sleep()` for non-blocking delays and supports concurrent request handling.

## Development Commands

### Build and Installation
```bash
# Install in development mode
make dev-install

# Build the project
make build

# Clean build artifacts
make clean
make clean-all  # Deep clean including caches
```

### Running the Service
```bash
# Run the echo service (starts on http://localhost:8000)
make run

# Or directly via the script (if installed)
chuk-mcp-echo

# Or via Python module
python -m chuk_mcp_echo.main
```

### Testing
```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run a specific test file
uv run pytest tests/test_echo_service.py

# Run a specific test
uv run pytest tests/test_echo_service.py::test_echo_text
```

### Code Quality
```bash
# Run all checks (lint, typecheck, tests)
make check

# Run linter
make lint

# Auto-format code
make format

# Type checking
make typecheck
```

## Key Implementation Patterns

When modifying or extending this service:

1. **All tools must be async functions** decorated with `@echo_service.tool`
2. **All resources must be async functions** decorated with `@echo_service.resource(uri, mime_type)`
3. **Use `asyncio.sleep()` instead of `time.sleep()`** for delays
4. **Tool functions automatically generate JSON schemas** from type hints
5. **The service runs on Uvicorn** and handles concurrent requests efficiently

## Testing Approach

The project uses pytest with pytest-asyncio for testing async functions. Tests are located in the `tests/` directory and should test both the async behavior and the actual functionality of tools and resources.