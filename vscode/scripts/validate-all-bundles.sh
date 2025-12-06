#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="$ROOT/scripts/validate-bundle.sh"

mapfile -t ZIPS < <(find "$ROOT/exports/bundles" -maxdepth 1 -name '*-bundle.zip' -print)

if [[ ${#ZIPS[@]} -eq 0 ]]; then
	echo "No bundle zips found under exports/bundles" >&2
	exit 1
fi

PASS=0
FAIL=0

for zip in "${ZIPS[@]}"; do
	slug=$(basename "$zip" -bundle.zip)
	echo "==== Validating $slug ===="
	if "$VALIDATOR" "$slug"; then
		PASS=$((PASS + 1))
	else
		FAIL=$((FAIL + 1))
	fi
done

echo "Validation complete: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
