"""Shared transfer DTOs owned by torrent-downloader, consumed by the bot and
the orchestrator."""

from pydantic import BaseModel

from medialab_contracts.media import MediaType


class TransferInfo(BaseModel):
    """Runtime state snapshot for a single torrent."""

    name: str
    size: int
    progress: float
    hash: str
    state: str
    download_speed: int
    upload_speed: int
    eta_seconds: int
    save_path: str


class TransferHashInfo(BaseModel):
    """Cached metadata for a torrent, keyed by hash, looked up at completion.

    ``tmdb_id`` is optional: it is populated from v1.2 onward and absent for
    entries cached before that.
    """

    media_type: MediaType
    host_path: str
    tmdb_id: int | None = None
