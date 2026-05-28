"""Functions for updating additional_dependencies pins in a pre-commit config."""

from dataclasses import dataclass
from pathlib import Path

from ruamel.yaml import YAML  # pylint: disable=import-error

from .naming import normalize_package_name
from .patterns import SPECIFIER_PART_RE, SPECIFIER_RE

YAML_INSTANCE = YAML()
YAML_INSTANCE.preserve_quotes = True
YAML_INSTANCE.indent(mapping=2, sequence=4, offset=2)


@dataclass(frozen=True)
class Change:
    hook_id: str
    package: str
    old: str
    new: str


@dataclass
class UpdateResult:
    changes: list[Change]
    warnings: list[str]
    missing: list[str]


@dataclass
class DependencyResult:
    new_dependency: str | None = None
    change: Change | None = None
    warning: str | None = None
    missing: bool = False


def _process_dependency(
    *, entry: str, hook_id: str, lock: dict[str, str], operator: str | None = None
) -> DependencyResult:
    match = SPECIFIER_RE.match(entry)
    if not match:
        return DependencyResult(warning=f"{hook_id}: {entry!r} has no version specifier — skipping")
    original_name, extras, specifier, marker = match.groups()
    normalized_name = normalize_package_name(original_name)
    if normalized_name not in lock:
        return DependencyResult(
            missing=True,
            warning=f"{hook_id}: {original_name} not found in lockfile — leaving unchanged",
        )
    new_version = lock[normalized_name]
    parts = SPECIFIER_PART_RE.findall(specifier)  # [(operator, version), ...]

    if operator:
        output_operator = operator
    elif len(parts) == 1:
        output_operator = parts[0][0]
    else:
        output_operator = "=="  # collapse compound ranges to an exact pin

    new_dependency = f"{original_name}{extras or ''}{output_operator}{new_version}{marker or ''}"
    if new_dependency == entry:
        return DependencyResult()

    old = parts[0][1] if len(parts) == 1 else specifier
    return DependencyResult(
        new_dependency=new_dependency,
        change=Change(hook_id=hook_id, package=original_name, old=old, new=new_version),
    )


def _process_hook_dependencies(
    dependencies: list,
    *,
    hook_id: str,
    lock: dict[str, str],
    operator: str | None,
) -> UpdateResult:
    result = UpdateResult(changes=[], warnings=[], missing=[])
    for index, entry in enumerate(dependencies):
        dependency = _process_dependency(entry=str(entry), hook_id=hook_id, lock=lock, operator=operator)
        if dependency.missing and dependency.warning:
            result.missing.append(dependency.warning)
        elif dependency.warning:
            result.warnings.append(dependency.warning)
        if dependency.change:
            dependencies[index] = dependency.new_dependency
            result.changes.append(dependency.change)
    return result


def update_config(
    config_path: Path,
    *,
    lock: dict[str, str],
    operator: str | None = None,
    dry_run: bool = False,
) -> UpdateResult:
    """Rewrite stale version pins in config_path in place.

    When *dry_run* is True, compute changes but do not write the file.
    """
    data: dict = YAML_INSTANCE.load(config_path)
    result = UpdateResult(changes=[], warnings=[], missing=[])

    for repo in data.get("repos", []):
        for hook in repo.get("hooks", []):
            dependencies = hook.get("additional_dependencies")
            if not dependencies:
                continue
            hook_result = _process_hook_dependencies(
                dependencies,
                hook_id=hook.get("id", "<unknown>"),
                lock=lock,
                operator=operator,
            )
            result.changes.extend(hook_result.changes)
            result.warnings.extend(hook_result.warnings)
            result.missing.extend(hook_result.missing)

    if result.changes and not dry_run:
        with config_path.open("w") as config_file:
            YAML_INSTANCE.dump(data, config_file)

    return result
