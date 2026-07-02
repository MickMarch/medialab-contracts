"""Shared torrent-search scope owned by torrent-downloader, consumed by the
orchestrator gateway."""

from pydantic import BaseModel, model_validator

from medialab_contracts.media import MediaType


class TorrentSearchScope(BaseModel):
    """Targets a torrent search at a whole title, a season, or a single episode.

    Movies target the whole title (``season`` and ``episode`` must be unset).
    Shows may target the whole series (both unset), a season (``season`` set),
    or a single episode (``season`` and ``episode`` both set).
    """

    media_type: MediaType
    season: int | None = None
    episode: int | None = None

    @model_validator(mode="after")
    def _validate_scope(self) -> "TorrentSearchScope":
        if self.media_type is MediaType.MOVIE and (
            self.season is not None or self.episode is not None
        ):
            raise ValueError("A movie scope must not set season or episode.")

        if self.episode is not None and self.season is None:
            raise ValueError("An episode scope requires a season.")

        if self.season is not None and self.season < 1:
            raise ValueError("season must be >= 1.")

        if self.episode is not None and self.episode < 1:
            raise ValueError("episode must be >= 1.")

        return self
