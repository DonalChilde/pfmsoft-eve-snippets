"""Mixin classes for timestamp handling."""

from dataclasses import dataclass
from typing import Protocol

from whenever import Instant


class TimestampInstant(Protocol):
    @property
    def timestamp_instant(self) -> Instant:
        """Return the timestamp as an Instant."""
        ...


@dataclass(slots=True, kw_only=True)
class Timestamped(TimestampInstant):
    timestamp: str
    """A timestamp in ISO 8601 format."""

    @property
    def timestamp_instant(self) -> Instant:
        """Return the timestamp as an Instant."""
        return Instant.parse_iso(self.timestamp)
