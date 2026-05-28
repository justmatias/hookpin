"""Package name normalisation helpers."""

from __future__ import annotations

from .patterns import NORMALIZATION_RE


def normalize_package_name(name: str) -> str:
    """Normalise a PEP 503 package name to its canonical lowercase-hyphenated form."""
    return NORMALIZATION_RE.sub("-", name).lower()
