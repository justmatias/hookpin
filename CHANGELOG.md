# CHANGELOG


## v7.0.0 (2026-05-29)

### Bug Fixes

- Improve output diff ([#9](https://github.com/justmatias/hookpin/pull/9),
  [`890c456`](https://github.com/justmatias/hookpin/commit/890c4565f97d968e7cfaf4d417b4402130e0ba87))

* fix: improve output diff

* fix: add support for ignoring specific dependency pins via hookpin: ignore comments

### Features

- Breaking change detected [skip ci]
  ([`c4220a7`](https://github.com/justmatias/hookpin/commit/c4220a7591fa57543ae9fd7f7f2c9a9d34c6a152))


## v6.0.0 (2026-05-28)

### Features

- Add support for multiple config files and glob patterns with --…
  ([#8](https://github.com/justmatias/hookpin/pull/8),
  [`6dd3e6b`](https://github.com/justmatias/hookpin/commit/6dd3e6b9053e2e7decffa262957152bdfd3c03c8))

* feat: add support for multiple config files and glob patterns with --config, including dry-run
  mode and CLI entry point

* fix: config rename variables for clarity

* test: refactor test fixtures into external files and standardize directory-based management

* refactor: modularize test fixtures and add features documentation

- Breaking change detected [skip ci]
  ([`ae8a9af`](https://github.com/justmatias/hookpin/commit/ae8a9af27c42f19490d58fcbbbb661a5884e0ec1))


## v5.0.0 (2026-05-27)

### Chores

- Add --dry-run support docs ([#7](https://github.com/justmatias/hookpin/pull/7),
  [`a45f57c`](https://github.com/justmatias/hookpin/commit/a45f57c8bcb7758b71336fc6cbe775d7b3a5071e))

### Features

- Breaking change detected [skip ci]
  ([`d05efb5`](https://github.com/justmatias/hookpin/commit/d05efb5cced9b2b50a07fef07f15714e003423cc))


## v4.0.0 (2026-05-27)

### Features

- Breaking change detected [skip ci]
  ([`29727bb`](https://github.com/justmatias/hookpin/commit/29727bbeb84137c60e6da4458097188f00b1739f))


## v3.0.1 (2026-05-27)


## v3.0.0 (2026-05-27)

### Bug Fixes

- Add --dry-run option to check for stale pins without modifying configuration files
  ([`5f9bc76`](https://github.com/justmatias/hookpin/commit/5f9bc76a247c80ce514d35d07b56bad422aae66a))


## v2.0.0 (2026-05-27)

### Bug Fixes

- Rename CLI from sync-uv-additional-deps to hookpin
  ([`01d6d15`](https://github.com/justmatias/hookpin/commit/01d6d154c452edb27d0a2315ff2865026de971da))

- **config**: Update dependency handling in sync-uv-additional-deps
  ([`3ebd531`](https://github.com/justmatias/hookpin/commit/3ebd531fd76a9b00f23dd357ad882c33dd02ada3))

### Features

- Breaking change detected [skip ci]
  ([`ce19bdf`](https://github.com/justmatias/hookpin/commit/ce19bdf067ca9fb3cf37c4f2df765dfdb7127d60))


## v1.0.1 (2026-05-23)

### Bug Fixes

- Update reference for rev in semantic release config
  ([`a38698e`](https://github.com/justmatias/hookpin/commit/a38698e1797d4ac14c5b0c43890598d32564f5b0))


## v1.0.0 (2026-05-23)

### Bug Fixes

- Add tool to sync pre-commit additional_dependencies with uv.lock
  ([`de28b29`](https://github.com/justmatias/hookpin/commit/de28b2925c725b2a4abe2a0a131917aaf7ac811e))

- Modularize dependency processing, improve warning handling, and add project-level linting
  configurations
  ([`6f1627f`](https://github.com/justmatias/hookpin/commit/6f1627f2011faec982b4caef08b480a7e8ee0df6))

### Chores

- **config**: Add semantic release setup
  ([`c03dbfe`](https://github.com/justmatias/hookpin/commit/c03dbfefce1cb664cbdd2c5f659b869146fe4dc6))

- **config**: Initial setup
  ([`cd70788`](https://github.com/justmatias/hookpin/commit/cd707889c1a1a83fa923c355473b0fbd92bd182e))

- **config**: Remove unused import
  ([`a90fa3d`](https://github.com/justmatias/hookpin/commit/a90fa3d9bc26aa5fc99babb597a0c88641ca0b0c))

### Features

- Breaking change detected [skip ci]
  ([`668880b`](https://github.com/justmatias/hookpin/commit/668880b8583e42b24802115ae6a66daf14018b83))
