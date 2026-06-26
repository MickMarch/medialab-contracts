# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
