import shutil
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent / "fixtures"


@pytest.fixture
def lock_packages() -> dict[str, str]:
    return {
        "pydantic": "2.13.4",
        "pydantic-core": "2.33.2",
        "ruamel-yaml": "0.18.6",
        "black": "24.10.0",
        "mypy": "1.14.1",
        "ruff": "0.9.0",
    }


@pytest.fixture
def config_basic(tmp_path: Path) -> Path:
    dest = tmp_path / "config.yaml"
    shutil.copy(FIXTURES / "config_basic.yaml", dest)
    return dest


@pytest.fixture
def config_with_extras(tmp_path: Path) -> Path:
    dest = tmp_path / "config.yaml"
    shutil.copy(FIXTURES / "config_with_extras.yaml", dest)
    return dest


@pytest.fixture
def config_with_comments(tmp_path: Path) -> Path:
    dest = tmp_path / "config.yaml"
    shutil.copy(FIXTURES / "config_with_comments.yaml", dest)
    return dest


@pytest.fixture
def multi_hook_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook-a
    rev: v1
    hooks:
      - id: hook-a
        additional_dependencies:
          - pydantic==1.0.0
  - repo: https://example.com/hook-b
    rev: v1
    hooks:
      - id: hook-b
        additional_dependencies:
          - pydantic==1.0.0
"""
    )
    return config_path


@pytest.fixture
def missing_package_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - unknown-package==1.0.0
"""
    )
    return config_path


@pytest.fixture
def case_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - Pydantic==1.0.0
"""
    )
    return config_path
