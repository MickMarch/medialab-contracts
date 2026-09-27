"""Runtime settings, owned by each service, relayed by the gateway, rendered by
the clients. A service declares its tunables as ``SettingSpec`` entries; the
wire shape is ``SettingView``."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator

SettingValue = int | str


class SettingType(str, Enum):
    INT = "int"
    STR = "str"
    CHOICE = "choice"


class SettingSource(str, Enum):
    """Where the effective value comes from."""

    DEFAULT = "default"
    ENV = "env"
    OVERRIDE = "override"


class SettingSpec(BaseModel):
    """One tunable: its key on the owning service's config, its type and
    bounds, and when a change takes effect."""

    key: str
    type: SettingType
    description: str
    applies: str
    choices: list[str] | None = None
    min: int | None = None
    max: int | None = None

    @model_validator(mode="after")
    def _validate_shape(self) -> "SettingSpec":
        if self.type is SettingType.CHOICE and not self.choices:
            raise ValueError("A choice setting needs choices.")
        if self.type is not SettingType.INT and (self.min is not None or self.max is not None):
            raise ValueError("Only an int setting has bounds.")
        return self

    def coerce(self, raw: Any) -> SettingValue:
        """The validated value for ``raw``, or ``ValueError`` with the reason."""
        if self.type is SettingType.INT:
            if isinstance(raw, bool):
                raise ValueError(f"{self.key} must be an integer.")
            try:
                value = int(raw)
            except (TypeError, ValueError) as error:
                raise ValueError(f"{self.key} must be an integer.") from error
            if self.min is not None and value < self.min:
                raise ValueError(f"{self.key} must be at least {self.min}.")
            if self.max is not None and value > self.max:
                raise ValueError(f"{self.key} must be at most {self.max}.")
            return value
        text = str(raw).strip()
        if not text:
            raise ValueError(f"{self.key} must not be empty.")
        if self.type is SettingType.CHOICE:
            lowered = text.lower()
            if lowered not in (self.choices or []):
                raise ValueError(f"{self.key} must be one of: {', '.join(self.choices or [])}.")
            return lowered
        return text


class SettingView(BaseModel):
    """A setting as a client sees it: the spec plus the effective value."""

    key: str
    value: SettingValue
    default: SettingValue
    source: SettingSource
    type: SettingType
    description: str
    applies: str
    choices: list[str] | None = None
    min: int | None = None
    max: int | None = None


class SettingUpdate(BaseModel):
    """Body of ``PUT /settings/{key}``."""

    value: SettingValue


class SettingsResponse(BaseModel):
    """Body of a service's ``GET /settings``."""

    status: str
    settings: list[SettingView] = Field(default_factory=list)


class SuiteSettingsResponse(BaseModel):
    """Body of the gateway's ``GET /settings``: every service's settings keyed
    by service name."""

    status: str
    services: dict[str, list[SettingView]] = Field(default_factory=dict)
