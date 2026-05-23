from dataclasses import dataclass
from pathlib import Path
from typing import Any

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


def update_config(
    config_path: Path,
    lock: dict[str, str],
) -> UpdateResult:
    """Rewrite stale == pins in config_path in place."""
    data: dict[str, Any] = YAML_INSTANCE.load(config_path)
    changes: list[Change] = []
    warnings: list[str] = []

    for repo in data.get("repos", []):
        for hook in repo.get("hooks", []):
            hook_id = hook.get("id", "<unknown>")
            deps = hook.get("additional_dependencies")
            if not deps:
                continue
            for i, entry in enumerate(deps):
                m = PIN_RE.match(str(entry))
                if not m:
                    continue
                orig_name, extras, old_ver = m.group(1), m.group(2), m.group(3)
                norm = normalize_package_name(orig_name)
                if norm not in lock:
                    warnings.append(
                        f"{hook_id}: {orig_name} not found in lockfile — leaving unchanged"
                    )
                    continue
                new_ver = lock[norm]
                if new_ver == old_ver:
                    continue
                deps[i] = f"{orig_name}{extras or ''}=={new_ver}"
                changes.append(Change(hook_id=hook_id, package=orig_name, old=old_ver, new=new_ver))

    if changes:
        with config_path.open("w") as fh:
            YAML_INSTANCE.dump(data, fh)

    return UpdateResult(changes=changes, warnings=warnings)
