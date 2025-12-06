<#
Thin helper: install extensions into VS Code profiles from generated exports.
Requires: Python 3, VS Code CLI (`code`).

Usage:
  pwsh -File .\Install-Profiles.ps1               # all slugs
  pwsh -File .\Install-Profiles.ps1 core-base-dev  # specific slugs
#>

$root = (Resolve-Path "$PSScriptRoot\..\..").Path
$map = Join-Path $root 'vscode/export-map.yaml'

if (-not (Test-Path $map)) {
  Write-Error "export-map.yaml not found at $map"
  exit 1
}

$filter = $args

$lines = python3 - <<'PY'
import sys, yaml, pathlib
path = pathlib.Path(sys.argv[1])
data = yaml.safe_load(path.read_text())
filters = set(sys.argv[2:])
profiles = data.get("profiles", {})
for slug, meta in profiles.items():
    if filters and slug not in filters:
        continue
    print("\t".join([
        slug,
        meta.get("profile_name", slug),
        meta.get("workspace_dir", ""),
        meta.get("workspace_file", ""),
    ]))
PY
"$map" @filter

if (-not $lines) {
  Write-Error "No matching slugs found."
  exit 1
}

foreach ($line in $lines) {
  $parts = $line -split "`t"
  $slug, $profileName, $workspaceDir, $workspaceFile = $parts

  if (-not $workspaceDir) {
    Write-Warning "[$slug] workspace_dir missing in export-map.yaml"
    continue
  }

  $wsPath = Join-Path $root $workspaceDir
  if (-not (Test-Path $wsPath)) {
    Write-Warning "[$slug] export missing at $workspaceDir. Run: cd vscode; python scripts/export-packs.py $slug"
    continue
  }

  $extList = Join-Path $wsPath '.vscode/extensions.list'
  if (-not (Test-Path $extList)) {
    Write-Warning "[$slug] extensions.list missing under $workspaceDir"
    continue
  }

  Write-Host "[$slug] Ensuring profile '$profileName' exists..."
  code --profile "$profileName" --list-extensions *> $null

  Write-Host "[$slug] Installing extensions from $extList"
  Get-Content $extList | Where-Object { $_ -ne '' } | ForEach-Object {
    code --install-extension $_ --profile "$profileName"
  }

  if ($workspaceFile) {
    $wsFilePath = Join-Path $root $workspaceFile
    if (Test-Path $wsFilePath) {
      Write-Host "[$slug] Opening workspace once to finish setup"
      code $wsFilePath --profile "$profileName" --reuse-window *> $null
    }
  }
}

Write-Host "Done. Review warnings above for any missing exports."
