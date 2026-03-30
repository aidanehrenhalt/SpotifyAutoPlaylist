from __future__ import annotations

from dataclasses import dataclass

from .models import RankedTrack
from .spotify.client import PlaylistWriteRequest, SpotifyClient


@dataclass(slots=True)
class PlaylistWriteResult:
    playlist_uri: str
    added_count: int


class PlaylistWriter:
    def __init__(self, spotify_client: SpotifyClient) -> None:
        self._spotify_client = spotify_client

    def write(self, playlist_name: str, description: str, accepted: list[RankedTrack]) -> PlaylistWriteResult:
        track_ids = [item.candidate.track_id for item in accepted]
        playlist_uri = self._spotify_client.create_playlist(
            PlaylistWriteRequest(name=playlist_name, description=description, track_ids=track_ids)
        )
        return PlaylistWriteResult(playlist_uri=playlist_uri, added_count=len(track_ids))
