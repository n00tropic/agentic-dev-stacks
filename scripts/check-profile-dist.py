#!/usr/bin/env python3
"""Validate that production stacks have matching .code-profile dist files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
PROFILE_DIST_PATH = ROOT / "PROFILE_DIST.md"


def parse_stack_table(path: Path) -> list[tuple[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    stacks: list[tuple[str, str]] = []
    in_section = False
    started_table = False
    for line in lines:
        if line.strip() == "## Stacks you can install":
            in_section = True
            continue
        if in_section:
            if not line.strip():
                if started_table:
                    break
                continue
            if not line.startswith("|"):
                if started_table:
                    break
                continue
            if set(line.strip()) <= {"|", "-", " "}:
                continue
            started_table = True
            parts = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(parts) < 3:
                continue
            slug, status = parts[0], parts[2]
            if slug.lower() in {"stack", "slug"} or status.lower() == "status":
                continue
            stacks.append((slug, status))
    return stacks


def parse_profile_table(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    profiles: dict[str, str] = {}
    in_table = False
    for line in lines:
        if line.strip().startswith("| Slug"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                if line.strip():
                    continue
                break
            if set(line.strip()) <= {"|", "-", " "}:
                continue
            parts = [part.strip(" `") for part in line.strip().strip("|").split("|")]
            if len(parts) < 4:
                continue
            slug, local_dist = parts[0], parts[3]
            profiles[slug] = local_dist
    return profiles


def main() -> int:
    stacks = parse_stack_table(README_PATH)
    profiles = parse_profile_table(PROFILE_DIST_PATH)

    missing: list[str] = []
    warnings: list[str] = []

    for slug, status in stacks:
        status_lower = status.lower()
        profile_path = profiles.get(slug)

        if status_lower.startswith("prod"):
            if profile_path is None:
                missing.append(
                    f"Missing PROFILE_DIST entry for production stack '{slug}'"
                )
                continue

            expected = ROOT / profile_path
            if not expected.is_file():
                missing.append(
                    f"Missing dist profile for production stack '{slug}': expected {profile_path}"
                )
        else:
            if profile_path is None:
                warnings.append(
                    f"WARN: Beta stack '{slug}' has no mapped dist profile (ok for now)"
                )
            else:
                expected = ROOT / profile_path
                if not expected.is_file():
                    warnings.append(
                        f"WARN: Beta stack '{slug}' maps to {profile_path} but file is missing"
                    )

    for warning in warnings:
        print(warning)

    if missing:
        print("Profile dist check failed:")
        for msg in missing:
            print(f"- {msg}")
        return 1

    print("Profile dist check passed: production stacks have mapped dist profiles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
