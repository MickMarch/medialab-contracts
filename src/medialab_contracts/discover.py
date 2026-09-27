"""Discover (trending and by-genre) titles owned by torrent-downloader, and
the library TMDB ids owned by medialab-jellyfin."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from medialab_contracts.media import MediaType
from medialab_contracts.watchlist import WatchlistKind

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"


class PosterSize(str, Enum):
    """TMDB image widths used by the UIs."""

    GRID = "w342"
    THUMBNAIL = "w154"


def poster_url(poster_path: str | None, size: PosterSize) -> str | None:
    """Full TMDB image URL for ``poster_path`` (which starts with ``/``), or None."""
    if not poster_path:
        return None
    return f"{TMDB_IMAGE_BASE_URL}/{size.value}{poster_path}"


class DiscoverItem(BaseModel):
    tmdb_id: int
    media_type: MediaType
    title: str
    year: str | None = None
    overview: str = ""
    vote_average: float = 0.0
    poster_path: str | None = None
    on_watchlist: bool = False
    watchlist_kind: WatchlistKind | None = None
    in_library: bool = False


class DiscoverResponse(BaseModel):
    items: list[DiscoverItem]
    page: int
    total_pages: int
    cached_at: datetime


class Genre(BaseModel):
    id: int
    name: str


class GenresResponse(BaseModel):
    genres: list[Genre]


class LibraryTmdbIdsResponse(BaseModel):
    media_type: MediaType
    tmdb_ids: list[int]
