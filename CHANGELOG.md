# Changelog

This document tracks notable updates to the repository.

Format:

- Dates use `YYYY-MM-DD`.
- Entries are grouped by release or milestone.
- Keep notes brief and focused on user-visible or architecture-significant changes.

## Unreleased

### Added

- Placeholder for upcoming changes.

## 2026-03-30

### Changed

- Replaced the Flask tutorial scaffold with a CLI-first `src/spc` package aligned to `docs/spotify-cli-roadmap.md`.
- Added command scaffolding for `spc auth`, `spc curate`, and `spc explain`.
- Added typed domain models, config handling, genre profiling, scoring, curation pipeline orchestration, and playlist writer scaffolding.
- Updated packaging metadata in `pyproject.toml` to install the `spc` CLI.

### Added

- Added architecture documentation in `docs/architecture.md`.
- Added source research notes in `docs/research/genre-sources.md`.
- Added CLI and domain tests under `tests/spc/`.
- Added local auth and run artifact handling under `./.spc/`.

### Removed

- Removed the remaining Flask tutorial-specific app structure, tests, and helper files from active use.
