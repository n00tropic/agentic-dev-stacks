#!/usr/bin/env python3
"""Export VS Code packs to workspace-ready folders.

Usage (run from repo root or ./vscode):
    cd vscode
    python scripts/export-packs.py core-base-dev fullstack-js-ts

Exports live under vscode/exports/ and are safe to overwrite.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

EXPORT_MAP_FILENAME = "vscode/export-map.yaml"


def load_export_map(repo_root: Path) -> Dict[str, Any]:
    """Load the export map (YAML encoded as JSON-compatible) into a dict."""
    path = repo_root / EXPORT_MAP_FILENAME
    if not path.exists():
        raise FileNotFoundError(f"Missing export map: {path}")
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"export-map.yaml is not valid JSON/YAML: {exc}") from exc


def ensure_exports_root(repo_root: Path, workspace_dir: Path) -> None:
    exports_root = (repo_root / "vscode" / "exports").resolve()
    target = workspace_dir.resolve()
    if not str(target).startswith(str(exports_root)):
        raise ValueError(f"Refusing to write outside exports/ ({target})")
    workspace_dir.mkdir(parents=True, exist_ok=True)


def read_extension_ids(source: Path) -> list[str]:
    if not source.exists():
        raise FileNotFoundError(f"Missing extensions list: {source}")
    lines = source.read_text(encoding="utf-8").splitlines()
    cleaned = []
    for line in lines:
        trimmed = line.strip()
        if not trimmed or trimmed.startswith("#"):
            continue
        cleaned.append(trimmed)
    return cleaned


def copy_settings(source: Path, dest: Path) -> Dict[str, Any]:
    if not source.exists():
        raise FileNotFoundError(f"Missing settings: {source}")
    text = source.read_text(encoding="utf-8")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return json.loads(text)


def write_extensions_list(ext_ids: list[str], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(ext_ids) + ("\n" if ext_ids else ""), encoding="utf-8")


def write_workspace_file(
    profile_name: str,
    dest: Path,
    settings: Dict[str, Any],
    extensions: list[str],
) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    workspace = {
        "folders": [{"path": ".."}],
        "settings": settings,
        "name": profile_name,
    }
    if extensions:
        workspace["extensions"] = {"recommendations": extensions}
    dest.write_text(json.dumps(workspace, indent=2) + "\n", encoding="utf-8")


def export_profile(slug: str, config: Dict[str, Any], repo_root: Path) -> None:
    required = {"pack", "workspace_dir", "workspace_file", "profile_name"}
    missing = required - set(config.keys())
    if missing:
        raise ValueError(f"Profile '{slug}' missing keys: {', '.join(sorted(missing))}")

    pack = config["pack"]
    workspace_dir = (repo_root / config["workspace_dir"]).resolve()
    workspace_file = (repo_root / config["workspace_file"]).resolve()
    profile_name = config["profile_name"]

    ensure_exports_root(repo_root, workspace_dir)

    pack_root = repo_root / "vscode" / "packs" / pack
    settings_src = pack_root / "settings" / f"settings.{slug}.json"
    extensions_src = pack_root / "extensions" / f"extensions.{slug}.txt"

    settings_data = copy_settings(
        settings_src, workspace_dir / ".vscode" / "settings.json"
    )

    extensions = read_extension_ids(extensions_src)
    write_extensions_list(extensions, workspace_dir / ".vscode" / "extensions.list")

    write_workspace_file(profile_name, workspace_file, settings_data, extensions)

    print(f"[OK] {slug}: exported to {workspace_dir}")


def main(argv: list[str]) -> int:
    if len(argv) < 1:
        print(
            "Usage: python scripts/export-packs.py <slug> [<slug> ...]", file=sys.stderr
        )
        return 1

    # scripts/ is two levels below the repo root: <repo>/vscode/scripts/export-packs.py
    repo_root = Path(__file__).resolve().parents[2]
    try:
        export_map = load_export_map(repo_root)
    except Exception as exc:  # pragma: no cover - CLI guardrail
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    profiles = export_map.get("profiles", {}) if isinstance(export_map, dict) else {}
    success = 0

    for slug in argv:
        config = profiles.get(slug)
        if not config:
            print(f"[SKIP] Unknown profile slug: {slug}")
            continue
        try:
            export_profile(slug, config, repo_root)
            success += 1
        except Exception as exc:
            print(f"[FAIL] {slug}: {exc}")

    if success == 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
