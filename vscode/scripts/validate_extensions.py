#!/usr/bin/env python3
"""Validate VS Code extension lists in the packs tree.

- Ensures each non-empty, non-comment line in `extensions/*.txt` contains a dot (publisher.name).
- Reports duplicate extension IDs per file.
- Warns if the Codex placeholder id is still present.
- Prints a summary at the end.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS_DIR = ROOT / "packs"
CODEX_PLACEHOLDER = "your-org.codex-vscode"


def validate_extensions_file(path: Path) -> dict:
    errors = []
    warnings = []
    ids = []

    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "." not in line:
            errors.append(f"{path}: line {lineno}: invalid id (missing dot): {line!r}")
        ids.append(line)
        if line == CODEX_PLACEHOLDER:
            warnings.append(
                f"{path}: line {lineno}: Codex placeholder still present; replace with the real extension id."
            )

    counter = Counter(ids)
    dups = [ext for ext, count in counter.items() if count > 1]
    for ext in dups:
        warnings.append(f"{path}: duplicate extension id in file: {ext}")

    return {
        "path": path,
        "errors": errors,
        "warnings": warnings,
        "count": len(ids),
    }


def main() -> int:
    if not PACKS_DIR.exists():
        print(f"packs directory not found at {PACKS_DIR}", file=sys.stderr)
        return 1

    all_txt_files = sorted(PACKS_DIR.rglob("extensions.*.txt"))
    if not all_txt_files:
        print("No extensions.*.txt files found under packs/", file=sys.stderr)
        return 1

    total_files = 0
    total_ids = 0
    total_errors = 0
    total_warnings = 0

    for path in all_txt_files:
        total_files += 1
        result = validate_extensions_file(path)
        total_ids += result["count"]
        if result["errors"] or result["warnings"]:
            print(f"\n=== {path} ===")
        for msg in result["errors"]:
            print(f"ERROR: {msg}")
            total_errors += 1
        for msg in result["warnings"]:
            print(f"WARNING: {msg}")
            total_warnings += 1

    print("\nValidation summary:")
    print(f"  Files checked:   {total_files}")
    print(f"  IDs inspected:   {total_ids}")
    print(f"  Errors:          {total_errors}")
    print(f"  Warnings:        {total_warnings}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
