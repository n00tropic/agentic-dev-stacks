#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
	echo "Usage: $(basename "$0") <profile-slug>"
	echo "Example: $(basename "$0") fullstack-js-ts"
	exit 1
fi

SLUG="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKS_DIR="$ROOT/packs"

if [[ ! -d $PACKS_DIR ]]; then
	echo "packs directory not found at $PACKS_DIR"
	exit 1
fi

# Resolve settings override file
mapfile -t settings_matches < <(find "$PACKS_DIR" -type f -name "settings.${SLUG}.json" 2>/dev/null || true)

if [[ ${#settings_matches[@]} -eq 0 ]]; then
	echo "No settings override found for slug '${SLUG}' (looked for settings.${SLUG}.json)"
	exit 1
elif [[ ${#settings_matches[@]} -gt 1 ]]; then
	echo "Multiple settings overrides found for slug '${SLUG}':"
	printf '  %s
' "${settings_matches[@]}"
	echo "Please disambiguate."
	exit 1
fi

SETTINGS_FILE="${settings_matches[0]}"
echo "Using settings override: $SETTINGS_FILE"

# Resolve extensions list
mapfile -t ext_matches < <(find "$PACKS_DIR" -type f -name "extensions.${SLUG}.txt" 2>/dev/null || true)

if [[ ${#ext_matches[@]} -eq 0 ]]; then
	echo "No extensions list found for slug '${SLUG}' (looked for extensions.${SLUG}.txt)"
elif [[ ${#ext_matches[@]} -gt 1 ]]; then
	echo "Multiple extensions lists found for slug '${SLUG}':"
	printf '  %s
' "${ext_matches[@]}"
	echo "Please disambiguate manually."
else
	EXT_FILE="${ext_matches[0]}"
	echo "Extensions list: $EXT_FILE"
fi

# Pick merge script based on OS
UNAME="$(uname -s)"
if [[ $UNAME == "Darwin" ]]; then
	MERGER="$ROOT/scripts/macos/merge-settings.sh"
else
	MERGER="$ROOT/scripts/linux/merge-settings.sh"
fi

if [[ ! -x $MERGER ]]; then
	echo "Merge script not found or not executable: $MERGER"
	exit 1
fi

echo "Merging settings via: $MERGER"
"$MERGER" "$SETTINGS_FILE"

if [[ -n ${EXT_FILE-} && -f $EXT_FILE ]]; then
	echo
	echo "To install extensions for profile '${SLUG}', run (example):"
	echo
	while IFS= read -r line; do
		trimmed="${line#"${line%%[![:space:]]*}"}"
		[[ -z $trimmed || $trimmed == \#* ]] && continue
		echo "  code --install-extension "$trimmed""
	done <"$EXT_FILE"
	echo
	echo "You can optionally add: --profile " Name <Profile >" to bind installs to a specific VS Code profile."
fi

echo "Done."
