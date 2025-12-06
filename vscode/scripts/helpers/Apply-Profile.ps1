#!/usr/bin/env pwsh
Param(
  [Parameter(Mandatory = $true)]
  [string]$Slug
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$PacksDir = Join-Path $RepoRoot "packs"

if (-not (Test-Path $PacksDir)) {
    Write-Error "packs directory not found at $PacksDir"
    exit 1
}

# Resolve settings override file
$settingsPattern = "settings.$Slug.json"
$settingsMatches = Get-ChildItem -Path $PacksDir -Recurse -Filter $settingsPattern -File -ErrorAction SilentlyContinue

if (-not $settingsMatches) {
    Write-Error "No settings override found for slug '$Slug' (looked for $settingsPattern)"
    exit 1
} elseif ($settingsMatches.Count -gt 1) {
    Write-Error "Multiple settings overrides found for slug '$Slug'. Please disambiguate:"
    $settingsMatches | ForEach-Object { Write-Host "  $($_.FullName)" }
    exit 1
}

$settingsFile = $settingsMatches[0].FullName
Write-Host "Using settings override: $settingsFile"

# Resolve extensions list
$extPattern = "extensions.$Slug.txt"
$extMatches = Get-ChildItem -Path $PacksDir -Recurse -Filter $extPattern -File -ErrorAction SilentlyContinue

if ($extMatches.Count -eq 0) {
    Write-Warning "No extensions list found for slug '$Slug' (looked for $extPattern)"
    $extFile = $null
} elseif ($extMatches.Count -gt 1) {
    Write-Warning "Multiple extensions lists found for slug '$Slug'. Please disambiguate manually:"
    $extMatches | ForEach-Object { Write-Host "  $($_.FullName)" }
    $extFile = $null
} else {
    $extFile = $extMatches[0].FullName
    Write-Host "Extensions list: $extFile"
}

# Merge settings
$merger = Join-Path $RepoRoot "scripts/windows/Merge-Settings.ps1"
if (-not (Test-Path $merger)) {
    Write-Error "Merge script not found: $merger"
    exit 1
}

Write-Host "Merging settings via: $merger"
& $merger -OverridePath $settingsFile

if ($extFile) {
    Write-Host ""
    Write-Host "To install extensions for profile '$Slug', run (example):" -ForegroundColor Cyan
    Write-Host ""
    Get-Content $extFile | ForEach-Object {
        $line = $_.Trim()
        if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith("#")) { return }
        Write-Host ("  code --install-extension `"{0}`"" -f $line)
    }
    Write-Host ""
    Write-Host "You can optionally add: --profile `"<Profile Name>`" to bind installs to a specific VS Code profile."
}

Write-Host "Done."
