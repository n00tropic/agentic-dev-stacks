#!/usr/bin/env bash
set -euo pipefail

# Export a workspace tarball and push it to an existing GitHub gist over SSH.
# Requirements:
# - You already created a gist (secret or public) in the GitHub UI and have its ID.
# - Your SSH key is loaded and allowed to write to gists (same permissions as repo SSH).
#
# Usage:
#   ./scripts/helpers/export-gist-ssh.sh <slug> <gist_id>
#
# Example:
#   ./scripts/helpers/export-gist-ssh.sh core-base-dev abcdef1234567890deadbeef

if [[ $# -lt 2 ]]; then
	echo "Usage: $(basename "$0") <slug> <gist_id>"
	exit 1
fi

SLUG="$1"
GIST_ID="$2"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXPORT_DIR="${REPO_ROOT}/vscode/exports/workspaces/${SLUG}"
TARBALL="${REPO_ROOT}/vscode/${SLUG}.tar.gz"

if [[ ! -d ${EXPORT_DIR} ]]; then
	echo "Export not found for slug '${SLUG}'. Run:"
	echo "  cd vscode && python scripts/export-packs.py ${SLUG}"
	exit 1
fi

echo "Packing ${EXPORT_DIR} -> ${TARBALL}"
tar -czf "${TARBALL}" -C "${EXPORT_DIR}" .

TMPDIR="$(mktemp -d)"
trap 'rm -rf "${TMPDIR}" "${TARBALL}"' EXIT

cd "${TMPDIR}"
git init -q
cp "${TARBALL}" .
git add "$(basename "${TARBALL}")"
git commit -qm "Export ${SLUG}"

git remote add origin "git@gist.github.com:${GIST_ID}.git"
git push -f origin HEAD:master

echo "Pushed ${SLUG} export to gist ${GIST_ID} over SSH."
