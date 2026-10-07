"""Per-credential health: which operator-supplied key still works, reported by its owner.

Each worker checks the credentials it holds and exposes a map of these states on
its health response; the orchestrator aggregates them. The credential names equal
the answer field names in medialab-setup so a state maps to a wizard field directly.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

CREDENTIAL_TMDB_API_KEY = "tmdb_api_key"
CREDENTIAL_QB_API_KEY = "qb_api_key"
CREDENTIAL_JELLYFIN_API_KEY = "jellyfin_api_key"
CREDENTIAL_DISCORD_TOKEN = "discord_token"

CREDENTIAL_NAMES: tuple[str, ...] = (
    CREDENTIAL_TMDB_API_KEY,
    CREDENTIAL_QB_API_KEY,
    CREDENTIAL_JELLYFIN_API_KEY,
    CREDENTIAL_DISCORD_TOKEN,
)
"""Every credential a worker reports on, in display order."""


class CredentialStatus(str, Enum):
    OK = "ok"
    INVALID = "invalid"
    """The service refused the credential; the operator must replace it."""
    UNREACHABLE = "unreachable"
    """The service could not be asked; nothing is known about the credential."""
    UNKNOWN = "unknown"
    """Not checked yet."""


class CredentialState(BaseModel):
    status: CredentialStatus = CredentialStatus.UNKNOWN
    checked_at: datetime | None = None
    detail: str = ""

    @property
    def needs_operator(self) -> bool:
        return self.status is CredentialStatus.INVALID
