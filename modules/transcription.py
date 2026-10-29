"""Audio transcription using faster-whisper.

Decouples model loading from I/O logic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Tuple

from config import settings
from config.secrets import SecretsError
from modules.io_utils import ensure_dir, list_audio_files, write_text
from modules.logger import get_logger

logger = get_logger(__name__)


def _load_model():
    """Load Whisper model once lazily."""
    from faster_whisper import WhisperModel

    model = WhisperModel(
        settings.whisper_model,
        device=settings.whisper_device,
        compute_type=settings.whisper_compute_type,
    )
    return model


MODEL = None  # initialized on demand


def transcribe_file(audio_path: Path | str) -> str:
    """Transcribe a single audio file and return text."""
    global MODEL
    if MODEL is None:
        logger.info("Loading Whisper model: %s", settings.whisper_model)
        MODEL = _load_model()

    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    logger.info("Transcribing: %s", audio_path.name)
    segments, info = MODEL.transcribe(
        str(audio_path),
        language=settings.language,
        beam_size=settings.beam_size,
    )
    text = " ".join(seg.text for seg in segments)
    return text.strip()


def transcribe_all(
    audios_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
) -> Iterator[Tuple[Path, Path, str]]:
    """Transcribe all audios in directory and save .txt.

    Yields:
        Tuple (audio_path, txt_path, text).
    """
    audios_dir = Path(audios_dir or settings.audios_dir)
    output_dir = Path(output_dir or settings.transcricoes_dir)
    ensure_dir(output_dir)

    files = list_audio_files(audios_dir)
    if not files:
        logger.warning("No audio files found in %s", audios_dir)
        return

    for audio_path in files:
        try:
            text = transcribe_file(audio_path)
        except Exception as exc:
            logger.exception("Failed to transcribe %s: %s", audio_path.name, exc)
            continue

        txt_name = audio_path.stem + ".txt"
        txt_path = output_dir / txt_name
        write_text(txt_path, text)
        logger.info("✓ Saved: %s", txt_path.name)

        if settings.delete_after:
            try:
                audio_path.unlink()
                logger.info("Audio removed: %s", audio_path.name)
            except Exception:
                logger.exception("Could not remove %s", audio_path.name)

        yield audio_path, txt_path, text