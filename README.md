# sync-uv-additional-deps

A pre-commit hook that keeps `additional_dependencies` pins in `.pre-commit-config.yaml` in sync with your `uv.lock` file.

## Usage

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/justmatias/pre-commit-uv-sync
    rev: v1.0.1
    hooks:
      - id: sync-uv-additional-deps
```

The hook reads `uv.lock` and rewrites any `==`-pinned `additional_dependencies` entries that are out of date.

## Exit codes

| Code | Meaning                                          |
| ---- | ------------------------------------------------ |
| 0    | All pins are current — nothing changed           |
| 1    | File was rewritten (pre-commit fixer convention) |
| 2    | Hard error (e.g. `uv.lock` not found)            |
