"""Progress of a torrent search in flight, owned by torrent-downloader, relayed
by the orchestrator gateway, rendered by the web UI.

A search runs one qBittorrent job per pattern; the unit of progress is the
pattern, since which plugins finished is not on the wire.
"""

from enum import Enum

from pydantic import BaseModel, Field, model_validator


class SearchProgressState(str, Enum):
    IDLE = "idle"
    """No pattern of this search has started."""
    RUNNING = "running"
    """At least one pattern is in flight."""
    DONE = "done"
    """Every pattern is cached or finished."""


class TorrentSearchProgress(BaseModel):
    state: SearchProgressState
    patterns_total: int = Field(ge=0)
    patterns_done: int = Field(ge=0)
    results_so_far: int = Field(ge=0)
    elapsed_seconds: float = Field(ge=0.0)
    """Of the longest-running pattern still in flight; 0 when none is."""
    timeout_seconds: int = Field(ge=0)

    @model_validator(mode="after")
    def _done_within_total(self) -> "TorrentSearchProgress":
        if self.patterns_done > self.patterns_total:
            raise ValueError("patterns_done must not exceed patterns_total.")
        return self

    @classmethod
    def idle(cls, *, patterns_total: int, timeout_seconds: int) -> "TorrentSearchProgress":
        return cls(
            state=SearchProgressState.IDLE,
            patterns_total=patterns_total,
            patterns_done=0,
            results_so_far=0,
            elapsed_seconds=0.0,
            timeout_seconds=timeout_seconds,
        )

    @property
    def fraction(self) -> float:
        """How far along the search is, 0 to 1: finished patterns count whole,
        the in-flight ones count by elapsed time over the timeout. Within one
        pattern time is the only signal there is."""
        if self.patterns_total == 0:
            return 0.0
        if self.state is SearchProgressState.DONE:
            return 1.0
        in_flight = self.patterns_total - self.patterns_done
        if in_flight == 0 or self.timeout_seconds == 0:
            return self.patterns_done / self.patterns_total
        time_fraction = min(self.elapsed_seconds / self.timeout_seconds, 1.0)
        return (self.patterns_done + time_fraction) / self.patterns_total
