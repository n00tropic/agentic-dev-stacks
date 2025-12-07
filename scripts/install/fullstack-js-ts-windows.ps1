#!/usr/bin/env pwsh
# Fullstack JS/TS installer (Windows)
# Runs the stack compiler for this persona, installs extensions into the profile, and opens the workspace.

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptRoot "..\")
$VsCodeDir = Join-Path $RepoRoot "vscode"

$ProfileSlug = "fullstack-js-ts"
$ProfileName = "Fullstack JS/TS – Web & API"
$ProfileDist = Join-Path $VsCodeDir "profiles-dist/$ProfileSlug.code-profile"
$WorkspaceFile = Join-Path $VsCodeDir "exports/workspaces/$ProfileSlug/$ProfileSlug.code-workspace"

function Require-Cmd {
  param (
    [string]$Name,
    [string]$Message
  )
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    Write-Error $Message
    exit 1
  }
}

Write-Output "[$ProfileSlug] Prerequisite check (Windows)"
Require-Cmd git "Git is required; install via https://git-scm.com/download/win or winget"

$Python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command python -ErrorAction SilentlyContinue }
if (-not $Python) {
  Write-Error "Python 3 is required (for export scripts). Install from https://www.python.org/downloads/windows/"
  exit 1
}
Require-Cmd code "VS Code CLI 'code' not found. Install VS Code then enable the CLI via the Command Palette."

if (Get-Command devcontainer -ErrorAction SilentlyContinue) {
  Write-Output "- Devcontainer CLI found: $(Get-Command devcontainer).Source"
} else {
  Write-Output "- Devcontainer CLI not found (optional). You can still use VS Code Dev Containers UI."
}
if (Get-Command docker -ErrorAction SilentlyContinue) {
  Write-Output "- Docker detected (required for the devcontainer)"
} else {
  Write-Output "- Docker/Podman not found. Devcontainer will remain optional until installed."
}

Write-Output "[$ProfileSlug] Validating agent ecosystem configs"
& $Python.Source (Join-Path $RepoRoot "agent-ecosystems/scripts/validate-ecosystem-configs.py")

Write-Output "[$ProfileSlug] Building export + installing profile"
& (Join-Path $VsCodeDir "scripts/Install-FullstackJsTs.ps1")

Write-Output "[$ProfileSlug] Workspace path: $WorkspaceFile"
if (Test-Path $ProfileDist) {
  Write-Output "[$ProfileSlug] Optional: import a vetted VS Code profile export from $ProfileDist (Profiles > Import Profile…) to mirror reviewed settings."
} else {
  Write-Warning "[$ProfileSlug] No dist profile export found yet. Use VS Code 'Export Profile…' to create $ProfileDist once you are happy."
}

Write-Output @'
Next steps:
- If the workspace did not open, run: code vscode/exports/workspaces/fullstack-js-ts/fullstack-js-ts.code-workspace --profile "Fullstack JS/TS – Web & API"
- To work in a containerised toolchain: Dev Containers: Reopen in Container (uses vscode/.devcontainer/devcontainer.json).
- MCP servers ship with placeholders only; follow codex/docs/config-guides.md to merge generated TOML into your local ~/.codex/config.toml without adding secrets to git.
'@
