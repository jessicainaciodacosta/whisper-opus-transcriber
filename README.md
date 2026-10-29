# Whisper Opus Transcriber

Modular Python pipeline to transcribe WhatsApp voice notes and audio files to Portuguese text using faster-whisper. Configuration is via environment variables and secrets are never committed.

## Structure

```
.
├── config/          # Configuration and secret access
├── modules/         # Processing and transcription logic
├── tests/           # Basic tests
├── data/            # Project data, ignored by git
│   ├── audios/      # Original audio files .opus
│   ├── transcricoes/# Generated text files .txt
│   └── conversas/   # Exported conversations
├── main.py          # Entry point
├── pyproject.toml   # Poetry dependencies
└── README.md
```

## Installation

```bash
poetry install
```

Create a `.env` file from the example:

```bash
cp config/.env.example .env
```

Edit `.env` if you want to change folders or model.

## Usage

Transcribe all audios from the configured folder:

```bash
poetry run python main.py
```

To enable consolidation into `tudo_junto.txt`, set in `.env`:
```
TRANSCREVER_CONSOLIDATE=true
```

## Environment Variables

See `config/.env.example`. Defaults:
- `TRANSCREVER_AUDIOS_DIR=data/audios`
- `TRANSCREVER_TRANSCRICOES_DIR=data/transcricoes`
- `TRANSCREVER_WHISPER_MODEL=base`
- `TRANSCREVER_WHISPER_DEVICE=cpu`

## Security

- Never commit `.env`.
- Secrets are accessed via `config.secrets.get_secret`.
- `data/` is in `.gitignore`.

## Tests

```bash
poetry run pytest -q
```

## Notes

This repository does not contain original audios. Place your files in `data/audios/` locally.