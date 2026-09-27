"""Tests for the shared runtime-settings models."""

import pytest
from pydantic import ValidationError

from medialab_contracts import (
    SettingSource,
    SettingSpec,
    SettingType,
    SettingView,
    SuiteSettingsResponse,
)


def _int_spec(**kw) -> SettingSpec:
    base = {
        "key": "minimum_seeders",
        "type": SettingType.INT,
        "description": "d",
        "applies": "next search",
        "min": 0,
        "max": 1000,
    }
    return SettingSpec(**{**base, **kw})


class TestSettingSpec:
    def test_int_coerces_and_bounds(self) -> None:
        spec = _int_spec()
        assert spec.coerce("15") == 15
        assert spec.coerce(0) == 0
        with pytest.raises(ValueError, match="at least"):
            spec.coerce(-1)
        with pytest.raises(ValueError, match="at most"):
            spec.coerce(1001)
        with pytest.raises(ValueError, match="integer"):
            spec.coerce("ten")
        with pytest.raises(ValueError, match="integer"):
            spec.coerce(True)

    def test_choice_is_case_insensitive_and_closed(self) -> None:
        spec = SettingSpec(
            key="audio_language_filter",
            type=SettingType.CHOICE,
            description="d",
            applies="next search",
            choices=["lenient", "strict", "off"],
        )
        assert spec.coerce(" Strict ") == "strict"
        with pytest.raises(ValueError, match="one of"):
            spec.coerce("maybe")

    def test_str_strips_and_rejects_empty(self) -> None:
        spec = SettingSpec(
            key="target_language", type=SettingType.STR, description="d", applies="next search"
        )
        assert spec.coerce(" en ") == "en"
        with pytest.raises(ValueError, match="empty"):
            spec.coerce("  ")

    def test_choice_needs_choices_and_only_int_has_bounds(self) -> None:
        with pytest.raises(ValidationError):
            SettingSpec(key="k", type=SettingType.CHOICE, description="d", applies="a")
        with pytest.raises(ValidationError):
            SettingSpec(key="k", type=SettingType.STR, description="d", applies="a", min=1)


class TestSettingView:
    def test_round_trip(self) -> None:
        view = SettingView(
            key="minimum_seeders",
            value=15,
            default=10,
            source="override",
            type="int",
            description="d",
            applies="next search",
            min=0,
            max=1000,
        )
        assert view.source is SettingSource.OVERRIDE
        assert SettingView.model_validate(view.model_dump()) == view

    def test_suite_response_groups_by_service(self) -> None:
        body = SuiteSettingsResponse(status="success", services={"torrent-downloader": []})
        assert list(body.services) == ["torrent-downloader"]
