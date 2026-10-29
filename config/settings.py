"""Project settings loaded from environment variables.

All keys are read via `os.environ` (or `.env` loaded by
`python-dotenv`). If a variable is not defined, a safe default is used
that does not expose secrets.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _env_str(name: str, default: str) -> str:
    return os.environ.get(name, default)


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_dir(value: str) -> Path:
    return Path(value).expanduser().resolve()


@dataclass(frozen=True)
class Settings:
    audios_dir: Path = _resolve_dir(_env_str("TRANSCREVER_AUDIOS_DIR", "data/audios"))
    transcricoes_dir: Path = _resolve_dir(_env_str("TRANSCREVER_TRANSCRICOES_DIR", "data/transcricoes"))
    conversas_dir: Path = _resolve_dir(_env_str("TRANSCREVER_CONVERSAS_DIR", "data/conversas"))

    whisper_model: str = _env_str("TRANSCREVER_WHISPER_MODEL", "base")
    whisper_device: str = _env_str("TRANSCREVER_WHISPER_DEVICE", "cpu")
    whisper_compute_type: str = _env_str("TRANSCREVER_WHISPER_COMPUTE_TYPE", "int8")
    language: str = _env_str("TRANSCREVER_LANGUAGE", "pt")
    beam_size: int = _env_int("TRANSCREVER_BEAM_SIZE", 5)
    audio_extensions: tuple[str, ...] = (".opus", ".mp3", ".wav", ".m4a", ".ogg")
    delete_after: bool = _env_bool("TRANSCREVER_DELETE_AFTER", False)
    consolidate: bool = _env_bool("TRANSCREVER_CONSOLIDATE", False)
    consolidated_name: str = _env_str("TRANSCREVER_CONSOLIDATED_NAME", "tudo_junto.txt")
    consolidated_separator: str = _env_str("TRANSCREVER_CONSOLIDATED_SEPARATOR", "\n\n")


settings = Settings()


def get_api_key(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)