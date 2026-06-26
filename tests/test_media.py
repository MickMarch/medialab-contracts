"""Tests for the shared MediaType enum."""

import pytest
from pydantic import BaseModel, ValidationError

from medialab_contracts import MediaType


class TestMediaType:
    def test_members_have_expected_wire_values(self) -> None:
        assert MediaType.MOVIE.value == "movie"
        assert MediaType.SHOW.value == "show"

    def test_is_a_str_enum(self) -> None:
        assert isinstance(MediaType.MOVIE, str)

    def test_constructed_from_wire_value(self) -> None:
        assert MediaType("movie") is MediaType.MOVIE
        assert MediaType("show") is MediaType.SHOW

    def test_rejects_unknown_value(self) -> None:
        with pytest.raises(ValueError):
            MediaType("episode")

    def test_validates_inside_a_model_from_wire_value(self) -> None:
        class Wrapper(BaseModel):
            media_type: MediaType

        assert Wrapper(media_type="movie").media_type is MediaType.MOVIE

    def test_model_rejects_invalid_wire_value(self) -> None:
        class Wrapper(BaseModel):
            media_type: MediaType

        with pytest.raises(ValidationError):
            Wrapper(media_type="invalid")
