"""Parser for uv.lock TOML files."""

import tomllib
from pathlib import Path
from typing import Any

from .naming import normalize_package_name


def parse_lock(path: Path) -> dict[str, str]:
    """Return a mapping of normalised package name → version from a uv.lock file."""
    if not path.exists():
        raise FileNotFoundError(f"lockfile not found: {path}")
    data: dict[str, Any] = tomllib.loads(path.read_text())
    return {normalize_package_name(package["name"]): package["version"] for package in data.get("package", [])}
