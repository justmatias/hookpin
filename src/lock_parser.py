import tomllib
from pathlib import Path
from typing import Any

from .utils import normalize_package_name


def parse_lock(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"lockfile not found: {path}")
    data: dict[str, Any] = tomllib.loads(path.read_text())
    return {normalize_package_name(pkg["name"]): pkg["version"] for pkg in data.get("package", [])}
