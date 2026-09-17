# medialab-contracts

Shared Pydantic models and enums for the
[medialab](https://github.com/MickMarch/medialab) suite. Cross-service
contracts are defined once here so they are not copy-pasted and silently
drifted across torrent-downloader, medialab-bot, medialab-jellyfin and
medialab-orchestrator.

Runtime dependency: `pydantic` only.

## Public surface

```python
from medialab_contracts import (
    MediaType,           # enum: MOVIE = "movie", SHOW = "show"
    ErrorResponse,       # {status, code, detail} structured-error shape
    CommonErrorCode,     # error codes shared by every HTTP service
    TransferInfo,        # per-torrent runtime snapshot
    TransferHashInfo,    # cached media_type + host_path + tmdb_id for a hash
    TorrentSearchScope,  # media_type + optional season / episode for torrent search
)
```

Each service keeps its own full `ErrorCode` enum that includes
`CommonErrorCode` plus its service-specific codes.

## Consuming this package

Declare it as a tag-pinned uv git dependency:

```toml
[project]
dependencies = ["medialab-contracts"]

[tool.uv.sources]
medialab-contracts = { git = "https://github.com/MickMarch/medialab-contracts", rev = "<tag>" }
```

Use the newest tag from this repo's releases. Bumping the pin is a deliberate
change; a breaking model change is a major version bump.

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check . && uv run ruff format --check . && uv run mypy src
```

Standards, workflow and release process: [workspace CLAUDE.md](../CLAUDE.md).
Code-local notes: [CLAUDE.md](CLAUDE.md).
