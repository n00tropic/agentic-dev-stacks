#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(
	cd "$(dirname "$0")/../.." && pwd
)"
DOCS_DIR="${ROOT_DIR}/docs"

cd "${DOCS_DIR}"

if [[ ${SKIP_DOCS_BUILD:-0} == "1" ]]; then
	echo "Skipping docs build (SKIP_DOCS_BUILD=1)" >&2
else
	./build-docs.sh
fi

CHECK_EXTERNAL=${CHECK_EXTERNAL:-0} ./check-links.sh
