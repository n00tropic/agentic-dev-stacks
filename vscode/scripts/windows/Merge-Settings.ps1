#!/usr/bin/env pwsh
Param(
  [Parameter(Mandatory = $true)]
  [string]$OverridePath
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $OverridePath)) {
    Write-Error "Override file not found: $OverridePath"
    exit 1
}

$settingsTarget = if ($IsWindows) {
    Join-Path $env:APPDATA "Code/User/settings.json"
} elseif ($IsMacOS) {
    Join-Path $env:HOME "Library/Application Support/Code/User/settings.json"
} else {
    Join-Path $env:HOME ".config/Code/User/settings.json"
}
$settingsDir = Split-Path $settingsTarget -Parent
if (-not (Test-Path $settingsDir)) {
    New-Item -ItemType Directory -Force -Path $settingsDir | Out-Null
}

function Merge-Dictionaries {
    param(
        [hashtable]$Base,
        [hashtable]$Override
    )

    $result = @{}
    foreach ($key in $Base.Keys) { $result[$key] = $Base[$key] }

    foreach ($key in $Override.Keys) {
        if ($result.ContainsKey($key) -and
            $result[$key] -is [hashtable] -and
            $Override[$key] -is [hashtable]) {
            $result[$key] = Merge-Dictionaries -Base $result[$key] -Override $Override[$key]
        } else {
            $result[$key] = $Override[$key]
        }
    }

    return $result
}

$baseObj = $null
if (Test-Path $settingsTarget) {
    $backup = "$settingsTarget.bak.$((Get-Date).ToString('yyyyMMddHHmmss'))"
    Copy-Item $settingsTarget $backup -Force
    Write-Host "Existing settings backed up to: $backup"

    try {
        $baseJson = Get-Content $settingsTarget -Raw
        $baseObj = $baseJson | ConvertFrom-Json -ErrorAction Stop
    } catch {
        Write-Warning "Existing settings.json is not valid JSON; starting from override only."
        $baseObj = $null
    }
}

try {
    $overrideJson = Get-Content $OverridePath -Raw
    $overrideObj = $overrideJson | ConvertFrom-Json -ErrorAction Stop
} catch {
    Write-Error "Override file is not valid JSON: $OverridePath"
    exit 1
}

if ($baseObj -eq $null) {
    $merged = $overrideObj
} else {
    $baseHash = @{}
    $baseObj.PSObject.Properties | ForEach-Object { $baseHash[$_.Name] = $_.Value }
    $overrideHash = @{}
    $overrideObj.PSObject.Properties | ForEach-Object { $overrideHash[$_.Name] = $_.Value }
    $mergedHash = Merge-Dictionaries -Base $baseHash -Override $overrideHash
    $merged = New-Object PSObject -Property $mergedHash
}

$merged | ConvertTo-Json -Depth 10 | Set-Content -Path $settingsTarget -Encoding UTF8
Write-Host "Settings updated at: $settingsTarget"
