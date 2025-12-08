#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="test-scripts"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

usage() {
	cat <<'USAGE'
Usage: scripts/test-scripts.sh [--help]

Runs lightweight self-tests for scripts that implement --help to ensure they respond successfully.

Options:
  -h, --help    Show this help message
USAGE
}

if (($#)); then
	case "$1" in
	-h | --help)
		usage
		exit 0
		;;
	*)
		printf 'Unknown option: %s\n' "$1" >&2
		usage
		exit 1
		;;
	esac
fi

SCRIPTS_WITH_HELP=(
	"scripts/validate-all.sh"
	"scripts/qa-preflight.sh"
	"scripts/validate-all-scripts.sh"
	"scripts/check-agent-ecosystems.sh"
)

failures=0

for script in "${SCRIPTS_WITH_HELP[@]}"; do
	if [[ ! -x ${script} ]]; then
		log "WARN: ${script} is not executable"
		failures=$((failures + 1))
		continue
	fi
	log "Checking --help for ${script}"
	if ! "${script}" --help >/dev/null 2>&1; then
		log "FAIL: ${script} --help returned non-zero"
		failures=$((failures + 1))
	fi
done

if ((failures > 0)); then
	log "Script self-test failed (${failures} scripts)"
	exit 1
fi

log "Script self-test passed"
