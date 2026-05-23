from __future__ import annotations

from .config import NORMALIZE_RE


def normalize_package_name(name: str) -> str:
    return NORMALIZE_RE.sub("-", name).lower()
