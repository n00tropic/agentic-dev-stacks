#!/usr/bin/env bash
set -euo pipefail

# Comprehensive QA preflight check for agentic-dev-stacks
# Run this before any release to ensure everything is healthy

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=========================================="
echo "QA Preflight Health Checks"
echo "=========================================="
echo ""

PASS=0
FAIL=0

run_check() {
	local name="$1"
	shift
	echo ">>> Checking: $name"
	if "$@"; then
		echo "    ✓ PASS"
		PASS=$((PASS + 1))
	else
		echo "    ✗ FAIL"
		FAIL=$((FAIL + 1))
	fi
	echo ""
}

# 1. Extension validation
run_check "Extension lists validation (shell)" \
	bash vscode/scripts/helpers/validate-extensions.sh

run_check "Extension metadata validation (Python)" \
	python3 vscode/scripts/validate_extensions.py

# 2. MCP configuration validation
run_check "Workspace MCP config validation" \
	python3 scripts/validate-mcp-config.py

# 3. Python syntax check
run_check "Python syntax check (all scripts)" \
	python3 -m compileall vscode codex scripts docs

# 4. JSON validation (skip .vscode which allows comments/JSONC)
run_check "JSON syntax validation" bash -c '
python3 - <<PY
import json, pathlib, sys
root = pathlib.Path(".")
skip_parts = {".trunk/tools", "exports/", ".vscode/"}
fail = False
for path in root.rglob("*.json"):
  posix = path.as_posix()
  if any(part in posix for part in skip_parts):
    continue
  try:
    json.loads(path.read_text(encoding="utf-8"))
  except Exception as exc:
    print(f"{path}: {exc}")
    fail = True
if fail:
  sys.exit(1)
PY
'

# 4b. Agent ecosystem schema validation
run_check "Agent ecosystem config validation" \
	python3 agent-ecosystems/scripts/validate-ecosystem-configs.py

# 5. TOML validation
run_check "TOML syntax validation" bash -c '
python3 - <<PY
import pathlib, sys
try:
  import tomllib
except ImportError:
  print("tomllib not available; skipping")
  sys.exit(0)
root = pathlib.Path(".")
skip_parts = {".trunk/tools", "exports/"}
fail = False
for path in root.rglob("*.toml"):
  posix = path.as_posix()
  if any(part in posix for part in skip_parts):
    continue
  try:
    tomllib.loads(path.read_text(encoding="utf-8"))
  except Exception as exc:
    print(f"{path}: {exc}")
    fail = True
if fail:
  sys.exit(1)
PY
'

# 6. Shell script validation (skip trunk if not available)
run_check "Shell scripts validation" \
	env SKIP_TRUNK=1 bash scripts/validate-all-scripts.sh

# 7. Verify all profile slugs have installation scripts
run_check "Verify standalone installation scripts exist" bash -c '
for slug in core-base-dev qa-static-analysis docs-librarian gitops-code-review \
  experimental-preview fullstack-js-ts frontend-ux-ui node-backend-services \
  python-services-clis python-data-ml infra-devops data-db-analytics \
  desktop-gui-cross macos-apple-platforms windows-polyglot-wsl linux-ci-headless; do
  if [[ ! -f "vscode/scripts/install-${slug}.sh" ]]; then
    echo "Missing install-${slug}.sh"
    exit 1
  fi
done
echo "All 16 profile installation scripts found"
'

# 8. Verify pack-level installation scripts exist
run_check "Verify pack-level installation scripts exist" bash -c '
for pack in 00-core-base 10-fullstack-js-ts 20-python-data-ml \
  30-infra-devops-platform 40-docs-knowledge 50-experimental-playground; do
  for platform in linux macos; do
    script="vscode/packs/${pack}/scripts/${platform}/install-profiles.sh"
    if [[ ! -f "$script" ]]; then
      echo "Missing ${script}"
      exit 1
    fi
  done
  script="vscode/packs/${pack}/scripts/windows/Install-Profiles.ps1"
  if [[ ! -f "$script" ]]; then
    echo "Missing ${script}"
    exit 1
  fi
done
echo "All pack-level installation scripts found"
'

# 9. Check that CONTROL.md and export-map.yaml are in sync
run_check "Profile metadata consistency check" bash -c '
python3 - <<PY
import json
from pathlib import Path

root = Path(".")
control = (root / "CONTROL.md").read_text()
export_map_data = json.loads((root / "vscode/export-map.yaml").read_text())

control_slugs = set()
for line in control.splitlines():
  if "|" in line:
    parts = [p.strip() for p in line.strip("|").split("|")]
    if len(parts) >= 3:
      slug = parts[2]
      if slug and slug not in {"Slug", "---------------------"}:
        control_slugs.add(slug)

export_slugs = set(export_map_data.get("profiles", {}).keys())

if control_slugs != export_slugs:
  missing_in_export = control_slugs - export_slugs
  missing_in_control = export_slugs - control_slugs
  if missing_in_export:
    print(f"Slugs in CONTROL.md but not in export-map.yaml: {missing_in_export}")
  if missing_in_control:
    print(f"Slugs in export-map.yaml but not in CONTROL.md: {missing_in_control}")
  exit(1)

print(f"Profile metadata is consistent: {len(control_slugs)} profiles")
PY
'

# Summary
echo "=========================================="
echo "QA Preflight Summary"
echo "=========================================="
echo "Checks passed: $PASS"
echo "Checks failed: $FAIL"
echo ""

if [[ $FAIL -eq 0 ]]; then
	echo "✓ All checks passed! Project is healthy."
	exit 0
else
	echo "✗ Some checks failed. Review output above."
	exit 1
fi
