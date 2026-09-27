"""Tests for the show browsing models."""

from datetime import date

from medialab_contracts import (
    STILL_SIZE,
    TMDB_IMAGE_BASE_URL,
    Episode,
    EpisodeKey,
    EpisodeState,
    LibraryEpisodesResponse,
    Season,
    SeriesEpisodesResponse,
    ShowBrowseResponse,
    still_url,
)


def _episode(**overrides: object) -> Episode:
    fields: dict[str, object] = {
        "season": 2,
        "episode": 5,
        "title": "Feel Her Love",
        "air_date": date(2025, 5, 11),
        "overview": "...",
        "still_path": "/abc.jpg",
        "runtime_minutes": 58,
    }
    fields.update(overrides)
    return Episode.model_validate(fields)


class TestEpisode:
    def test_round_trips_through_json(self) -> None:
        episode = _episode()
        assert Episode.model_validate_json(episode.model_dump_json()) == episode

    def test_only_numbers_are_required(self) -> None:
        episode = Episode(season=1, episode=1)
        assert episode.air_date is None
        assert episode.still_path is None
        assert episode.runtime_minutes is None


class TestSeriesEpisodesResponse:
    def test_round_trips_through_json(self) -> None:
        response = SeriesEpisodesResponse(
            tmdb_id=100088,
            seasons=[Season(season=1, name="Season 1", episode_count=9)],
            episodes=[_episode(season=1, episode=1)],
            next_episode=_episode(season=1, episode=2, air_date=None),
            status="Returning Series",
        )
        assert SeriesEpisodesResponse.model_validate_json(response.model_dump_json()) == response


class TestLibraryEpisodesResponse:
    def test_holds_episode_keys(self) -> None:
        response = LibraryEpisodesResponse(tmdb_id=1, episodes=[EpisodeKey(season=1, episode=3)])
        assert response.episodes[0].season == 1
        assert response.episodes[0].episode == 3


class TestShowBrowseResponse:
    def test_episode_state_flags_default_to_false(self) -> None:
        state = EpisodeState(season=1, episode=1)
        assert state.aired is False
        assert state.in_library is False
        assert state.queued_job_id is None

    def test_round_trips_through_json(self) -> None:
        response = ShowBrowseResponse(
            tmdb_id=1,
            title="The Last of Us",
            year="2023",
            seasons=[Season(season=1)],
            episodes=[EpisodeState(season=1, episode=1, aired=True, in_library=True)],
        )
        assert ShowBrowseResponse.model_validate_json(response.model_dump_json()) == response


class TestStillUrl:
    def test_joins_base_size_and_path(self) -> None:
        assert still_url("/abc.jpg") == f"{TMDB_IMAGE_BASE_URL}/{STILL_SIZE}/abc.jpg"

    def test_no_path_gives_none(self) -> None:
        assert still_url(None) is None
