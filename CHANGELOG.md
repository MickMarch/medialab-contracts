# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `TorrentSearchScope` model - targets a torrent search at a whole title, a
  season, or a single episode. Validates that movies carry no season/episode,
  an episode requires a season, and season/episode are >= 1. Owned by
  torrent-downloader, consumed by the orchestrator gateway.

### Changed

- `TransferHashInfo.tmdb_id` is now a required `int` (was optional). The id is
  always captured at download submission, so the cached metadata always carries
  it. Breaking for any consumer that relied on the optional field.

## [0.1.0] - 2026-06-26

### Added

- Initial shared models for the medialab service suite:
  - `MediaType` enum (`movie`, `show`) - the canonical media classification.
  - `ErrorResponse` model - the structured-error shape used by every service.
  - `CommonErrorCode` enum - the six error codes shared by all HTTP services.
  - `TransferInfo` and `TransferHashInfo` transfer DTOs (the latter carries an
    optional `tmdb_id` for v1.2 onward).
- Engineering standards from the first commit: ruff lint + format, mypy with
  the pydantic plugin, pre-commit hooks, dependabot, and a CI gate running
  lint, format check, mypy, tests, and a dependency audit.
