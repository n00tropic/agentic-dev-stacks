#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
cd "$(dirname "$0")"

SCRIPT_NAME="build-docs"

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

usage() {
	cat <<'USAGE'
Usage: docs/build-docs.sh [--help]

Builds the documentation site, including the Agentic Neon UI bundle if present.

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

# Build the custom Agentic Neon UI bundle before running Antora.
if [ -d "ui/agentic-neon-ui" ]; then
	log "Building Agentic Neon UI bundle..."
	(
		cd ui/agentic-neon-ui
		npm ci --no-fund --no-audit
		npm run build
	)
fi

npx -y -p @antora/cli@3.1.14 -p @antora/site-generator@3.1.14 -p asciidoctor-kroki@0.18.1 antora antora-playbook.yml
