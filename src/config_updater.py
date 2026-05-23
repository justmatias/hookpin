"""Functions for updating additional_dependencies pins in a pre-commit config."""

from dataclasses import dataclass
from pathlib import Path

from .config import PIN_RE, YAML_INSTANCE
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


def _process_dep(entry: str, hook_id: str, lock: dict[str, str]) -> DependencyResult:
    m = PIN_RE.match(entry)
    if not m:
        return DependencyResult(warning=f"{hook_id}: {entry!r} has no == pin — skipping")
    orig_name, extras, old_ver = m.group(1), m.group(2), m.group(3)
    norm = normalize_package_name(orig_name)
    if norm not in lock:
        return DependencyResult(
            warning=f"{hook_id}: {orig_name} not found in lockfile — leaving unchanged"
        )
    new_ver = lock[norm]
    if new_ver == old_ver:
        return DependencyResult()
    return DependencyResult(
        new_dependency=f"{orig_name}{extras or ''}=={new_ver}",
        change=Change(hook_id=hook_id, package=orig_name, old=old_ver, new=new_ver),
    )


def update_config(config_path: Path, lock: dict[str, str]) -> UpdateResult:
    """Rewrite stale == pins in config_path in place."""
    data: dict = YAML_INSTANCE.load(config_path)
    changes: list[Change] = []
    warnings: list[str] = []

    for repo in data.get("repos", []):
        for hook in repo.get("hooks", []):
            hook_id = hook.get("id", "<unknown>")
            deps = hook.get("additional_dependencies")
            if not deps:
                continue
            for i, entry in enumerate(deps):
                result = _process_dep(str(entry), hook_id, lock)
                if result.warning:
                    warnings.append(result.warning)
                if result.change:
                    deps[i] = result.new_dependency
                    changes.append(result.change)

    if changes:
        with config_path.open("w") as fh:
            YAML_INSTANCE.dump(data, fh)

    return UpdateResult(changes=changes, warnings=warnings)
