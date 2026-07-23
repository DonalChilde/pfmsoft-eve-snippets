"""Mixin classes for timestamp handling."""

from dataclasses import dataclass
from typing import Protocol

from whenever import Instant


class TimestampInstant(Protocol):
    def timestamp_instant(self) -> Instant:
        """Return the timestamp as an Instant."""
        ...


@dataclass(kw_only=True)
class Timestamp(TimestampInstant):
    timestamp: int

    def timestamp_instant(self) -> Instant:
        """Return the timestamp as an Instant."""
        return Instant.from_timestamp(self.timestamp)


@dataclass(kw_only=True)
class TimestampNanos(TimestampInstant):
    timestamp_nanos: int

    def timestamp_instant(self) -> Instant:
        """Return the timestamp as an Instant."""
        return Instant.from_timestamp_nanos(self.timestamp_nanos)


@dataclass(kw_only=True)
class TimestampMillis(TimestampInstant):
    timestamp_millis: int

    def timestamp_instant(self) -> Instant:
        """Return the timestamp as an Instant."""
        return Instant.from_timestamp_millis(self.timestamp_millis)
