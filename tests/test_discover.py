"""Tests for the discover, genre, wishlist and library-id models."""

from datetime import UTC, datetime

from medialab_contracts import (
    TMDB_IMAGE_BASE_URL,
    DiscoverItem,
    DiscoverResponse,
    Genre,
    GenresResponse,
    LibraryTmdbIdsResponse,
    MediaType,
    PosterSize,
    WishlistAddRequest,
    WishlistItem,
    WishlistResponse,
    poster_url,
)


def _item(**overrides: object) -> DiscoverItem:
    fields: dict[str, object] = {
        "tmdb_id": 438631,
        "media_type": "movie",
        "title": "Dune",
        "year": "2021",
        "overview": "Spice.",
        "vote_average": 7.8,
        "poster_path": "/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
    }
    fields.update(overrides)
    return DiscoverItem.model_validate(fields)


class TestDiscoverItem:
    def test_flags_default_to_false(self) -> None:
        item = _item()
        assert item.media_type is MediaType.MOVIE
        assert item.on_wishlist is False
        assert item.in_library is False

    def test_year_and_poster_are_optional(self) -> None:
        item = _item(year=None, poster_path=None)
        assert item.year is None
        assert item.poster_path is None

    def test_round_trips_through_json(self) -> None:
        item = _item(media_type="show", on_wishlist=True, in_library=True)
        assert DiscoverItem.model_validate_json(item.model_dump_json()) == item


class TestDiscoverResponse:
    def test_round_trips_through_json(self) -> None:
        response = DiscoverResponse(
            items=[_item()],
            page=1,
            total_pages=500,
            cached_at=datetime(2026, 9, 27, tzinfo=UTC),
        )
        assert DiscoverResponse.model_validate_json(response.model_dump_json()) == response


class TestGenres:
    def test_genres_response_holds_id_and_name(self) -> None:
        response = GenresResponse(genres=[Genre(id=878, name="Science Fiction")])
        assert response.genres[0].id == 878
        assert response.genres[0].name == "Science Fiction"


class TestWishlist:
    def test_item_round_trips_and_defaults_in_library(self) -> None:
        item = WishlistItem(
            tmdb_id=1399,
            media_type=MediaType.SHOW,
            title="Game of Thrones",
            year="2011",
            poster_path=None,
            overview="",
            added_at=datetime(2026, 9, 27, tzinfo=UTC),
        )
        assert item.in_library is False
        response = WishlistResponse(items=[item])
        assert WishlistResponse.model_validate_json(response.model_dump_json()) == response


class TestWishlistAddRequest:
    def test_only_title_is_required(self) -> None:
        body = WishlistAddRequest(title="Dune")
        assert body.year is None
        assert body.poster_path is None
        assert body.overview == ""


class TestLibraryTmdbIds:
    def test_holds_media_type_and_ids(self) -> None:
        response = LibraryTmdbIdsResponse(media_type="movie", tmdb_ids=[1, 2])
        assert response.media_type is MediaType.MOVIE
        assert response.tmdb_ids == [1, 2]


class TestPosterUrl:
    def test_joins_base_size_and_path(self) -> None:
        url = poster_url("/abc.jpg", PosterSize.GRID)
        assert url == f"{TMDB_IMAGE_BASE_URL}/{PosterSize.GRID.value}/abc.jpg"

    def test_no_path_gives_none(self) -> None:
        assert poster_url(None, PosterSize.THUMBNAIL) is None
