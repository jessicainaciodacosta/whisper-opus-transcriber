"""Basic tests for transcription modules (without calling real model)."""

from pathlib import Path
import tempfile

from modules.io_utils import write_text
from modules.transcription import transcribe_all


def test_transcribe_all_no_files():
    with tempfile.TemporaryDirectory() as audios_dir, tempfile.TemporaryDirectory() as out_dir:
        # no files, should return empty without error
        results = list(transcribe_all(audios_dir, out_dir))
        assert results == []


def test_transcribe_all_empty_file():
    # Flow test with model mock: we do not load real Whisper.
    # Just ensure listing works.
    from modules.io_utils import list_audio_files
    with tempfile.TemporaryDirectory() as audios_dir:
        audios = Path(audios_dir)
        # create a dummy .opus file
        dummy = audios / "dummy.opus"
        write_text(dummy, "")
        files = list_audio_files(audios)
        assert any(p.name == "dummy.opus" for p in files)