"""Entry point for the audio transcription project.

Flow:
1. Read settings from `config.settings`.
2. Transcribe all audios with `modules.transcription`.
3. Optionally consolidate texts into a single file.
"""

from __future__ import annotations

from pathlib import Path

from config import settings
from modules import transcribe_all, consolidate_texts, get_logger, ensure_dir

logger = get_logger("main")


def main() -> None:
    logger.info("Starting transcription")
    logger.info("Audios in: %s", settings.audios_dir)
    logger.info("Outputs to: %s", settings.transcricoes_dir)

    # Ensure folders exist
    ensure_dir(settings.audios_dir)
    ensure_dir(settings.transcricoes_dir)
    ensure_dir(settings.conversas_dir)

    texts: list[tuple[str, str]] = []

    for audio_path, txt_path, text in transcribe_all():
        texts.append((txt_path.name, text))

    if settings.consolidate and texts:
        output_path = settings.transcricoes_dir / settings.consolidated_name
        consolidate_texts(
            texts,
            output_path,
            separator=settings.consolidated_separator,
        )
        logger.info("Consolidated file created: %s", output_path)

    logger.info("Transcription finished")


if __name__ == "__main__":
    main()