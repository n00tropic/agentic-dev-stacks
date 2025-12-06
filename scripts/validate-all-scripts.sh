#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TRUNK_BIN="${TRUNK:-trunk}"
# Allow override: TRUNK_CHECK_ARGS="--no-progress --ci"
read -r -a TRUNK_FLAGS <<<"${TRUNK_CHECK_ARGS:---no-progress}"

fatal() {
	echo "[validate-all-scripts] Error: $*" >&2
	exit 1
}

log() {
	echo "[validate-all-scripts] $*"
}

usage() {
	cat <<'EOF'
Usage: scripts/validate-all-scripts.sh

Runs the full script validation suite:
- trunk check (use TRUNK_CHECK_ARGS to override flags, or SKIP_TRUNK=1 to skip)
- Python bytecode compile, JSON/TOML structural checks
- PSScriptAnalyzer across PowerShell scripts (installs module if missing)
EOF
}

if [[ ${1-} == "-h" || ${1-} == "--help" ]]; then
	usage
	exit 0
fi

run_trunk_check() {
	if [[ ${SKIP_TRUNK:-0} == "1" ]]; then
		log "Skipping trunk check (SKIP_TRUNK=1)"
		return
	fi
	if ! command -v "${TRUNK_BIN}" >/dev/null 2>&1; then
		fatal "trunk CLI not found; install trunk or set TRUNK to its path"
	fi
	log "Running trunk check (${TRUNK_BIN} ${TRUNK_FLAGS[*]})"
	"${TRUNK_BIN}" check "${TRUNK_FLAGS[@]}"
}

run_python_compile() {
	if ! command -v python3 >/dev/null 2>&1; then
		log "python3 not found; skipping compile step"
		return
	fi
	log "Running python -m compileall"
	python3 -m compileall "${ROOT}/vscode" "${ROOT}/codex" "${ROOT}/scripts" "${ROOT}/docs"
}

run_json_validation() {
	if ! command -v python3 >/dev/null 2>&1; then
		return
	fi
	log "Validating JSON files"
	ROOT_PATH="${ROOT}" python3 - <<'PY'
	import json, os, pathlib, sys
	root = pathlib.Path(os.environ["ROOT_PATH"])
	skip_parts = {'.trunk/tools', 'exports/', '.vscode/'}
fail = False
for path in root.rglob('*.json'):
    posix = path.as_posix()
    if any(part in posix for part in skip_parts):
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:  # pragma: no cover - CI guardrail
        print(f"{path}: {exc}")
        fail = True
if fail:
    sys.exit(1)
PY
}

run_toml_validation() {
	if ! command -v python3 >/dev/null 2>&1; then
		return
	fi
	log "Validating TOML files"
	ROOT_PATH="${ROOT}" python3 - <<'PY'
	import os, pathlib, sys
try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover - best effort
    sys.exit(0)
root = pathlib.Path(os.environ["ROOT_PATH"])
	skip_parts = {'.trunk/tools', 'exports/', '.vscode/'}
fail = False
for path in root.rglob('*.toml'):
    posix = path.as_posix()
    if any(part in posix for part in skip_parts):
        continue
    try:
        tomllib.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:  # pragma: no cover - CI guardrail
        print(f"{path}: {exc}")
        fail = True
if fail:
    sys.exit(1)
PY
}

run_psscriptanalyzer() {
	if ! command -v pwsh >/dev/null 2>&1; then
		log "pwsh not found; skipping PowerShell analysis"
		return
	fi
	log "Running PSScriptAnalyzer"
	# shellcheck disable=SC2016  # PowerShell expands $env:ROOT_PATH inside the here-string
	pwsh -NoLogo -NoProfile -Command @'
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
$root = "$env:ROOT_PATH"
$config = Join-Path $root "scripts/psscriptanalyzer.psd1"
$files = Get-ChildItem -Path $root -Include *.ps1,*.psm1 -File -Recurse
if (-not $files) { return }
if (-not (Get-Module -ListAvailable -Name PSScriptAnalyzer)) {
    Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force -ErrorAction Stop
}
Invoke-ScriptAnalyzer -Path $files.FullName -Settings $config -Recurse -EnableExit
'@
}

main() {
	log "Starting script validations from ${ROOT}"
	run_trunk_check
	run_python_compile
	run_json_validation
	run_toml_validation
	ROOT_PATH="${ROOT}" run_psscriptanalyzer
	log "All script validations completed"
}

main "$@"
