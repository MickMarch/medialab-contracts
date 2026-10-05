"""Tests for the torrent search progress model."""

import pytest
from pydantic import ValidationError

from medialab_contracts import SearchProgressState, TorrentSearchProgress


class TestTorrentSearchProgress:
    def test_round_trips_through_json(self) -> None:
        progress = TorrentSearchProgress(
            state="running",
            patterns_total=3,
            patterns_done=1,
            results_so_far=57,
            elapsed_seconds=4.5,
            timeout_seconds=15,
        )
        again = TorrentSearchProgress.model_validate_json(progress.model_dump_json())
        assert again == progress
        assert again.state is SearchProgressState.RUNNING

    def test_states(self) -> None:
        assert {s.value for s in SearchProgressState} == {"idle", "running", "done"}

    def test_idle_search_has_nothing_started(self) -> None:
        progress = TorrentSearchProgress.idle(patterns_total=2, timeout_seconds=15)
        assert progress.state is SearchProgressState.IDLE
        assert progress.patterns_done == 0
        assert progress.results_so_far == 0
        assert progress.elapsed_seconds == 0.0

    def test_done_cannot_exceed_total(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchProgress(
                state="done",
                patterns_total=1,
                patterns_done=2,
                results_so_far=0,
                elapsed_seconds=1.0,
                timeout_seconds=15,
            )

    def test_counts_are_non_negative(self) -> None:
        with pytest.raises(ValidationError):
            TorrentSearchProgress(
                state="idle",
                patterns_total=1,
                patterns_done=0,
                results_so_far=-1,
                elapsed_seconds=0.0,
                timeout_seconds=15,
            )

    def test_fraction_blends_done_patterns_with_elapsed_time(self) -> None:
        # One of two patterns done; the other a third of the way to timeout.
        progress = TorrentSearchProgress(
            state="running",
            patterns_total=2,
            patterns_done=1,
            results_so_far=3,
            elapsed_seconds=5.0,
            timeout_seconds=15,
        )
        assert progress.fraction == pytest.approx((1 + 5 / 15) / 2)

    def test_fraction_is_one_when_done_and_zero_when_nothing_to_do(self) -> None:
        done = TorrentSearchProgress(
            state="done",
            patterns_total=2,
            patterns_done=2,
            results_so_far=9,
            elapsed_seconds=30.0,
            timeout_seconds=15,
        )
        assert done.fraction == 1.0
        assert TorrentSearchProgress.idle(patterns_total=0, timeout_seconds=15).fraction == 0.0
