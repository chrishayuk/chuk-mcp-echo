#!/usr/bin/env python3
"""
Test suite for main.py entry point
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path before any other imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestMainFunction:
    """Test the main entry point."""

    def test_main_import(self):
        """Test that we can import main."""
        from chuk_mcp_echo.main import main

        assert main is not None

    @patch("chuk_mcp_echo.main.echo_service")
    def test_main_http_mode_default(self, mock_service):
        """Test main with default HTTP mode."""
        from chuk_mcp_echo.main import main

        # Mock run to prevent actual server startup
        mock_service.run = MagicMock()

        with patch("sys.argv", ["chuk-mcp-echo"]):
            main()

        # Should call run with HTTP defaults
        mock_service.run.assert_called_once()
        call_args = mock_service.run.call_args
        assert call_args[1]["host"] == "localhost"
        assert call_args[1]["port"] == 8000
        assert call_args[1]["stdio"] is False

    @patch("chuk_mcp_echo.main.echo_service")
    def test_main_http_mode_custom(self, mock_service):
        """Test main with custom HTTP settings."""
        from chuk_mcp_echo.main import main

        mock_service.run = MagicMock()

        with patch(
            "sys.argv", ["chuk-mcp-echo", "http", "--host", "0.0.0.0", "--port", "9000"]
        ):
            main()

        mock_service.run.assert_called_once()
        call_args = mock_service.run.call_args
        assert call_args[1]["host"] == "0.0.0.0"
        assert call_args[1]["port"] == 9000

    @patch("chuk_mcp_echo.main.echo_service")
    def test_main_http_mode_debug(self, mock_service):
        """Test main with debug flag."""
        from chuk_mcp_echo.main import main

        mock_service.run = MagicMock()

        with patch("sys.argv", ["chuk-mcp-echo", "http", "--debug"]):
            main()

        mock_service.run.assert_called_once()
        call_args = mock_service.run.call_args
        assert call_args[1]["debug"] is True

    @patch("chuk_mcp_echo.main.echo_service")
    def test_main_stdio_mode(self, mock_service):
        """Test main with stdio mode."""
        from chuk_mcp_echo.main import main

        mock_service.run = MagicMock()

        with patch("sys.argv", ["chuk-mcp-echo", "stdio"]):
            main()

        mock_service.run.assert_called_once()
        call_args = mock_service.run.call_args
        assert call_args[1]["stdio"] is True
        assert call_args[1]["debug"] is False

    @patch("chuk_mcp_echo.main.echo_service")
    def test_main_stdio_mode_debug(self, mock_service):
        """Test main with stdio mode and debug."""
        from chuk_mcp_echo.main import main

        mock_service.run = MagicMock()

        with patch("sys.argv", ["chuk-mcp-echo", "stdio", "--debug"]):
            main()

        mock_service.run.assert_called_once()
        call_args = mock_service.run.call_args
        assert call_args[1]["stdio"] is True
        assert call_args[1]["debug"] is True


class TestMainServerInfo:
    """Test main function server info output."""

    @patch("chuk_mcp_echo.main.echo_service")
    def test_main_displays_server_info(self, mock_service):
        """Test that main displays server info."""
        from chuk_mcp_echo.main import main

        mock_service.run = MagicMock()
        mock_service.get_tools = MagicMock(return_value=[MagicMock(), MagicMock()])
        mock_service.get_resources = MagicMock(return_value=[MagicMock()])

        with patch("sys.argv", ["chuk-mcp-echo"]):
            with patch("builtins.print") as mock_print:
                main()

        # Should print server info
        assert mock_print.called
        # Should mention tools and resources
        printed_output = " ".join(str(call[0][0]) for call in mock_print.call_args_list)
        assert "Echo Service" in printed_output or "tools" in printed_output.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
