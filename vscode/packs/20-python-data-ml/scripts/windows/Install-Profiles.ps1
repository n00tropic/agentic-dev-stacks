#!/usr/bin/env pwsh
# Pack: 20-python-data-ml
# Profiles in this pack: python-services-clis, python-data-ml

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackDir = Resolve-Path (Join-Path $ScriptDir "..\..")
$RepoRoot = Resolve-Path (Join-Path $PackDir "..\..")
$VsCodeDir = Join-Path $RepoRoot "vscode"

$Pack = "20-python-data-ml"

# Profile metadata: slug -> profile name
$Profiles = @{
  "python-services-clis" = "Python Services & CLIs"
  "python-data-ml" = "Python Data & ML"
}

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
  param([string]$Slug)
  $exportDir = Join-Path $VsCodeDir "exports/workspaces/$Slug"
  $workspaceFile = Join-Path $exportDir "$Slug.code-workspace"
  
  if (Test-Path $workspaceFile) { return }
  Write-Host "[$Slug] Export not found; generating via export-packs.py"
  $proc = Start-Process -FilePath $PythonPath -ArgumentList @("$($VsCodeDir)/scripts/export-packs.py", $Slug) -WorkingDirectory $VsCodeDir -Wait -PassThru
  if ($proc.ExitCode -ne 0) {
    Write-Error "[$Slug] export-packs.py failed"
    return $false
  }
  if (-not (Test-Path $workspaceFile)) {
    Write-Error "[$Slug] Export still missing at $workspaceFile"
    return $false
  }
  return $true
}

function Set-ExtensionsList {
  param([string]$Slug)
  $exportDir = Join-Path $VsCodeDir "exports/workspaces/$Slug"
  $dest = Join-Path $exportDir ".vscode/extensions.list"
  $packExtensions = Join-Path $VsCodeDir "packs/$Pack/extensions/extensions.$Slug.txt"
  
  if (Test-Path $dest -and (Get-Item $dest).Length -gt 0) { return }
  New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null
  if (-not (Test-Path $packExtensions)) {
    Write-Error "[$Slug] Missing pack extensions file: $packExtensions"
    return $false
  }
  Get-Content $packExtensions | Where-Object { $_ -and (-not ($_ -match '^#')) } | Set-Content $dest
  return $true
}

function Install-Extensions {
  param([string]$Slug, [string]$ProfileName)
  $exportDir = Join-Path $VsCodeDir "exports/workspaces/$Slug"
  $dest = Join-Path $exportDir ".vscode/extensions.list"
  $entries = @()
  if (Test-Path $dest) {
    $entries = Get-Content $dest | Where-Object { $_ }
  }
  if (-not (Test-Path $dest) -or $entries.Count -eq 0) {
    Write-Warning "[$Slug] No extensions listed; skipping install"
    return
  }
  $entries | ForEach-Object {
    code --install-extension $_ --profile "$ProfileName" --force
  }
}

function Install-Profile {
  param([string]$Slug, [string]$ProfileName)
  
  Write-Host "==== Installing profile: $ProfileName ($Slug) ===="
  
  if (-not (Test-ExportExists -Slug $Slug)) { return }
  if (-not (Set-ExtensionsList -Slug $Slug)) { return }
  
  Write-Host "[$Slug] Ensuring profile '$ProfileName' exists"
  code --profile "$ProfileName" --list-extensions *> $null
  
  Write-Host "[$Slug] Installing extensions"
  Install-Extensions -Slug $Slug -ProfileName $ProfileName
  
  $workspaceFile = Join-Path $VsCodeDir "exports/workspaces/$Slug/$Slug.code-workspace"
  if (Test-Path $workspaceFile) {
    Write-Host "[$Slug] Opening workspace"
    code $workspaceFile --profile "$ProfileName" --reuse-window *> $null
  }
  
  Write-Host "[$Slug] Done"
}

# Main logic
if ($args.Count -eq 0) {
  # Install all profiles in this pack
  foreach ($slug in $Profiles.Keys) {
    $profileName = $Profiles[$slug]
    Install-Profile -Slug $slug -ProfileName $profileName
  }
} else {
  # Install specified profiles
  foreach ($slug in $args) {
    if (-not $Profiles.ContainsKey($slug)) {
      Write-Error "Error: profile '$slug' not in pack $Pack"
      exit 1
    }
    $profileName = $Profiles[$slug]
    Install-Profile -Slug $slug -ProfileName $profileName
  }
}

Write-Host "Pack installation complete"
