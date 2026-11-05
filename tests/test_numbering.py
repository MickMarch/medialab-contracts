"""Tests for the episode numbering models."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from medialab_contracts import (
    EpisodeGroupInfo,
    EpisodeGroupsResponse,
    EpisodeNumber,
    EpisodeState,
    FollowRequest,
    FollowStart,
    FollowState,
    NumberingMode,
    ShowNumbering,
)

GROUP_ID = "64a3fc4fe9da6900ae2fa807"
START = FollowStart(mode="from", season=1, episode=48)


def _numbering() -> ShowNumbering:
    return ShowNumbering(
        tmdb_id=95479,
        group_id=GROUP_ID,
        group_name="Seasons",
        episodes=[
            EpisodeNumber(season=1, episode=24, release_season=1, release_episode=24, absolute=24),
            EpisodeNumber(season=1, episode=48, release_season=3, release_episode=1, absolute=48),
            EpisodeNumber(season=1, episode=49, release_season=3, release_episode=2, absolute=49),
        ],
    )


class TestNumberingMode:
    def test_wire_values(self) -> None:
        assert [m.value for m in NumberingMode] == ["auto", "tmdb", "group"]


class TestShowNumbering:
    def test_round_trip(self) -> None:
        numbering = _numbering()
        assert ShowNumbering.model_validate_json(numbering.model_dump_json()) == numbering

    def test_lookups(self) -> None:
        numbering = _numbering()
        assert numbering.for_canonical(1, 48) == numbering.episodes[1]
        assert numbering.for_canonical(2, 1) is None
        assert numbering.for_release(3, 2) == numbering.episodes[2]
        assert numbering.for_absolute(48) == numbering.episodes[1]
        assert numbering.for_absolute(99) is None

    def test_release_season_members(self) -> None:
        assert [e.episode for e in _numbering().release_season_episodes(3)] == [48, 49]

    def test_identity_is_tmdb(self) -> None:
        identity = ShowNumbering(tmdb_id=1, episodes=[])
        assert identity.group_id is None
        assert not identity.is_mapped


class TestEpisodeGroups:
    def test_round_trip(self) -> None:
        response = EpisodeGroupsResponse(
            tmdb_id=95479,
            groups=[EpisodeGroupInfo(id=GROUP_ID, name="Seasons", group_count=4, episode_count=64)],
            auto_group_id=GROUP_ID,
        )
        assert EpisodeGroupsResponse.model_validate_json(response.model_dump_json()) == response


class TestFollowNumbering:
    def test_defaults_are_auto_without_audio_preference(self) -> None:
        request = FollowRequest(start=START)
        assert request.numbering is NumberingMode.AUTO
        assert request.episode_group_id is None
        assert request.prefer_multi_audio is False

    def test_group_mode_needs_a_group_id(self) -> None:
        with pytest.raises(ValidationError):
            FollowRequest(start=START, numbering="group")
        assert FollowRequest(start=START, numbering="group", episode_group_id=GROUP_ID)

    @pytest.mark.parametrize("mode", ["auto", "tmdb"])
    def test_other_modes_reject_a_group_id(self, mode: str) -> None:
        with pytest.raises(ValidationError):
            FollowRequest(start=START, numbering=mode, episode_group_id=GROUP_ID)

    def test_state_carries_the_options(self) -> None:
        state = FollowState(
            start=START,
            followed_at=datetime(2026, 11, 5, tzinfo=UTC),
            numbering="group",
            episode_group_id=GROUP_ID,
            prefer_multi_audio=True,
        )
        assert FollowState.model_validate_json(state.model_dump_json()) == state


class TestEpisodeStateReleaseCode:
    def test_release_numbers_default_to_none(self) -> None:
        state = EpisodeState(season=1, episode=48)
        assert state.release_season is None and state.release_episode is None
