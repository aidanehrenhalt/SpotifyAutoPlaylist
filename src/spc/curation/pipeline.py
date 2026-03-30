from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone

from ..config import AppConfig
from ..genre_intelligence.profile import build_genre_profile
from ..models import CurateRequest, RunArtifact, RunSummary
from ..playlist_writer import PlaylistWriteResult, PlaylistWriter
from ..sources.spotify import SpotifyCatalogSource
from .scoring import rank_candidates


@dataclass(slots=True)
class CurateResult:
    artifact: RunArtifact
    artifact_path: str
    playlist_result: PlaylistWriteResult | None


class CurationPipeline:
    def __init__(
        self,
        config: AppConfig,
        catalog_source: SpotifyCatalogSource,
        playlist_writer: PlaylistWriter,
    ) -> None:
        self._config = config
        self._catalog_source = catalog_source
        self._playlist_writer = playlist_writer

    def run(self, request: CurateRequest) -> CurateResult:
        now = datetime.now(timezone.utc)
        run_id = now.strftime("%Y%m%dT%H%M%SZ")
        profile = build_genre_profile(request.genre)
        candidates = self._catalog_source.fetch_candidates(request, profile)
        accepted, rejected = rank_candidates(request, profile, candidates)

        playlist_result: PlaylistWriteResult | None = None
        if not request.dry_run and accepted:
            playlist_name = f"SPC {request.genre.title()} {run_id}"
            description = f"Curated from genre={request.genre} market={request.market}"
            playlist_result = self._playlist_writer.write(playlist_name, description, accepted)

        artifact = RunArtifact(
            run_id=run_id,
            created_at=now.isoformat(),
            request=request,
            summary=RunSummary(
                candidate_count=len(candidates),
                accepted_count=len(accepted),
                rejected_count=len(rejected),
                playlist_written=playlist_result is not None,
            ),
            accepted=accepted,
            rejected=rejected,
        )

        artifact_path = self._config.artifact_path(run_id)
        artifact_path.write_text(json.dumps(artifact.to_dict(), indent=2) + "\n", encoding="utf-8")
        return CurateResult(artifact=artifact, artifact_path=str(artifact_path), playlist_result=playlist_result)
