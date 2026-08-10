"""Tests for timestamp mixins."""

import pytest

from pfmsoft.eve_snippets.whenever.timestamp import Timestamped


def test_timestamped_parses_timestamp_into_instant() -> None:
    """The mixin should expose the timestamp as a parsed Instant."""
    timestamped = Timestamped(timestamp="2026-08-10T12:34:56Z")

    assert timestamped.timestamp_instant.format_iso() == "2026-08-10T12:34:56Z"


def test_timestamped_requires_keyword_only_arguments() -> None:
    """The dataclass should reject positional construction."""
    with pytest.raises(TypeError, match="takes 1 positional argument but 2 were given"):
        Timestamped("2026-08-10T12:34:56Z")
