#!/usr/bin/env python3
"""
Build workspace bundles for one or more profile slugs.

Bundles live under vscode/exports/bundles/<slug>/ (gitignored) and include:
  - workspace/.code-workspace and .vscode assets
  - extensions list (from export or packs)
  - MCP manifest + generated codex-mcp TOML
  - prompts (best-effort match)
  - per-OS install scripts
  - README and metadata

Usage:
  python scripts/build-bundles.py            # all slugs from CONTROL.md
  python scripts/build-bundles.py slug1 slug2

Note: This script only writes under vscode/exports/** and does not touch user dotfiles.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
VSCODE = ROOT / "vscode"
EXPORTS = VSCODE / "exports"
WORKSPACES = EXPORTS / "workspaces"
BUNDLES = EXPORTS / "bundles"
PACKS = VSCODE / "packs"
PROMPTS = ROOT / "prompts" / "packs"
AGENTS_ROOT = ROOT / "agents"
CONTROL = ROOT / "CONTROL.md"
VSCODE_DIRNAME = ".vscode"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "slugs", nargs="*", help="Profile slugs to bundle; default: all from CONTROL.md"
    )
    return ap.parse_args()


def slugs_from_control() -> List[Tuple[str, str]]:
    rows = []
    for line in CONTROL.read_text().splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        pack, slug = parts[1], parts[2]
        if slug in {"Slug", "---------------------"}:
            continue
        if slug and pack:
            rows.append((slug, pack))
    return rows


def ensure_exports(slug: str):
    ws_dir = WORKSPACES / slug
    if ws_dir.exists():
        return
    print(f"[bundles] export missing for {slug}; running export-packs.py")
    subprocess.run(
        [sys.executable, str(VSCODE / "scripts" / "export-packs.py"), slug],
        cwd=VSCODE,
        check=True,
    )


def load_profile_meta(slug: str, pack: str) -> Dict[str, str]:
    # Pull a friendly name from CONTROL.md; fallback to slug
    name = slug
    for line in CONTROL.read_text().splitlines():
        if slug in line and pack in line and "|" in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 4:
                name = parts[3]
                break
    return {"slug": slug, "pack": pack, "profile_name": name}


def copy_workspace(slug: str, bundle_dir: Path):
    ws_src = WORKSPACES / slug
    if not ws_src.exists():
        raise FileNotFoundError(f"workspace export missing: {ws_src}")
    dest_ws = bundle_dir / "workspace"
    dest_ws.mkdir(parents=True, exist_ok=True)
    for item in [f"{slug}.code-workspace", VSCODE_DIRNAME]:
        src = ws_src / item
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dest_ws / VSCODE_DIRNAME, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dest_ws / src.name)


def ensure_extensions_list(slug: str, pack: str, bundle_dir: Path):
    dest = bundle_dir / "workspace" / VSCODE_DIRNAME / "extensions.list"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return
    src = PACKS / pack / "extensions" / f"extensions.{slug}.txt"
    if not src.exists():
        raise FileNotFoundError(f"extensions list not found: {src}")
    shutil.copy2(src, dest)


def copy_mcp(slug: str, pack: str, bundle_dir: Path):
    mcp_src = PACKS / pack / "mcp" / f"servers.{slug}.json"
    if mcp_src.exists():
        dest_dir = bundle_dir / "mcp"
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(mcp_src, dest_dir / mcp_src.name)


def generate_mcp_toml(slug: str, bundle_dir: Path):
    dest_dir = bundle_dir / "mcp"
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_file = dest_dir / f"codex-mcp.{slug}.generated.toml"
    cmd = [sys.executable, str(VSCODE / "scripts" / "merge-mcp-fragments.py"), slug]
    subprocess.run(cmd, cwd=VSCODE, check=True)
    gen = VSCODE / "codex-mcp.generated.toml"
    if gen.exists():
        shutil.copy2(gen, out_file)
        gen.unlink()


def copy_prompts(slug: str, bundle_dir: Path):
    dest = bundle_dir / "prompts"
    dest.mkdir(parents=True, exist_ok=True)
    candidates = list(PROMPTS.glob(f"{slug}*.md"))
    if not candidates:
        base = PROMPTS / "core-engineering.md"
        if base.exists():
            candidates = [base]
    for p in candidates:
        shutil.copy2(p, dest / p.name)


def copy_agents(slug: str, bundle_dir: Path):
    src_dir = AGENTS_ROOT / slug
    if not src_dir.exists():
        return
    dest = bundle_dir / "workspace" / ".github" / "agents"
    dest.mkdir(parents=True, exist_ok=True)
    for agent_file in src_dir.glob("*.agent.md"):
        shutil.copy2(agent_file, dest / agent_file.name)


def write_meta(meta: Dict[str, str], bundle_dir: Path):
    meta_dir = bundle_dir / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta["generated_at"] = meta.get("generated_at") or "TBD"
    (meta_dir / "bundle.meta.json").write_text(json.dumps(meta, indent=2))


INSTALL_SH = """#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
PROFILE_NAME="{profile_name}"
SLUG="{slug}"

command -v code >/dev/null 2>&1 || {{ echo "VS Code CLI 'code' not found" >&2; exit 1; }}

EXT_LIST="$ROOT/workspace/.vscode/extensions.list"
if [[ ! -f "$EXT_LIST" ]]; then
  echo "extensions.list missing at $EXT_LIST" >&2
  exit 1
fi

echo "[${{SLUG}}] Ensuring profile '${{PROFILE_NAME}}' exists"
code --profile "${{PROFILE_NAME}}" --list-extensions >/dev/null 2>&1 || true

