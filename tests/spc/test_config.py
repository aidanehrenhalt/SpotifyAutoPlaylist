import os
import stat

from spc.config import AppConfig
from spc.spotify.client import AuthState


def test_auth_state_round_trip(tmp_path, monkeypatch):
    monkeypatch.setenv("SPC_HOME", str(tmp_path / ".spc"))
    config = AppConfig.load()

    config.write_auth_state(
        AuthState(
            access_token="token",
            refresh_token="refresh",
            expires_at="2026-03-30T12:00:00Z",
            user_id="tester",
            display_name="Test User",
        )
    )

    loaded = config.read_auth_state()
    assert loaded is not None
    assert loaded.user_id == "tester"
    assert stat.S_IMODE(os.stat(config.auth_file).st_mode) == 0o600
