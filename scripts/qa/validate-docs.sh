#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="validate-docs"
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
DOCS_DIR="${ROOT_DIR}/docs"

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

cd "${DOCS_DIR}"

if [[ ${SKIP_DOCS_BUILD:-0} == "1" ]]; then
	log "Skipping docs build (SKIP_DOCS_BUILD=1)"
else
	./build-docs.sh
fi

CHECK_EXTERNAL=${CHECK_EXTERNAL:-0} ./check-links.sh
