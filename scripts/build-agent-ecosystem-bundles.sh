#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="build-agent-ecosystem-bundles"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

log "Building agent ecosystem bundles"

python3 agent-ecosystems/scripts/build-ecosystem-bundles.py "$@"
