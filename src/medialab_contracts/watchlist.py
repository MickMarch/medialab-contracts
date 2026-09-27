"""The watchlist owned by the orchestrator: saved titles kept for later, and
followed shows whose new episodes are downloaded automatically."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, model_validator

from medialab_contracts.media import MediaType

DEFAULT_FOLLOW_RESOLUTION = "1080p"


class WatchlistKind(str, Enum):
    SAVED = "saved"
    FOLLOWING = "following"


class FollowStartMode(str, Enum):
    NEW_ONLY = "new_only"
    """Episodes airing on or after the follow date."""
    FROM = "from"
    """A season and episode onward, inclusive."""
    BEGINNING = "beginning"
    """Season 1 episode 1 onward."""


class FollowStart(BaseModel):
    mode: FollowStartMode
    season: int | None = None
    episode: int | None = None

    @model_validator(mode="after")
    def _validate_scope(self) -> "FollowStart":
        if self.mode is FollowStartMode.FROM:
            if self.season is None or self.episode is None:
                raise ValueError("A 'from' start needs both season and episode.")
        elif self.season is not None or self.episode is not None:
            raise ValueError(f"A '{self.mode.value}' start must not set season or episode.")
        return self


class FollowRequest(BaseModel):
    """Body of ``PUT /watchlist/show/{tmdb_id}/follow``."""

    start: FollowStart
    resolution: str = DEFAULT_FOLLOW_RESOLUTION


class FollowState(BaseModel):
    start: FollowStart
    resolution: str = DEFAULT_FOLLOW_RESOLUTION
    paused: bool = False
    followed_at: datetime
    last_checked_at: datetime | None = None
    last_submitted: str | None = None
    """The last episode code this follow submitted, e.g. ``S02E05``."""


class WatchlistAddRequest(BaseModel):
    """Body of ``PUT /watchlist/{media_type}/{tmdb_id}``; stored so listing never calls TMDB."""

    title: str
    year: str | None = None
    poster_path: str | None = None
    overview: str = ""


class WatchlistItem(BaseModel):
    tmdb_id: int
    media_type: MediaType
    kind: WatchlistKind = WatchlistKind.SAVED
    title: str
    year: str | None = None
    poster_path: str | None = None
    overview: str = ""
    added_at: datetime
    in_library: bool = False
    follow: FollowState | None = None


class WatchlistResponse(BaseModel):
    items: list[WatchlistItem]


class SubmissionState(str, Enum):
    SUBMITTED = "submitted"
    IGNORED = "ignored"
