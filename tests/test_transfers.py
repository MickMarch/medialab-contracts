"""Tests for the shared transfer DTOs."""

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

    def test_tmdb_id_is_optional(self) -> None:
        info = TransferHashInfo(media_type="show", host_path="/media/Shows")
        assert info.tmdb_id is None
        assert info.media_type is MediaType.SHOW
