from __future__ import annotations

from dataclasses import dataclass

from ..genre_intelligence.profile import GenreProfile
from ..models import CurateRequest, TrackCandidate
from ..spotify.client import SpotifyClient


@dataclass(slots=True)
class SpotifyCatalogSource:
    client: SpotifyClient

    def fetch_candidates(self, request: CurateRequest, profile: GenreProfile) -> list[TrackCandidate]:
        candidates: dict[str, TrackCandidate] = {}
        for term in profile.search_terms:
            for track in self.client.search_tracks(
                genre=term,
                market=request.market,
                seed_artists=request.seed_artists,
            ):
                candidates[track.track_id] = track
        return list(candidates.values())
