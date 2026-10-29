# Changelog

All notable changes to this project will be documented here.

## [0.1.0] - 2026-10-28
### Added
- Modular architecture with `config/`, `modules/`, `tests/`.
- Clean entry point `main.py`.
- Environment-based configuration with `config/settings.py` and `config/secrets.py`.
- Dependencies managed with Poetry in `pyproject.toml`.
- Configurable logger and I/O utilities.
- Transcription with faster-whisper decoupled in `modules/transcription.py`.
- Basic tests for settings, io_utils and transcription.
- `.env.example` and `.gitignore` for security.
- Data organized in `data/audios`, `data/transcricoes`, `data/conversas`.
- Professional README.

### Removed
- Legacy scripts with absolute paths from `tools/`.

### Improvements
- Data folders moved to `data/` and ignored by git.
- Configuration defaults updated for local use.