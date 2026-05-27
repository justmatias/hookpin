from pathlib import Path

from hookpin.main import main  # pylint: disable=import-error


def test_stale_pin_returns_1(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    return_code = main(["--config", str(config_path), "--lockfile", str(lock)])
    assert return_code == 1
    assert "pydantic==2.13.4" in config_path.read_text()


def test_idempotent(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    main(["--config", str(config_path), "--lockfile", str(lock)])
    before = config_path.read_bytes()
    return_code = main(["--config", str(config_path), "--lockfile", str(lock)])
    assert return_code == 0
    assert config_path.read_bytes() == before


def test_missing_lockfile_returns_2(config_with_missing_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_with_missing_lock
    original = config_path.read_bytes()
    return_code = main(["--config", str(config_path), "--lockfile", str(lock)])
    assert return_code == 2
    assert config_path.read_bytes() == original


def test_already_current_returns_0(config_current_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_current_and_lock
    return_code = main(["--config", str(config_path), "--lockfile", str(lock)])
    assert return_code == 0


def test_extras_end_to_end(config_extras_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_extras_and_lock
    return_code = main(["--config", str(config_path), "--lockfile", str(lock)])
    assert return_code == 1
    text = config_path.read_text()
    assert "pydantic[email]==2.13.4" in text
    assert "black>=24.10.0" in text


def test_operator_flag_end_to_end(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    return_code = main(["--config", str(config_path), "--lockfile", str(lock), "--operator", "~="])
    assert return_code == 1
    assert "pydantic~=2.13.4" in config_path.read_text()


def test_dry_run_stale_returns_1_no_write(config_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_and_lock
    original = config_path.read_bytes()
    return_code = main(["--config", str(config_path), "--lockfile", str(lock), "--dry-run"])
    assert return_code == 1
    assert config_path.read_bytes() == original


def test_dry_run_current_returns_0(config_current_and_lock: tuple[Path, Path]) -> None:
    config_path, lock = config_current_and_lock
    return_code = main(["--config", str(config_path), "--lockfile", str(lock), "--dry-run"])
    assert return_code == 0
