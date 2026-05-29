from pathlib import Path

from hookpin.config_updater import update_config


def test_stale_pin_updated(config_basic: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(config_basic, lock=lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].package == "pydantic"
    assert result.changes[0].old == "pydantic==1.0.0"
    assert result.changes[0].new == "pydantic==2.13.4"
    assert not result.warnings
    assert "pydantic==2.13.4" in config_basic.read_text()


def test_current_pin_is_noop(config_basic: Path, lock_packages: dict[str, str]) -> None:
    update_config(config_basic, lock=lock_packages)
    before = config_basic.read_bytes()
    result = update_config(config_basic, lock=lock_packages)
    assert not result.changes
    assert config_basic.read_bytes() == before


def test_gte_pin_updated(config_with_extras: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(config_with_extras, lock=lock_packages)
    assert "black>=24.10.0" in config_with_extras.read_text()
    assert not any("black" in w for w in result.warnings)


def test_bare_package_name_warns(
    bare_dependency_config: Path, lock_packages: dict[str, str]
) -> None:
    result = update_config(bare_dependency_config, lock=lock_packages)
    assert not result.changes
    assert any("black" in w for w in result.warnings)
    assert "black" in bare_dependency_config.read_text()


def test_extras_preserved(config_with_extras: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(config_with_extras, lock=lock_packages)
    pydantic_change = next(change for change in result.changes if change.package == "pydantic")
    assert pydantic_change.old == "pydantic[email]==2.0.0"
    assert pydantic_change.new == "pydantic[email]==2.13.4"
    assert "pydantic[email]==2.13.4" in config_with_extras.read_text()


def test_multiple_hooks_updated(multiple_hooks_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(multiple_hooks_config, lock=lock_packages)
    assert len(result.changes) == 2
    assert all(change.package == "pydantic" for change in result.changes)


def test_missing_from_lock_tracked(
    missing_package_config: Path, lock_packages: dict[str, str]
) -> None:
    result = update_config(missing_package_config, lock=lock_packages)
    assert not result.changes
    assert not result.warnings
    assert len(result.missing) == 1
    assert "unknown-package" in result.missing[0]
    assert "unknown-package==1.0.0" in missing_package_config.read_text()


def test_bare_name_not_in_missing(
    bare_unknown_dependency_config: Path, lock_packages: dict[str, str]
) -> None:
    result = update_config(bare_unknown_dependency_config, lock=lock_packages)
    assert not result.missing
    assert len(result.warnings) == 1


def test_comments_preserved(config_with_comments: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(config_with_comments, lock=lock_packages)
    assert len(result.changes) == 2
    text = config_with_comments.read_text()
    assert "# pinned from uv.lock" in text
    assert "# keep in sync" in text


def test_case_preserved(mixed_case_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(mixed_case_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert "Pydantic==2.13.4" in mixed_case_config.read_text()


def test_compatible_release_pin_updated(
    compatible_release_config: Path, lock_packages: dict[str, str]
) -> None:
    result = update_config(compatible_release_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].old == "pydantic~=1.0.0"
    assert result.changes[0].new == "pydantic~=2.13.4"
    assert "pydantic~=2.13.4" in compatible_release_config.read_text()


def test_lte_pin_updated(less_than_or_equal_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(less_than_or_equal_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert "pydantic<=2.13.4" in less_than_or_equal_config.read_text()


def test_ne_pin_updated(not_equal_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(not_equal_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert "pydantic!=2.13.4" in not_equal_config.read_text()


def test_range_collapses_to_exact(range_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(range_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].old == "pydantic>=1.0,<3.0"
    assert result.changes[0].new == "pydantic==2.13.4"
    assert "pydantic==2.13.4" in range_config.read_text()


def test_operator_flag_overrides(exact_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(exact_config, lock=lock_packages, operator="~=")
    assert len(result.changes) == 1
    assert "pydantic~=2.13.4" in exact_config.read_text()


def test_marker_preserved(marker_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(marker_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert result.changes[0].old == 'pydantic==1.0.0; python_version>="3.11"'
    assert result.changes[0].new == 'pydantic==2.13.4; python_version>="3.11"'
    assert 'pydantic==2.13.4; python_version>="3.11"' in marker_config.read_text()


def test_marker_with_extras_preserved(
    marker_with_extras_config: Path, lock_packages: dict[str, str]
) -> None:
    result = update_config(marker_with_extras_config, lock=lock_packages)
    assert len(result.changes) == 1
    assert (
        'pydantic[email]==2.13.4; python_version>="3.11"' in marker_with_extras_config.read_text()
    )


def test_marker_noop_when_current(
    marker_already_current_config: Path, lock_packages: dict[str, str]
) -> None:
    result = update_config(marker_already_current_config, lock=lock_packages)
    assert not result.changes
    assert not result.warnings


def test_operator_flag_collapses_range(range_config: Path, lock_packages: dict[str, str]) -> None:
    result = update_config(range_config, lock=lock_packages, operator=">=")
    assert len(result.changes) == 1
    assert "pydantic>=2.13.4" in range_config.read_text()
