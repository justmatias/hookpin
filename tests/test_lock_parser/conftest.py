import pytest

MINIMAL_LOCK = """\
version = 1
requires-python = ">=3.11"

[[package]]
name = "pydantic"
version = "2.13.4"
source = { registry = "https://pypi.org/simple" }
"""

NORMALIZED_NAME_LOCK = """\
version = 1

[[package]]
name = "Pydantic_Core"
version = "2.33.2"
source = { registry = "https://pypi.org/simple" }

[[package]]
name = "pydantic-core"
version = "2.33.2"
source = { registry = "https://pypi.org/simple" }
"""


@pytest.fixture
def minimal_lock_file(tmp_path):
    lock = tmp_path / "uv.lock"
    lock.write_text(MINIMAL_LOCK)
    return lock


@pytest.fixture
def normalized_name_lock_file(tmp_path):
    lock = tmp_path / "uv.lock"
    lock.write_text(NORMALIZED_NAME_LOCK)
    return lock


@pytest.fixture
def empty_lock_file(tmp_path):
    lock = tmp_path / "uv.lock"
    lock.write_text("version = 1\n")
    return lock


@pytest.fixture
def missing_lock_file(tmp_path):
    return tmp_path / "nonexistent.lock"
