"""Episode numbering: how one show's TMDB default numbering maps to the
release-season and absolute numbers release names use, from a TMDB episode
group. Owned by torrent-downloader; the orchestrator searches, picks and
renames through it. Spec: ``docs/specs/anime-numbering.md``."""

from enum import Enum

from pydantic import BaseModel


class NumberingMode(str, Enum):
    AUTO = "auto"
    """The first TMDB episode group that qualifies, else TMDB numbering."""
    TMDB = "tmdb"
    """TMDB default numbering only (the identity map)."""
    GROUP = "group"
    """One chosen TMDB episode group."""


class EpisodeNumber(BaseModel):
    """One regular episode under every numbering."""

    season: int
    episode: int
    """TMDB default (canonical) numbering: library layout and follow start."""
    release_season: int
    release_episode: int
    absolute: int
    """Position across the non-special groups, from 1."""


class ShowNumbering(BaseModel):
    """A show's numbering map. ``group_id`` None is TMDB numbering, where the
    release numbers equal the canonical ones."""

    tmdb_id: int
    group_id: str | None = None
    group_name: str = ""
    episodes: list[EpisodeNumber]

    @property
    def is_mapped(self) -> bool:
        return self.group_id is not None

    def for_canonical(self, season: int, episode: int) -> EpisodeNumber | None:
        return next((e for e in self.episodes if (e.season, e.episode) == (season, episode)), None)

    def for_release(self, season: int, episode: int) -> EpisodeNumber | None:
        return next(
            (
                e
                for e in self.episodes
                if (e.release_season, e.release_episode) == (season, episode)
            ),
            None,
        )

    def for_absolute(self, absolute: int) -> EpisodeNumber | None:
        return next((e for e in self.episodes if e.absolute == absolute), None)

    def release_season_episodes(self, release_season: int) -> list[EpisodeNumber]:
        return [e for e in self.episodes if e.release_season == release_season]


class EpisodeGroupInfo(BaseModel):
    """One TMDB episode group of type TV, as the follow form lists it."""

    id: str
    name: str
    group_count: int
    episode_count: int


class EpisodeGroupsResponse(BaseModel):
    """Body of ``GET /search/tmdb/show/{tmdb_id}/episode-groups``."""

    tmdb_id: int
    groups: list[EpisodeGroupInfo]
    auto_group_id: str | None = None
    """The group auto numbering resolves to; None means TMDB numbering."""
