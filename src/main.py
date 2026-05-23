import argparse
import sys
from pathlib import Path

from .config_updater import update_config
from .lock_parser import parse_lock


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync additional_dependencies pins in .pre-commit-config.yaml from uv.lock"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(".pre-commit-config.yaml"),
        help="Path to .pre-commit-config.yaml (default: .pre-commit-config.yaml)",
    )
    parser.add_argument(
        "--lockfile",
        type=Path,
        default=Path("uv.lock"),
        help="Path to uv.lock (default: uv.lock)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        lock = parse_lock(args.lockfile)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    result = update_config(args.config, lock)
    for w in result.warnings:
        print(f"warning: {w}", file=sys.stderr)
    for c in result.changes:
        print(f"{c.hook_id}: {c.package} {c.old} → {c.new}")
    return 1 if result.changes else 0


if __name__ == "__main__":
    sys.exit(main())
