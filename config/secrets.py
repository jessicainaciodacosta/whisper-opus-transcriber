"""Secret access layer (API keys, tokens).

Uses `config.settings.get_api_key` to read environment variables.
Never expose values in logs or error messages.
"""

from __future__ import annotations

from typing import Optional

from config.settings import get_api_key


class SecretsError(RuntimeError):
    """Raised when a required secret is not available."""


def get_secret(name: str, *, required: bool = True) -> Optional[str]:
    """Retrieve a secret by environment variable name.

    Args:
        name: Environment variable name.
        required: If True, raises `SecretsError` when not found.

    Returns:
        The variable value or None when required=False and missing.
    """
    value = get_api_key(name)
    if value is None and required:
        raise SecretsError(
            f"Environment variable '{name}' is not set. "
            "Check your .env file."
        )
    return value