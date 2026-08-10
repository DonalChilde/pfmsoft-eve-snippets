"""Tests for Typer output helpers."""

from pathlib import Path

import pytest

from pfmsoft.eve_snippets.typer import output


class RecordingConsole:
    """Capture console output for assertions."""

    def __init__(self) -> None:
        """Initialize an empty message buffer."""
        self.messages: list[str] = []

    def print(self, message: str) -> None:
        """Record a printed message."""
        self.messages.append(message)


def test_output_to_stdout_or_file_writes_to_stdout_when_path_is_dash(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A dash path should print the payload and skip file writing."""
    console = RecordingConsole()

    def fail_save_text_file(**kwargs: object) -> Path:
        raise AssertionError("save_text_file should not be called for stdout output")

    monkeypatch.setattr(output, "save_text_file", fail_save_text_file)

    output.output_to_stdout_or_file(
        data_string="hello world",
        filepath=Path("-"),
        overwrite=False,
        messenger=console,
    )

    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
    assert console.messages == []


def test_output_to_stdout_or_file_saves_file_and_reports_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """File output should call the save helper and report the written path."""
    console = RecordingConsole()
    calls: list[dict[str, object]] = []

    def fake_save_text_file(**kwargs: object) -> Path:
        calls.append(kwargs)
        return Path("/tmp/output/message.txt")

    monkeypatch.setattr(output, "save_text_file", fake_save_text_file)

    output.output_to_stdout_or_file(
        data_string="payload",
        filepath=Path("/tmp/output/message.txt"),
        overwrite=True,
        messenger=console,
    )

    assert calls == [
        {
            "text": "payload",
            "directory": Path("/tmp/output"),
            "filename": "message.txt",
            "overwrite": True,
        }
    ]
    assert console.messages == ["Output saved to /tmp/output/message.txt"]


def test_output_to_stdout_or_file_reports_existing_file_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Existing files should surface a helpful overwrite message."""
    console = RecordingConsole()

    def fake_save_text_file(**kwargs: object) -> Path:
        raise FileExistsError("already exists")

    monkeypatch.setattr(output, "save_text_file", fake_save_text_file)

    with pytest.raises(FileExistsError, match="already exists"):
        output.output_to_stdout_or_file(
            data_string="payload",
            filepath=Path("/tmp/output/message.txt"),
            overwrite=False,
            messenger=console,
        )

    assert console.messages == [
        "File /tmp/output/message.txt already exists. Use --overwrite to overwrite it."
    ]
