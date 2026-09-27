"""A show's seasons and episodes: the TMDB listing owned by torrent-downloader,
library presence owned by medialab-jellyfin, and the joined browse view owned
by the orchestrator."""

from datetime import date

from pydantic import BaseModel

from medialab_contracts.discover import TMDB_IMAGE_BASE_URL

STILL_SIZE = "w300"
"""TMDB image width for episode stills."""


def still_url(still_path: str | None) -> str | None:
    """Full TMDB image URL for an episode ``still_path``, or None."""
    if not still_path:
        return None
    return f"{TMDB_IMAGE_BASE_URL}/{STILL_SIZE}{still_path}"


class Episode(BaseModel):
    season: int
    episode: int
    title: str = ""
    air_date: date | None = None
    overview: str = ""
    still_path: str | None = None
    runtime_minutes: int | None = None


class Season(BaseModel):
    season: int
    name: str = ""
    episode_count: int = 0
    air_date: date | None = None
    poster_path: str | None = None
    overview: str = ""


class SeriesEpisodesResponse(BaseModel):
    """Every season and episode of a show except specials (season 0)."""

    tmdb_id: int
    seasons: list[Season]
    episodes: list[Episode]
    next_episode: Episode | None = None
    status: str = ""


class EpisodeKey(BaseModel):
    season: int
    episode: int


class LibraryEpisodesResponse(BaseModel):
    tmdb_id: int
    episodes: list[EpisodeKey]


class EpisodeState(Episode):
    """An episode with what medialab knows about it."""

    aired: bool = False
    in_library: bool = False
    queued_job_id: str | None = None


class ShowBrowseResponse(BaseModel):
    tmdb_id: int
    title: str
    year: str | None = None
    poster_path: str | None = None
    overview: str = ""
    status: str = ""
    seasons: list[Season]
    episodes: list[EpisodeState]
    next_episode: Episode | None = None
    on_wishlist: bool = False
    in_library: bool = False
