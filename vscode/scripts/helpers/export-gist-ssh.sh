#!/usr/bin/env bash
set -euo pipefail

# Push an exported VS Code *.code-profile to an existing GitHub gist over SSH.
# Requirements:
# - Export the profile from VS Code (File → Preferences → Profiles → Export Profile…)
#   to vscode/profiles-dist/<slug>.code-profile.
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
PROFILE_FILE="${REPO_ROOT}/vscode/profiles-dist/${SLUG}.code-profile"

if [[ ! -f ${PROFILE_FILE} ]]; then
	echo "Profile export not found for slug '${SLUG}'. Run the VS Code export flow and save to ${PROFILE_FILE}."
	exit 1
fi

TMPDIR="$(mktemp -d)"
trap 'rm -rf "${TMPDIR}"' EXIT

cd "${TMPDIR}"
git init -q
cp "${PROFILE_FILE}" .
git add "$(basename "${PROFILE_FILE}")"
git commit -qm "Export ${SLUG} profile"

git remote add origin "git@gist.github.com:${GIST_ID}.git"
git branch -M main
git push -f origin HEAD:main

echo "Pushed ${SLUG} .code-profile to gist ${GIST_ID} over SSH."
