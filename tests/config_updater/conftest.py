import shutil
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
SHARED_FIXTURES = Path(__file__).parent.parent / "fixtures"


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


def _config(tmp_path: Path, fixtures_dir: Path, name: str) -> Path:
    dest = tmp_path / "config.yaml"
    shutil.copy(fixtures_dir / name, dest)
    return dest


def _shared(tmp_path: Path, name: str) -> Path:
    return _config(tmp_path, SHARED_FIXTURES, name)


def _local(tmp_path: Path, name: str) -> Path:
    return _config(tmp_path, FIXTURES, name)


@pytest.fixture
def config_basic(tmp_path: Path) -> Path:
    return _shared(tmp_path, "config_basic.yaml")


@pytest.fixture
def config_with_extras(tmp_path: Path) -> Path:
    return _shared(tmp_path, "config_with_extras.yaml")


@pytest.fixture
def config_with_comments(tmp_path: Path) -> Path:
    return _shared(tmp_path, "config_with_comments.yaml")


@pytest.fixture
def multiple_hooks_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_multiple_hooks.yaml")


@pytest.fixture
def missing_package_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_missing_package.yaml")


@pytest.fixture
def mixed_case_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_mixed_case_package.yaml")


@pytest.fixture
def bare_dependency_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_bare_dependency.yaml")


@pytest.fixture
def bare_unknown_dependency_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_bare_unknown_dependency.yaml")


@pytest.fixture
def compatible_release_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_operator_compatible_release.yaml")


@pytest.fixture
def less_than_or_equal_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_operator_less_than_or_equal.yaml")


@pytest.fixture
def not_equal_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_operator_not_equal.yaml")


@pytest.fixture
def range_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_operator_range.yaml")


@pytest.fixture
def exact_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_operator_exact.yaml")


@pytest.fixture
def marker_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_marker.yaml")


@pytest.fixture
def marker_with_extras_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_marker_with_extras.yaml")


@pytest.fixture
def marker_already_current_config(tmp_path: Path) -> Path:
    return _local(tmp_path, "config_marker_already_current.yaml")
