"""Discover placeholders in Jellyfin: the folders medialab-jellyfin writes, the
libraries medialab-setup creates over them, and the favorite event that turns
a placeholder into a request for the orchestrator."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from medialab_contracts.media import MediaType

DISCOVER_LIBRARY_NAMES: dict[MediaType, str] = {
    MediaType.MOVIE: "Discover Movies",
    MediaType.SHOW: "Discover Shows",
}
"""Jellyfin library name per media type. Each library points at
``<discover root>/<MEDIA_TYPE_SUBDIRS[media_type]>``."""

DISCOVER_CLIP_SUBDIR = "_clip"
"""Subdirectory of the discover root holding the source clip, beside the
library roots so Jellyfin never indexes it."""

DISCOVER_CLIP_FILENAME = "request.mp4"
"""Clip copied into every placeholder; Jellyfin needs a playable file to
create an item."""

PLACEHOLDER_TITLE_SEPARATOR = " - "


class PlaceholderState(str, Enum):
    AVAILABLE = "available"
    REQUESTED = "requested"
    DOWNLOADING = "downloading"
    NOT_FOUND = "not_found"


PLACEHOLDER_TITLE_SUFFIXES: dict[PlaceholderState, str | None] = {
    PlaceholderState.AVAILABLE: None,
    PlaceholderState.REQUESTED: "Requested",
    PlaceholderState.DOWNLOADING: "Downloading",
    PlaceholderState.NOT_FOUND: "Not found yet",
}
"""Suffix written into the placeholder title; the only state feedback every
Jellyfin client shows."""


def placeholder_title(title: str, state: PlaceholderState) -> str:
    """Display title for a placeholder in ``state``."""
    suffix = PLACEHOLDER_TITLE_SUFFIXES[state]
    return f"{title}{PLACEHOLDER_TITLE_SEPARATOR}{suffix}" if suffix else title


JELLYFIN_ITEM_TYPES: dict[str, MediaType] = {
    "Movie": MediaType.MOVIE,
    "Series": MediaType.SHOW,
}
"""Jellyfin ``ItemType`` values that can be placeholders."""


class JellyfinRequestEvent(BaseModel):
    """A favorite toggled on a placeholder, from the Webhook plugin or the poll.

    The Webhook plugin template renders every value as a string and sends the
    Jellyfin item type, so both are coerced here.
    """

    model_config = ConfigDict(populate_by_name=True)

    jellyfin_user_id: str
    item_id: str
    media_type: MediaType = Field(alias="item_type")
    tmdb_id: int
    is_favorite: bool

    @field_validator("media_type", mode="before")
    @classmethod
    def _map_jellyfin_item_type(cls, value: Any) -> Any:
        return JELLYFIN_ITEM_TYPES.get(value, value)
