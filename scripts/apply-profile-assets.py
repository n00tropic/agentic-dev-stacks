#!/usr/bin/env python3
"""
Helper to inspect or apply exported profile assets (.vscode tasks/launch/snippets/keybindings) and MCP TOML.

Examples:
  python scripts/apply-profile-assets.py --slug core-base-dev --dry-run
  python scripts/apply-profile-assets.py --slug fullstack-js-ts --apply --target-dir /path/to/workspace
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
VSCODE = ROOT / "vscode"
EXPORTS = VSCODE / "exports" / "workspaces"
EXPORT_MAP = VSCODE / "export-map.yaml"


def load_export_map() -> Dict:
    try:
        return json.loads(EXPORT_MAP.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: export map missing at {EXPORT_MAP}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: export-map.yaml is not valid JSON: {exc}")


def ensure_known_slug(slug: str) -> None:
    profiles = load_export_map().get("profiles", {})
    if slug not in profiles:
        raise SystemExit(f"ERROR: Unknown slug '{slug}' (not in export-map)")


def ensure_export(slug: str) -> Path:
    ws_dir = EXPORTS / slug
    if ws_dir.exists():
        return ws_dir
    print(f"[{slug}] Export not found; generating via export-packs.py")
    cmd = [sys.executable, str(VSCODE / "scripts" / "export-packs.py"), slug]
    result = subprocess.run(cmd, cwd=VSCODE)
    if result.returncode != 0:
        raise SystemExit(f"ERROR: export-packs.py failed for {slug}")
    if not ws_dir.exists():
        raise SystemExit(f"ERROR: Export still missing at {ws_dir}")
    return ws_dir


def collect_assets(ws_dir: Path, target_dir: Path) -> List[Tuple[Path, Path]]:
    actions: List[Tuple[Path, Path]] = []
    vscode_dir = ws_dir / ".vscode"
    if not vscode_dir.is_dir():
        return actions

    def add_if_exists(filename: str, dest_name: str | None = None) -> None:
        src = vscode_dir / filename
        if src.is_file():
            dest = target_dir / ".vscode" / (dest_name or filename)
            if src.resolve() == dest.resolve():
                return
            actions.append((src, dest))

    add_if_exists("tasks.json")
    add_if_exists("launch.json")
    add_if_exists("keybindings.json")

    snippets_dir = vscode_dir / "snippets"
    if snippets_dir.is_dir():
        for snippet_file in sorted(snippets_dir.glob("*.code-snippets")):
            dest = target_dir / ".vscode" / "snippets" / snippet_file.name
            if snippet_file.resolve() == dest.resolve():
                continue
            actions.append((snippet_file, dest))

    return actions


def print_actions(actions: List[Tuple[Path, Path]]) -> None:
    if not actions:
        print("No tasks/launch/snippets/keybindings found for this profile.")
        return
    print("Planned actions:")
    for src, dest in actions:
        print(f"- copy {src} -> {dest}")


def apply_actions(actions: List[Tuple[Path, Path]]) -> None:
    for src, dest in actions:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"Copied {src} -> {dest}")


def generate_mcp_snippet(slug: str) -> str | None:
    cmd = [sys.executable, str(VSCODE / "scripts" / "merge-mcp-fragments.py"), slug]
    result = subprocess.run(cmd, cwd=VSCODE)
    if result.returncode != 0:
        print(f"[{slug}] merge-mcp-fragments.py failed; skip MCP snippet", file=sys.stderr)
        return None
    generated = VSCODE / "codex-mcp.generated.toml"
    if not generated.is_file():
        return None
    return generated.read_text(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="Profile slug to apply assets for")
    parser.add_argument(
        "--target-dir",
        help="Target workspace directory (default: exports/workspaces/<slug>)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Preview actions without copying files (default)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply assets to the target directory",
    )
    mcp_group = parser.add_mutually_exclusive_group()
    mcp_group.add_argument(
        "--print-mcp",
        dest="print_mcp",
        action="store_true",
        help="Print merged MCP TOML snippet for this profile (default)",
    )
    mcp_group.add_argument(
        "--no-print-mcp",
        dest="print_mcp",
        action="store_false",
        help="Skip MCP TOML output",
    )
    parser.set_defaults(print_mcp=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    slug = args.slug

    # Normalise dry-run vs apply flags
    dry_run = True
    if args.apply:
        dry_run = False

    ensure_known_slug(slug)

    ws_dir = ensure_export(slug)
    target_dir = Path(args.target_dir) if args.target_dir else ws_dir

    if not target_dir.exists() and not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    actions = collect_assets(ws_dir, target_dir)

    mode_label = "DRY RUN" if dry_run else "APPLY"
    print(f"[{slug}] apply-profile-assets ({mode_label})")
    print(f"- source export: {ws_dir}")
    print(f"- target workspace: {target_dir}")
    print_actions(actions)

    if not dry_run and actions:
        apply_actions(actions)

    if args.print_mcp:
        snippet = generate_mcp_snippet(slug)
        if snippet:
            print("\n# MCP snippet (copy into ~/.codex/config.toml)")
            print(snippet.strip())
        else:
            print("\nNo MCP snippet available; ensure manifests exist for this slug.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
