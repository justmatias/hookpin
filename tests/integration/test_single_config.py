from pathlib import Path

from .helpers import run_hookpin


def test_stale_pin_returns_1(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    return_code = run_hookpin(config_path, lockfile=lock)
    assert return_code == 1
    assert "pydantic==2.13.4" in config_path.read_text()


def test_idempotent(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    run_hookpin(config_path, lockfile=lock)
    before = config_path.read_bytes()
    return_code = run_hookpin(config_path, lockfile=lock)
    assert return_code == 0
    assert config_path.read_bytes() == before


def test_missing_lockfile_returns_2(config_with_missing_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_with_missing_lock
    original = config_path.read_bytes()
    return_code = run_hookpin(config_path, lockfile=lock)
    assert return_code == 2
    assert config_path.read_bytes() == original


def test_already_current_returns_0(config_current_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_current_and_lock
    return_code = run_hookpin(config_path, lockfile=lock)
    assert return_code == 0


def test_extras_end_to_end(config_extras_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_extras_and_lock
    return_code = run_hookpin(config_path, lockfile=lock)
    assert return_code == 1
    text = config_path.read_text()
    assert "pydantic[email]==2.13.4" in text
    assert "black>=24.10.0" in text


def test_operator_flag_end_to_end(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    return_code = run_hookpin(config_path, lockfile=lock, extra=["--operator", "~="])
    assert return_code == 1
    assert "pydantic~=2.13.4" in config_path.read_text()


def test_missing_dep_returns_1(config_missing_dep_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_missing_dep_and_lock
    original = config_path.read_bytes()
    return_code = run_hookpin(config_path, lockfile=lock)
    assert return_code == 1
    assert config_path.read_bytes() == original
