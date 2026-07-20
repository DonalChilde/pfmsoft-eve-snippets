"""Tests for YAML load and dump helpers."""

from __future__ import annotations

import importlib
import io
import sys
import types
from pathlib import Path

import pytest

from pfmsoft.eve_snippets.yaml import yaml_io


def test_yaml_io_uses_pure_python_loader_when_c_extensions_are_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The module should fall back to safe loader/dumper imports when needed."""
    real_yaml = sys.modules["yaml"]
    fake_yaml = types.ModuleType("yaml")
    fake_yaml.SafeDumper = object()
    fake_yaml.SafeLoader = object()
    fake_yaml.dump = lambda *args, **kwargs: None
    fake_yaml.load = lambda *args, **kwargs: None

    monkeypatch.setitem(sys.modules, "yaml", fake_yaml)

    try:
        reloaded = importlib.reload(yaml_io)

        assert reloaded.SafeDumper is fake_yaml.SafeDumper
        assert reloaded.SafeLoader is fake_yaml.SafeLoader
    finally:
        monkeypatch.setitem(sys.modules, "yaml", real_yaml)
        importlib.reload(yaml_io)


def test_yaml_dump_path_helpers_write_and_overwrite_files(tmp_path: Path) -> None:
    """Path-based dump helpers should create directories and honor overwrite."""
    text_path = tmp_path / "nested" / "text.yaml"
    binary_path = tmp_path / "nested" / "binary.yaml"

    yaml_io.safe_dump_str_path({"name": "Jill", "accent": "Größe"}, text_path)
    yaml_io.safe_dump_bytes_path(
        {"name": "Jill", "accent": "Größe"},
        binary_path,
    )

    assert text_path.read_text(encoding="utf-8") == "accent: Größe\nname: Jill\n"
    assert binary_path.read_bytes() == b"accent: Gr\xc3\xb6\xc3\x9fe\nname: Jill\n"

    with pytest.raises(FileExistsError):
        yaml_io.safe_dump_str_path({"name": "other"}, text_path)

    with pytest.raises(FileExistsError):
        yaml_io.safe_dump_bytes_path({"name": "other"}, binary_path)

    yaml_io.safe_dump_str_path({"name": "other"}, text_path, overwrite=True)
    yaml_io.safe_dump_bytes_path({"name": "other"}, binary_path, overwrite=True)

    assert yaml_io.safe_load_path(text_path) == {"name": "other"}
    assert yaml_io.safe_load_path(binary_path) == {"name": "other"}


def test_yaml_stream_dump_helpers_round_trip_data() -> None:
    """Stream-based dump helpers should serialize content for later loading."""
    payload = {"items": [1, 2, 3], "active": True}
    text_stream = io.StringIO()
    binary_stream = io.BytesIO()

    yaml_io.safe_dump_text_io(payload, text_stream)
    yaml_io.safe_dump_binary_io(payload, binary_stream)

    assert yaml_io.safe_load_IO(io.StringIO(text_stream.getvalue())) == payload
    assert yaml_io.safe_load_IO(io.BytesIO(binary_stream.getvalue())) == payload


def test_yaml_string_and_bytes_helpers_round_trip_data() -> None:
    """String and bytes helpers should round-trip through safe_load."""
    payload = {"items": [1, 2, 3], "active": True}

    yaml_text = yaml_io.safe_dump_str(payload)
    yaml_bytes = yaml_io.safe_dump_bytes(payload)

    assert isinstance(yaml_text, str)
    assert isinstance(yaml_bytes, bytes)
    assert yaml_io.safe_load(yaml_text) == payload
    assert yaml_io.safe_load(yaml_bytes) == payload


def test_yaml_dump_bytes_rejects_non_bytes_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bytes dumping should fail if the YAML backend does not return bytes."""

    monkeypatch.setattr(yaml_io.yaml, "dump", lambda *args, **kwargs: "not-bytes")

    with pytest.raises(TypeError, match="Expected bytes from safe_dump"):
        yaml_io.safe_dump_bytes({"items": [1, 2, 3]})
