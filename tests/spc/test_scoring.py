from spc.curation.scoring import compute_audio_fit, compute_genre_match, rank_candidates
from spc.genre_intelligence.profile import build_genre_profile
from spc.models import CurateRequest, TrackCandidate


def test_genre_match_uses_profile_aliases():
    profile = build_genre_profile("shoegaze")
    candidate = TrackCandidate(
        track_id="1",
        title="Track",
        artist="Artist",
        album="Album",
        year=1993,
        popularity=40,
        genres=["dream pop"],
        tags=["wall of sound"],
        audio_features={"energy": 0.7, "danceability": 0.4, "valence": 0.3, "tempo": 120.0},
    )

    assert compute_genre_match(profile, candidate) > 0


def test_audio_fit_rewards_close_values():
    request = CurateRequest(genre="deep house", size=5, energy=0.8, danceability=0.8)
    close_candidate = TrackCandidate(
        track_id="1",
        title="Close",
        artist="Artist",
        album="Album",
        year=2020,
        popularity=50,
        genres=["deep house"],
        tags=["club"],
        audio_features={"energy": 0.78, "danceability": 0.82, "valence": 0.6, "tempo": 122.0},
    )
    far_candidate = TrackCandidate(
        track_id="2",
        title="Far",
        artist="Artist",
        album="Album",
        year=2020,
        popularity=50,
        genres=["deep house"],
        tags=["club"],
        audio_features={"energy": 0.2, "danceability": 0.2, "valence": 0.6, "tempo": 90.0},
    )

    assert compute_audio_fit(request, close_candidate) > compute_audio_fit(request, far_candidate)


def test_rank_candidates_enforces_artist_cap():
    request = CurateRequest(genre="shoegaze", size=3, max_tracks_per_artist=1)
    profile = build_genre_profile("shoegaze")
    candidates = [
        TrackCandidate(
            track_id="1",
            title="A",
            artist="Same Artist",
            album="Album",
            year=1993,
            popularity=40,
            genres=["shoegaze"],
            tags=["shoegaze"],
            audio_features={"energy": 0.7, "danceability": 0.4, "valence": 0.3, "tempo": 120.0},
        ),
        TrackCandidate(
            track_id="2",
            title="B",
            artist="Same Artist",
            album="Album",
            year=1994,
            popularity=41,
            genres=["shoegaze"],
            tags=["shoegaze"],
            audio_features={"energy": 0.68, "danceability": 0.39, "valence": 0.31, "tempo": 121.0},
        ),
    ]

    accepted, rejected = rank_candidates(request, profile, candidates)
    assert len(accepted) == 1
    assert "artist_cap" in rejected[0].reasons
