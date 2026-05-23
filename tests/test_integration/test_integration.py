from pathlib import Path

from sync_uv_additional_deps.main import main


def test_stale_pin_returns_1(config_and_lock: tuple[Path, Path]) -> None:
    cfg, lock = config_and_lock
    rc = main(["--config", str(cfg), "--lockfile", str(lock)])
    assert rc == 1
    assert "pydantic==2.13.4" in cfg.read_text()


def test_idempotent(config_and_lock: tuple[Path, Path]) -> None:
    cfg, lock = config_and_lock
    main(["--config", str(cfg), "--lockfile", str(lock)])
    before = cfg.read_bytes()
    rc = main(["--config", str(cfg), "--lockfile", str(lock)])
    assert rc == 0
    assert cfg.read_bytes() == before


def test_missing_lockfile_returns_2(config_with_missing_lock: tuple[Path, Path]) -> None:
    cfg, lock = config_with_missing_lock
    original = cfg.read_bytes()
    rc = main(["--config", str(cfg), "--lockfile", str(lock)])
    assert rc == 2
    assert cfg.read_bytes() == original


def test_already_current_returns_0(config_current_and_lock: tuple[Path, Path]) -> None:
    cfg, lock = config_current_and_lock
    rc = main(["--config", str(cfg), "--lockfile", str(lock)])
    assert rc == 0


def test_extras_end_to_end(config_extras_and_lock: tuple[Path, Path]) -> None:
    cfg, lock = config_extras_and_lock
    rc = main(["--config", str(cfg), "--lockfile", str(lock)])
    assert rc == 1
    text = cfg.read_text()
    assert "pydantic[email]==2.13.4" in text
    assert "black>=22.0" in text
