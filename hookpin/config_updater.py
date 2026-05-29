from dataclasses import dataclass
from pathlib import Path
from typing import Self

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

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

    @classmethod
    def unchanged(cls) -> Self:
        return cls()

    @classmethod
    def invalid(cls, message: str) -> Self:
        return cls(warning=message)

    @classmethod
    def not_in_lock(cls, message: str) -> Self:
        return cls(missing=True, warning=message)

    @classmethod
    def updated(cls, new_dependency: str, change: Change) -> Self:
        return cls(new_dependency=new_dependency, change=change)


def update_config(
    config_path: Path,
    *,
    lock: dict[str, str],
    operator: str | None = None,
    dry_run: bool = False,
    only: set[str] | None = None,
    exclude: set[str] | None = None,
) -> UpdateResult:
    """Rewrite stale version pins in config_path in place.

    When *dry_run* is True, compute changes but do not write the file.
    When *only* is given, only process hooks whose id is in the set.
    When *exclude* is given, skip hooks whose id is in the set.
    """
    data: CommentedMap = YAML_INSTANCE.load(config_path)
    result = UpdateResult(changes=[], warnings=[], missing=[])

    for repository in data.get("repos", []):
        for hook in repository.get("hooks", []):
            dependencies = hook.get("additional_dependencies")
            if not dependencies:
                continue

            hook_id = hook.get("id", "<unknown>")
            if only and hook_id not in only:
                continue
            if exclude and hook_id in exclude:
                continue

            hook_result = _process_hook_dependencies(
                dependencies,
                hook_id=hook_id,
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


def _process_dependency(
    *, entry: str, hook_id: str, lock: dict[str, str], operator: str | None = None
) -> DependencyResult:
    match = SPECIFIER_RE.match(entry)
    if not match:
        return DependencyResult.invalid(
            message=f"{hook_id}: {entry!r} has no version specifier — skipping"
        )

    original_name, extras, specifier, marker = match.groups()

    normalized_name = normalize_package_name(original_name)
    if normalized_name not in lock:
        return DependencyResult.not_in_lock(
            message=f"{hook_id}: {original_name} not found in lockfile — leaving unchanged"
        )

    new_version = lock[normalized_name]

    if operator:
        output_operator = operator
    else:
        parts = SPECIFIER_PART_RE.findall(specifier)
        output_operator = parts[0][0] if len(parts) == 1 else "=="

    new_dependency = f"{original_name}{extras or ''}{output_operator}{new_version}{marker or ''}"
    if new_dependency == entry:
        return DependencyResult.unchanged()

    change = Change(hook_id=hook_id, package=original_name, old=entry, new=new_dependency)
    return DependencyResult.updated(new_dependency, change)


def _is_dependency_ignored(dependencies: CommentedSeq, index: int) -> bool:
    """Return True if the dependency at index has an inline # hookpin: ignore comment."""
    tokens = dependencies.ca.items.get(index, [None])
    return tokens[0] and "hookpin: ignore" in tokens[0].value


def _process_hook_dependencies(
    dependencies: CommentedSeq,
    *,
    hook_id: str,
    lock: dict[str, str],
    operator: str | None,
) -> UpdateResult:
    result = UpdateResult(changes=[], warnings=[], missing=[])
    for index, entry in enumerate(dependencies):
        if _is_dependency_ignored(dependencies, index):
            continue

        dependency = _process_dependency(
            entry=str(entry),
            hook_id=hook_id,
            lock=lock,
            operator=operator,
        )
        if dependency.missing:
            result.missing.append(dependency.warning)  # type: ignore[arg-type]
        elif dependency.warning:
            result.warnings.append(dependency.warning)
        if dependency.change:
            dependencies[index] = dependency.new_dependency
            result.changes.append(dependency.change)
    return result
