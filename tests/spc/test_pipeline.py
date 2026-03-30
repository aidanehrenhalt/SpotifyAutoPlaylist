from spc.config import AppConfig
from spc.curation.pipeline import CurationPipeline
from spc.models import CurateRequest
from spc.playlist_writer import PlaylistWriter
from spc.sources.spotify import SpotifyCatalogSource
from spc.spotify.client import DemoSpotifyClient


def test_pipeline_defaults_to_dot_spc_directory(tmp_path, monkeypatch):
    monkeypatch.delenv("SPC_HOME", raising=False)
    config = AppConfig.load(cwd=tmp_path)
    pipeline = CurationPipeline(
        config=config,
        catalog_source=SpotifyCatalogSource(DemoSpotifyClient(auth_state=None)),
        playlist_writer=PlaylistWriter(DemoSpotifyClient(auth_state=None)),
    )

    result = pipeline.run(CurateRequest(genre="shoegaze", size=2, dry_run=True))

    assert result.artifact_path.startswith(str(tmp_path / ".spc" / "runs"))
