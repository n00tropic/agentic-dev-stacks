#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
cd "$(dirname "$0")"

SCRIPT_NAME="build-docs"

log() {
	printf '[%s] %s\n' "${SCRIPT_NAME}" "$*" >&2
}

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
