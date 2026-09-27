"""Shared Pydantic models, enums and wire constants for the medialab service suite."""

from medialab_contracts.constants import (
    API_KEY_HEADER,
    API_PREFIX,
    HEALTH_PATH,
    MEDIA_TYPE_SUBDIRS,
    STAGING_SUBDIR,
)
from medialab_contracts.discover import (
    TMDB_IMAGE_BASE_URL,
    DiscoverItem,
    DiscoverResponse,
    Genre,
    GenresResponse,
    LibraryTmdbIdsResponse,
    PosterSize,
    WishlistAddRequest,
    WishlistItem,
    WishlistResponse,
    poster_url,
)
from medialab_contracts.errors import CommonErrorCode, ErrorResponse
from medialab_contracts.media import MediaType
from medialab_contracts.progress import ETA_UNKNOWN_SECONDS, JobProgress
from medialab_contracts.search import TorrentSearchScope
from medialab_contracts.settings import (
    SettingSource,
    SettingSpec,
    SettingsResponse,
    SettingType,
    SettingUpdate,
    SettingValue,
    SettingView,
    SuiteSettingsResponse,
)
from medialab_contracts.shows import (
    STILL_SIZE,
    Episode,
    EpisodeKey,
    EpisodeState,
    LibraryEpisodesResponse,
    Season,
    SeriesEpisodesResponse,
    ShowBrowseResponse,
    still_url,
)
from medialab_contracts.transfers import TransferHashInfo, TransferInfo

__all__ = [
    "API_KEY_HEADER",
    "API_PREFIX",
    "CommonErrorCode",
    "DiscoverItem",
    "DiscoverResponse",
    "ETA_UNKNOWN_SECONDS",
    "Episode",
    "EpisodeKey",
    "EpisodeState",
    "ErrorResponse",
    "Genre",
    "GenresResponse",
    "HEALTH_PATH",
    "JobProgress",
    "LibraryEpisodesResponse",
    "LibraryTmdbIdsResponse",
    "MEDIA_TYPE_SUBDIRS",
    "MediaType",
    "PosterSize",
    "STAGING_SUBDIR",
    "STILL_SIZE",
    "Season",
    "SeriesEpisodesResponse",
    "SettingSource",
    "SettingSpec",
    "SettingType",
    "SettingUpdate",
    "SettingValue",
    "SettingView",
    "SettingsResponse",
    "ShowBrowseResponse",
    "SuiteSettingsResponse",
    "TMDB_IMAGE_BASE_URL",
    "TorrentSearchScope",
    "TransferHashInfo",
    "TransferInfo",
    "WishlistAddRequest",
    "WishlistItem",
    "WishlistResponse",
    "poster_url",
    "still_url",
]
