import shutil
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
SHARED_FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def minimal_lock_file(tmp_path: Path) -> Path:
    lock = tmp_path / "uv.lock"
    shutil.copy(FIXTURES / "uv_minimal.lock", lock)
    return lock


@pytest.fixture
def normalized_name_lock_file(tmp_path: Path) -> Path:
    lock = tmp_path / "uv.lock"
    shutil.copy(FIXTURES / "uv_normalized_names.lock", lock)
    return lock


@pytest.fixture
def empty_lock_file(tmp_path: Path) -> Path:
    lock = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "uv_empty.lock", lock)
    return lock


@pytest.fixture
def missing_lock_file(tmp_path: Path) -> Path:
    return tmp_path / "nonexistent.lock"
