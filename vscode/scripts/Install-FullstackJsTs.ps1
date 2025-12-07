#!/usr/bin/env pwsh
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$VsCodeDir = Join-Path $RepoRoot "vscode"

$ProfileSlug = "fullstack-js-ts"
$ProfileName = "Fullstack JS/TS – Web & API"
$Pack = "10-fullstack-js-ts"
$ExportDir = Join-Path $VsCodeDir "exports/workspaces/$ProfileSlug"
$WorkspaceFile = Join-Path $ExportDir "$ProfileSlug.code-workspace"
$PackExtensions = Join-Path $VsCodeDir "packs/$Pack/extensions/extensions.$ProfileSlug.txt"

if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
  Write-Error "VS Code CLI 'code' not found in PATH"
  exit 1
}
$PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $PythonCmd) { $PythonCmd = Get-Command python -ErrorAction SilentlyContinue }
if (-not $PythonCmd) {
  Write-Error "Python 3 interpreter not found (python3/python)"
  exit 1
}
$PythonPath = $PythonCmd.Source

function Test-ExportExists {
  if (Test-Path $WorkspaceFile) { return }
  Write-Host "[$ProfileSlug] Export not found; generating via export-packs.py"
  $proc = Start-Process -FilePath $PythonPath -ArgumentList @("$($VsCodeDir)/scripts/export-packs.py", $ProfileSlug) -WorkingDirectory $VsCodeDir -Wait -PassThru
  if ($proc.ExitCode -ne 0) {
    Write-Error "[$ProfileSlug] export-packs.py failed"
    exit 1
  }
  if (-not (Test-Path $WorkspaceFile)) {
    Write-Error "[$ProfileSlug] Export still missing at $WorkspaceFile"
    exit 1
  }
}

function Set-ExtensionsList {
  $dest = Join-Path $ExportDir ".vscode/extensions.list"
  if (Test-Path $dest -and (Get-Item $dest).Length -gt 0) { return }
  New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
  if (-not (Test-Path $PackExtensions)) {
    Write-Error "[$ProfileSlug] Missing pack extensions file: $PackExtensions"
    exit 1
  }
  Get-Content $PackExtensions | Where-Object { $_ -and (-not ($_ -match '^#')) } | Set-Content $dest
}

function Install-Extensions {
  $dest = Join-Path $ExportDir ".vscode/extensions.list"
  $entries = @()
  if (Test-Path $dest) {
    $entries = Get-Content $dest | Where-Object { $_ }
  }
  if (-not (Test-Path $dest) -or $entries.Count -eq 0) {
    Write-Warning "[$ProfileSlug] No extensions listed; skipping install"
    return
  }
  $entries | ForEach-Object {
    code --install-extension $_ --profile "$ProfileName" --force
  }
}

Test-ExportExists
Set-ExtensionsList

Write-Host "[$ProfileSlug] Ensuring profile '$ProfileName' exists"
code --profile "$ProfileName" --list-extensions *> $null

Write-Host "[$ProfileSlug] Installing extensions"
Install-Extensions

if (Test-Path $WorkspaceFile) {
  Write-Host "[$ProfileSlug] Opening workspace"
  code $WorkspaceFile --profile "$ProfileName" --reuse-window *> $null
}

Write-Host "[$ProfileSlug] Done"
