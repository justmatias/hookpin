import shutil
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def config_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    lock = tmp_path / "uv.lock"
    shutil.copy(FIXTURES / "config_basic.yaml", config_path)
    shutil.copy(FIXTURES / "uv.lock", lock)
    return config_path, lock


@pytest.fixture
def config_extras_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    lock = tmp_path / "uv.lock"
    shutil.copy(FIXTURES / "config_with_extras.yaml", config_path)
    shutil.copy(FIXTURES / "uv.lock", lock)
    return config_path, lock


@pytest.fixture
def config_with_missing_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    shutil.copy(FIXTURES / "config_basic.yaml", config_path)
    return config_path, tmp_path / "nonexistent.lock"


@pytest.fixture
def config_current_and_lock(tmp_path: Path) -> tuple[Path, Path]:
    config_path = tmp_path / ".pre-commit-config.yaml"
    lock = tmp_path / "uv.lock"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - ruff==0.9.0
"""
    )
    shutil.copy(FIXTURES / "uv.lock", lock)
    return config_path, lock
