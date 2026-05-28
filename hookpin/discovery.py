"""Resolve pre-commit config file paths from literal paths and glob patterns."""

from __future__ import annotations

import glob
from pathlib import Path


def resolve_configs(patterns: list[Path]) -> list[Path]:
    """Expand literal paths and glob patterns into a deduplicated list of config files.

    Glob patterns are expanded internally (pre-commit passes args literally, with no
    shell expansion). An unmatched glob or a missing literal path raises FileNotFoundError.
    """
    seen: set[Path] = set()
    resolved: list[Path] = []
    for pattern in patterns:
        pattern_str = str(pattern)
        if glob.has_magic(pattern_str):
            matches = sorted(Path(p) for p in glob.glob(pattern_str, recursive=True))
            if not matches:
                raise FileNotFoundError(f"no config files matched pattern: {pattern}")
            candidates = matches
        else:
            if not pattern.exists():
                raise FileNotFoundError(f"config file not found: {pattern}")
            candidates = [pattern]
        for candidate in candidates:
            resolved_key = candidate.resolve()
            if resolved_key not in seen:
                seen.add(resolved_key)
                resolved.append(candidate)
    return resolved
