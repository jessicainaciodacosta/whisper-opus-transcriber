"""Modules package — processing and transcription logic."""

from modules.transcription import transcribe_file, transcribe_all
from modules.io_utils import (
    ensure_dir,
    list_audio_files,
    write_text,
    consolidate_texts,
)
from modules.logger import get_logger

__all__ = [
    "transcribe_file",
    "transcribe_all",
    "ensure_dir",
    "list_audio_files",
    "write_text",
    "consolidate_texts",
    "get_logger",
]