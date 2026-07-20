"""Tests for text file saving helpers."""

from pathlib import Path

import pytest

from pfmsoft.eve_snippets.files.save_text_file import save_text_file


def test_save_text_file_creates_parent_directories_and_appends_newline(
    tmp_path: Path,
) -> None:
    """Saving a file should create missing parents and write a trailing newline."""
    output = save_text_file(
        text="hello world",
        directory=tmp_path / "nested" / "output",
        filename="message.txt",
    )

    assert output == tmp_path / "nested" / "output" / "message.txt"
    assert output.read_text(encoding="utf-8") == "hello world\n"


def test_save_text_file_rejects_existing_file_without_overwrite(
    tmp_path: Path,
) -> None:
    """Saving without overwrite should fail when the target file already exists."""
    output = tmp_path / "message.txt"
    output.write_text("seed\n", encoding="utf-8")

    with pytest.raises(FileExistsError):
        save_text_file(text="replacement", directory=tmp_path, filename="message.txt")

    assert output.read_text(encoding="utf-8") == "seed\n"


def test_save_text_file_overwrites_existing_file_without_newline(
    tmp_path: Path,
) -> None:
    """Saving with overwrite should replace contents and respect newline flags."""
    output = tmp_path / "message.txt"
    output.write_text("seed\n", encoding="utf-8")

    written = save_text_file(
        text="replacement",
        directory=tmp_path,
        filename="message.txt",
        overwrite=True,
        add_newline=False,
    )

    assert written == output
    assert output.read_text(encoding="utf-8") == "replacement"
