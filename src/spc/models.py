from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class TrackCandidate:
    track_id: str
    title: str
    artist: str
    album: str
    year: int
    popularity: int
    genres: list[str]
    tags: list[str]
    audio_features: dict[str, float]
    explicit: bool = False


@dataclass(slots=True)
class CurateRequest:
    genre: str
    size: int
    market: str = "US"
    seed_artists: list[str] = field(default_factory=list)
    energy: float | None = None
    danceability: float | None = None
    valence: float | None = None
    tempo: float | None = None
    era_start: int | None = None
    era_end: int | None = None
    dry_run: bool = False
    clean_only: bool = False
    max_tracks_per_artist: int = 2


@dataclass(slots=True)
class ScoreBreakdown:
    genre_match_score: float
    audio_fit_score: float
    diversity_score: float
    policy_score: float
    final_score: float


@dataclass(slots=True)
class RankedTrack:
    candidate: TrackCandidate
    breakdown: ScoreBreakdown
    accepted: bool
    reasons: list[str]


@dataclass(slots=True)
class RunSummary:
    candidate_count: int
    accepted_count: int
    rejected_count: int
    playlist_written: bool


@dataclass(slots=True)
class RunArtifact:
    run_id: str
    created_at: str
    request: CurateRequest
    summary: RunSummary
    accepted: list[RankedTrack]
    rejected: list[RankedTrack]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
