#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Fullstack JS/TS installer (macOS)
# Runs the stack compiler for this persona, installs extensions into the profile, and opens the workspace.

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "${ROOT}" && pwd)"
VSCODE_DIR="${REPO_ROOT}/vscode"
PROFILE_SLUG="fullstack-js-ts"
PROFILE_NAME="Fullstack JS/TS – Web & API"
PROFILE_DIST="${VSCODE_DIR}/profiles-dist/${PROFILE_SLUG}.code-profile"
WORKSPACE_FILE="${VSCODE_DIR}/exports/workspaces/${PROFILE_SLUG}/${PROFILE_SLUG}.code-workspace"

require_cmd() {
	local cmd="$1"
	local msg="$2"
	if ! command -v "${cmd}" >/dev/null 2>&1; then
		echo "${msg}" >&2
		exit 1
	fi
}

echo "[${PROFILE_SLUG}] Prerequisite check (macOS)"
require_cmd git "Git is required; install via Xcode Command Line Tools or https://git-scm.com/download/mac"
require_cmd python3 "Python 3 is required (for export scripts). Install from https://www.python.org/downloads/"
require_cmd code "VS Code CLI 'code' not found. Install VS Code then run 'Shell Command: Install \"code\" command in PATH'"

if command -v devcontainer >/dev/null 2>&1; then
	echo "- Devcontainer CLI found: $(command -v devcontainer)"
else
	echo "- Devcontainer CLI not found (optional). You can still use VS Code Dev Containers UI."
fi
if command -v docker >/dev/null 2>&1; then
	echo "- Docker detected (required for the devcontainer)"
else
	echo "- Docker/Podman not found. Devcontainer will remain optional until installed."
fi

echo "[${PROFILE_SLUG}] Validating agent ecosystem configs"
python3 "${REPO_ROOT}/agent-ecosystems/scripts/validate-ecosystem-configs.py"

echo "[${PROFILE_SLUG}] Building export + installing profile"
bash "${VSCODE_DIR}/scripts/install-fullstack-js-ts.sh"

echo "[${PROFILE_SLUG}] Workspace path: ${WORKSPACE_FILE}"
if [[ -f ${PROFILE_DIST} ]]; then
	echo "[${PROFILE_SLUG}] Optional: import a vetted VS Code profile export from ${PROFILE_DIST} (Profiles > Import Profile…) to mirror reviewed settings."
else
	echo "[${PROFILE_SLUG}] No dist profile export found yet. Use VS Code 'Export Profile…' to create ${PROFILE_DIST} once you are happy."
fi

cat <<'NOTE'
Next steps:
- If the workspace did not open, run: code vscode/exports/workspaces/fullstack-js-ts/fullstack-js-ts.code-workspace --profile "Fullstack JS/TS – Web & API"
- To work in a containerised toolchain: Dev Containers: Reopen in Container (uses vscode/.devcontainer/devcontainer.json).
- MCP servers ship with placeholders only; follow codex/docs/config-guides.md to merge generated TOML into your local ~/.codex/config.toml without adding secrets to git.
NOTE
