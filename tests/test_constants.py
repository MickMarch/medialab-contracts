"""Tests for the shared wire-level constants."""

from medialab_contracts import (
    API_KEY_HEADER,
    API_PREFIX,
    HEALTH_PATH,
    MEDIA_TYPE_SUBDIRS,
    STAGING_SUBDIR,
    MediaType,
)


class TestApiConstants:
    def test_prefix_is_versioned_and_rooted(self) -> None:
        assert API_PREFIX == "/api/v1"
        assert API_PREFIX.startswith("/")
        assert not API_PREFIX.endswith("/")

    def test_health_path_lives_under_the_prefix(self) -> None:
        assert HEALTH_PATH == API_PREFIX + "/health"

    def test_api_key_header_name(self) -> None:
        assert API_KEY_HEADER == "X-API-Key"


class TestMediaTypeSubdirs:
    def test_every_media_type_has_a_subdir(self) -> None:
        assert set(MEDIA_TYPE_SUBDIRS) == set(MediaType)

    def test_subdirs_are_distinct_plain_names(self) -> None:
        values = list(MEDIA_TYPE_SUBDIRS.values())
        assert len(set(values)) == len(values)
        for name in values:
            assert "/" not in name
            assert "\\" not in name

    def test_expected_names(self) -> None:
        assert MEDIA_TYPE_SUBDIRS[MediaType.MOVIE] == "Movies"
        assert MEDIA_TYPE_SUBDIRS[MediaType.SHOW] == "Shows"


class TestStagingSubdir:
    def test_is_a_plain_name_distinct_from_the_library_subdirs(self) -> None:
        assert STAGING_SUBDIR == "_incoming"
        assert "/" not in STAGING_SUBDIR and "\\" not in STAGING_SUBDIR
        assert STAGING_SUBDIR not in MEDIA_TYPE_SUBDIRS.values()
