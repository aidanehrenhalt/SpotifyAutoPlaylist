# Spotify CLI Curation Tool

CLI-first scaffolding for building curated Spotify playlists from genre and audio-profile inputs.

The repository now follows the architecture in [docs/spotify-cli-roadmap.md](docs/spotify-cli-roadmap.md):

- `src/spc/cli.py`: command entrypoint
- `src/spc/config.py`: app config, auth storage, run artifact paths
- `src/spc/spotify/client.py`: Spotify client contracts and local scaffold
- `src/spc/sources/`: catalog source adapters
- `src/spc/genre_intelligence/`: genre profile building
- `src/spc/curation/`: ranking and pipeline logic
- `tests/spc/`: CLI and domain tests

Project history is tracked in [CHANGELOG.md](CHANGELOG.md).

## Current Status

Implemented:

- CLI package scaffold with `auth`, `curate`, and `explain` commands
- Typed domain models for requests, tracks, scores, and run artifacts
- Local token storage with strict file permissions
- Spotify-only scaffold source backed by a deterministic demo catalog
- Dry-run curation pipeline with explainability artifacts in `./.spc/runs/`
- Baseline docs for architecture and genre-source research

Not implemented yet:

- Real Spotify OAuth PKCE flow
- Real Spotify Web API integration
- Real Last.fm enrichment requests
- Retry/backoff and fixture-based API contract tests

## Usage

Create a virtual environment, install the package, and run:

```bash
python3 -m pip install -e .
spc auth login --user-id alice --display-name "Alice Example" --access-token demo-token
spc auth whoami
spc curate --genre shoegaze --size 5 --dry-run
spc explain --run-id <run-id>
```

Use `SPC_HOME` to override the local app directory if needed.
