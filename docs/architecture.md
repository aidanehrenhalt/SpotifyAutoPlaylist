# Spotify CLI Architecture

## Modules

- `spc.cli`
  - Parses commands and renders concise CLI output.
- `spc.config`
  - Resolves `SPC_HOME`, token storage, and artifact locations.
- `spc.spotify.client`
  - Defines the Spotify client contract and the current local scaffold client.
- `spc.sources.spotify`
  - Fetches Spotify-backed candidate tracks for a genre profile.
- `spc.sources.lastfm`
  - Holds initial tag normalization utilities for future enrichment work.
- `spc.genre_intelligence.profile`
  - Builds a normalized genre profile with aliases and related terms.
- `spc.curation.scoring`
  - Computes genre, audio-fit, diversity, and policy scores.
- `spc.curation.pipeline`
  - Coordinates profile creation, candidate fetch, ranking, playlist writing, and artifact persistence.
- `spc.playlist_writer`
  - Encapsulates playlist creation and future retry/backoff behavior.

## Run Flow

1. CLI parses the requested genre, constraints, and run mode.
2. Config resolves local state in `./.spc/` or `SPC_HOME`.
3. Genre intelligence expands the requested genre into search terms.
4. Catalog sources fetch candidate tracks.
5. Ranking computes explainable score components.
6. Accepted and rejected tracks are written to `./.spc/runs/<run-id>.json`.
7. If the run is not a dry-run, the playlist writer publishes the accepted tracks.

## Extension Points

- Replace `DemoSpotifyClient` with a real PKCE + Web API implementation.
- Add Last.fm enrichment before scoring.
- Add fallback modes and retry budgets in `playlist_writer`.
- Add recorded contract fixtures around source adapters.
