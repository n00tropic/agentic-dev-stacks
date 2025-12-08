#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="validate-docs"
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

usage() {
	cat <<'USAGE'
Usage: scripts/qa/validate-docs.sh [--help]

Builds docs (unless SKIP_DOCS_BUILD=1) then runs link checks. By default link
checks run in offline mode; set CHECK_EXTERNAL=1 to include external HTTP/HTTPS.

Options:
  -h, --help    Show this help message

Environment:
  SKIP_DOCS_BUILD=1  Skip docs build step
  CHECK_EXTERNAL=1   Include external link checks
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

cd "${DOCS_DIR}"

if [[ ${SKIP_DOCS_BUILD:-0} == "1" ]]; then
	log "Skipping docs build (SKIP_DOCS_BUILD=1)"
else
	./build-docs.sh
fi

CHECK_EXTERNAL=${CHECK_EXTERNAL:-0} ./check-links.sh
