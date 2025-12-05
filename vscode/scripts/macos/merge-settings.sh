#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: merge-settings.sh path/to/override-settings.json"
  exit 1
fi

OVERRIDE="$1"

if [[ ! -f "$OVERRIDE" ]]; then
  echo "Override file not found: $OVERRIDE"
  exit 1
fi

UNAME="$(uname -s)"
if [[ "$UNAME" == "Darwin" ]]; then
  TARGET="$HOME/Library/Application Support/Code/User/settings.json"
else
  TARGET="$HOME/.config/Code/User/settings.json"
fi

mkdir -p "$(dirname "$TARGET")"

if command -v jq >/dev/null 2>&1; then
  echo "Using jq to merge settings..."
  if [[ -f "$TARGET" ]]; then
    BACKUP="${TARGET}.bak.$(date +%Y%m%d%H%M%S)"
    cp "$TARGET" "$BACKUP"
    echo "Existing settings backed up to: $BACKUP"
    jq -s '.[0] * .[1]' "$TARGET" "$OVERRIDE" > "${TARGET}.tmp"
  else
    jq '.' "$OVERRIDE" > "${TARGET}.tmp"
  fi
  mv "${TARGET}.tmp" "$TARGET"
else
  echo "jq not found; copying override file directly to: $TARGET"
  if [[ -f "$TARGET" ]]; then
    BACKUP="${TARGET}.bak.$(date +%Y%m%d%H%M%S)"
    cp "$TARGET" "$BACKUP"
    echo "Existing settings backed up to: $BACKUP"
  fi
  cp "$OVERRIDE" "$TARGET"
fi

echo "Settings updated at: $TARGET"
