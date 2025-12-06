#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d build/site ]; then
	echo "Docs not built. Run ./build-docs.sh first." >&2
	exit 1
fi

npx @lycheeverse/lychee@latest \
	--base build/site \
	--no-progress \
	build/site
