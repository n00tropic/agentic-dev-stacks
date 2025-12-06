#!/usr/bin/env bash
set -euo pipefail

# Thin helper: install extensions into VS Code profiles from generated exports.
# Requires: python3, VS Code CLI (`code`). Works on macOS (but is POSIX-safe).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAP="${ROOT}/vscode/export-map.yaml"

if [[ ! -f ${MAP} ]]; then
	echo "export-map.yaml not found at ${MAP}" >&2
	exit 1
fi

FILTER_SLUGS=()
if [[ $# -gt 0 ]]; then
	FILTER_SLUGS=("$@")
fi

PY_OUT=$(python3 - "${MAP}" "${FILTER_SLUGS[@]-}" <<'PY') || exit 1
import sys, yaml, pathlib
path = pathlib.Path(sys.argv[1])
data = yaml.safe_load(path.read_text())
filter_slugs = set(sys.argv[2:])
profiles = data.get("profiles", {})
for slug, meta in profiles.items():
    if filter_slugs and slug not in filter_slugs:
        continue
    print("\t".join([
        slug,
        meta.get("profile_name", slug),
        meta.get("workspace_dir", ""),
        meta.get("workspace_file", ""),
    ]))
PY
readarray -t ENTRIES <<<"${PY_OUT}"

if [[ ${#ENTRIES[@]} -eq 0 ]]; then
	echo "No matching slugs found." >&2
	exit 1
fi

for line in "${ENTRIES[@]}"; do
	IFS=$'\t' read -r SLUG PROFILE_NAME WORKSPACE_DIR WORKSPACE_FILE <<<"${line}"
	if [[ -z ${WORKSPACE_DIR} ]]; then
		echo "[${SLUG}] workspace_dir missing in export-map.yaml" >&2
		continue
	fi
	if [[ ! -d "${ROOT}/${WORKSPACE_DIR}" ]]; then
		echo "[${SLUG}] export missing at ${WORKSPACE_DIR}. Run: cd vscode && python scripts/export-packs.py ${SLUG}" >&2
		continue
	fi

	EXT_LIST="${ROOT}/${WORKSPACE_DIR}/.vscode/extensions.list"
	if [[ ! -f ${EXT_LIST} ]]; then
		echo "[${SLUG}] extensions.list missing under ${WORKSPACE_DIR}" >&2
		continue
	fi

	echo "[${SLUG}] Ensuring profile '${PROFILE_NAME}' exists..."
	code --profile "${PROFILE_NAME}" --list-extensions >/dev/null 2>&1 || true

	echo "[${SLUG}] Installing extensions from ${EXT_LIST}"
	if [[ -s ${EXT_LIST} ]]; then
		xargs -n1 code --install-extension --profile "${PROFILE_NAME}" <"${EXT_LIST}"
	else
		echo "[${SLUG}] No extensions listed; skipping install" >&2
	fi

	if [[ -n ${WORKSPACE_FILE} && -f "${ROOT}/${WORKSPACE_FILE}" ]]; then
		echo "[${SLUG}] Opening workspace (once) to finish setup"
		code "${ROOT}/${WORKSPACE_FILE}" --profile "${PROFILE_NAME}" --reuse-window >/dev/null 2>&1 || true
	fi
done

echo "Done. Review logs above for any missing exports."
