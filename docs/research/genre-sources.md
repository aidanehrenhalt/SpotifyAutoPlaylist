# Genre Source Research Notes

## Last.fm

Planned role:

- Enrich Spotify candidates with artist and track tags.
- Improve genre confidence beyond Spotify search terms alone.

Validation points before integration:

- Confirm public API availability and quotas for expected CLI traffic.
- Confirm whether API key storage in local config is sufficient for developer use.
- Confirm acceptable caching behavior for tags and artist lookups.
- Confirm mapping reliability from Spotify artist names to Last.fm entities.

Initial mapping plan:

1. Resolve candidate artist and track names from Spotify.
2. Request Last.fm artist tags first, then track tags when available.
3. Normalize tags to lowercase lexical aliases.
4. Merge normalized tags into the internal candidate model with source attribution.
5. Degrade gracefully when Last.fm is unavailable by retaining Spotify-only scoring.

## MusicBrainz

Potential role:

- Backfill artist identity normalization and metadata linking.

Open issue:

- Tags are less direct than Last.fm for an initial v1 genre-confidence pass.

## Recommendation

Use Last.fm as the first external enrichment source in v1, then reassess MusicBrainz for identity resolution rather than primary genre tagging.
