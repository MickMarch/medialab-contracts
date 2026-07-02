"""Tests for the shared torrent search scope model."""

import pytest
from pydantic import ValidationError

from medialab_contracts import MediaType, TorrentSearchScope


class TestTorrentSearchScope:
    def test_movie_scope_has_no_season_or_episode(self) -> None:
        scope = TorrentSearchScope(media_type="movie")
        assert scope.media_type is MediaType.MOVIE
        assert scope.season is None
        assert scope.episode is None

    def test_whole_series_scope_has_no_season(self) -> None:
        scope = TorrentSearchScope(media_type="show")
        assert scope.media_type is MediaType.SHOW
        assert scope.season is None
        assert scope.episode is None

    def test_season_scope_parses(self) -> None:
        scope = TorrentSearchScope(media_type="show", season=2)
        assert scope.season == 2
        assert scope.episode is None

    def test_episode_scope_parses(self) -> None:
        scope = TorrentSearchScope(media_type="show", season=2, episode=5)
        assert scope.season == 2
        assert scope.episode == 5

    def test_movie_with_season_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchScope(media_type="movie", season=1)

    def test_movie_with_episode_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchScope(media_type="movie", episode=1)

    def test_orphan_episode_without_season_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchScope(media_type="show", episode=5)

    def test_season_below_one_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchScope(media_type="show", season=0)

    def test_episode_below_one_is_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchScope(media_type="show", season=1, episode=0)
