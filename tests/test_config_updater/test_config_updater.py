from pathlib import Path

from hookpin.config_updater import update_config  # pylint: disable=import-error


def test_stale_pin_updated(config_basic: Path, lock_packages: dict) -> None:
    result = update_config(config_basic, lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].package == "pydantic"
    assert result.changes[0].old == "1.0.0"
    assert result.changes[0].new == "2.13.4"
    assert not result.warnings
    assert "pydantic==2.13.4" in config_basic.read_text()


def test_current_pin_is_noop(config_basic: Path, lock_packages: dict) -> None:
    update_config(config_basic, lock_packages)
    before = config_basic.read_bytes()
    result = update_config(config_basic, lock_packages)
    assert not result.changes
    assert config_basic.read_bytes() == before


def test_gte_pin_updated(config_with_extras: Path, lock_packages: dict) -> None:
    result = update_config(config_with_extras, lock_packages)
    assert "black>=24.10.0" in config_with_extras.read_text()
    assert not any("black" in w for w in result.warnings)


def test_bare_package_name_warns(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
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
    result = update_config(config_path, lock_packages)
    assert not result.changes
    assert any("black" in w for w in result.warnings)
    assert "black" in config_path.read_text()


def test_extras_preserved(config_with_extras: Path, lock_packages: dict) -> None:
    result = update_config(config_with_extras, lock_packages)
    pydantic_change = next(change for change in result.changes if change.package == "pydantic")
    assert pydantic_change.old == "2.0.0"
    assert pydantic_change.new == "2.13.4"
    assert "pydantic[email]==2.13.4" in config_with_extras.read_text()


def test_multiple_hooks_updated(multi_hook_config: Path, lock_packages: dict) -> None:
    result = update_config(multi_hook_config, lock_packages)
    assert len(result.changes) == 2
    assert all(change.package == "pydantic" for change in result.changes)


def test_missing_from_lock_warns(missing_package_config: Path, lock_packages: dict) -> None:
    result = update_config(missing_package_config, lock_packages)
    assert not result.changes
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


def test_compatible_release_pin_updated(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic~=1.0.0
"""
    )
    result = update_config(config_path, lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].old == "1.0.0"
    assert result.changes[0].new == "2.13.4"
    assert "pydantic~=2.13.4" in config_path.read_text()


def test_lte_pin_updated(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic<=1.0.0
"""
    )
    result = update_config(config_path, lock_packages)
    assert len(result.changes) == 1
    assert "pydantic<=2.13.4" in config_path.read_text()


def test_ne_pin_updated(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic!=1.0.0
"""
    )
    result = update_config(config_path, lock_packages)
    assert len(result.changes) == 1
    assert "pydantic!=2.13.4" in config_path.read_text()


def test_range_collapses_to_exact(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic>=1.0,<3.0
"""
    )
    result = update_config(config_path, lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].old == ">=1.0,<3.0"
    assert result.changes[0].new == "2.13.4"
    assert "pydantic==2.13.4" in config_path.read_text()


def test_operator_flag_overrides(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic==1.0.0
"""
    )
    result = update_config(config_path, lock_packages, operator="~=")
    assert len(result.changes) == 1
    assert "pydantic~=2.13.4" in config_path.read_text()


def test_marker_preserved(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic==1.0.0; python_version>="3.11"
"""
    )
    result = update_config(config_path, lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].old == "1.0.0"
    assert result.changes[0].new == "2.13.4"
    assert 'pydantic==2.13.4; python_version>="3.11"' in config_path.read_text()


def test_marker_with_extras_preserved(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic[email]==1.0.0; python_version>="3.11"
"""
    )
    result = update_config(config_path, lock_packages)
    assert len(result.changes) == 1
    assert 'pydantic[email]==2.13.4; python_version>="3.11"' in config_path.read_text()


def test_marker_noop_when_current(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic==2.13.4; python_version>="3.11"
"""
    )
    result = update_config(config_path, lock_packages)
    assert not result.changes
    assert not result.warnings


def test_operator_flag_collapses_range(tmp_path: Path, lock_packages: dict) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """\
repos:
  - repo: https://example.com/hook
    rev: v1
    hooks:
      - id: my-hook
        additional_dependencies:
          - pydantic>=1.0,<3.0
"""
    )
    result = update_config(config_path, lock_packages, operator=">=")
    assert len(result.changes) == 1
    assert "pydantic>=2.13.4" in config_path.read_text()
