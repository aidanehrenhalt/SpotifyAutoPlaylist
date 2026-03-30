from __future__ import annotations

from collections import Counter

from ..genre_intelligence.profile import GenreProfile
from ..models import CurateRequest, RankedTrack, ScoreBreakdown, TrackCandidate


def _round_score(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 4)


def compute_genre_match(profile: GenreProfile, candidate: TrackCandidate) -> float:
    target_terms = {value.lower() for value in profile.search_terms}
    candidate_terms = {value.lower() for value in [*candidate.genres, *candidate.tags]}
    if not target_terms:
        return 0.0
    return _round_score(len(target_terms & candidate_terms) / len(target_terms))


def compute_audio_fit(request: CurateRequest, candidate: TrackCandidate) -> float:
    requested = {
        "energy": request.energy,
        "danceability": request.danceability,
        "valence": request.valence,
        "tempo": request.tempo,
    }
    active = {key: value for key, value in requested.items() if value is not None}
    if not active:
        return 0.5

    distances: list[float] = []
    for key, target in active.items():
        actual = candidate.audio_features.get(key)
        if actual is None:
            distances.append(1.0)
            continue
        scale = 200.0 if key == "tempo" else 1.0
        distances.append(min(abs(actual - target) / scale, 1.0))
    return _round_score(1.0 - (sum(distances) / len(distances)))


def compute_policy_score(candidate: TrackCandidate) -> float:
    # Mildly prefer less mainstream tracks for genre curation.
    return _round_score(1.0 - (candidate.popularity / 100.0))


def rank_candidates(
    request: CurateRequest,
    profile: GenreProfile,
    candidates: list[TrackCandidate],
) -> tuple[list[RankedTrack], list[RankedTrack]]:
    provisional: list[RankedTrack] = []
    artist_counts: Counter[str] = Counter()

    for candidate in candidates:
        genre_match = compute_genre_match(profile, candidate)
        audio_fit = compute_audio_fit(request, candidate)
        diversity = 1.0 if artist_counts[candidate.artist] == 0 else 0.35
        policy = compute_policy_score(candidate)
        final_score = _round_score(
            (0.55 * genre_match) + (0.25 * audio_fit) + (0.10 * diversity) + (0.10 * policy)
        )
        provisional.append(
            RankedTrack(
                candidate=candidate,
                breakdown=ScoreBreakdown(
                    genre_match_score=genre_match,
                    audio_fit_score=audio_fit,
                    diversity_score=diversity,
                    policy_score=policy,
                    final_score=final_score,
                ),
                accepted=False,
                reasons=[],
            )
        )

    ranked = sorted(provisional, key=lambda item: item.breakdown.final_score, reverse=True)
    accepted: list[RankedTrack] = []
    rejected: list[RankedTrack] = []

    for ranked_track in ranked:
        candidate = ranked_track.candidate
        reasons: list[str] = []

        if request.clean_only and candidate.explicit:
            reasons.append("explicit_filtered")
        if request.era_start is not None and candidate.year < request.era_start:
            reasons.append("below_era")
        if request.era_end is not None and candidate.year > request.era_end:
            reasons.append("above_era")
        if artist_counts[candidate.artist] >= request.max_tracks_per_artist:
            reasons.append("artist_cap")
        if ranked_track.breakdown.genre_match_score == 0:
            reasons.append("weak_genre_match")

        if reasons or len(accepted) >= request.size:
            ranked_track.accepted = False
            ranked_track.reasons = reasons or ["size_limit"]
            rejected.append(ranked_track)
            continue

        artist_counts[candidate.artist] += 1
        ranked_track.accepted = True
        ranked_track.reasons = ["accepted"]
        accepted.append(ranked_track)

    return accepted, rejected
