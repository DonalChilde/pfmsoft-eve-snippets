"""Tests for EVE downtime date helpers."""

import pytest
from whenever import Instant

from pfmsoft.eve_snippets.eve import eve_dates


def test_downtime_bracket_returns_previous_and_next_downtime() -> None:
    """Downtime brackets should straddle 11:00 UTC for the given day."""
    instant = Instant("2026-07-20T10:30:00Z")

    previous_dt, next_dt = eve_dates.downtime_bracket(instant)

    assert previous_dt.format_iso() == "2026-07-19T11:00:00Z"
    assert next_dt.format_iso() == "2026-07-20T11:00:00Z"


def test_downtime_bracket_handles_exact_downtime_boundary() -> None:
    """At the downtime boundary, the previous downtime should be the same instant."""
    instant = Instant("2026-07-20T11:00:00Z")

    previous_dt, next_dt = eve_dates.downtime_bracket(instant)

    assert previous_dt.format_iso() == "2026-07-20T11:00:00Z"
    assert next_dt.format_iso() == "2026-07-21T11:00:00Z"


def test_previous_and_next_downtime_delegate_to_bracket() -> None:
    """The directional helpers should return the matching side of the bracket."""
    instant = Instant("2026-07-20T12:00:00Z")

    assert eve_dates.previous_downtime(instant).format_iso() == "2026-07-20T11:00:00Z"
    assert eve_dates.next_downtime(instant).format_iso() == "2026-07-21T11:00:00Z"


def test_previous_and_next_downtime_default_to_current_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The optional instant should default to Instant.now()."""
    instant = Instant("2026-07-20T12:00:00Z")

    class FakeInstant:
        @staticmethod
        def now() -> Instant:
            return instant

        def __new__(cls, value: str) -> Instant:
            return Instant(value)

    monkeypatch.setattr(eve_dates, "Instant", FakeInstant)

    assert eve_dates.previous_downtime().format_iso() == "2026-07-20T11:00:00Z"
    assert eve_dates.next_downtime().format_iso() == "2026-07-21T11:00:00Z"


def test_latest_schema_date_uses_previous_downtime() -> None:
    """The latest schema date should be one day before the previous downtime."""
    previous = Instant("2026-07-20T11:00:00Z")
    original_previous_downtime = eve_dates.previous_downtime

    try:
        eve_dates.previous_downtime = lambda instant=None: previous

        assert eve_dates.latest_schema_date() == "2026-07-19"
    finally:
        eve_dates.previous_downtime = original_previous_downtime
