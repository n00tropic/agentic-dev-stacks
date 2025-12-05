#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$ROOT/scripts/validate_extensions.py"

if [[ ! -f $SCRIPT ]]; then
	echo "Validator script not found at: $SCRIPT"
	exit 1
fi

if command -v python3 >/dev/null 2>&1; then
	python3 "$SCRIPT"
else
	python "$SCRIPT"
fi
