"""Tests for package settings."""

from pfmsoft.eve_snippets import __app_name__, __url__, __version__
from pfmsoft.eve_snippets.settings import USER_AGENT


def test_user_agent_uses_package_metadata() -> None:
    """The user agent should be composed from the package metadata."""
    assert USER_AGENT == f"{__app_name__}/{__version__} ({__url__})"
