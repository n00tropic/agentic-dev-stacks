#!/usr/bin/env python3
"""
Generate pack-level installation scripts in each pack's scripts/{linux,macos,windows}/ directories.

Each pack may contain multiple profiles. The generated scripts allow users to:
1. Install all profiles in a pack
2. Install specific profiles from a pack (via arguments)

The scripts are placed in:
  - vscode/packs/<pack>/scripts/linux/install-profiles.sh
  - vscode/packs/<pack>/scripts/macos/install-profiles.sh
  - vscode/packs/<pack>/scripts/windows/Install-Profiles.ps1

Usage:
  python scripts/generate-pack-scripts.py              # all packs
  python scripts/generate-pack-scripts.py pack1 pack2  # specific packs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[2]
VSCODE = ROOT / "vscode"
PACKS = VSCODE / "packs"
EXPORT_MAP = VSCODE / "export-map.yaml"
CONTROL = ROOT / "CONTROL.md"

# Shell script template for pack installation (macOS/Linux)
PACK_INSTALL_SH_TEMPLATE = '''#!/usr/bin/env bash
set -euo pipefail

# Pack: {pack_name}
# Profiles in this pack: {profile_list}

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}})")" && pwd)"
PACK_DIR="$(cd "${{SCRIPT_DIR}}/../.." && pwd)"
REPO_ROOT="$(cd "${{PACK_DIR}}/../.." && pwd)"
VSCODE_DIR="${{REPO_ROOT}}/vscode"
PYTHON_BIN="$(command -v python3 || command -v python || true)"

PACK="{pack_id}"

# Profile metadata: slug, profile name
declare -A PROFILES=(
{profile_map}
)

if ! command -v code >/dev/null 2>&1; then
\techo "VS Code CLI 'code' not found in PATH" >&2
\texit 1
fi
if [[ -z ${{PYTHON_BIN}} ]]; then
\techo "Python 3 interpreter not found (python3/python)" >&2
\texit 1
fi

ensure_export() {{
\tlocal slug="$1"
\tlocal export_dir="${{VSCODE_DIR}}/exports/workspaces/${{slug}}"
\tlocal workspace_file="${{export_dir}}/${{slug}}.code-workspace"
\t
\tif [[ -f ${{workspace_file}} ]]; then
\t\treturn
\tfi
\techo "[${{slug}}] Export not found; generating via export-packs.py"
\tif ! "${{PYTHON_BIN}}" "${{VSCODE_DIR}}/scripts/export-packs.py" "${{slug}}"; then
\t\techo "[${{slug}}] export-packs.py failed" >&2
\t\treturn 1
\tfi
\tif [[ ! -f ${{workspace_file}} ]]; then
\t\techo "[${{slug}}] Export still missing at ${{workspace_file}}" >&2
\t\treturn 1
\tfi
}}

write_extensions_list() {{
\tlocal slug="$1"
\tlocal export_dir="${{VSCODE_DIR}}/exports/workspaces/${{slug}}"
\tlocal dest="${{export_dir}}/.vscode/extensions.list"
\tlocal pack_extensions="${{VSCODE_DIR}}/packs/${{PACK}}/extensions/extensions.${{slug}}.txt"
\t
\tif [[ -s ${{dest}} ]]; then
\t\treturn
\tfi
\tmkdir -p "${{export_dir}}/.vscode"
\tif [[ ! -f ${{pack_extensions}} ]]; then
\t\techo "[${{slug}}] Missing pack extensions file: ${{pack_extensions}}" >&2
\t\treturn 1
\tfi
\tgrep -v '^[[:space:]]*$' "${{pack_extensions}}" | grep -v '^#' >"${{dest}}" || true
}}

install_extensions() {{
\tlocal slug="$1"
\tlocal profile_name="$2"
\tlocal export_dir="${{VSCODE_DIR}}/exports/workspaces/${{slug}}"
\tlocal dest="${{export_dir}}/.vscode/extensions.list"
\t
\tif [[ ! -s ${{dest}} ]]; then
\t\techo "[${{slug}}] No extensions listed; skipping install" >&2
\t\treturn
\tfi
\twhile IFS= read -r ext; do
\t\t[[ -z ${{ext}} ]] && continue
\t\tcode --install-extension "${{ext}}" --profile "${{profile_name}}" --force
\tdone <"${{dest}}"
}}

install_profile() {{
\tlocal slug="$1"
\tlocal profile_name="$2"
\t
\techo "==== Installing profile: ${{profile_name}} (${{slug}}) ===="
\t
\tensure_export "${{slug}}"
\twrite_extensions_list "${{slug}}"
\t
\techo "[${{slug}}] Ensuring profile '${{profile_name}}' exists"
\tcode --profile "${{profile_name}}" --list-extensions >/dev/null 2>&1 || true
\t
\techo "[${{slug}}] Installing extensions"
\tinstall_extensions "${{slug}}" "${{profile_name}}"
\t
\tlocal workspace_file="${{VSCODE_DIR}}/exports/workspaces/${{slug}}/${{slug}}.code-workspace"
\tif [[ -f ${{workspace_file}} ]]; then
\t\techo "[${{slug}}] Opening workspace"
\t\tcode "${{workspace_file}}" --profile "${{profile_name}}" --reuse-window >/dev/null 2>&1 || true
\tfi
\t
\techo "[${{slug}}] Done"
}}

# Main logic
if [[ $# -eq 0 ]]; then
\t# Install all profiles in this pack
\tfor slug in "${{!PROFILES[@]}}"; do
\t\tprofile_name="${{PROFILES[$slug]}}"
\t\tinstall_profile "${{slug}}" "${{profile_name}}"
\tdone
else
\t# Install specified profiles
\tfor slug in "$@"; do
\t\tif [[ -z ${{PROFILES[$slug]:-}} ]]; then
\t\t\techo "Error: profile '${{slug}}' not in pack ${{PACK}}" >&2
\t\t\texit 1
\t\tfi
\t\tprofile_name="${{PROFILES[$slug]}}"
\t\tinstall_profile "${{slug}}" "${{profile_name}}"
\tdone
fi

echo "Pack installation complete"
'''

# PowerShell script template for pack installation (Windows)
PACK_INSTALL_PS1_TEMPLATE = '''#!/usr/bin/env pwsh
# Pack: {pack_name}
# Profiles in this pack: {profile_list}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackDir = Resolve-Path (Join-Path $ScriptDir "..\\..")
$RepoRoot = Resolve-Path (Join-Path $PackDir "..\\..")
$VsCodeDir = Join-Path $RepoRoot "vscode"

$Pack = "{pack_id}"

# Profile metadata: slug -> profile name
$Profiles = @{{
{profile_map_ps}
}}

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
  param([string]$Slug)
  $exportDir = Join-Path $VsCodeDir "exports/workspaces/$Slug"
  $workspaceFile = Join-Path $exportDir "$Slug.code-workspace"
  
  if (Test-Path $workspaceFile) {{ return }}
  Write-Host "[$Slug] Export not found; generating via export-packs.py"
  $proc = Start-Process -FilePath $PythonPath -ArgumentList @("$($VsCodeDir)/scripts/export-packs.py", $Slug) -WorkingDirectory $VsCodeDir -Wait -PassThru
  if ($proc.ExitCode -ne 0) {{
    Write-Error "[$Slug] export-packs.py failed"
    return $false
  }}
  if (-not (Test-Path $workspaceFile)) {{
    Write-Error "[$Slug] Export still missing at $workspaceFile"
    return $false
  }}
  return $true
}}

function Set-ExtensionsList {{
  param([string]$Slug)
  $exportDir = Join-Path $VsCodeDir "exports/workspaces/$Slug"
  $dest = Join-Path $exportDir ".vscode/extensions.list"
  $packExtensions = Join-Path $VsCodeDir "packs/$Pack/extensions/extensions.$Slug.txt"
  
  if (Test-Path $dest -and (Get-Item $dest).Length -gt 0) {{ return }}
  New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
  if (-not (Test-Path $packExtensions)) {{
    Write-Error "[$Slug] Missing pack extensions file: $packExtensions"
    return $false
  }}
  Get-Content $packExtensions | Where-Object {{ $_ -and (-not ($_ -match '^#')) }} | Set-Content $dest
  return $true
}}

function Install-Extensions {{
  param([string]$Slug, [string]$ProfileName)
  $exportDir = Join-Path $VsCodeDir "exports/workspaces/$Slug"
  $dest = Join-Path $exportDir ".vscode/extensions.list"
  $entries = @()
  if (Test-Path $dest) {{
    $entries = Get-Content $dest | Where-Object {{ $_ }}
  }}
  if (-not (Test-Path $dest) -or $entries.Count -eq 0) {{
    Write-Warning "[$Slug] No extensions listed; skipping install"
    return
  }}
  $entries | ForEach-Object {{
    code --install-extension $_ --profile "$ProfileName" --force
  }}
}}

function Install-Profile {{
  param([string]$Slug, [string]$ProfileName)
  
  Write-Host "==== Installing profile: $ProfileName ($Slug) ===="
  
  if (-not (Test-ExportExists -Slug $Slug)) {{ return }}
  if (-not (Set-ExtensionsList -Slug $Slug)) {{ return }}
  
  Write-Host "[$Slug] Ensuring profile '$ProfileName' exists"
  code --profile "$ProfileName" --list-extensions *> $null
  
  Write-Host "[$Slug] Installing extensions"
  Install-Extensions -Slug $Slug -ProfileName $ProfileName
  
  $workspaceFile = Join-Path $VsCodeDir "exports/workspaces/$Slug/$Slug.code-workspace"
  if (Test-Path $workspaceFile) {{
    Write-Host "[$Slug] Opening workspace"
    code $workspaceFile --profile "$ProfileName" --reuse-window *> $null
  }}
  
  Write-Host "[$Slug] Done"
}}

# Main logic
if ($args.Count -eq 0) {{
  # Install all profiles in this pack
  foreach ($slug in $Profiles.Keys) {{
    $profileName = $Profiles[$slug]
    Install-Profile -Slug $slug -ProfileName $profileName
  }}
}} else {{
  # Install specified profiles
  foreach ($slug in $args) {{
    if (-not $Profiles.ContainsKey($slug)) {{
      Write-Error "Error: profile '$slug' not in pack $Pack"
      exit 1
    }}
    $profileName = $Profiles[$slug]
    Install-Profile -Slug $slug -ProfileName $profileName
  }}
}}

Write-Host "Pack installation complete"
'''


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "packs",
        nargs="*",
        help="Pack IDs to generate scripts for; default: all packs"
    )
    return ap.parse_args()


def load_export_map() -> Dict[str, Dict[str, str]]:
    """Load profile metadata from export-map.yaml (JSON format)"""
    if not EXPORT_MAP.exists():
        raise FileNotFoundError(f"export-map.yaml not found at {EXPORT_MAP}")
    
    content = EXPORT_MAP.read_text()
    data = json.loads(content)
    return data.get("profiles", {})


def get_pack_profiles(pack_id: str, export_map: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    """Get all profiles belonging to a pack: {slug: profile_name}"""
    profiles = {}
    for slug, data in export_map.items():
        if data.get("pack") == pack_id:
            profiles[slug] = data.get("profile_name", slug)
    return profiles


def get_pack_friendly_name(pack_id: str) -> str:
    """Get a friendly name for the pack from the pack directory"""
    pack_readme = PACKS / pack_id / "README.md"
    if pack_readme.exists():
        # Try to extract first heading
        for line in pack_readme.read_text().splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return pack_id


def generate_pack_scripts(pack_id: str, profiles: Dict[str, str]):
    """Generate installation scripts for a pack in linux/macos/windows subdirectories"""
    pack_dir = PACKS / pack_id
    if not pack_dir.exists():
        print(f"Warning: pack directory not found: {pack_dir}", file=sys.stderr)
        return
    
    pack_name = get_pack_friendly_name(pack_id)
    profile_list = ", ".join(profiles.keys())
    
    # Create bash profile map: ["slug"]="Profile Name"
    profile_map_entries = [f'  ["{slug}"]="{name}"' for slug, name in profiles.items()]
    profile_map = "\n".join(profile_map_entries)
    
    # Create PowerShell profile map: "slug" = "Profile Name"
    profile_map_ps_entries = [f'  "{slug}" = "{name}"' for slug, name in profiles.items()]
    profile_map_ps = "\n".join(profile_map_ps_entries)
    
    # Generate Linux script
    linux_dir = pack_dir / "scripts" / "linux"
    linux_dir.mkdir(parents=True, exist_ok=True)
    linux_script = linux_dir / "install-profiles.sh"
    linux_content = PACK_INSTALL_SH_TEMPLATE.format(
        pack_name=pack_name,
        pack_id=pack_id,
        profile_list=profile_list,
        profile_map=profile_map
    )
    linux_script.write_text(linux_content)
    linux_script.chmod(0o755)
    print(f"Generated: {linux_script.relative_to(ROOT)}")
    
    # Generate macOS script (same as Linux)
    macos_dir = pack_dir / "scripts" / "macos"
    macos_dir.mkdir(parents=True, exist_ok=True)
    macos_script = macos_dir / "install-profiles.sh"
    macos_script.write_text(linux_content)
    macos_script.chmod(0o755)
    print(f"Generated: {macos_script.relative_to(ROOT)}")
    
    # Generate Windows script
    windows_dir = pack_dir / "scripts" / "windows"
    windows_dir.mkdir(parents=True, exist_ok=True)
    windows_script = windows_dir / "Install-Profiles.ps1"
    windows_content = PACK_INSTALL_PS1_TEMPLATE.format(
        pack_name=pack_name,
        pack_id=pack_id,
        profile_list=profile_list,
        profile_map_ps=profile_map_ps
    )
    windows_script.write_text(windows_content)
    print(f"Generated: {windows_script.relative_to(ROOT)}")


def main():
    args = parse_args()
    export_map = load_export_map()
    
    # Get all unique pack IDs
    all_packs = sorted(set(data.get("pack", "") for data in export_map.values() if data.get("pack")))
    
    # Determine which packs to process
    if args.packs:
        packs = args.packs
    else:
        packs = all_packs
    
    # Validate packs
    invalid = [p for p in packs if p not in all_packs]
    if invalid:
        print(f"Error: invalid pack IDs: {invalid}", file=sys.stderr)
        print(f"Valid packs: {all_packs}", file=sys.stderr)
        sys.exit(1)
    
    # Generate scripts for each pack
    for pack in packs:
        profiles = get_pack_profiles(pack, export_map)
        if not profiles:
            print(f"Warning: no profiles found for pack {pack}", file=sys.stderr)
            continue
        generate_pack_scripts(pack, profiles)
    
    print(f"\nGenerated pack-level installation scripts for {len(packs)} pack(s)")


if __name__ == "__main__":
    main()
