#!/usr/bin/env python3
"""Validate agent ecosystem JSON files against their schemas.

Validates all JSON files under agent-ecosystems/{agents,toolsets,stacks,bundles}
using the schemas in agent-ecosystems/schemas.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[2]
ECOSYSTEM_ROOT = ROOT / "agent-ecosystems"
SCHEMA_DIR = ECOSYSTEM_ROOT / "schemas"

# Map subdirectory to schema filename
SCHEMA_MAP = {
    "agents": "agent.schema.json",
    "toolsets": "toolset.schema.json",
    "stacks": "stack.schema.json",
    "bundles": "bundle.schema.json",
}


def load_schema_store() -> Dict[str, dict]:
    store: Dict[str, dict] = {}
    for schema_path in SCHEMA_DIR.glob("*.schema.json"):
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_id = data.get("$id")
        if schema_id:
            store[schema_id] = data
    return store


def validate_file(path: Path, schema: dict, resolver: RefResolver) -> List[str]:
    errors: List[str] = []
    instance = json.loads(path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, resolver=resolver)
    for error in validator.iter_errors(instance):
        location = " / ".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{path}: {location}: {error.message}")
    return errors


def main() -> int:
    if not ECOSYSTEM_ROOT.exists():
        sys.stderr.write("agent-ecosystems directory not found.\n")
        return 1

    store = load_schema_store()
    resolver = RefResolver.from_schema({}, store=store)
    all_errors: List[str] = []
    checked: List[Tuple[str, int]] = []

    for subdir, schema_file in SCHEMA_MAP.items():
        schema_path = SCHEMA_DIR / schema_file
        if not schema_path.exists():
            all_errors.append(f"Missing schema: {schema_path}")
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        target_dir = ECOSYSTEM_ROOT / subdir
        if not target_dir.exists():
            continue
        count = 0
        for path in sorted(target_dir.glob("*.json")):
            count += 1
            all_errors.extend(validate_file(path, schema, resolver))
        checked.append((subdir, count))

    for subdir, count in checked:
        print(f"Validated {count} file(s) in {subdir}/")

    if all_errors:
        print("Validation errors:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("All agent ecosystem configs are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
