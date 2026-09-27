"""Live download progress the orchestrator attaches to jobs waiting on qBittorrent."""

from pydantic import BaseModel, Field

ETA_UNKNOWN_SECONDS = 8640000
"""qBittorrent's ETA when it cannot estimate one; mapped to ``None`` on the wire."""


class JobProgress(BaseModel):
    progress: float = Field(ge=0.0, le=1.0)
    download_speed: int = Field(ge=0)
    """Bytes per second."""
    eta_seconds: int | None = None
    """``None`` when qBittorrent cannot estimate one."""
    state: str
