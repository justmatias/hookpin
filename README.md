# hookpin

A pre-commit hook that keeps `additional_dependencies` pins in `.pre-commit-config.yaml` in sync with your `uv.lock` file.

## Usage

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/justmatias/hookpin
    rev: v7.0.1
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

## Ignoring specific pins

Add a `# hookpin: ignore` inline comment to exclude a pin from updates:

```yaml
additional_dependencies:
  - flake8-bugbear==1.0.0  # hookpin: ignore
  - pydantic==1.0.0
```

`flake8-bugbear` will be left at `1.0.0` regardless of what `uv.lock` contains; `pydantic` is updated as normal.

## Options

### `--operator`

Override the output operator for all rewritten pins, regardless of what was in the config:

```yaml
- repo: https://github.com/justmatias/hookpin
  rev: v7.0.1
  hooks:
    - id: sync-uv-additional-deps
      args: [--operator, '==']
```

Accepted values: `==`, `~=`, `>=`, `<=`, `!=`. When omitted, the existing operator is preserved (ranges collapse to `==`).

### `--dry-run`

Report stale pins and missing dependencies without writing any files. Exits 1 if any issues are found, making it useful as a CI gate:

```yaml
- repo: https://github.com/justmatias/hookpin
  rev: v7.0.1
  hooks:
    - id: hookpin
      args: [--dry-run]
```

### `--config`

Path or glob pattern to a pre-commit config file. May be repeated to cover multiple
files (e.g. in a monorepo). Glob patterns are expanded by hookpin — no shell quoting
tricks required. Defaults to `.pre-commit-config.yaml` when omitted.

```yaml
- repo: https://github.com/justmatias/hookpin
  rev: v7.0.1
  hooks:
    - id: hookpin
      args: [--config, 'packages/*/.pre-commit-config.yaml']
```

An unmatched glob pattern or a literal path that does not exist exits with code 2.

### `--only`

Process only the hooks with the given id. May be repeated to include multiple hooks:

```yaml
- repo: https://github.com/justmatias/hookpin
  rev: v7.0.1
  hooks:
    - id: hookpin
      args: [--only, mypy, --only, ruff]
```

Hooks not listed are left completely untouched.

### `--exclude`

Skip the hooks with the given id. May be repeated to exclude multiple hooks:

```yaml
- repo: https://github.com/justmatias/hookpin
  rev: v7.0.1
  hooks:
    - id: hookpin
      args: [--exclude, mypy]
```

`--only` and `--exclude` are independent: `--only` is an allowlist, `--exclude` is a denylist.

### `--lockfile`

Path to the lock file. Defaults to `uv.lock`.

## Exit codes

| Code | Meaning                                                           |
| ---- | ----------------------------------------------------------------- |
| 0    | All pins are current — nothing changed                            |
| 1    | Pins were rewritten, or deps in config are missing from `uv.lock` |
| 2    | Hard error (e.g. `uv.lock` not found)                             |
