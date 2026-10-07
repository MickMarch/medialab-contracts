"""Tests for the credential health model."""

from datetime import UTC, datetime

from medialab_contracts import (
    CREDENTIAL_DISCORD_TOKEN,
    CREDENTIAL_JELLYFIN_API_KEY,
    CREDENTIAL_NAMES,
    CREDENTIAL_QB_API_KEY,
    CREDENTIAL_TMDB_API_KEY,
    CredentialState,
    CredentialStatus,
)


class TestCredentialState:
    def test_defaults_to_unknown_and_unchecked(self) -> None:
        state = CredentialState()
        assert state.status is CredentialStatus.UNKNOWN
        assert state.checked_at is None
        assert state.detail == ""
        assert not state.needs_operator

    def test_round_trips_through_json(self) -> None:
        state = CredentialState(
            status=CredentialStatus.INVALID,
            checked_at=datetime(2026, 10, 7, 12, 0, tzinfo=UTC),
            detail="HTTP 401",
        )
        assert CredentialState.model_validate_json(state.model_dump_json()) == state

    def test_only_invalid_needs_the_operator(self) -> None:
        for status in CredentialStatus:
            state = CredentialState(status=status)
            assert state.needs_operator is (status is CredentialStatus.INVALID)

    def test_status_wire_values_are_stable(self) -> None:
        assert [s.value for s in CredentialStatus] == ["ok", "invalid", "unreachable", "unknown"]


class TestCredentialNames:
    def test_names_are_unique_and_in_display_order(self) -> None:
        assert CREDENTIAL_NAMES == (
            CREDENTIAL_TMDB_API_KEY,
            CREDENTIAL_QB_API_KEY,
            CREDENTIAL_JELLYFIN_API_KEY,
            CREDENTIAL_DISCORD_TOKEN,
        )
        assert len(set(CREDENTIAL_NAMES)) == len(CREDENTIAL_NAMES)

    def test_names_match_the_setup_tool_answer_fields(self) -> None:
        assert CREDENTIAL_TMDB_API_KEY == "tmdb_api_key"
        assert CREDENTIAL_QB_API_KEY == "qb_api_key"
        assert CREDENTIAL_JELLYFIN_API_KEY == "jellyfin_api_key"
        assert CREDENTIAL_DISCORD_TOKEN == "discord_token"
