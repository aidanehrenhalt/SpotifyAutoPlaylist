from __future__ import annotations


class LastfmSourceUnavailableError(RuntimeError):
    """Raised when the external enrichment source is not configured."""


def normalize_lastfm_tags(tags: list[str]) -> list[str]:
    normalized = {tag.strip().lower().replace("-", " ") for tag in tags if tag.strip()}
    return sorted(normalized)
