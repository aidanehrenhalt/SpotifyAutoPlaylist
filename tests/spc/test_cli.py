import json

from spc.cli import main


def test_curate_dry_run_writes_artifact(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SPC_HOME", str(tmp_path / ".spc"))

    exit_code = main(["curate", "--genre", "shoegaze", "--size", "2", "--dry-run"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidates:" in output
    assert "Artifact:" in output

    run_id_line = next(line for line in output.splitlines() if line.startswith("Run ID: "))
    run_id = run_id_line.split(": ", maxsplit=1)[1]
    artifact_path = tmp_path / ".spc" / "runs" / f"{run_id}.json"
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["request"]["genre"] == "shoegaze"
    assert payload["summary"]["playlist_written"] is False


def test_explain_reads_previous_run(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SPC_HOME", str(tmp_path / ".spc"))
    main(["curate", "--genre", "jazz", "--size", "2", "--dry-run"])
    curate_output = capsys.readouterr().out
    run_id = next(line for line in curate_output.splitlines() if line.startswith("Run ID: ")).split(": ", 1)[1]

    exit_code = main(["explain", "--run-id", run_id])
    explain_output = capsys.readouterr().out

    assert exit_code == 0
    assert f"Run {run_id} genre=jazz" in explain_output


def test_auth_login_and_whoami(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SPC_HOME", str(tmp_path / ".spc"))

    assert (
        main(
            [
                "auth",
                "login",
                "--access-token",
                "demo-token",
                "--user-id",
                "tester",
                "--display-name",
                "Test User",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert main(["auth", "whoami"]) == 0
    output = capsys.readouterr().out
    assert "tester (Test User)" in output
