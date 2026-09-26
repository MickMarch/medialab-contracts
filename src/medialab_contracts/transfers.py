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
    content_path: str = ""
    """Absolute host path of the torrent's root file or folder, as qBittorrent
    reports it. Its basename is the on-disk name the orchestrator renames from;
    the display ``name`` is not reliable for that. Empty when unknown."""


class TransferHashInfo(BaseModel):
    """Cached metadata for a torrent, keyed by hash, looked up at completion."""

    media_type: MediaType
    host_path: str
    tmdb_id: int
