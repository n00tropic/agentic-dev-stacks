#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONWARNINGS="${PYTHONWARNINGS:-ignore::DeprecationWarning}"

WITH_BUNDLES=0
if [[ ${1-} == "--with-bundles" ]]; then
	WITH_BUNDLES=1
fi

echo "[check-agent-ecosystems] Validating ecosystem configs"
python3 agent-ecosystems/scripts/validate-ecosystem-configs.py

echo "[check-agent-ecosystems] Validating scenarios (static)"
python3 agent-ecosystems/scripts/run-agent-scenarios.py --no-output

if [[ $WITH_BUNDLES -eq 1 ]]; then
	echo "[check-agent-ecosystems] Building bundles"
	python3 agent-ecosystems/scripts/build-ecosystem-bundles.py
fi

echo "[check-agent-ecosystems] Done"
