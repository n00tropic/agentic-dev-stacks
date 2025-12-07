#!/usr/bin/env python3
"""
Generate standalone installation scripts for all profile slugs.

This script reads profile metadata from export-map.yaml and CONTROL.md,
then generates Unix shell and PowerShell installation scripts for each profile.

The generated scripts are idempotent and placed in vscode/scripts/ with
naming conventions:
  - install-<slug>.sh (macOS/Linux)
  - Install-<Slug>.ps1 (Windows, with PascalCase slug)

Usage:
  python scripts/generate-install-scripts.py              # all profiles
  python scripts/generate-install-scripts.py slug1 slug2  # specific profiles
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[2]
VSCODE = ROOT / "vscode"
SCRIPTS = VSCODE / "scripts"
CONTROL = ROOT / "CONTROL.md"
EXPORT_MAP = VSCODE / "export-map.yaml"

# Shell script template (macOS/Linux)
INSTALL_SH_TEMPLATE = '''#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
REPO_ROOT="$(cd "${{SCRIPT_DIR}}/../.." && pwd)"
VSCODE_DIR="${{REPO_ROOT}}/vscode"
PYTHON_BIN="$(command -v python3 || command -v python || true)"

PROFILE_SLUG="{slug}"
PROFILE_NAME="{profile_name}"
PACK="{pack}"
EXPORT_DIR="${{VSCODE_DIR}}/exports/workspaces/${{PROFILE_SLUG}}"
WORKSPACE_FILE="${{EXPORT_DIR}}/${{PROFILE_SLUG}}.code-workspace"
PACK_EXTENSIONS="${{VSCODE_DIR}}/packs/${{PACK}}/extensions/extensions.${{PROFILE_SLUG}}.txt"

if ! command -v code >/dev/null 2>&1; then
\techo "VS Code CLI 'code' not found in PATH" >&2
\texit 1
fi
if [[ -z ${{PYTHON_BIN}} ]]; then
\techo "Python 3 interpreter not found (python3/python)" >&2
\texit 1
fi

ensure_export() {{
\tif [[ -f ${{WORKSPACE_FILE}} ]]; then
\t\treturn
\tfi
\techo "[${{PROFILE_SLUG}}] Export not found; generating via export-packs.py"
\tif ! "${{PYTHON_BIN}}" "${{VSCODE_DIR}}/scripts/export-packs.py" "${{PROFILE_SLUG}}"; then
\t\techo "[${{PROFILE_SLUG}}] export-packs.py failed" >&2
\t\texit 1
\tfi
\tif [[ ! -f ${{WORKSPACE_FILE}} ]]; then
\t\techo "[${{PROFILE_SLUG}}] Export still missing at ${{WORKSPACE_FILE}}" >&2
\t\texit 1
\tfi
}}

write_extensions_list() {{
\tlocal dest="${{EXPORT_DIR}}/.vscode/extensions.list"
\tif [[ -s ${{dest}} ]]; then
\t\treturn
\tfi
\tmkdir -p "${{EXPORT_DIR}}/.vscode"
\tif [[ ! -f ${{PACK_EXTENSIONS}} ]]; then
\t\techo "[${{PROFILE_SLUG}}] Missing pack extensions file: ${{PACK_EXTENSIONS}}" >&2
\t\texit 1
\tfi
\tgrep -v '^[[:space:]]*$' "${{PACK_EXTENSIONS}}" | grep -v '^#' >"${{dest}}" || true
}}

install_extensions() {{
\tlocal dest="${{EXPORT_DIR}}/.vscode/extensions.list"
\tif [[ ! -s ${{dest}} ]]; then
\t\techo "[${{PROFILE_SLUG}}] No extensions listed; skipping install" >&2
\t\treturn
\tfi
\twhile IFS= read -r ext; do
\t\t[[ -z ${{ext}} ]] && continue
\t\tcode --install-extension "${{ext}}" --profile "${{PROFILE_NAME}}" --force
\tdone <"${{dest}}"
}}

ensure_export
write_extensions_list

echo "[${{PROFILE_SLUG}}] Ensuring profile '${{PROFILE_NAME}}' exists"
code --profile "${{PROFILE_NAME}}" --list-extensions >/dev/null 2>&1 || true

echo "[${{PROFILE_SLUG}}] Installing extensions"
install_extensions

if [[ -f ${{WORKSPACE_FILE}} ]]; then
\techo "[${{PROFILE_SLUG}}] Opening workspace"
\tcode "${{WORKSPACE_FILE}}" --profile "${{PROFILE_NAME}}" --reuse-window >/dev/null 2>&1 || true
fi

echo "[${{PROFILE_SLUG}}] Done"
'''

# PowerShell script template (Windows)
INSTALL_PS1_TEMPLATE = '''#!/usr/bin/env pwsh
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\\..")
$VsCodeDir = Join-Path $RepoRoot "vscode"

$ProfileSlug = "{slug}"
$ProfileName = "{profile_name}"
$Pack = "{pack}"
$ExportDir = Join-Path $VsCodeDir "exports/workspaces/$ProfileSlug"
$WorkspaceFile = Join-Path $ExportDir "$ProfileSlug.code-workspace"
$PackExtensions = Join-Path $VsCodeDir "packs/$Pack/extensions/extensions.$ProfileSlug.txt"

if (-not (Get-Command code -ErrorAction SilentlyContinue)) {{
  Write-Error "VS Code CLI 'code' not found in PATH"
  exit 1
}}
$PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $PythonCmd) {{ $PythonCmd = Get-Command python -ErrorAction SilentlyContinue }}
if (-not $PythonCmd) {{
  Write-Error "Python 3 interpreter not found (python3/python)"
  exit 1
}}
$PythonPath = $PythonCmd.Source

function Test-ExportExists {{
  if (Test-Path $WorkspaceFile) {{ return }}
  Write-Host "[$ProfileSlug] Export not found; generating via export-packs.py"
  $proc = Start-Process -FilePath $PythonPath -ArgumentList @("$($VsCodeDir)/scripts/export-packs.py", $ProfileSlug) -WorkingDirectory $VsCodeDir -Wait -PassThru
  if ($proc.ExitCode -ne 0) {{
    Write-Error "[$ProfileSlug] export-packs.py failed"
    exit 1
  }}
  if (-not (Test-Path $WorkspaceFile)) {{
    Write-Error "[$ProfileSlug] Export still missing at $WorkspaceFile"
    exit 1
  }}
}}

function Set-ExtensionsList {{
  $dest = Join-Path $ExportDir ".vscode/extensions.list"
  if (Test-Path $dest -and (Get-Item $dest).Length -gt 0) {{ return }}
  New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
  if (-not (Test-Path $PackExtensions)) {{
    Write-Error "[$ProfileSlug] Missing pack extensions file: $PackExtensions"
    exit 1
  }}
  Get-Content $PackExtensions | Where-Object {{ $_ -and (-not ($_ -match '^#')) }} | Set-Content $dest
}}

function Install-Extensions {{
  $dest = Join-Path $ExportDir ".vscode/extensions.list"
  $entries = @()
  if (Test-Path $dest) {{
    $entries = Get-Content $dest | Where-Object {{ $_ }}
  }}
  if (-not (Test-Path $dest) -or $entries.Count -eq 0) {{
    Write-Warning "[$ProfileSlug] No extensions listed; skipping install"
    return
  }}
  $entries | ForEach-Object {{
    code --install-extension $_ --profile "$ProfileName" --force
  }}
}}

Test-ExportExists
Set-ExtensionsList

Write-Host "[$ProfileSlug] Ensuring profile '$ProfileName' exists"
code --profile "$ProfileName" --list-extensions *> $null

Write-Host "[$ProfileSlug] Installing extensions"
Install-Extensions

if (Test-Path $WorkspaceFile) {{
  Write-Host "[$ProfileSlug] Opening workspace"
  code $WorkspaceFile --profile "$ProfileName" --reuse-window *> $null
}}

Write-Host "[$ProfileSlug] Done"
'''


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "slugs",
        nargs="*",
        help="Profile slugs to generate scripts for; default: all from export-map.yaml"
    )
    return ap.parse_args()


def load_export_map() -> Dict[str, Dict[str, str]]:
    """Load profile metadata from export-map.yaml (it's actually JSON)"""
    if not EXPORT_MAP.exists():
        raise FileNotFoundError(f"export-map.yaml not found at {EXPORT_MAP}")
    
    content = EXPORT_MAP.read_text()
    data = json.loads(content)
    return data.get("profiles", {})


def slugs_from_control() -> List[str]:
    """Extract all profile slugs from CONTROL.md"""
    slugs = []
    for line in CONTROL.read_text().splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        slug = parts[2]
        if slug in {"Slug", "---------------------"}:
            continue
        if slug:
            slugs.append(slug)
    return slugs


def to_pascal_case(slug: str) -> str:
    """Convert slug to PascalCase for PowerShell script names"""
    return "".join(word.capitalize() for word in slug.split("-"))


def generate_install_script(slug: str, profile_data: Dict[str, str]):
    """Generate both shell and PowerShell installation scripts for a profile"""
    pack = profile_data.get("pack", "")
    profile_name = profile_data.get("profile_name", slug)
    
    # Generate shell script (macOS/Linux)
    sh_content = INSTALL_SH_TEMPLATE.format(
        slug=slug,
        profile_name=profile_name,
        pack=pack
    )
    sh_path = SCRIPTS / f"install-{slug}.sh"
    sh_path.write_text(sh_content)
    sh_path.chmod(0o755)
    print(f"Generated: {sh_path.relative_to(ROOT)}")
    
    # Generate PowerShell script (Windows)
    ps1_content = INSTALL_PS1_TEMPLATE.format(
        slug=slug,
        profile_name=profile_name,
        pack=pack
    )
    pascal_slug = to_pascal_case(slug)
    ps1_path = SCRIPTS / f"Install-{pascal_slug}.ps1"
    ps1_path.write_text(ps1_content)
    print(f"Generated: {ps1_path.relative_to(ROOT)}")


def main():
    args = parse_args()
    export_map = load_export_map()
    
    # Determine which slugs to process
    if args.slugs:
        slugs = args.slugs
    else:
        slugs = list(export_map.keys())
    
    # Validate all slugs exist in export map
    missing = [s for s in slugs if s not in export_map]
    if missing:
        print(f"Error: slugs not found in export-map.yaml: {missing}", file=sys.stderr)
        sys.exit(1)
    
    # Generate scripts
    for slug in slugs:
        generate_install_script(slug, export_map[slug])
    
    print(f"\nGenerated installation scripts for {len(slugs)} profile(s)")


if __name__ == "__main__":
    main()
