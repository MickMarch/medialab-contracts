"""Tests for the shared transfer DTOs."""

import pytest
from pydantic import ValidationError

from medialab_contracts import MediaType, TransferHashInfo, TransferInfo


class TestTransferInfo:
    def test_parses_a_full_transfer_snapshot(self) -> None:
        info = TransferInfo(
            name="Some.Release.1080p",
            size=1_000_000,
            progress=0.5,
            hash="abc123",
            state="downloading",
            download_speed=2048,
            upload_speed=512,
            eta_seconds=300,
            save_path="/media/Movies",
        )
        assert info.progress == 0.5
        assert info.hash == "abc123"


class TestTransferHashInfo:
    def test_carries_media_type_host_path_and_tmdb_id(self) -> None:
        info = TransferHashInfo(media_type="movie", host_path="/media/Movies", tmdb_id=27205)
        assert info.media_type is MediaType.MOVIE
        assert info.host_path == "/media/Movies"
        assert info.tmdb_id == 27205

    def test_tmdb_id_is_required(self) -> None:
        with pytest.raises(ValidationError):
            TransferHashInfo(media_type="show", host_path="/media/Shows")


class TestContentPath:
    def test_defaults_to_empty_for_older_producers(self):
        info = TransferInfo(
            name="n",
            size=1,
            progress=0.5,
            hash="h",
            state="downloading",
            download_speed=0,
            upload_speed=0,
            eta_seconds=0,
            save_path="F:\Media\Movies",
        )
        assert info.content_path == ""

    def test_round_trips(self):
        info = TransferInfo(
            name="n",
            size=1,
            progress=1.0,
            hash="h",
            state="stoppedUP",
            download_speed=0,
            upload_speed=0,
            eta_seconds=0,
            save_path="F:\Media\Movies",
            content_path="F:\Media\Movies\Movie.2021.1080p",
        )
        assert TransferInfo.model_validate(info.model_dump()).content_path.endswith(
            "Movie.2021.1080p"
        )
