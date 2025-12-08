#!/usr/bin/env python3
"""Generate minimal .code-profile files from pack settings and extensions.

The output mirrors VS Code's `IUserDataProfileTemplate` surface: `name`,
`settings` (JSON as string), and `extensions` (JSON as string). We omit
`shortName`, `globalState`, `tasks`, `snippets`, and `keybindings` to keep
profiles minimal and machine-agnostic. Settings and extensions are pulled
directly from `vscode/packs/**` (source of truth).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

# Internal shape (pre-serialisation):
# - name: str
# - settings: dict (standard settings.json)
# - extensions: list[str] (extension ids like "publisher.extension")
#
# Serialised shape (IUserDataProfileTemplate):
# - name: str
# - settings: stringified JSON object: { "settings": "<settings.json text>" }
# - extensions: stringified JSON array of { identifier: { id } }

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP = ROOT / "vscode" / "profile-map.json"
DEFAULT_OUT_DIR = ROOT / "vscode" / "profiles-generated"


def load_map(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Profile map not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Profile map is invalid JSON: {path}\n{exc}")


def load_settings(path: Path) -> Dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing settings file: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Settings JSON invalid: {path}\n{exc}")


def load_extensions(path: Path) -> List[str]:
    if not path.is_file():
        raise SystemExit(f"Missing extensions file: {path}")
    extensions: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        extensions.append(stripped)
    return extensions


def merge_settings(settings_list: List[Dict]) -> Dict:
    merged: Dict = {}
    for settings in settings_list:
        merged.update(settings)
    return merged


def merge_extensions(extension_lists: List[List[str]]) -> List[str]:
    seen = set()
    merged: List[str] = []
    for ext_list in extension_lists:
        for ext in ext_list:
            if ext in seen:
                continue
            seen.add(ext)
            merged.append(ext)
    return merged


def serialise_profile(name: str, settings: Dict, extensions: List[str]) -> Dict:
    inner_settings = {
        "settings": json.dumps(settings or {}, indent=2, ensure_ascii=True)
    }
    extensions_json = [{"identifier": {"id": ext_id}} for ext_id in (extensions or [])]

    template: Dict = {"name": name}
    template["settings"] = json.dumps(inner_settings, indent=2, ensure_ascii=True)
    template["extensions"] = json.dumps(extensions_json, indent=2, ensure_ascii=True)
    return template


def validate_profile_file(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))

    for key in ("settings", "extensions"):
        if key not in data:
            raise ValueError(f"{path}: missing required field '{key}'")
        if not isinstance(data[key], str):
            raise ValueError(f"{path}: field '{key}' must be a string")
        inner = json.loads(data[key])
        if key == "settings":
            if not isinstance(inner, dict):
                raise ValueError(f"{path}: settings inner JSON must be an object")
            if "settings" not in inner or not isinstance(inner["settings"], str):
                raise ValueError(
                    f"{path}: settings inner JSON must contain string field 'settings'"
                )
        if key == "extensions":
            if not isinstance(inner, list):
                raise ValueError(f"{path}: extensions inner JSON must be a list")
            for idx, item in enumerate(inner):
                ident = item.get("identifier", {}) if isinstance(item, dict) else None
                ext_id = ident.get("id") if isinstance(ident, dict) else None
                if not isinstance(ext_id, str) or not ext_id.strip():
                    raise ValueError(f"{path}: extensions[{idx}] missing identifier.id")


def generate_profile(slug: str, entry: dict, out_dir: Path) -> Path:
    name = entry.get("name")
    packs = entry.get("packs") or []

    if not name or not packs:
        raise SystemExit(f"Profile '{slug}' is missing 'name' or 'packs' in the map")

    settings_list: List[Dict] = []
    ext_lists: List[List[str]] = []

    for pack in packs:
        pack_dir = ROOT / "vscode" / "packs" / pack
        settings_path = pack_dir / "settings" / f"settings.{slug}.json"
        extensions_path = pack_dir / "extensions" / f"extensions.{slug}.txt"

        settings_list.append(load_settings(settings_path))
        ext_lists.append(load_extensions(extensions_path))

    profile_template = serialise_profile(
        name=name,
        settings=merge_settings(settings_list),
        extensions=merge_extensions(ext_lists),
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"{slug}.code-profile"
    dest.write_text(
        json.dumps(profile_template, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    validate_profile_file(dest)
    return dest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate minimal .code-profile files from packs"
    )
    parser.add_argument(
        "--map",
        dest="map_path",
        default=DEFAULT_MAP,
        type=Path,
        help="Path to profile-map.json",
    )
    parser.add_argument(
        "--out",
        dest="out_dir",
        default=DEFAULT_OUT_DIR,
        type=Path,
        help="Output directory for generated profiles",
    )
    parser.add_argument(
        "--slug",
        dest="slugs",
        action="append",
        help="Limit generation to specific slugs (repeatable)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile_map = load_map(args.map_path)

    targets = args.slugs if args.slugs else sorted(profile_map.keys())
    generated: List[Path] = []

    for slug in targets:
        entry = profile_map.get(slug)
        if entry is None:
            print(f"Skipping unknown slug '{slug}' (not in map)")
            continue
        dest = generate_profile(slug, entry, args.out_dir)
        generated.append(dest)

    if generated:
        print("Generated profiles:")
        for path in generated:
            print(f"- {path.relative_to(ROOT)}")
    else:
        print("No profiles generated; check --slug filters or map content")

    return 0


if __name__ == "__main__":
    sys.exit(main())
