from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .config import AppConfig
from .curation.pipeline import CurationPipeline
from .models import CurateRequest
from .playlist_writer import PlaylistWriter
from .sources.spotify import SpotifyCatalogSource
from .spotify.client import AuthState, DemoSpotifyClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spc", description="Spotify playlist curation CLI scaffold")
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_parser = subparsers.add_parser("auth", help="Manage Spotify auth state")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", required=True)

    login_parser = auth_subparsers.add_parser("login", help="Persist local auth state")
    login_parser.add_argument("--access-token", required=True)
    login_parser.add_argument("--refresh-token")
    login_parser.add_argument("--expires-at")
    login_parser.add_argument("--user-id", required=True)
    login_parser.add_argument("--display-name")

    auth_subparsers.add_parser("whoami", help="Show the stored Spotify identity")

    curate_parser = subparsers.add_parser("curate", help="Curate a playlist from a genre profile")
    curate_parser.add_argument("--genre", required=True)
    curate_parser.add_argument("--size", type=int, default=50)
    curate_parser.add_argument("--market")
    curate_parser.add_argument("--seed-artist", action="append", default=[])
    curate_parser.add_argument("--energy", type=float)
    curate_parser.add_argument("--danceability", type=float)
    curate_parser.add_argument("--valence", type=float)
    curate_parser.add_argument("--tempo", type=float)
    curate_parser.add_argument("--era")
    curate_parser.add_argument("--dry-run", action="store_true")
    curate_parser.add_argument("--clean-only", action="store_true")

    explain_parser = subparsers.add_parser("explain", help="Explain a previous curate run")
    explain_parser.add_argument("--run-id", required=True)

    return parser


def _parse_era(raw: str | None) -> tuple[int | None, int | None]:
    if not raw:
        return None, None
    if "-" not in raw:
        value = int(raw)
        return value, value
    start, end = raw.split("-", maxsplit=1)
    return int(start), int(end)


def _build_pipeline(config: AppConfig) -> CurationPipeline:
    auth_state = config.read_auth_state()
    client = DemoSpotifyClient(auth_state)
    return CurationPipeline(
        config=config,
        catalog_source=SpotifyCatalogSource(client),
        playlist_writer=PlaylistWriter(client),
    )


def _print_ranked_tracks(title: str, entries: list[dict[str, object]]) -> None:
    print(title)
    for entry in entries[:5]:
        candidate = entry["candidate"]
        breakdown = entry["breakdown"]
        reasons = ", ".join(entry["reasons"])
        print(
            f"  - {candidate['artist']} - {candidate['title']} "
            f"(score={breakdown['final_score']}, reasons={reasons})"
        )


def handle_auth(args: argparse.Namespace, config: AppConfig) -> int:
    if args.auth_command == "login":
        config.write_auth_state(
            AuthState(
                access_token=args.access_token,
                refresh_token=args.refresh_token,
                expires_at=args.expires_at,
                user_id=args.user_id,
                display_name=args.display_name,
            )
        )
        print(f"Stored auth state in {config.auth_file}")
        return 0

    auth_state = config.read_auth_state()
    client = DemoSpotifyClient(auth_state)
    profile = client.whoami()
    if profile is None:
        print("No Spotify auth state found.")
        return 1
    display_name = f" ({profile.display_name})" if profile.display_name else ""
    print(f"{profile.user_id}{display_name}")
    return 0


def handle_curate(args: argparse.Namespace, config: AppConfig) -> int:
    era_start, era_end = _parse_era(args.era)
    request = CurateRequest(
        genre=args.genre,
        size=args.size,
        market=args.market or config.default_market,
        seed_artists=args.seed_artist,
        energy=args.energy,
        danceability=args.danceability,
        valence=args.valence,
        tempo=args.tempo,
        era_start=era_start,
        era_end=era_end,
        dry_run=args.dry_run,
        clean_only=args.clean_only,
        max_tracks_per_artist=config.max_tracks_per_artist,
    )
    result = _build_pipeline(config).run(request)

    print(f"Run ID: {result.artifact.run_id}")
    print(f"Candidates: {result.artifact.summary.candidate_count}")
    print(f"Accepted: {result.artifact.summary.accepted_count}")
    print(f"Rejected: {result.artifact.summary.rejected_count}")
    if result.playlist_result is not None:
        print(f"Playlist URI: {result.playlist_result.playlist_uri}")
    print(f"Artifact: {result.artifact_path}")

    artifact_dict = result.artifact.to_dict()
    _print_ranked_tracks("Top accepted", artifact_dict["accepted"])
    _print_ranked_tracks("Top rejected", artifact_dict["rejected"])
    return 0


def handle_explain(args: argparse.Namespace, config: AppConfig) -> int:
    artifact_path = config.artifact_path(args.run_id)
    if not artifact_path.exists():
        print(f"Run artifact not found: {artifact_path}")
        return 1
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    request = artifact["request"]
    summary = artifact["summary"]
    print(
        f"Run {artifact['run_id']} genre={request['genre']} "
        f"size={request['size']} market={request['market']}"
    )
    print(
        f"Candidates={summary['candidate_count']} "
        f"Accepted={summary['accepted_count']} "
        f"Rejected={summary['rejected_count']}"
    )
    _print_ranked_tracks("Accepted tracks", artifact["accepted"])
    _print_ranked_tracks("Rejected tracks", artifact["rejected"])
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = AppConfig.load(cwd=Path.cwd())

    if args.command == "auth":
        return handle_auth(args, config)
    if args.command == "curate":
        return handle_curate(args, config)
    if args.command == "explain":
        return handle_explain(args, config)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
