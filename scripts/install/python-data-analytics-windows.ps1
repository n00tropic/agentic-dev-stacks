#!/usr/bin/env pwsh
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptRoot "..\")

Write-Output "[python-data-analytics] Validating agent ecosystem configs"
python3 (Join-Path $RepoRoot "agent-ecosystems/scripts/validate-ecosystem-configs.py")

$devcontainer = Join-Path $RepoRoot "vscode/.devcontainer/python-data-analytics/devcontainer.json"
$profile = Join-Path $RepoRoot "vscode/profiles-dist/python-data-analytics.code-profile"

if (Test-Path $devcontainer) {
  Write-Output "Devcontainer present: $devcontainer"
} else {
  Write-Warning "Devcontainer missing: $devcontainer"
}
if (Test-Path $profile) {
  Write-Output "Profile present: $profile"
} else {
  Write-Warning "Profile missing: $profile (export via VS Code 'Export Profile…')"
}

Write-Output "Next steps: import the profile in VS Code and reopen in devcontainer."
