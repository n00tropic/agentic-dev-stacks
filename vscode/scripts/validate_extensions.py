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
    ids, errors, warnings = _collect_extension_issues(path)
    warnings.extend(_duplicate_warnings(ids, path))

    return {
        "path": path,
        "errors": errors,
        "warnings": warnings,
        "count": len(ids),
    }


def _collect_extension_issues(path: Path) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids: list[str] = []

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

    return ids, errors, warnings


def _duplicate_warnings(ids: list[str], path: Path) -> list[str]:
    counter = Counter(ids)
    return [
        f"{path}: duplicate extension id in file: {ext}"
        for ext, count in counter.items()
        if count > 1
    ]


def main() -> int:
    if not PACKS_DIR.exists():
        print(f"packs directory not found at {PACKS_DIR}", file=sys.stderr)
        return 1

    all_txt_files = sorted(PACKS_DIR.rglob("extensions.*.txt"))
    if not all_txt_files:
        print("No extensions.*.txt files found under packs/", file=sys.stderr)
        return 1

    totals = {"files": 0, "ids": 0, "errors": 0, "warnings": 0}

    for path in all_txt_files:
        totals["files"] += 1
        result = validate_extensions_file(path)
        totals["ids"] += result["count"]
        _print_result(path, result, totals)

    _print_summary(totals)
    return 1 if totals["errors"] else 0


def _print_result(path: Path, result: dict, totals: dict) -> None:
    if result["errors"] or result["warnings"]:
        print(f"\n=== {path} ===")
    totals["errors"] += _print_messages("ERROR", result["errors"])
    totals["warnings"] += _print_messages("WARNING", result["warnings"])


def _print_messages(label: str, messages: list[str]) -> int:
    for msg in messages:
        print(f"{label}: {msg}")
    return len(messages)


def _print_summary(totals: dict) -> None:
    print("\nValidation summary:")
    print(f"  Files checked:   {totals['files']}")
    print(f"  IDs inspected:   {totals['ids']}")
    print(f"  Errors:          {totals['errors']}")
    print(f"  Warnings:        {totals['warnings']}")


if __name__ == "__main__":
    raise SystemExit(main())
