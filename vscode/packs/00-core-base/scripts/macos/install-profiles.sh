#!/usr/bin/env bash
set -euo pipefail

# Pack: 00-core-base
# Profiles in this pack: core-base-dev, qa-static-analysis, gitops-code-review, macos-apple-platforms, windows-polyglot-wsl

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]})")" && pwd)"
PACK_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
REPO_ROOT="$(cd "${PACK_DIR}/../.." && pwd)"
VSCODE_DIR="${REPO_ROOT}/vscode"
PYTHON_BIN="$(command -v python3 || command -v python || true)"

PACK="00-core-base"

# Profile metadata: slug, profile name
declare -A PROFILES=(
  ["core-base-dev"]="Core / Base Dev"
  ["qa-static-analysis"]="QA / Static Analysis"
  ["gitops-code-review"]="GitOps & Code Review"
  ["macos-apple-platforms"]="macOS – Apple Platforms & Tooling"
  ["windows-polyglot-wsl"]="Windows – Polyglot + WSL"
)

if ! command -v code >/dev/null 2>&1; then
	echo "VS Code CLI 'code' not found in PATH" >&2
	exit 1
fi
if [[ -z ${PYTHON_BIN} ]]; then
	echo "Python 3 interpreter not found (python3/python)" >&2
	exit 1
fi

ensure_export() {
	local slug="$1"
	local export_dir="${VSCODE_DIR}/exports/workspaces/${slug}"
	local workspace_file="${export_dir}/${slug}.code-workspace"
	
	if [[ -f ${workspace_file} ]]; then
		return
	fi
	echo "[${slug}] Export not found; generating via export-packs.py"
	if ! "${PYTHON_BIN}" "${VSCODE_DIR}/scripts/export-packs.py" "${slug}"; then
		echo "[${slug}] export-packs.py failed" >&2
		return 1
	fi
	if [[ ! -f ${workspace_file} ]]; then
		echo "[${slug}] Export still missing at ${workspace_file}" >&2
		return 1
	fi
}

write_extensions_list() {
	local slug="$1"
	local export_dir="${VSCODE_DIR}/exports/workspaces/${slug}"
	local dest="${export_dir}/.vscode/extensions.list"
	local pack_extensions="${VSCODE_DIR}/packs/${PACK}/extensions/extensions.${slug}.txt"
	
	if [[ -s ${dest} ]]; then
		return
	fi
	mkdir -p "${export_dir}/.vscode"
	if [[ ! -f ${pack_extensions} ]]; then
		echo "[${slug}] Missing pack extensions file: ${pack_extensions}" >&2
		return 1
	fi
	grep -v '^[[:space:]]*$' "${pack_extensions}" | grep -v '^#' >"${dest}" || true
}

install_extensions() {
	local slug="$1"
	local profile_name="$2"
	local export_dir="${VSCODE_DIR}/exports/workspaces/${slug}"
	local dest="${export_dir}/.vscode/extensions.list"
	
	if [[ ! -s ${dest} ]]; then
		echo "[${slug}] No extensions listed; skipping install" >&2
		return
	fi
	while IFS= read -r ext; do
		[[ -z ${ext} ]] && continue
		code --install-extension "${ext}" --profile "${profile_name}" --force
	done <"${dest}"
}

install_profile() {
	local slug="$1"
	local profile_name="$2"
	
	echo "==== Installing profile: ${profile_name} (${slug}) ===="
	
	ensure_export "${slug}"
	write_extensions_list "${slug}"
	
	echo "[${slug}] Ensuring profile '${profile_name}' exists"
	code --profile "${profile_name}" --list-extensions >/dev/null 2>&1 || true
	
	echo "[${slug}] Installing extensions"
	install_extensions "${slug}" "${profile_name}"
	
	local workspace_file="${VSCODE_DIR}/exports/workspaces/${slug}/${slug}.code-workspace"
	if [[ -f ${workspace_file} ]]; then
		echo "[${slug}] Opening workspace"
		code "${workspace_file}" --profile "${profile_name}" --reuse-window >/dev/null 2>&1 || true
	fi
	
	echo "[${slug}] Done"
}

# Main logic
if [[ $# -eq 0 ]]; then
	# Install all profiles in this pack
	for slug in "${!PROFILES[@]}"; do
		profile_name="${PROFILES[$slug]}"
		install_profile "${slug}" "${profile_name}"
	done
else
	# Install specified profiles
	for slug in "$@"; do
		if [[ -z ${PROFILES[$slug]:-} ]]; then
			echo "Error: profile '${slug}' not in pack ${PACK}" >&2
			exit 1
		fi
		profile_name="${PROFILES[$slug]}"
		install_profile "${slug}" "${profile_name}"
	done
fi

echo "Pack installation complete"
