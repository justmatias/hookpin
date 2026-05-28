from pathlib import Path

from .helpers import run_hookpin


def test_dry_run_stale_returns_1_no_write(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    original = config_path.read_bytes()
    return_code = run_hookpin(config_path, lockfile=lock, extra=["--dry-run"])
    assert return_code == 1
    assert config_path.read_bytes() == original


def test_dry_run_current_returns_0(config_current_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_current_and_lock
    return_code = run_hookpin(config_path, lockfile=lock, extra=["--dry-run"])
    assert return_code == 0


def test_missing_dep_dry_run_returns_1_no_write(
    config_missing_dep_and_lock: tuple[Path, Path],
) -> None:
    config_path, lock = config_missing_dep_and_lock
    original = config_path.read_bytes()
    return_code = run_hookpin(config_path, lockfile=lock, extra=["--dry-run"])
    assert return_code == 1
    assert config_path.read_bytes() == original
