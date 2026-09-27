"""Tests for the watchlist models."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from medialab_contracts import (
    DEFAULT_FOLLOW_RESOLUTION,
    DiscoverItem,
    FollowRequest,
    FollowStart,
    FollowStartMode,
    FollowState,
    MediaType,
    SubmissionState,
    WatchlistAddRequest,
    WatchlistItem,
    WatchlistKind,
    WatchlistResponse,
)

NOW = datetime(2026, 9, 27, tzinfo=UTC)


class TestFollowStart:
    def test_from_needs_season_and_episode(self) -> None:
        start = FollowStart(mode="from", season=2, episode=3)
        assert start.mode is FollowStartMode.FROM
        with pytest.raises(ValidationError):
            FollowStart(mode="from", season=2)

    @pytest.mark.parametrize("mode", ["new_only", "beginning"])
    def test_other_modes_reject_scope(self, mode: str) -> None:
        assert FollowStart(mode=mode).season is None
        with pytest.raises(ValidationError):
            FollowStart(mode=mode, season=1, episode=1)


class TestFollowRequest:
    def test_defaults_resolution(self) -> None:
        request = FollowRequest(start=FollowStart(mode="new_only"))
        assert request.resolution == DEFAULT_FOLLOW_RESOLUTION


class TestWatchlistItem:
    def test_saved_item_has_no_follow(self) -> None:
        item = WatchlistItem(tmdb_id=1, media_type="movie", title="Dune", added_at=NOW)
        assert item.kind is WatchlistKind.SAVED
        assert item.follow is None
        assert item.in_library is False

    def test_following_item_round_trips(self) -> None:
        item = WatchlistItem(
            tmdb_id=100088,
            media_type=MediaType.SHOW,
            kind=WatchlistKind.FOLLOWING,
            title="The Last of Us",
            added_at=NOW,
            follow=FollowState(
                start=FollowStart(mode="from", season=2, episode=1),
                followed_at=NOW,
                last_submitted="S02E05",
            ),
        )
        response = WatchlistResponse(items=[item])
        assert WatchlistResponse.model_validate_json(response.model_dump_json()) == response

    def test_add_request_needs_only_a_title(self) -> None:
        assert WatchlistAddRequest(title="Dune").overview == ""


class TestFlagsOnOtherModels:
    def test_discover_item_carries_watchlist_kind(self) -> None:
        item = DiscoverItem(tmdb_id=1, media_type="movie", title="Dune")
        assert item.on_watchlist is False
        assert item.watchlist_kind is None
        flagged = item.model_copy(
            update={"on_watchlist": True, "watchlist_kind": WatchlistKind.FOLLOWING}
        )
        assert flagged.watchlist_kind is WatchlistKind.FOLLOWING

    def test_submission_state_wire_values(self) -> None:
        assert SubmissionState.SUBMITTED.value == "submitted"
        assert SubmissionState.IGNORED.value == "ignored"
