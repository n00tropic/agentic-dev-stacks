#!/usr/bin/env bash
set -euo pipefail

# Validate a workspace bundle zip without touching user dotfiles or real VS Code profiles.
# Usage: ./validate-bundle.sh <slug>

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLUG="${1-}"
if [[ -z $SLUG ]]; then
	echo "Usage: $0 <slug>" >&2
	exit 1
fi

ZIP="$ROOT/exports/bundles/${SLUG}-bundle.zip"
if [[ ! -f $ZIP ]]; then
	echo "Bundle zip not found: $ZIP" >&2
	exit 1
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

unzip -q "$ZIP" -d "$TMPDIR"
BROOT="$TMPDIR/${SLUG}"

require() {
	for f in "$@"; do
		if [[ ! -f "$BROOT/$f" ]]; then
			echo "Missing required file: $f" >&2
			exit 1
		fi
	done
}

require \
	"workspace/${SLUG}.code-workspace" \
	"workspace/.vscode/extensions.list" \
	"mcp/servers.${SLUG}.json" \
	"mcp/codex-mcp.${SLUG}.generated.toml" \
	"scripts/install-macos.sh" \
	"scripts/Install-Windows.ps1"

# Validate JSON
python3 -m json.tool "$BROOT/mcp/servers.${SLUG}.json" >/dev/null

# Validate TOML (best-effort if tomllib available)
python3 - "$BROOT/mcp/codex-mcp.${SLUG}.generated.toml" <<'PY'
import sys
try:
    import tomllib
except ImportError:
    print("tomllib not available; skipping TOML parse", file=sys.stderr)
    sys.exit(0)
path = sys.argv[1]
with open(path, 'rb') as f:
    tomllib.load(f)
PY

echo "Structure + JSON/TOML OK for $SLUG"

# Optional VS Code CLI check (isolated user data dir)
if command -v code >/dev/null 2>&1; then
	USER_DATA_DIR=$(mktemp -d)
	PROFILE_NAME=$(
		python3 - "$BROOT/meta/bundle.meta.json" <<'PY'
import json, pathlib, sys
meta_path = pathlib.Path(sys.argv[1])
bundle = meta_path.parent.parent
name = json.loads(meta_path.read_text()).get("profile_name", bundle.name)
print(name)
PY
	)
	echo "VS Code CLI detected; performing isolated extension install check..."
	code --user-data-dir "$USER_DATA_DIR" --profile "$PROFILE_NAME" --list-extensions >/dev/null 2>&1 || true
	while IFS= read -r ext; do
		[[ -z $ext ]] && continue
		code --user-data-dir "$USER_DATA_DIR" --install-extension "$ext" --profile "$PROFILE_NAME" >/dev/null 2>&1 || true
	done <"$BROOT/workspace/.vscode/extensions.list"
	COUNT=$(grep -cvE '^\s*$' "${BROOT}/workspace/.vscode/extensions.list" || true)
	echo "Installed ${COUNT} extensions in isolated profile"
	rm -rf "$USER_DATA_DIR"
else
	echo "VS Code CLI not present; skipped CLI checks." >&2
fi

echo "Validation complete for $SLUG"
