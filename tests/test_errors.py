"""Tests for the shared ErrorResponse model and CommonErrorCode enum."""

from medialab_contracts import CommonErrorCode, ErrorResponse


class TestErrorResponse:
    def test_round_trips_the_structured_error_shape(self) -> None:
        payload = {"status": "error", "code": "UNAUTHORIZED", "detail": "Missing API key."}
        model = ErrorResponse(**payload)
        assert model.model_dump() == payload

    def test_code_is_a_plain_string(self) -> None:
        # code stays str on the wire so any service's ErrorCode serialises in.
        model = ErrorResponse(status="error", code="QB_UNAVAILABLE", detail="down")
        assert model.code == "QB_UNAVAILABLE"

    def test_exposes_a_json_schema_example(self) -> None:
        schema = ErrorResponse.model_json_schema()
        assert "example" in schema


class TestCommonErrorCode:
    def test_contains_the_six_shared_codes(self) -> None:
        expected = {
            "UNAUTHORIZED",
            "RATE_LIMITED",
            "INVALID_INPUT",
            "INTERNAL_ERROR",
            "PATH_NOT_FOUND",
            "PERMISSION_DENIED",
        }
        assert {c.value for c in CommonErrorCode} == expected

    def test_is_a_str_enum(self) -> None:
        assert isinstance(CommonErrorCode.UNAUTHORIZED, str)

    def test_value_matches_name(self) -> None:
        for code in CommonErrorCode:
            assert code.value == code.name
