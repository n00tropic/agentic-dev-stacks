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
