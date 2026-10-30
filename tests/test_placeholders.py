"""Tests for the Jellyfin Discover placeholder contracts."""

import pytest
from pydantic import ValidationError

from medialab_contracts import (
    DISCOVER_CLIP_FILENAME,
    DISCOVER_CLIP_SUBDIR,
    DISCOVER_LIBRARY_NAMES,
    MEDIA_TYPE_SUBDIRS,
    PLACEHOLDER_TITLE_SEPARATOR,
    PLACEHOLDER_TITLE_SUFFIXES,
    JellyfinRequestEvent,
    MediaType,
    PlaceholderState,
    placeholder_title,
)

TMDB_ID = 238


class TestPlaceholderState:
    def test_wire_values(self) -> None:
        assert {state.value for state in PlaceholderState} == {
            "available",
            "requested",
            "downloading",
            "not_found",
        }

    def test_every_state_has_a_suffix_entry(self) -> None:
        assert set(PLACEHOLDER_TITLE_SUFFIXES) == set(PlaceholderState)

    def test_only_available_has_no_suffix(self) -> None:
        assert PLACEHOLDER_TITLE_SUFFIXES[PlaceholderState.AVAILABLE] is None
        others = [s for s in PlaceholderState if s is not PlaceholderState.AVAILABLE]
        assert all(PLACEHOLDER_TITLE_SUFFIXES[s] for s in others)


class TestPlaceholderTitle:
    def test_available_is_the_plain_title(self) -> None:
        assert placeholder_title("The Godfather", PlaceholderState.AVAILABLE) == "The Godfather"

    def test_other_states_append_the_suffix(self) -> None:
        title = placeholder_title("Severance", PlaceholderState.NOT_FOUND)
        assert title == f"Severance{PLACEHOLDER_TITLE_SEPARATOR}Not found yet"

    def test_requested_suffix(self) -> None:
        assert placeholder_title("Dune", PlaceholderState.REQUESTED) == "Dune - Requested"


class TestDiscoverLayout:
    def test_every_media_type_has_a_library_name(self) -> None:
        assert set(DISCOVER_LIBRARY_NAMES) == set(MediaType)

    def test_library_names_are_distinct(self) -> None:
        names = list(DISCOVER_LIBRARY_NAMES.values())
        assert len(set(names)) == len(names)

    def test_clip_subdir_is_a_plain_name_outside_the_library_roots(self) -> None:
        assert "/" not in DISCOVER_CLIP_SUBDIR and "\\" not in DISCOVER_CLIP_SUBDIR
        assert DISCOVER_CLIP_SUBDIR not in MEDIA_TYPE_SUBDIRS.values()

    def test_clip_is_an_mp4(self) -> None:
        assert DISCOVER_CLIP_FILENAME.endswith(".mp4")


class TestJellyfinRequestEvent:
    def test_parses_a_webhook_template_payload(self) -> None:
        """Webhook plugin template values arrive as strings, Jellyfin item types and all."""
        event = JellyfinRequestEvent.model_validate(
            {
                "jellyfin_user_id": "4b1c",
                "item_id": "4bb025f4",
                "item_type": "Movie",
                "tmdb_id": str(TMDB_ID),
                "is_favorite": "True",
            }
        )
        assert event.media_type is MediaType.MOVIE
        assert event.tmdb_id == TMDB_ID
        assert event.is_favorite is True

    def test_series_maps_to_show(self) -> None:
        event = JellyfinRequestEvent(
            jellyfin_user_id="u", item_id="i", item_type="Series", tmdb_id=1, is_favorite=False
        )
        assert event.media_type is MediaType.SHOW

    def test_accepts_contract_media_type_values(self) -> None:
        event = JellyfinRequestEvent(
            jellyfin_user_id="u", item_id="i", item_type="show", tmdb_id=1, is_favorite=True
        )
        assert event.media_type is MediaType.SHOW

    @pytest.mark.parametrize("item_type", ["Episode", "Season", ""])
    def test_rejects_other_item_types(self, item_type: str) -> None:
        with pytest.raises(ValidationError):
            JellyfinRequestEvent(
                jellyfin_user_id="u", item_id="i", item_type=item_type, tmdb_id=1, is_favorite=True
            )

    def test_round_trips_with_contract_values(self) -> None:
        event = JellyfinRequestEvent(
            jellyfin_user_id="u", item_id="i", item_type="Movie", tmdb_id=1, is_favorite=True
        )
        dumped = event.model_dump(mode="json", by_alias=True)
        assert dumped["item_type"] == "movie"
        assert JellyfinRequestEvent.model_validate(dumped) == event
