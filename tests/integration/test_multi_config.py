import os
from pathlib import Path

import pytest

from hookpin.cli import main  # pylint: disable=import-error


def test_multiple_configs_repeated_flag(monorepo_and_lock: tuple[Path, Path, Path]) -> None:
    cfg_a, cfg_b, lock = monorepo_and_lock
    return_code = main(["--config", str(cfg_a), "--config", str(cfg_b), "--lockfile", str(lock)])
    assert return_code == 1
    assert "pydantic==2.13.4" in cfg_a.read_text()
    assert "pydantic==2.13.4" in cfg_b.read_text()


def test_multiple_configs_glob(
    monorepo_and_lock: tuple[Path, Path, Path], capsys: pytest.CaptureFixture
) -> None:
    cfg_a, cfg_b, lock = monorepo_and_lock
    root = cfg_a.parent.parent
    old_cwd = os.getcwd()
    try:
        os.chdir(root)
        return_code = main(["--config", "pkg_*/.pre-commit-config.yaml", "--lockfile", str(lock)])
    finally:
        os.chdir(old_cwd)
    assert return_code == 1
    assert "pydantic==2.13.4" in cfg_a.read_text()
    assert "pydantic==2.13.4" in cfg_b.read_text()
    out = capsys.readouterr().out
    assert "pkg_a" in out
    assert "pkg_b" in out


def test_glob_no_match_returns_2(empty_lock: Path) -> None:
    return_code = main(
        [
            "--config",
            str(empty_lock.parent / "no_match_*" / ".pre-commit-config.yaml"),
            "--lockfile",
            str(empty_lock),
        ]
    )
    assert return_code == 2


def test_literal_missing_config_returns_2(empty_lock: Path) -> None:
    return_code = main(
        ["--config", str(empty_lock.parent / "ghost.yaml"), "--lockfile", str(empty_lock)]
    )
    assert return_code == 2


def test_dedup_same_file_processed_once(monorepo_and_lock: tuple[Path, Path, Path]) -> None:
    cfg_a, _cfg_b, lock = monorepo_and_lock
    return_code = main(["--config", str(cfg_a), "--config", str(cfg_a), "--lockfile", str(lock)])
    assert return_code == 1
    return_code2 = main(["--config", str(cfg_a), "--lockfile", str(lock)])
    assert return_code2 == 0


def test_output_prefix_multiple_configs(
    monorepo_and_lock: tuple[Path, Path, Path], capsys: pytest.CaptureFixture
) -> None:
    cfg_a, cfg_b, lock = monorepo_and_lock
    main(["--config", str(cfg_a), "--config", str(cfg_b), "--lockfile", str(lock)])
    out = capsys.readouterr().out
    assert str(cfg_a) in out
    assert str(cfg_b) in out


def test_no_output_prefix_single_config(
    config_and_lock: tuple[Path, Path], capsys: pytest.CaptureFixture
) -> None:
    config_path, lock = config_and_lock
    main(["--config", str(config_path), "--lockfile", str(lock)])
    out = capsys.readouterr().out
    assert str(config_path) not in out
    assert "pydantic" in out
