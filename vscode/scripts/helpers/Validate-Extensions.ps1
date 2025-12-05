\
    $Root = Split-Path -Parent $MyInvocation.MyCommand.Path
    $Script = Join-Path $Root "scripts\\validate_extensions.py"

    if (-not (Test-Path $Script)) {
        Write-Error "Validator script not found at: $Script"
        exit 1
    }

    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        python3 $Script
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python $Script
    } else {
        Write-Error "Neither python3 nor python is available on PATH."
        exit 1
    }
