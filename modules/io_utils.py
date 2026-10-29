"""I/O utilities (listing, folder creation, writing, consolidation)."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable, List

from config import settings


def ensure_dir(path: Path) -> Path:
    """Create folder if it does not exist and return the path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_audio_files(root: Path | str = settings.audios_dir) -> List[Path]:
    """List audio files recursively in the given directory."""
    root = Path(root)
    extensions = settings.audio_extensions
    files: List[Path] = []
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)
    for ext in extensions:
        files.extend(root.rglob(f"*{ext}"))
    # Sort predictably
    files.sort(key=lambda p: p.as_posix())
    return files


def write_text(path: Path | str, text: str) -> None:
    """Write UTF-8 text to a file, creating parent folders automatically."""
    path = Path(path)
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        f.write(text)


def consolidate_texts(
    texts: Iterable[tuple[str, str]],
    output_path: Path | str,
    separator: str | None = None,
) -> None:
    """Consolidate multiple texts into a single file.

    Args:
        texts: Sequence of tuples (filename, content).
        output_path: Path to the final file.
        separator: Separator between blocks; uses config if None.
    """
    if separator is None:
        separator = settings.consolidated_separator

    lines: List[str] = []
    for name, content in texts:
        lines.append(f"--- {name} ---")
        lines.append(content.strip())
        lines.append(separator)
    merged = "".join(lines)
    write_text(output_path, merged)