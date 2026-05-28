"""CLI entry point for hookpin."""

import argparse
import sys
from pathlib import Path

from .config_updater import update_config
from .discovery import resolve_configs
from .lock_parser import parse_lock


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync additional_dependencies pins in .pre-commit-config.yaml from uv.lock"
    )
    parser.add_argument(
        "--config",
        type=Path,
        action="append",
        default=None,
        help=(
            "Path or glob to a pre-commit config file; may be repeated. "
            "Glob patterns are expanded by hookpin (shell expansion is not required). "
            "Defaults to .pre-commit-config.yaml when omitted."
        ),
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
    patterns = args.config or [Path(".pre-commit-config.yaml")]
    try:
        configs = resolve_configs(patterns)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        lock = parse_lock(args.lockfile)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    multi = len(configs) > 1
    any_changes = False
    for config_path in configs:
        prefix = f"{config_path}: " if multi else ""
        result = update_config(config_path, lock=lock, operator=args.operator, dry_run=args.dry_run)
        for warning in result.warnings:
            print(f"warning: {prefix}{warning}", file=sys.stderr)
        for item in result.missing:
            print(f"warning: {prefix}{item}", file=sys.stderr)
        for change in result.changes:
            print(f"{prefix}{change.hook_id}: {change.package} {change.old} → {change.new}")
        if result.changes or result.missing:
            any_changes = True

    return 1 if any_changes else 0
