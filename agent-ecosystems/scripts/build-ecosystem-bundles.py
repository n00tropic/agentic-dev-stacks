#!/usr/bin/env python3
"""Build versioned ZIP bundles for agent ecosystems.

- Discovers bundle JSON files.
- Validates bundles and referenced artefacts.
- Runs ecosystem + scenario validation as a preflight.
- Produces ZIPs under dist/bundles and metadata under dist/metadata.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
ECOSYSTEM_ROOT = ROOT / "agent-ecosystems"
SCHEMA_DIR = ECOSYSTEM_ROOT / "schemas"
BUNDLE_SCHEMA_PATH = SCHEMA_DIR / "bundle.schema.json"
BUNDLES_DIR = ECOSYSTEM_ROOT / "bundles"
STACKS_DIR = ECOSYSTEM_ROOT / "stacks"
DIST_DIR = ROOT / "dist"
DIST_BUNDLES = DIST_DIR / "bundles"
DIST_METADATA = DIST_DIR / "metadata"
TEMP_ROOT = DIST_DIR / "tmp"


class BundleError(Exception):
    pass


def run_preflight() -> None:
    cmds = [
        ["python3", str(ECOSYSTEM_ROOT / "scripts" / "validate-ecosystem-configs.py")],
        [
            "python3",
            str(ECOSYSTEM_ROOT / "scripts" / "run-agent-scenarios.py"),
            "--no-output",
        ],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            sys.stderr.write(result.stdout)
            sys.stderr.write(result.stderr)
            raise BundleError(f"Preflight command failed: {' '.join(cmd)}")


def load_schema(path: Path) -> dict:
    if not path.exists():
        raise BundleError(f"Missing schema: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_stacks() -> Dict[str, dict]:
    stacks: Dict[str, dict] = {}
    for stack_path in STACKS_DIR.glob("*.json"):
        data = load_json(stack_path)
        stacks[data["id"]] = data
    return stacks


def validate_bundle(bundle: dict, schema: dict, path: Path) -> List[str]:
    errors: List[str] = []
    validator = Draft202012Validator(schema)
    for err in validator.iter_errors(bundle):
        location = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{path}: {location}: {err.message}")
    return errors


def resolve_artifacts(bundle: dict) -> List[Tuple[str, Path]]:
    resolved: List[Tuple[str, Path]] = []
    for art in bundle.get("artifacts", []):
        abs_path = (ROOT / art).resolve()
        resolved.append((art, abs_path))
    return resolved


def ensure_artifacts_exist(resolved: List[Tuple[str, Path]]) -> None:
    missing = [orig for orig, ap in resolved if not ap.exists()]
    if missing:
        raise BundleError(f"Missing artefacts: {', '.join(missing)}")


def copy_artifacts(resolved: List[Tuple[str, Path]], dest_root: Path) -> None:
    for original, abs_path in resolved:
        target = dest_root / original
        target.parent.mkdir(parents=True, exist_ok=True)
        if abs_path.is_dir():
            shutil.copytree(abs_path, target, dirs_exist_ok=True)
        else:
            shutil.copy2(abs_path, target)


def write_manifest(bundle: dict, stack: dict | None, dest_root: Path) -> None:
    manifest = {
        "id": bundle["id"],
        "version": bundle["version"],
        "os": bundle["os"],
        "stackId": bundle.get("stackId"),
        "artifacts": bundle.get("artifacts", []),
        "built_at": datetime.now(timezone.utc).isoformat(),
    }
    if stack:
        manifest["defaultAgents"] = stack.get("defaultAgents", [])
        manifest["defaultToolsets"] = stack.get("defaultToolsets", [])
    (dest_root / "BUNDLE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_bundle(
    bundle_path: Path, schema: dict, stacks: Dict[str, dict]
) -> Tuple[str, str, str, str | None, Path, str, List[str], List[str]]:
    bundle = load_json(bundle_path)
    errors = validate_bundle(bundle, schema, bundle_path)
    if errors:
        raise BundleError("; ".join(errors))

    bundle_id = bundle["id"]
    version = bundle["version"]
    os_name = bundle["os"]
    if os_name not in {"macos", "windows", "linux"}:
        raise BundleError(f"Invalid os '{os_name}' in {bundle_path}")

    resolved = resolve_artifacts(bundle)
    ensure_artifacts_exist(resolved)

    stack_id = bundle.get("stackId")
    stack = stacks.get(stack_id)

    temp_dir = TEMP_ROOT / f"{bundle_id}-v{version}-{os_name}"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    copy_artifacts(resolved, temp_dir)
    write_manifest(bundle, stack, temp_dir)

    zip_name = f"{bundle_id}-v{version}-{os_name}.zip"
    zip_path = DIST_BUNDLES / zip_name
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.make_archive(zip_path.with_suffix(""), "zip", temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)

    hash_hex = sha256_file(zip_path)
    agents = stack.get("defaultAgents", []) if stack else []
    toolsets = stack.get("defaultToolsets", []) if stack else []
    return bundle_id, version, os_name, stack_id, zip_path, hash_hex, agents, toolsets


def write_checksums(
    built: List[Tuple[str, str, str, str | None, Path, str, List[str], List[str]]],
) -> None:
    by_version: Dict[str, List[Tuple[Path, str]]] = {}
    for _, version, _, _, zip_path, sha, _, _ in built:
        by_version.setdefault(version, []).append((zip_path, sha))

    for version, entries in by_version.items():
        lines = [f"{sha}  {p.name}" for p, sha in entries]
        out_path = DIST_METADATA / f"checksums-v{version}.txt"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(
    built: List[Tuple[str, str, str, str | None, Path, str, List[str], List[str]]],
) -> None:
    index_path = DIST_METADATA / "bundles-index.json"
    entries = []
    for bundle_id, version, os_name, stack_id, zip_path, sha, agents, toolsets in built:
        entries.append(
            {
                "id": bundle_id,
                "version": version,
                "os": os_name,
                "stackId": stack_id,
                "filename": zip_path.name,
                "sha256": sha,
                "agents": agents,
                "toolsets": toolsets,
            }
        )
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def discover_bundles(bundle_id: str | None, os_filter: List[str]) -> List[Path]:
    paths = []
    for path in sorted(BUNDLES_DIR.glob("*.bundle.json")):
        bundle = load_json(path)
        if bundle_id and bundle.get("id") != bundle_id:
            continue
        if os_filter and bundle.get("os") not in os_filter:
            continue
        paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Build agent ecosystem bundles")
    parser.add_argument("--bundle-id", help="Bundle ID to build", default=None)
    parser.add_argument(
        "--os", nargs="*", choices=["macos", "windows", "linux"], help="OS filter"
    )
    args = parser.parse_args()

    DIST_DIR.mkdir(exist_ok=True)
    DIST_BUNDLES.mkdir(parents=True, exist_ok=True)
    DIST_METADATA.mkdir(parents=True, exist_ok=True)
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)

    try:
        run_preflight()
        schema = load_schema(BUNDLE_SCHEMA_PATH)
        stacks = load_stacks()
        bundle_paths = discover_bundles(args.bundle_id, args.os or [])
        if not bundle_paths:
            raise BundleError("No bundles found matching filters")

        built: List[
            Tuple[str, str, str, str | None, Path, str, List[str], List[str]]
        ] = []
        failed = 0
        for path in bundle_paths:
            try:
                result = build_bundle(path, schema, stacks)
                built.append(result)
                bundle_id, version, os_name, _, zip_path, _, _, _ = result
                print(f"Built {bundle_id} ({version} / {os_name}) -> {zip_path.name}")
            except Exception as exc:  # pragma: no cover - build guardrail
                failed += 1
                import traceback

                sys.stderr.write(f"Failed to build {path}: {exc}\n")
                traceback.print_exc()

        if failed:
            raise BundleError(f"{failed} bundle(s) failed")

        if built:
            write_checksums(built)
            write_index(built)

        print(
            f"Summary: discovered={len(bundle_paths)} built={len(built)} failed={failed} output_dir={DIST_BUNDLES}"
        )
        return 0
    except BundleError as exc:
        sys.stderr.write(f"[bundle-builder] Error: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
