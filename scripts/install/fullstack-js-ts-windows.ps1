#!/usr/bin/env pwsh
# Fullstack JS/TS bundle installer (Windows)
# Non-destructive scaffold: validates configs, checks prerequisites, and prints next steps.

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptRoot "..\")

Write-Output "[fullstack-js-ts] Validating agent ecosystem configs"
python3 (Join-Path $RepoRoot "agent-ecosystems/scripts/validate-ecosystem-configs.py")

$DevcontainerPath = Join-Path $RepoRoot "vscode/.devcontainer/devcontainer.json"
$ProfilePath = Join-Path $RepoRoot "vscode/profiles-dist/fullstack-js-ts.code-profile"

Write-Output "[fullstack-js-ts] Checking prerequisites"
if (Get-Command code -ErrorAction SilentlyContinue) {
  Write-Output "- VS Code CLI found: $(Get-Command code).Source"
} else {
  Write-Warning "- VS Code CLI not found. Install VS Code and enable 'Shell Command: Install code command in PATH' (or use VS Code UI)."
}

if (Get-Command devcontainer -ErrorAction SilentlyContinue) {
  Write-Output "- Devcontainer CLI found: $(Get-Command devcontainer).Source"
} else {
  Write-Output "- Devcontainer CLI not found (optional). You can use VS Code Dev Containers UI instead."
}

if (Test-Path $DevcontainerPath) {
  Write-Output "[fullstack-js-ts] Devcontainer present: $DevcontainerPath"
} else {
  Write-Warning "[fullstack-js-ts] Devcontainer missing: $DevcontainerPath. TODO: add automation to fetch/prepare devcontainer."
}

if (Test-Path $ProfilePath) {
  Write-Output "[fullstack-js-ts] VS Code profile export present: $ProfilePath"
} else {
  Write-Warning "[fullstack-js-ts] VS Code profile export missing. Export via VS Code 'Export Profile…' to $ProfilePath."
}

Write-Output @'
Next steps (manual):
- Import the exported profile in VS Code (Settings Profiles > Import Profile... or `code --import-profile` when available).
- Open the repository in the devcontainer (Command Palette: Dev Containers: Reopen in Container).
- Ensure MCP commands (github-mcp, context7-mcp, sonatype-mcp, elastic-mcp) are installed and configured via environment variables (no secrets in git).

TODOs for automation:
- Auto-import the profile when safe.
- Wire MCP command installation when packaged.
- Add integrity checks for artefacts.
'@
