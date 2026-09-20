# CLAUDE.md - medialab-contracts

Workspace rules, conventions, standards and workflow live in the root
[`medialab/CLAUDE.md`](../CLAUDE.md); it is the authority when anything here
disagrees. This file holds only what is specific to this code.

## Purpose

Cross-service contracts defined once. Created in response to real drift:
`ErrorResponse` was defined three times, `MediaType` had diverged (`Literal`
in torrent-downloader vs `Enum` in medialab-jellyfin), and `TransferInfo` was
duplicated byte-for-byte in the bot. Public surface: [README](README.md).

## What belongs here

Only models and constants that genuinely cross a service boundary (the
workspace DRY rule: never abstract across domains just to dedupe):

- `MediaType` `(str, Enum)`, `MOVIE = "movie"`, `SHOW = "show"`. Wire values
  are stable.
- `ErrorResponse` `{status, code, detail}`; `code` is a plain `str` so any
  service's `ErrorCode` serialises in.
- `CommonErrorCode`: the codes every HTTP service shares. A service defines its
  own `ErrorCode` that includes these plus its specific codes.
- `TransferInfo`, `TransferHashInfo`: transfer DTOs owned by torrent-downloader,
  consumed by the bot and the orchestrator. `TransferHashInfo.tmdb_id` is a
  required `int`.
- `TorrentSearchScope`: whole title / season / episode targeting for a torrent
  search; validates the movie/season/episode combinations.
- Wire constants (`constants.py`): `API_PREFIX`, `API_KEY_HEADER`,
  `HEALTH_PATH`, `MEDIA_TYPE_SUBDIRS`. A route prefix or directory name that
  two services must agree on is declared here, not in each.

## What stays out

Service-internal schemas (TMDB detail shapes, torrent grouping, Jellyfin DTOs,
Discord embeds), each service's full `ErrorCode`, and any behaviour. Data
models only; `pydantic` is the sole runtime dependency.

## Module layout

```
src/medialab_contracts/
├── __init__.py   public re-exports (import from the package, not submodules)
├── media.py      MediaType
├── errors.py     ErrorResponse, CommonErrorCode
├── search.py     TorrentSearchScope
├── constants.py  API_PREFIX, API_KEY_HEADER, HEALTH_PATH, MEDIA_TYPE_SUBDIRS
└── transfers.py  TransferInfo, TransferHashInfo
```

## Consumption

Tag-pinned uv git dependency (`rev = "<tag>"` in the consumer's
`[tool.uv.sources]`). Bumping a consumer's pin is a deliberate, reviewable
step: this is the controlled-drift seam. A breaking model change is a major
bump. A git-ref dependency needs git and network in a consumer's Docker build
stage.

## Testing

Model parse / serialise / round-trip and enum wire values. Nothing external.
