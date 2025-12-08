#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_NAME="check-agent-ecosystems"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONWARNINGS="${PYTHONWARNINGS:-ignore::DeprecationWarning}"

usage() {
	cat <<'USAGE'
Usage: scripts/check-agent-ecosystems.sh [--with-bundles] [--help]

Validates agent ecosystem configs and scenarios. Optionally builds bundles.

Options:
  --with-bundles  Build bundles after validations
  -h, --help      Show this help message
USAGE
}

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

WITH_BUNDLES=0
while (($#)); do
	case "$1" in
	--with-bundles)
		WITH_BUNDLES=1
		shift
		;;
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
done

log "Validating ecosystem configs"
python3 agent-ecosystems/scripts/validate-ecosystem-configs.py

log "Validating scenarios (static)"
python3 agent-ecosystems/scripts/run-agent-scenarios.py --no-output

if [[ $WITH_BUNDLES -eq 1 ]]; then
	log "Building bundles"
	python3 agent-ecosystems/scripts/build-ecosystem-bundles.py
fi

log "Done"
