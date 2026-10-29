"""Basic tests for configuration."""

from pathlib import Path

import sys

# Ensure project is on PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import settings, Settings


def test_defaults():
    s = Settings()
    assert isinstance(s.audios_dir, Path)
    assert isinstance(s.transcricoes_dir, Path)
    assert s.whisper_model == "base"
    assert s.whisper_device == "cpu"
    assert s.beam_size == 5
    assert s.delete_after is False
    assert s.consolidate is False


def test_global_settings():
    assert isinstance(settings, Settings)