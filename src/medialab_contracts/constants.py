"""Wire-level constants every medialab HTTP service and client must agree on.

Declared once here so a route prefix, header name or directory name cannot
drift between the service that serves it and the clients that call it.
"""

from medialab_contracts.media import MediaType

API_PREFIX = "/api/v1"
"""Path prefix under which every service mounts its routers."""

API_KEY_HEADER = "X-API-Key"
"""Header carrying the static inter-service API key."""

HEALTH_PATH = f"{API_PREFIX}/health"
"""The one unauthenticated endpoint on every service."""

STAGING_SUBDIR = "_incoming"
"""Subdirectory of the media root where downloads land before placement.

qBittorrent saves under ``<root>/_incoming/<Movies|Shows>``; the orchestrator
renames into ``<root>/<Movies|Shows>`` on completion. It sits beside the
Jellyfin library roots, never inside one, so Jellyfin never indexes a raw
download. Both services must agree on the name, hence a contract.
"""

MEDIA_TYPE_SUBDIRS: dict[MediaType, str] = {
    MediaType.MOVIE: "Movies",
    MediaType.SHOW: "Shows",
}
"""Subdirectory of the media root that holds each media type.

torrent-downloader uses it to build the qBittorrent save path; the
orchestrator uses it to locate the finished download for renaming. Both must
agree or completed downloads are never found.
"""
