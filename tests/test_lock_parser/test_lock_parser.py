from pathlib import Path

import pytest

from sync_uv_additional_deps.lock_parser import parse_lock


def test_parse_basic(minimal_lock_file: Path) -> None:
    assert parse_lock(minimal_lock_file) == {"pydantic": "2.13.4"}


def test_name_normalization(normalized_name_lock_file: Path) -> None:
    result = parse_lock(normalized_name_lock_file)
    assert result["pydantic-core"] == "2.33.2"
    assert len(result) == 1


def test_empty_packages(empty_lock_file: Path) -> None:
    assert parse_lock(empty_lock_file) == {}


def test_missing_file(missing_lock_file: Path) -> None:
    with pytest.raises(FileNotFoundError, match="lockfile not found"):
        parse_lock(missing_lock_file)
