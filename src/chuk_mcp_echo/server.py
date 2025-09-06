#!/usr/bin/env python3
# src/chuk_mcp_echo/server.py
"""
Echo Service Server - Main service configuration and initialization
"""

import logging
from chuk_mcp_server import ChukMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create the echo service instance
echo_service = ChukMCPServer(
    name="Echo Service",
    version="0.1.0",
    title="Simple Echo MCP Service",
    description="A demonstration service that echoes various types of data back to the client",
)
