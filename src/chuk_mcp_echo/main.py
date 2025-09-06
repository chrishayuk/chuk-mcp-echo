#!/usr/bin/env python3
# src/chuk_mcp_echo/main.py
"""
Echo Service Main - Entry point for the async native echo service
"""

import sys
import argparse
import logging

from .server import echo_service


def main():
    """Main function to run the echo service."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog="chuk-mcp-echo",
        description="Echo Service - ChukMCP Server Test (Async Native)",
    )

    # Add subcommands for different modes
    subparsers = parser.add_subparsers(dest="mode", help="Transport mode")

    # Stdio mode
    stdio_parser = subparsers.add_parser(
        "stdio", help="Run in stdio mode for MCP clients"
    )
    stdio_parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )

    # HTTP mode (default)
    http_parser = subparsers.add_parser("http", help="Run in HTTP mode (default)")
    http_parser.add_argument("--host", default="localhost", help="Host to bind to")
    http_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    http_parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )

    # Parse args - if no mode specified, default to http
    args = parser.parse_args()
    if args.mode is None:
        args.mode = "http"
        args.host = "localhost"
        args.port = 8000
        args.debug = False

    # Configure logging - always to stderr in stdio mode
    if args.mode == "stdio":
        # In stdio mode, all logging and prints go to stderr
        logging.basicConfig(
            level=logging.DEBUG if args.debug else logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stderr,
        )
        output = sys.stderr
    else:
        # In HTTP mode, can use stdout
        logging.basicConfig(
            level=logging.DEBUG if args.debug else logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        output = sys.stdout

    # Only show startup info in HTTP mode
    if args.mode == "http":
        print("🔄 Echo Service - ChukMCP Server Test (Async Native)", file=output)
        print("=" * 50, file=output)

        # Show what we've registered
        registered_tools = echo_service.get_tools()
        registered_resources = echo_service.get_resources()

        print(f"📝 Registered Async Tools ({len(registered_tools)}):", file=output)
        for tool in registered_tools:
            print(f"   - {tool.name}: {tool.description}", file=output)

        print(
            f"\n📂 Registered Async Resources ({len(registered_resources)}):",
            file=output,
        )
        for resource in registered_resources:
            print(f"   - {resource.uri}: {resource.description}", file=output)

        print("\n🔍 Developer Experience Test (Async Native):", file=output)
        print("   - All tools are async/await native", file=output)
        print("   - All resources use async handlers", file=output)
        print("   - Non-blocking I/O throughout", file=output)
        print("   - Proper asyncio.sleep() for delays", file=output)
        print("   - Async-first architecture", file=output)

        print("\n🌐 Testing Instructions:", file=output)
        print("   1. Run this service: chuk-mcp-echo", file=output)
        print(
            f"   2. Server will start on: http://{args.host}:{args.port}", file=output
        )
        print(f"   3. MCP endpoint: http://{args.host}:{args.port}/mcp", file=output)
        print("   4. All operations are non-blocking async", file=output)
        print("   5. Test 'echo_delay' to see async behavior", file=output)
        print("   6. Multiple concurrent requests work perfectly", file=output)

        print("=" * 50, file=output)

    # Run the service
    try:
        if args.mode == "stdio":
            # Run in stdio mode
            echo_service.run(stdio=True, debug=args.debug)
        else:
            # Run in HTTP mode
            echo_service.run(
                host=args.host, port=args.port, debug=args.debug, stdio=False
            )
    except KeyboardInterrupt:
        if args.mode == "http":
            print("\n👋 Echo service shutting down...", file=output)
    except Exception as e:
        print(f"❌ Service error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
