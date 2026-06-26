# medialab-contracts

Shared Pydantic models and enums for the medialab service suite. Defines the
cross-service contracts once so they are not copy-pasted (and silently drifted)
across `torrent-downloader`, `medialab-bot`, `medialab-jellyfin`, and the
`medialab-orchestrator`.

Runtime dependency: `pydantic` only - importable by any service without a web
framework.

## Public surface

```python
from medialab_contracts import (
    MediaType,          # enum: MOVIE = "movie", SHOW = "show"
    ErrorResponse,      # {status, code, detail} structured-error shape
    CommonErrorCode,    # the six error codes shared by all HTTP services
    TransferInfo,       # per-torrent runtime snapshot
    TransferHashInfo,   # cached media_type + host_path (+ optional tmdb_id)
)
```

Each service keeps its own full `ErrorCode` enum that includes
`CommonErrorCode` plus its service-specific codes - only the common base is
shared.

## Consuming this package

Declare it as a tag-pinned uv git dependency in the consumer's `pyproject.toml`:

```toml
[project]
dependencies = ["medialab-contracts"]

[tool.uv.sources]
medialab-contracts = { git = "https://github.com/MickMarch/medialab-contracts", tag = "v0.1.0" }
```

Bumping the version is a deliberate change of the tag. A breaking model change
is a major version bump.

## Development

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run mypy src
```
