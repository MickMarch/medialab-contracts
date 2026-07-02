# CLAUDE.md - medialab-contracts

Shared Pydantic models and enums for the medialab service suite. Independent
git repo inside the `medialab/` workspace, consumed by every service as a
tag-pinned uv git dependency.

---

## Purpose

Define cross-service contracts once instead of copy-pasting them into each
repo. Created in response to real drift: `ErrorResponse` was defined three
times, `MediaType` had diverged (`Literal` in torrent-downloader vs `Enum` in
medialab-jellyfin), and `TransferInfo` was duplicated byte-for-byte in the bot.

## What belongs here

Only models that genuinely cross a service boundary (per the DRY-with-judgment
standard - never abstract across domains just to dedupe):

- `MediaType` - `(str, Enum)` with `MOVIE = "movie"`, `SHOW = "show"`. The
  canonical media classification. Wire values are stable.
- `ErrorResponse` - `{status, code, detail}` with a `json_schema_extra`
  example. `code` is a plain `str` so any service's `ErrorCode` serialises in.
- `CommonErrorCode` - the six error codes shared by all HTTP services:
  `UNAUTHORIZED`, `RATE_LIMITED`, `INVALID_INPUT`, `INTERNAL_ERROR`,
  `PATH_NOT_FOUND`, `PERMISSION_DENIED`.
- `TransferInfo`, `TransferHashInfo` - transfer DTOs owned by
  torrent-downloader, consumed by the bot and the orchestrator.
  `TransferHashInfo.tmdb_id` is optional (populated from v1.2 onward).
- `TorrentSearchScope` - targets a torrent search at a whole title, a season, or
  a single episode (`media_type`, optional `season`, optional `episode`).
  Validates the movie/season/episode combinations. Owned by torrent-downloader,
  consumed by the orchestrator gateway (search-steering only, no job state).

## What stays out

- Service-internal schemas with no cross-service consumer (TMDB detail shapes,
  torrent search grouping, Jellyfin VirtualFolder DTOs, Discord embeds).
- Each service's full `ErrorCode` enum - only the common base is shared. A
  service defines its own `ErrorCode` that includes `CommonErrorCode` plus its
  specific codes.
- Behavior (no `AppException`, no logic). Data models only; `pydantic` is the
  sole runtime dependency - no FastAPI, no httpx.

## Public surface

`__init__.py` re-exports everything consumers should import:
`MediaType`, `ErrorResponse`, `CommonErrorCode`, `TransferInfo`,
`TransferHashInfo`, `TorrentSearchScope`. Import from `medialab_contracts`,
not submodules.

## Module layout

```
src/medialab_contracts/
├── __init__.py      - public re-exports
├── media.py         - MediaType
├── errors.py        - ErrorResponse, CommonErrorCode
├── search.py        - TorrentSearchScope
└── transfers.py     - TransferInfo, TransferHashInfo
```

## Consumption & versioning

- Tag-pinned uv git dependency (see README). Bumping a consumer's pin is a
  deliberate, reviewable step - this is the controlled-drift seam.
- A breaking model change is a major version bump.
- Docker build wrinkle: a git-ref dependency needs git + network in the build
  stage. Each consumer's Dockerfile must allow this or switch to a path /
  vendored source. Decide per service when its Dockerfile is touched.

## Versioning

Version derived from git tags via `hatch-vcs` - never hardcoded.
`src/medialab_contracts/_version.py` is generated at build time and gitignored.
Release: merge to main, tag (`git tag -a vX.Y.Z -m "vX.Y.Z"`), push the tag,
create a GitHub Release, update `CHANGELOG.md` before tagging.

## Engineering standards

Full workspace standards apply (see root `medialab/CLAUDE.md`): ruff lint +
format (`E,F,I,UP,B,SIM,PLR2004`, UP042 ignored to keep `(str, Enum)`), mypy
with the pydantic plugin, pre-commit, dependabot, and a CI gate running lint,
format check, mypy, tests, and a dependency audit. CI checks out with
`fetch-depth: 0` so hatch-vcs can resolve the version from tags.

## Testing

- `uv run pytest` always, never `python -m pytest`. pytest style only.
- Tests cover model parse / serialise / round-trip and enum wire values.
