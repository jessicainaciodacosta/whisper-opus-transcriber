"""Configurable logger for the project.

Avoids exposing secrets in messages: use `safe_log` to avoid logging sensitive values.
"""

from __future__ import annotations

import logging
import os
from typing import Any


def _env_log_level(default: str = "INFO") -> int:
    raw = os.environ.get("TRANSCREVER_LOG_LEVEL", default).strip().upper()
    return getattr(logging, raw, logging.INFO)


def get_logger(name: str = "transcricoes") -> logging.Logger:
    """Return a configured logger (avoids handler duplication)."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(_env_log_level())
    return logger


def safe_log(logger: logging.Logger, level: int, msg: str, *args: Any) -> None:
    """Safe log that does not display sensitive values.

    Use instead of `logger.log(level, msg, *args)` when `args` may contain secrets.
    """
    logger.log(level, msg)