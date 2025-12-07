#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VSCODE_DIR="${REPO_ROOT}/vscode"
PYTHON_BIN="$(command -v python3 || command -v python || true)"

PROFILE_SLUG="python-services-clis"
PROFILE_NAME="Python Services & CLIs"
PACK="20-python-data-ml"
EXPORT_DIR="${VSCODE_DIR}/exports/workspaces/${PROFILE_SLUG}"
WORKSPACE_FILE="${EXPORT_DIR}/${PROFILE_SLUG}.code-workspace"
PACK_EXTENSIONS="${VSCODE_DIR}/packs/${PACK}/extensions/extensions.${PROFILE_SLUG}.txt"

if ! command -v code >/dev/null 2>&1; then
	echo "VS Code CLI 'code' not found in PATH" >&2
	exit 1
fi
if [[ -z ${PYTHON_BIN} ]]; then
	echo "Python 3 interpreter not found (python3/python)" >&2
	exit 1
fi

ensure_export() {
	if [[ -f ${WORKSPACE_FILE} ]]; then
		return
	fi
	echo "[${PROFILE_SLUG}] Export not found; generating via export-packs.py"
	if ! "${PYTHON_BIN}" "${VSCODE_DIR}/scripts/export-packs.py" "${PROFILE_SLUG}"; then
		echo "[${PROFILE_SLUG}] export-packs.py failed" >&2
		exit 1
	fi
	if [[ ! -f ${WORKSPACE_FILE} ]]; then
		echo "[${PROFILE_SLUG}] Export still missing at ${WORKSPACE_FILE}" >&2
		exit 1
	fi
}

write_extensions_list() {
	local dest="${EXPORT_DIR}/.vscode/extensions.list"
	if [[ -s ${dest} ]]; then
		return
	fi
	mkdir -p "${EXPORT_DIR}/.vscode"
	if [[ ! -f ${PACK_EXTENSIONS} ]]; then
		echo "[${PROFILE_SLUG}] Missing pack extensions file: ${PACK_EXTENSIONS}" >&2
		exit 1
	fi
	grep -v '^[[:space:]]*$' "${PACK_EXTENSIONS}" | grep -v '^#' >"${dest}" || true
}

install_extensions() {
	local dest="${EXPORT_DIR}/.vscode/extensions.list"
	if [[ ! -s ${dest} ]]; then
		echo "[${PROFILE_SLUG}] No extensions listed; skipping install" >&2
		return
	fi
	while IFS= read -r ext; do
		[[ -z ${ext} ]] && continue
		code --install-extension "${ext}" --profile "${PROFILE_NAME}" --force
	done <"${dest}"
}

ensure_export
write_extensions_list

echo "[${PROFILE_SLUG}] Ensuring profile '${PROFILE_NAME}' exists"
code --profile "${PROFILE_NAME}" --list-extensions >/dev/null 2>&1 || true

echo "[${PROFILE_SLUG}] Installing extensions"
install_extensions

if [[ -f ${WORKSPACE_FILE} ]]; then
	echo "[${PROFILE_SLUG}] Opening workspace"
	code "${WORKSPACE_FILE}" --profile "${PROFILE_NAME}" --reuse-window >/dev/null 2>&1 || true
fi

echo "[${PROFILE_SLUG}] Done"
