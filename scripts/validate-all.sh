#!/usr/bin/env bash
# trunk-ignore-all(shfmt)
set -euo pipefail
IFS=$'
	'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

usage() {
	cat <<'USAGE'
Usage: scripts/validate-all.sh [--fast] [--help]

Runs the standard validation suite:
- trunk check (if installed)
- qa-preflight (extensions, MCP config, scripts, metadata)
- docs build (skipped with --fast or VALIDATE_FAST=1)

Options:
  --fast        Skip docs build
  -h, --help    Show this help
USAGE
}

FAST=${VALIDATE_FAST:-0}
while (($#)); do
	case "$1" in
	--fast)
		FAST=1
		shift
		;;
	-h | --help)
		usage
		exit 0
		;;
	*)
		echo "Unknown option: $1" >&2
		usage
		exit 1
		;;
	esac
done

log() { echo "[validate-all] $*"; }
check_python_deps() {
	python3 - <<'PY'
import importlib.util
import sys

missing = []
for mod in ("jsonschema", "yaml"):
    if importlib.util.find_spec(mod) is None:
        missing.append(mod)

if missing:
    mods = ", ".join(sorted(missing))
    sys.stderr.write(
        f"Missing Python modules: {mods}. Install with 'pip3 install --user -r requirements-dev.txt' or run inside the devcontainer.\n"
    )
    sys.exit(1)
PY
}
check_for_obvious_secrets() {
	python3 - <<'PY'
import re
import sys
from pathlib import Path

root = Path('.')
skip_dirs = {
    '.git', '.trunk', 'node_modules', 'dist', 'tmp',
    'docs/ui/agentic-neon-ui/node_modules',
}
patterns = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |DSA |EC )?PRIVATE KEY-----"),
]

def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & skip_dirs)

findings = []
for path in root.rglob('*'):
    if not path.is_file():
        continue
    if should_skip(path):
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    for pat in patterns:
        match = pat.search(text)
        if match:
            snippet = match.group(0)[:40] + ('…' if len(match.group(0)) > 40 else '')
            findings.append(f"{path}: possible secret-like token '{snippet}'")
            break

if findings:
    sys.stderr.write("Potential secret-like patterns detected:\n" + "\n".join(findings) + "\n")
    sys.exit(1)
PY
}
run_or_skip_trunk() {
	if command -v trunk >/dev/null 2>&1; then
		log "Running trunk check"
		TRUNK_ARGS=(--no-progress --ci)
		if [[ -n ${TRUNK_CHECK_ARGS:-} ]]; then
			# shellcheck disable=SC2206 # intentional split for user-provided args
			TRUNK_ARGS=(${TRUNK_CHECK_ARGS})
		fi
		trunk check "${TRUNK_ARGS[@]}"
	else
		log "Skipping trunk (not installed)"
	fi
}

main() {
	log "Starting validation suite"
	check_python_deps
	check_for_obvious_secrets
	run_or_skip_trunk

	log "Running qa-preflight"
	bash scripts/qa-preflight.sh

	if [[ "${FAST}" == "1" ]]; then
		log "Skipping docs build (--fast)"
	else
		log "Building docs"
		(cd docs && ./build-docs.sh)
	fi
	log "Validation complete"
}

main "$@"
