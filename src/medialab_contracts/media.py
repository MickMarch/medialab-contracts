"""Shared media-type enum used across the medialab services."""

from enum import Enum


class MediaType(str, Enum):
    """Canonical media classification. Wire values are ``movie`` and ``show``."""

    MOVIE = "movie"
    SHOW = "show"
