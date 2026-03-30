from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..models import TrackCandidate


@dataclass(slots=True)
class AuthState:
    access_token: str
    refresh_token: str | None = None
    expires_at: str | None = None
    user_id: str | None = None
    display_name: str | None = None


@dataclass(slots=True)
class SpotifyUserProfile:
    user_id: str
    display_name: str | None = None


@dataclass(slots=True)
class PlaylistWriteRequest:
    name: str
    description: str
    track_ids: list[str]


class SpotifyClient(Protocol):
    def whoami(self) -> SpotifyUserProfile | None:
        ...

    def search_tracks(self, genre: str, market: str, seed_artists: list[str]) -> list[TrackCandidate]:
        ...

    def create_playlist(self, request: PlaylistWriteRequest) -> str:
        ...


class DemoSpotifyClient:
    """Local deterministic scaffold until the real Spotify adapter is wired in."""

    def __init__(self, auth_state: AuthState | None) -> None:
        self._auth_state = auth_state
        self._catalog = [
            TrackCandidate(
                track_id="track-shoegaze-1",
                title="Static Bloom",
                artist="Pale Memory",
                album="Haze Line",
                year=1993,
                popularity=44,
                genres=["shoegaze", "dream pop", "noise pop"],
                tags=["shoegaze", "ethereal", "wall of sound"],
                audio_features={"energy": 0.72, "danceability": 0.41, "valence": 0.38, "tempo": 118.0},
            ),
            TrackCandidate(
                track_id="track-shoegaze-2",
                title="Glass Halo",
                artist="Pale Memory",
                album="Haze Line",
                year=1994,
                popularity=41,
                genres=["shoegaze", "indie rock"],
                tags=["shoegaze", "guitar wash"],
                audio_features={"energy": 0.67, "danceability": 0.39, "valence": 0.35, "tempo": 121.0},
            ),
            TrackCandidate(
                track_id="track-shoegaze-3",
                title="Blue Exit",
                artist="Star Circuit",
                album="Lunar Feedback",
                year=1991,
                popularity=48,
                genres=["shoegaze", "alternative rock"],
                tags=["shoegaze", "feedback", "reverb"],
                audio_features={"energy": 0.76, "danceability": 0.37, "valence": 0.33, "tempo": 124.0},
            ),
            TrackCandidate(
                track_id="track-house-1",
                title="Neon Tides",
                artist="Metro Tide",
                album="After Hours",
                year=2018,
                popularity=63,
                genres=["deep house", "house"],
                tags=["deep house", "club", "late night"],
                audio_features={"energy": 0.81, "danceability": 0.84, "valence": 0.57, "tempo": 122.0},
            ),
            TrackCandidate(
                track_id="track-house-2",
                title="Velvet Transit",
                artist="Metro Tide",
                album="After Hours",
                year=2020,
                popularity=58,
                genres=["deep house", "electronic"],
                tags=["deep house", "warm bass"],
                audio_features={"energy": 0.75, "danceability": 0.79, "valence": 0.49, "tempo": 120.0},
            ),
            TrackCandidate(
                track_id="track-jazz-1",
                title="Midnight Sketch",
                artist="Blue Meridian",
                album="Sessions in Smoke",
                year=1959,
                popularity=52,
                genres=["jazz", "modal jazz"],
                tags=["jazz", "modal", "cool jazz"],
                audio_features={"energy": 0.33, "danceability": 0.52, "valence": 0.44, "tempo": 98.0},
            ),
            TrackCandidate(
                track_id="track-jazz-2",
                title="Second Set",
                artist="Miles East",
                album="Street Quintet",
                year=1964,
                popularity=47,
                genres=["jazz", "hard bop"],
                tags=["jazz", "hard bop", "brass"],
                audio_features={"energy": 0.49, "danceability": 0.48, "valence": 0.46, "tempo": 132.0},
            ),
            TrackCandidate(
                track_id="track-dream-1",
                title="Soft Receiver",
                artist="Signal Youth",
                album="Sky Archive",
                year=2017,
                popularity=56,
                genres=["dream pop", "indie pop"],
                tags=["dream pop", "lush"],
                audio_features={"energy": 0.54, "danceability": 0.55, "valence": 0.51, "tempo": 109.0},
            ),
        ]

    def whoami(self) -> SpotifyUserProfile | None:
        if not self._auth_state or not self._auth_state.user_id:
            return None
        return SpotifyUserProfile(
            user_id=self._auth_state.user_id,
            display_name=self._auth_state.display_name,
        )

    def search_tracks(self, genre: str, market: str, seed_artists: list[str]) -> list[TrackCandidate]:
        genre_terms = {genre.strip().lower()}
        artist_terms = {artist.strip().lower() for artist in seed_artists}
        results: list[TrackCandidate] = []
        for track in self._catalog:
            labels = {value.lower() for value in [*track.genres, *track.tags]}
            if genre_terms & labels:
                results.append(track)
                continue
            if artist_terms and track.artist.lower() in artist_terms:
                results.append(track)
        return results

    def create_playlist(self, request: PlaylistWriteRequest) -> str:
        if not self._auth_state or not self._auth_state.user_id:
            raise RuntimeError("Spotify auth is required before writing playlists.")
        return f"spotify:playlist:demo:{self._auth_state.user_id}:{len(request.track_ids)}"
