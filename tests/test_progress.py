"""Tests for the job progress model."""

import pytest
from pydantic import ValidationError

from medialab_contracts import ETA_UNKNOWN_SECONDS, JobProgress


class TestJobProgress:
    def test_round_trips_through_json(self) -> None:
        progress = JobProgress(
            progress=0.42, download_speed=3_200_000, eta_seconds=720, state="downloading"
        )
        assert JobProgress.model_validate_json(progress.model_dump_json()) == progress

    def test_eta_may_be_unknown(self) -> None:
        progress = JobProgress(progress=0.0, download_speed=0, state="metaDL")
        assert progress.eta_seconds is None

    def test_progress_is_a_fraction(self) -> None:
        with pytest.raises(ValidationError):
            JobProgress(progress=1.5, download_speed=0, state="downloading")

    def test_unknown_eta_sentinel_matches_qbittorrent(self) -> None:
        assert ETA_UNKNOWN_SECONDS == 100 * 24 * 60 * 60