echo "[${{SLUG}}] Installing extensions"
if [[ -s "$EXT_LIST" ]]; then
  xargs -n1 code --install-extension --profile "${{PROFILE_NAME}}" < "$EXT_LIST"
else
  echo "No extensions listed; skipping install" >&2
fi

WS_FILE="$ROOT/workspace/{slug}.code-workspace"
if [[ -f "$WS_FILE" ]]; then
  echo "[${{SLUG}}] Opening workspace"
  code "$WS_FILE" --profile "${{PROFILE_NAME}}" --reuse-window >/dev/null 2>&1 || true
fi

echo "Done."
"""

INSTALL_PS = r"""# Requires VS Code CLI 'code' in PATH.
$Root = (Resolve-Path "$PSScriptRoot\..\").Path
$ProfileName = "{profile_name}"
$Slug = "{slug}"

if (-not (Get-Command code -ErrorAction SilentlyContinue)) {{
  Write-Error "VS Code CLI 'code' not found"
  exit 1
}}

$ExtList = Join-Path $Root 'workspace/.vscode/extensions.list'
if (-not (Test-Path $ExtList)) {{
  Write-Error "extensions.list missing at $ExtList"
  exit 1
}}

Write-Host "[$Slug] Ensuring profile '$ProfileName' exists"
code --profile "$ProfileName" --list-extensions *> $null

Write-Host "[$Slug] Installing extensions"
if ((Get-Content $ExtList | Where-Object {{$_ -ne ''}}).Count -gt 0) {{
  Get-Content $ExtList | Where-Object {{$_ -ne ''}} | ForEach-Object {{
    code --install-extension $_ --profile "$ProfileName"
  }}
}} else {{
  Write-Warning "No extensions listed; skipping install"
}}

$WsFile = Join-Path $Root "workspace/{slug}.code-workspace"
if (Test-Path $WsFile) {{
  Write-Host "[$Slug] Opening workspace"
  code $WsFile --profile "$ProfileName" --reuse-window *> $null
}}

Write-Host "Done."
"""


def write_install_scripts(meta: Dict[str, str], bundle_dir: Path):
    scripts_dir = bundle_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    (scripts_dir / "install-macos.sh").write_text(INSTALL_SH.format(**meta))
    (scripts_dir / "install-linux.sh").write_text(INSTALL_SH.format(**meta))
    (scripts_dir / "Install-Windows.ps1").write_text(INSTALL_PS.format(**meta))
    for sh in ["install-macos.sh", "install-linux.sh"]:
        os.chmod(scripts_dir / sh, 0o700)


def write_readme(meta: Dict[str, str], bundle_dir: Path):
    slug = meta["slug"]
    profile = meta["profile_name"]
    text = f"""# {profile} bundle ({slug})

This bundle is generated from agentic-dev-stacks. It contains a ready-to-use VS Code workspace and profile assets for **{profile}**.

## Quickstart (macOS/Linux)
```bash
./scripts/install-macos.sh   # or install-linux.sh
```

## Quickstart (Windows PowerShell)
```powershell
./scripts/Install-Windows.ps1
```

## What's inside
- workspace/ – .code-workspace and .vscode (settings, extensions.list, optional launch/tasks)
- mcp/ – servers manifest and generated codex-mcp TOML (copy snippets into ~/.codex/config.toml manually)
- prompts/ – suggested prompt packs for this stack
- scripts/ – per-OS installers using VS Code CLI only
- meta/bundle.meta.json – slug, pack, profile name

## Regenerate
```bash
cd vscode
python scripts/build-bundles.py {slug}
```

> Safety: installers use `code --profile` and never touch global settings or dotfiles directly. Copy MCP TOML blocks by hand.
"""
    (bundle_dir / "README.md").write_text(text.strip() + "\n")


def clean_bundle_dir(bundle_dir: Path):
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)


def build_bundle(slug: str, pack: str):
    ensure_exports(slug)
    bundle_dir = BUNDLES / slug
    clean_bundle_dir(bundle_dir)
    meta = load_profile_meta(slug, pack)
    copy_workspace(slug, bundle_dir)
    ensure_extensions_list(slug, pack, bundle_dir)
    copy_mcp(slug, pack, bundle_dir)
    generate_mcp_toml(slug, bundle_dir)
    copy_prompts(slug, bundle_dir)
    copy_agents(slug, bundle_dir)
    write_meta(meta, bundle_dir)
    write_install_scripts(meta, bundle_dir)
    write_readme(meta, bundle_dir)
    print(f"[bundles] built {slug} -> {bundle_dir}")


def zip_bundle(slug: str):
    bundle_dir = BUNDLES / slug
    if not bundle_dir.exists():
        raise FileNotFoundError(f"bundle directory missing: {bundle_dir}")
    zip_path = BUNDLES / f"{slug}-bundle.zip"
    tmp_zip = zip_path.with_suffix(".zip.tmp")
    if tmp_zip.exists():
        tmp_zip.unlink()
    with zipfile.ZipFile(tmp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in bundle_dir.rglob("*"):
            if path.name in {".DS_Store"}:
                continue
            zf.write(path, arcname=path.relative_to(bundle_dir.parent))
    tmp_zip.replace(zip_path)
    print(f"[bundles] zipped {slug} -> {zip_path}")


def main():
    args = parse_args()
    slugs = args.slugs or [s for s, _ in slugs_from_control()]
    pack_lookup = dict(slugs_from_control())
    for slug in slugs:
        pack = pack_lookup.get(slug)
        if not pack:
            print(f"[warn] slug {slug} not in CONTROL.md; skipping", file=sys.stderr)
            continue
        build_bundle(slug, pack)
        zip_bundle(slug)


if __name__ == "__main__":
    main()
