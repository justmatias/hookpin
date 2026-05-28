from pathlib import Path

import pytest

from .helpers import run_hookpin


def test_multiple_configs_repeated_flag(monorepo_and_lock: tuple[Path, Path, Path]) -> None:
    cfg_a, cfg_b, lock = monorepo_and_lock
    return_code = run_hookpin(cfg_a, cfg_b, lockfile=lock)
    assert return_code == 1
    assert "pydantic==2.13.4" in cfg_a.read_text()
    assert "pydantic==2.13.4" in cfg_b.read_text()


def test_multiple_configs_glob(
    monorepo_and_lock: tuple[Path, Path, Path],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    cfg_a, cfg_b, lock = monorepo_and_lock
    monkeypatch.chdir(cfg_a.parent.parent)
    return_code = run_hookpin("pkg_*/.pre-commit-config.yaml", lockfile=lock)
    assert return_code == 1
    assert "pydantic==2.13.4" in cfg_a.read_text()
    assert "pydantic==2.13.4" in cfg_b.read_text()
    out = capsys.readouterr().out
    assert "pkg_a" in out
    assert "pkg_b" in out


def test_glob_no_match_returns_2(empty_lock: Path) -> None:
    return_code = run_hookpin(
        empty_lock.parent / "no_match_*" / ".pre-commit-config.yaml",
        lockfile=empty_lock,
    )
    assert return_code == 2


def test_literal_missing_config_returns_2(empty_lock: Path) -> None:
    return_code = run_hookpin(empty_lock.parent / "ghost.yaml", lockfile=empty_lock)
    assert return_code == 2


def test_dedup_same_file_processed_once(monorepo_and_lock: tuple[Path, Path, Path]) -> None:
    cfg_a, _cfg_b, lock = monorepo_and_lock
    return_code = run_hookpin(cfg_a, cfg_a, lockfile=lock)
    assert return_code == 1
    return_code2 = run_hookpin(cfg_a, lockfile=lock)
    assert return_code2 == 0


def test_output_prefix_multiple_configs(
    monorepo_and_lock: tuple[Path, Path, Path], capsys: pytest.CaptureFixture
) -> None:
    cfg_a, cfg_b, lock = monorepo_and_lock
    run_hookpin(cfg_a, cfg_b, lockfile=lock)
    out = capsys.readouterr().out
    assert str(cfg_a) in out
    assert str(cfg_b) in out


def test_no_output_prefix_single_config(
    config_and_lock: tuple[Path, Path], capsys: pytest.CaptureFixture
) -> None:
    config_path, lock = config_and_lock
    run_hookpin(config_path, lockfile=lock)
    out = capsys.readouterr().out
    assert str(config_path) not in out
    assert "pydantic" in out
