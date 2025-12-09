#!/usr/bin/env python3
"""
Check profile invariants across CONTROL.md, profile-map.json, export-map, MCP manifests, and agents.

Hard errors:
- Missing slug in profile-map.json
- Missing slug in export-map
- Missing pack mapping
- Missing MCP manifest for a known profile

Warnings (non-fatal):
- Missing dist .code-profile
- Missing agents directory for the slug
- Orphaned SSoT assets (tasks/launch/snippets/keybindings) that reference unknown slugs
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / "CONTROL.md"
PROFILE_MAP = ROOT / "vscode" / "profile-map.json"
EXPORT_MAP = ROOT / "vscode" / "export-map.yaml"
DIST_PROFILES = ROOT / "vscode" / "profiles-dist"
AGENTS_ROOT = ROOT / "agents"
PACKS = ROOT / "vscode" / "packs"


def parse_control_slugs(path: Path) -> List[str]:
    """Extract profile slugs from the CONTROL.md table."""
    text = path.read_text(encoding="utf-8")
    slugs: List[str] = []
    for line in text.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        slug = parts[2]
        if not slug or slug in {"Slug", "---------------------"}:
            continue
        slugs.append(slug)
    return slugs


def load_json_file(path: Path) -> Dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - CLI guardrail
        raise SystemExit(f"ERROR: Invalid JSON in {path}: {exc}")
    except FileNotFoundError:
        raise SystemExit(f"ERROR: Missing required file {path}")


def load_export_map(path: Path) -> Dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Best-effort YAML fallback if someone swaps formats later
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise SystemExit(
                f"ERROR: {path} is not valid JSON and PyYAML is unavailable: {exc}"
            )
        return yaml.safe_load(text) or {}


def mcp_manifest_exists(slug: str, packs_for_slug: List[str]) -> bool:
    for pack in packs_for_slug:
        candidate = PACKS / pack / "mcp" / f"servers.{slug}.json"
        if candidate.is_file():
            return True
    return False


def warn_orphan_assets(known_slugs: Set[str]) -> List[str]:
    warnings: List[str] = []
    patterns = [
        ("tasks", r"tasks\.(?P<slug>.+)\.json"),
        ("launch", r"launch\.(?P<slug>.+)\.json"),
        ("snippets", r"snippets\.(?P<slug>.+)\.code-snippets"),
        ("keybindings", r"keybindings\.(?P<slug>.+)\.json"),
    ]
    for pack_dir in PACKS.glob("*"):
        if not pack_dir.is_dir():
            continue
        for subdir, pattern in patterns:
            p = re.compile(pattern)
            asset_dir = pack_dir / subdir
            if not asset_dir.is_dir():
                continue
            for file in asset_dir.iterdir():
                match = p.match(file.name)
                if not match:
                    continue
                slug = match.group("slug")
                if slug not in known_slugs:
                    warnings.append(
                        f"WARNING: Orphan {subdir} asset for unknown slug '{slug}' at {file}"
                    )
    return warnings


def main() -> int:
    control_slugs = parse_control_slugs(CONTROL)
    profile_map = load_json_file(PROFILE_MAP)
    export_map = load_export_map(EXPORT_MAP)
    export_profiles = (export_map.get("profiles") or {}) if isinstance(export_map, dict) else {}

    errors: List[str] = []
    warnings: List[str] = []

    for slug in sorted(control_slugs):
        profile_entry = profile_map.get(slug)
        if not profile_entry:
            errors.append(f"ERROR: profile '{slug}' missing from profile-map.json")
            packs_for_slug = []
        else:
            packs_for_slug = profile_entry.get("packs") or []
            if not isinstance(packs_for_slug, list):
                packs_for_slug = []
                errors.append(
                    f"ERROR: profile '{slug}' packs entry is invalid in profile-map.json"
                )

        export_entry = export_profiles.get(slug)
        if not export_entry:
            errors.append(f"ERROR: profile '{slug}' missing from export-map")
        else:
            pack_from_export = export_entry.get("pack")
            if pack_from_export and pack_from_export not in (packs_for_slug or []):
                # Normalise pack list if export map has info but profile map did not
                if not packs_for_slug:
                    packs_for_slug = [pack_from_export]

        if not packs_for_slug:
            errors.append(f"ERROR: profile '{slug}' has no pack mapping")
        elif not mcp_manifest_exists(slug, packs_for_slug):
            errors.append(
                f"ERROR: MCP profile '{slug}' missing manifest servers.{slug}.json under packs {packs_for_slug}"
            )

        dist_profile = DIST_PROFILES / f"{slug}.code-profile"
        if not dist_profile.is_file():
            warnings.append(f"WARNING: dist profile missing for slug '{slug}' at {dist_profile}")

        agent_dir = AGENTS_ROOT / slug
        if not agent_dir.is_dir() or not any(agent_dir.glob("*.agent.md")):
            warnings.append(f"WARNING: no agents found for slug '{slug}' under {agent_dir}")

    # Check for orphan assets referencing unknown slugs
    warnings.extend(warn_orphan_assets(set(control_slugs)))

    for line in warnings:
        print(line)
    for line in errors:
        print(line)

    if errors:
        return 1
    print(f"All {len(control_slugs)} profiles satisfy invariants.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
