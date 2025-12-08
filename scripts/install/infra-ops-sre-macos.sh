#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "${ROOT}/.." && pwd)"

echo "[infra-ops-sre] Validating agent ecosystem configs"
python3 "${REPO_ROOT}/agent-ecosystems/scripts/validate-ecosystem-configs.py"

devcontainer="${REPO_ROOT}/vscode/.devcontainer/infra-ops-sre/devcontainer.json"
profile="${REPO_ROOT}/vscode/profiles-dist/infra-ops-sre.code-profile"

if [[ -f $devcontainer ]]; then
	echo "Devcontainer present: $devcontainer"
else
	echo "Devcontainer missing: $devcontainer"
fi
if [[ -f $profile ]]; then
	echo "Profile present: $profile"
else
	echo "Profile missing: $profile (export via VS Code 'Export Profile…')"
fi

echo "Next steps: import the profile in VS Code and reopen in devcontainer."
