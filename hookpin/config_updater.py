"""Functions for updating additional_dependencies pins in a pre-commit config."""

from dataclasses import dataclass
from pathlib import Path

from .config import SPECIFIER_PART_RE, SPECIFIER_RE, YAML_INSTANCE
from .utils import normalize_package_name


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


@dataclass
class DependencyResult:
    new_dependency: str | None = None
    change: Change | None = None
    warning: str | None = None


def _process_dep(
    *, entry: str, hook_id: str, lock: dict[str, str], operator: str | None = None
) -> DependencyResult:
    match = SPECIFIER_RE.match(entry)
    if not match:
        return DependencyResult(warning=f"{hook_id}: {entry!r} has no version specifier — skipping")
    original_name, extras, specifier, marker = match.groups()
    normalized_name = normalize_package_name(original_name)
    if normalized_name not in lock:
        return DependencyResult(
            warning=f"{hook_id}: {original_name} not found in lockfile — leaving unchanged"
        )
    new_version = lock[normalized_name]
    parts = SPECIFIER_PART_RE.findall(specifier)  # [(op, ver), ...]

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


def update_config(
    config_path: Path, lock: dict[str, str], operator: str | None = None
) -> UpdateResult:
    """Rewrite stale version pins in config_path in place."""
    data: dict = YAML_INSTANCE.load(config_path)
    changes: list[Change] = []
    warnings: list[str] = []

    for repo in data.get("repos", []):
        for hook in repo.get("hooks", []):
            hook_id = hook.get("id", "<unknown>")
            dependencies = hook.get("additional_dependencies")
            if not dependencies:
                continue
            for index, entry in enumerate(dependencies):
                result = _process_dep(
                    entry=str(entry), hook_id=hook_id, lock=lock, operator=operator)
                if result.warning:
                    warnings.append(result.warning)
                if result.change:
                    dependencies[index] = result.new_dependency
                    changes.append(result.change)

    if changes:
        with config_path.open("w") as config_file:
            YAML_INSTANCE.dump(data, config_file)

    return UpdateResult(changes=changes, warnings=warnings)
