import os
import tomllib
from pathlib import Path


def load_config():
    """
    Load Teradata configuration from ~/.skewer.toml
    Returns a dict with secrets.
    """
    config_path = Path.home() / ".skewer.toml"

    if not config_path.exists():
        # Fallback or error? For now, let's return empty and log/print a warning
        # But for a real app, we might want to fail fast if this is required.
        print(f"Warning: Config file not found at {config_path}")
        return {}

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}
