#!/usr/bin/env bash
set -euo pipefail

# Fullstack JS/TS bundle installer (Linux)
# Non-destructive scaffold: validates configs, checks prerequisites, and prints next steps.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "${ROOT}/.." && pwd)"

echo "[fullstack-js-ts] Validating agent ecosystem configs"
python3 "${REPO_ROOT}/agent-ecosystems/scripts/validate-ecosystem-configs.py"

DEVCONTAINER_PATH="${REPO_ROOT}/vscode/.devcontainer/devcontainer.json"
PROFILE_PATH="${REPO_ROOT}/vscode/profiles-dist/fullstack-js-ts.code-profile"

echo "[fullstack-js-ts] Checking prerequisites"
if command -v code >/dev/null 2>&1; then
	echo "- VS Code CLI found: $(command -v code)"
else
	echo "- VS Code CLI not found. Install VS Code and enable 'Shell Command: Install 'code' command in PATH'"
fi

if command -v devcontainer >/dev/null 2>&1; then
	echo "- Devcontainer CLI found: $(command -v devcontainer)"
else
	echo "- Devcontainer CLI not found (optional). You can use VS Code Dev Containers UI instead."
fi

if [[ -f ${DEVCONTAINER_PATH} ]]; then
	echo "[fullstack-js-ts] Devcontainer present: ${DEVCONTAINER_PATH}"
else
	echo "[fullstack-js-ts] Devcontainer missing: ${DEVCONTAINER_PATH}. TODO: add automation to fetch/prepare devcontainer."
fi

if [[ -f ${PROFILE_PATH} ]]; then
	echo "[fullstack-js-ts] VS Code profile export present: ${PROFILE_PATH}"
else
	echo "[fullstack-js-ts] VS Code profile export missing. Export via VS Code 'Export Profile…' to ${PROFILE_PATH}."
fi

cat <<'NOTE'
Next steps (manual):
- Import the exported profile in VS Code (File > Preferences > Profiles > Import Profile... or `code --import-profile` when available).
- Open the repository in the devcontainer (Command Palette: Dev Containers: Reopen in Container).
- Ensure MCP commands (github-mcp, context7-mcp, sonatype-mcp, elastic-mcp) are installed and configured via environment variables (no secrets in git).

TODOs for automation:
- Auto-import the profile when safe.
- Wire MCP command installation when packaged.
- Add integrity checks for artefacts.
NOTE
