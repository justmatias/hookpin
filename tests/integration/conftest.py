import shutil
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
SHARED_FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def monorepo_and_lock(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Two stale configs (pkg_a, pkg_b) + shared uv.lock."""
    for pkg in ("pkg_a", "pkg_b"):
        (tmp_path / pkg).mkdir()
        shutil.copy(
            SHARED_FIXTURES / "config_basic.yaml", tmp_path / pkg / ".pre-commit-config.yaml"
        )
    lock = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "uv.lock", lock)
    return (
        tmp_path / "pkg_a" / ".pre-commit-config.yaml",
        tmp_path / "pkg_b" / ".pre-commit-config.yaml",
        lock,
    )


@pytest.fixture
def config_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    lock = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "config_basic.yaml", config_path)
    shutil.copy(SHARED_FIXTURES / "uv.lock", lock)
    return config_path, lock


@pytest.fixture
def config_extras_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    lock = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "config_with_extras.yaml", config_path)
    shutil.copy(SHARED_FIXTURES / "uv.lock", lock)
    return config_path, lock


@pytest.fixture
def config_with_missing_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    shutil.copy(SHARED_FIXTURES / "config_basic.yaml", config_path)
    return config_path, tmp_path / "nonexistent.lock"


@pytest.fixture
def config_current_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    lock = tmp_path / "uv.lock"
    shutil.copy(FIXTURES / "config_already_current.yaml", config_path)
    shutil.copy(SHARED_FIXTURES / "uv.lock", lock)
    return config_path, lock


@pytest.fixture
def empty_lock(tmp_path: Path) -> Path:
    lock = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "uv_empty.lock", lock)
    return lock


@pytest.fixture
def config_missing_dep_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    shutil.copy(FIXTURES / "config_missing_dependency.yaml", config_path)
    lock = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "uv_empty.lock", lock)
    return config_path, lock


@pytest.fixture
def multi_hook_config(tmp_path: Path) -> Path:
    config_path = tmp_path / ".pre-commit-config.yaml"
    shutil.copy(SHARED_FIXTURES / "config_multiple_hooks.yaml", config_path)
    return config_path


@pytest.fixture
def lock(tmp_path: Path) -> Path:
    path = tmp_path / "uv.lock"
    shutil.copy(SHARED_FIXTURES / "uv.lock", path)
    return path
