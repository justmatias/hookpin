from pathlib import Path

from sync_uv_additional_deps.config_updater import update_config  # pylint: disable=import-error


def test_stale_pin_updated(config_basic: Path, lock_packages: dict) -> None:
    result = update_config(config_basic, lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].package == "pydantic"
    assert result.changes[0].old == "1.0.0"
    assert result.changes[0].new == "2.13.4"
    assert result.warnings == []
    assert "pydantic==2.13.4" in config_basic.read_text()


def test_current_pin_is_noop(config_basic: Path, lock_packages: dict) -> None:
    update_config(config_basic, lock_packages)
    before = config_basic.read_bytes()
    result = update_config(config_basic, lock_packages)
    assert result.changes == []
    assert config_basic.read_bytes() == before


def test_unpinned_and_range_warns(config_with_extras: Path, lock_packages: dict) -> None:
    result = update_config(config_with_extras, lock_packages)
    assert "black>=22.0" in config_with_extras.read_text()
    assert any("black>=22.0" in w for w in result.warnings)


def test_bare_package_name_warns(tmp_path: Path, lock_packages: dict) -> None:
    cfg = tmp_path / "config.yaml"
    cfg.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - black
"""
    )
    result = update_config(cfg, lock_packages)
    assert result.changes == []
    assert any("black" in w for w in result.warnings)
    assert "black" in cfg.read_text()


def test_extras_preserved(config_with_extras: Path, lock_packages: dict) -> None:
    result = update_config(config_with_extras, lock_packages)
    pydantic_change = next(c for c in result.changes if c.package == "pydantic")
    assert pydantic_change.old == "2.0.0"
    assert pydantic_change.new == "2.13.4"
    assert "pydantic[email]==2.13.4" in config_with_extras.read_text()


def test_multiple_hooks_updated(multi_hook_config: Path, lock_packages: dict) -> None:
    result = update_config(multi_hook_config, lock_packages)
    assert len(result.changes) == 2
    assert all(c.package == "pydantic" for c in result.changes)


def test_missing_from_lock_warns(missing_package_config: Path, lock_packages: dict) -> None:
    result = update_config(missing_package_config, lock_packages)
    assert result.changes == []
    assert len(result.warnings) == 1
    assert "unknown-package" in result.warnings[0]
    assert "unknown-package==1.0.0" in missing_package_config.read_text()


def test_comments_preserved(config_with_comments: Path, lock_packages: dict) -> None:
    result = update_config(config_with_comments, lock_packages)
    assert len(result.changes) == 2
    text = config_with_comments.read_text()
    assert "# pinned from uv.lock" in text
    assert "# keep in sync" in text


def test_case_preserved(case_config: Path, lock_packages: dict) -> None:
    result = update_config(case_config, lock_packages)
    assert len(result.changes) == 1
    assert "Pydantic==2.13.4" in case_config.read_text()
