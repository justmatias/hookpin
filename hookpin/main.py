"""CLI entry point for hookpin."""

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
    parser.add_argument(
        "--operator",
        choices=["==", "~=", ">=", "<=", "!="],
        default=None,
        help="Operator to use when rewriting pins; preserves existing operator by default",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Report stale pins and exit non-zero without writing (CI gate)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the hook; return 0 (clean), 1 (pins updated), or 2 (error)."""
    args = _parse_args(argv)
    try:
        lock = parse_lock(args.lockfile)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    result = update_config(args.config, lock, args.operator, dry_run=args.dry_run)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for item in result.missing:
        print(f"warning: {item}", file=sys.stderr)
    for change in result.changes:
        print(f"{change.hook_id}: {change.package} {change.old} → {change.new}")
    return 1 if (result.changes or result.missing) else 0


if __name__ == "__main__":
    sys.exit(main())
