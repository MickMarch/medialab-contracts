"""Tests for the trailer models."""

from datetime import UTC, datetime

from medialab_contracts import (
    YOUTUBE_EMBED_BASE_URL,
    Video,
    VideosResponse,
    VideoType,
    youtube_embed_url,
)


class TestVideo:
    def test_round_trips_through_json(self) -> None:
        video = Video(
            key="_zHPsmXCjB0",
            name="Season 2 Official Trailer",
            type=VideoType.TRAILER,
            official=True,
            published_at=datetime(2025, 3, 1, tzinfo=UTC),
            language="en",
        )
        response = VideosResponse(videos=[video])
        assert VideosResponse.model_validate_json(response.model_dump_json()) == response

    def test_wire_values(self) -> None:
        assert VideoType.TRAILER.value == "trailer"
        assert VideoType.TEASER.value == "teaser"

    def test_only_key_and_type_are_required(self) -> None:
        video = Video(key="abc", type="teaser")
        assert video.official is False
        assert video.published_at is None


class TestEmbedUrl:
    def test_uses_the_nocookie_host(self) -> None:
        assert youtube_embed_url("abc") == f"{YOUTUBE_EMBED_BASE_URL}/abc"
        assert "youtube-nocookie.com" in YOUTUBE_EMBED_BASE_URL
