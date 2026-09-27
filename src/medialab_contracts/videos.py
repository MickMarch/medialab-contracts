"""Trailers and teasers for a title or a season, owned by torrent-downloader
(TMDB videos filtered to YouTube), consumed by the web UI."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

YOUTUBE_EMBED_BASE_URL = "https://www.youtube-nocookie.com/embed"
"""The privacy-enhanced embed host: no cookies until playback starts."""


def youtube_embed_url(key: str) -> str:
    return f"{YOUTUBE_EMBED_BASE_URL}/{key}"


class VideoType(str, Enum):
    TRAILER = "trailer"
    TEASER = "teaser"


class Video(BaseModel):
    key: str
    """The YouTube video id."""
    name: str = ""
    type: VideoType
    official: bool = False
    published_at: datetime | None = None
    language: str = ""


class VideosResponse(BaseModel):
    """Official first, then trailers before teasers, then newest first."""

    videos: list[Video]
