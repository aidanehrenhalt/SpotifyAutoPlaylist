# Spotify CLI Curation Tool Roadmap

## 1. Product Goal
Build a CLI-first tool that creates high-quality, genre-focused Spotify playlists using explicit metadata and external music signals, instead of relying only on Spotify's in-app recommendation flows.

Desired outcome:
- Input: genre (or genre mix), optional mood/energy/era constraints, playlist length.
- Output: new Spotify playlist populated with tracks that are more consistent to the requested genre profile.

## 2. Scope (CLI First)
In scope (v1):
- Authenticate user via Spotify OAuth.
- Create playlist in user's account.
- Fetch candidate tracks from Spotify + external metadata sources.
- Rank/filter tracks by genre relevance confidence.
- Push curated tracks to the playlist.
- Provide dry-run and explainability output in CLI.

Out of scope (for now):
- Web UI or desktop app.
- Team collaboration features.
- Real-time sync with listening history.

## 3. Proposed User Experience
Example commands:
- `spc auth login`
- `spc curate --genre shoegaze --size 50 --market US`
- `spc curate --genre "deep house" --energy 0.7 --danceability 0.8 --size 75`
- `spc curate --genre jazz --seed-artist "Miles Davis" --era 1955-1970 --dry-run`
- `spc explain --run-id <id>`

CLI behavior:
- Shows candidate counts at each filter stage.
- Prints top accepted/rejected tracks with reason codes.
- Writes run artifact JSON to `./.spc/runs/<timestamp>.json`.

## 4. High-Level Architecture
Components:
1. `spotify_client`
- OAuth (Authorization Code + PKCE for local CLI flow).
- API wrappers for search, artist/album/track lookups, audio features, playlist create/add.

2. `catalog_sources`
- Source adapters for Spotify and external services.
- Normalize track and artist entities into internal schema.

3. `genre_intelligence`
- Build genre profile (genre tags, related genres, seed artists, lexical aliases).
- Merge external tags and confidence scoring.

4. `ranking_engine`
- Score candidate tracks with weighted formula.
- Deduplicate, enforce artist diversity, and optional era/tempo constraints.

5. `playlist_writer`
- Create/replace/update playlist.
- Chunked write with retry and rate-limit handling.

6. `cli`
- Command parsing, progress output, explain command, config management.

## 5. Data Sources to Evaluate
Primary target for external genre signals:
1. Last.fm
- Artist tags and track tags useful for genre labeling.
- Need to validate API availability, terms, and rate limits.

Additional optional sources to assess:
2. MusicBrainz + tags ecosystem
3. Discogs metadata where legally usable
4. Open datasets from Kaggle/GitHub with genre annotations (license check required)

Evaluation criteria:
- API reliability and uptime
- Licensing and terms of use
- Genre coverage and granularity
- Ease of linking records to Spotify IDs
- Rate limits and request quotas

## 6. Curation Strategy (v1)
Pipeline:
1. Collect seeds
- Direct genre search terms
- Optional seed artists/tracks
- Related genres expansion

2. Build candidate pool
- Gather tracks from Spotify search and related artists.
- Enrich each candidate with external genre tags/signals.

3. Score each candidate
- `genre_match_score`: overlap between target genre profile and candidate tags.
- `audio_fit_score`: optional fit using audio features (energy, danceability, valence, tempo).
- `popularity_penalty`: optional dampening of over-mainstream tracks if requested.
- `diversity_bonus`: avoid over-indexing one artist/album.

Example combined score:
- `final_score = 0.55 * genre_match + 0.25 * audio_fit + 0.10 * diversity + 0.10 * recency_or_popularity_policy`

4. Apply constraints
- Remove explicit tracks if user requests clean-only mode.
- Enforce max tracks per artist.
- Enforce year/era bounds.

5. Produce explainability report
- Include per-track score components and rejection reason.

## 7. Security and Privacy Requirements
- Never hardcode secrets; use environment variables and local config files ignored by git.
- Store OAuth tokens locally with least-privilege file permissions.
- Support token refresh without exposing tokens in logs.
- Minimize personally identifiable data collection; no unnecessary telemetry.

## 8. Reliability Requirements
- Handle Spotify rate limits (429) with backoff + retry budget.
- Gracefully degrade if external source is down (continue with reduced confidence mode).
- Idempotent playlist runs with optional `--replace` and `--append` modes.

## 9. Testing Plan
Test layers:
1. Unit tests
- Score computation, filter logic, ID normalization, and command parsing.

2. Contract tests
- Validate API response mapping for Spotify + external adapters using recorded fixtures.

3. Integration tests
- End-to-end dry-run with mocked external APIs.

4. Manual smoke tests
- Real account flow in a dev Spotify app environment.

Acceptance checks for v1:
- Auth + token refresh works.
- `curate` creates a playlist with requested size.
- Dry-run and explain output are consistent.
- Tool handles temporary API failures.

## 10. Implementation Milestones
Milestone 0: Foundation
- Set project layout for CLI package.
- Add config loader and logging conventions.
- Add typed domain models.

Milestone 1: Spotify Auth + Playlist Write
- Implement OAuth login.
- Implement playlist create + add tracks.
- Add basic `curate` command with Spotify-only candidates.

Milestone 2: External Genre Enrichment
- Implement Last.fm adapter.
- Add tag normalization and alias mapping.
- Integrate enriched scoring.

Milestone 3: Explainability + Quality Controls
- Add `--dry-run` and `explain` command.
- Add diversity and artist-cap constraints.
- Add confidence thresholds and fallback modes.

Milestone 4: Hardening
- Retry/backoff and robust error taxonomy.
- Fixture-based integration tests.
- Packaging and CLI install docs.

## 11. Proposed Repository Additions
Suggested structure:
- `src/spc/cli.py`
- `src/spc/config.py`
- `src/spc/spotify/client.py`
- `src/spc/sources/lastfm.py`
- `src/spc/curation/scoring.py`
- `src/spc/curation/pipeline.py`
- `tests/spc/`
- `docs/architecture.md`
- `docs/research/genre-sources.md`

## 12. Open Decisions
- Python library choice for Spotify API: `spotipy` vs direct `httpx` client.
- Token storage approach: local encrypted keyring vs plain file with strict perms.
- Minimum viable external source set: Last.fm only in v1, or include MusicBrainz immediately.
- Default scoring weights and whether they are user-configurable in CLI.

## 13. Immediate Next Steps
1. Create a dedicated CLI package scaffold in this repository.
2. Implement Spotify OAuth and a `whoami` command to validate auth.
3. Add a minimal `curate` command that creates a playlist from seed genre search.
4. Draft `docs/research/genre-sources.md` with Last.fm API constraints and mapping plan.
5. Define a baseline scoring function and fixture tests before external integration.
