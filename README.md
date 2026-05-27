# hookpin

A pre-commit hook that keeps `additional_dependencies` pins in `.pre-commit-config.yaml` in sync with your `uv.lock` file.

## Usage

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/justmatias/hookpin
    rev: v4.0.0
    hooks:
      - id: hookpin
```

The hook reads `uv.lock` and rewrites stale `additional_dependencies` entries in place.

## Supported version specifiers

All PEP 440 operators are handled:

| Specifier in config  | Rewritten to       |
| -------------------- | ------------------ |
| `pydantic==1.0.0`    | `pydantic==2.13.4` |
| `pydantic>=1.0.0`    | `pydantic>=2.13.4` |
| `pydantic~=1.0.0`    | `pydantic~=2.13.4` |
| `pydantic<=1.0.0`    | `pydantic<=2.13.4` |
| `pydantic!=1.0.0`    | `pydantic!=2.13.4` |
| `pydantic>=1.0,<3.0` | `pydantic==2.13.4` |

Compound range specifiers (e.g. `>=1.0,<3.0`) are collapsed to an exact `==` pin.

Extras and PEP 508 environment markers are preserved verbatim:

```
pydantic[email]==1.0.0; python_version>="3.11"
→ pydantic[email]==2.13.4; python_version>="3.11"
```

Entries with no version specifier (bare package names, or names with only a marker) are left unchanged with a warning.

## Options

### `--operator`

Override the output operator for all rewritten pins, regardless of what was in the config:

```yaml
- repo: https://github.com/justmatias/pre-commit-uv-sync
  rev: v4.0.0
  hooks:
    - id: sync-uv-additional-deps
      args: [--operator, '==']
```

Accepted values: `==`, `~=`, `>=`, `<=`, `!=`. When omitted, the existing operator is preserved (ranges collapse to `==`).

### `--config`

Path to the pre-commit config file. Defaults to `.pre-commit-config.yaml`.

### `--lockfile`

Path to the lock file. Defaults to `uv.lock`.

## Exit codes

| Code | Meaning                                          |
| ---- | ------------------------------------------------ |
| 0    | All pins are current — nothing changed           |
| 1    | File was rewritten (pre-commit fixer convention) |
| 2    | Hard error (e.g. `uv.lock` not found)            |
