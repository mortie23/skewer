import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

# Add src to path if not installed
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from skewer.config import load_config


def test_load_config_success():
    mock_content = b'host = "localhost"\nuser = "test"\npassword = "pwd"'
    with (
        patch("pathlib.Path.home", return_value=Path("/tmp")),
        patch("skewer.config.Path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=mock_content)),
    ):
        config = load_config()
        assert config["host"] == "localhost"
        assert config["user"] == "test"


def test_load_config_missing_file():
    with (
        patch("pathlib.Path.home", return_value=Path("/tmp")),
        patch("skewer.config.Path.exists", return_value=False),
    ):
        config = load_config()
        assert config == {}
