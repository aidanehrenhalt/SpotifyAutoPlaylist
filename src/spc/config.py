from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from .spotify.client import AuthState


@dataclass(slots=True)
class AppConfig:
    app_home: Path
    runs_dir: Path
    auth_file: Path
    default_market: str = "US"
    max_tracks_per_artist: int = 2

    @classmethod
    def load(cls, cwd: Path | None = None) -> "AppConfig":
        if "SPC_HOME" in os.environ:
            base_dir = Path(os.environ["SPC_HOME"])
        else:
            base_dir = (cwd or Path.cwd()) / ".spc"
        return cls(
            app_home=base_dir,
            runs_dir=base_dir / "runs",
            auth_file=base_dir / "auth.json",
            default_market=os.environ.get("SPC_DEFAULT_MARKET", "US"),
            max_tracks_per_artist=int(os.environ.get("SPC_MAX_TRACKS_PER_ARTIST", "2")),
        )

    def ensure_directories(self) -> None:
        self.app_home.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    def write_auth_state(self, auth_state: AuthState) -> None:
        self.ensure_directories()
        self.auth_file.write_text(json.dumps(asdict(auth_state), indent=2) + "\n", encoding="utf-8")
        os.chmod(self.auth_file, 0o600)

    def read_auth_state(self) -> AuthState | None:
        if not self.auth_file.exists():
            return None
        payload = json.loads(self.auth_file.read_text(encoding="utf-8"))
        return AuthState(**payload)

    def artifact_path(self, run_id: str) -> Path:
        self.ensure_directories()
        return self.runs_dir / f"{run_id}.json"
