#!/usr/bin/env python3
"""Validate agent scenarios and emit manual checklists.

- Loads agents, toolsets, stacks.
- Validates scenario YAML files against schema and cross-references agent/toolset IDs.
- Writes markdown checklists to agent-ecosystems/tests/output/ (unless --no-output).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path
from typing import Dict, List

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
ECOSYSTEM_ROOT = ROOT / "agent-ecosystems"
TEST_ROOT = ECOSYSTEM_ROOT / "tests"
SCENARIO_DIR = TEST_ROOT / "scenarios"
OUTPUT_DIR = TEST_ROOT / "output"
SCHEMA_PATH = TEST_ROOT / "scenario.schema.yaml"
CONTRACT_DIR = ECOSYSTEM_ROOT / "contracts"


def load_json_files(directory: Path) -> Dict[str, dict]:
    items: Dict[str, dict] = {}
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        items[data["id"]] = data
    return items


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Missing scenario schema: {SCHEMA_PATH}")
    return yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_contracts() -> Dict[str, dict]:
    contracts: Dict[str, dict] = {}
    if not CONTRACT_DIR.exists():
        return contracts
    for path in sorted(CONTRACT_DIR.glob("*.contract.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        contracts[data.get("id")] = data
    return contracts


def validate_against_schema(instance: dict, schema: dict, path: Path) -> List[str]:
    errors: List[str] = []
    validator = Draft202012Validator(schema)
    for err in validator.iter_errors(instance):
        location = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{path}: {location}: {err.message}")
    return errors


def validate_cross_references(
    scenario: dict,
    agents: Dict[str, dict],
    toolsets: Dict[str, dict],
    contracts: Dict[str, dict],
    path: Path,
) -> List[str]:
    errors: List[str] = []
    agent_id = scenario.get("agentId")
    if agent_id not in agents:
        errors.append(f"{path}: agentId '{agent_id}' not found in agents/")
    else:
        agent_toolsets = set(agents[agent_id].get("toolsets", []))
        for ts in scenario.get("toolsets", []):
            if ts not in toolsets:
                errors.append(f"{path}: toolset '{ts}' not found in toolsets/")
            if ts not in agent_toolsets:
                errors.append(
                    f"{path}: toolset '{ts}' not listed on agent '{agent_id}'"
                )
        if contracts and agent_id not in contracts:
            errors.append(f"{path}: contract missing for agent '{agent_id}'")
        elif contracts and agent_id in contracts:
            contract_toolsets = set(contracts[agent_id].get("toolsets", []))
            for ts in scenario.get("toolsets", []):
                if ts not in contract_toolsets:
                    errors.append(
                        f"{path}: toolset '{ts}' not allowed by contract for '{agent_id}'"
                    )
    return errors


def check_contract_warnings(
    scenario: dict, contract: dict | None, path: Path
) -> List[str]:
    warnings: List[str] = []
    if not contract:
        return warnings
    allowed = contract.get("allowedPaths", [])
    forbidden = contract.get("forbiddenPaths", [])
    hint_paths = scenario.get("workspaceHints", {}).get("paths", [])
    for p in hint_paths:
        if forbidden and any(fnmatch.fnmatch(p, fpat) for fpat in forbidden):
            warnings.append(f"{path}: workspace hint '{p}' overlaps forbiddenPaths")
        if allowed and not any(fnmatch.fnmatch(p, apat) for apat in allowed):
            warnings.append(f"{path}: workspace hint '{p}' not covered by allowedPaths")
    return warnings


def render_checklist(scenario: dict, agent: dict) -> str:
    lines: List[str] = []
    lines.append(f"# Scenario: {scenario['id']}")
    lines.append("")
    lines.append(
        f"Agent: {agent.get('name', scenario['agentId'])} ({scenario['agentId']})"
    )
    lines.append(f"Description: {scenario['description']}")
    lines.append("")
    lines.append("## Inputs")
    for msg in scenario.get("inputs", []):
        lines.append(f"- {msg}")
    lines.append("")
    lines.append("## Must Do")
    for item in scenario.get("expectations", {}).get("mustDo", []):
        lines.append(f"- [ ] {item}")
    lines.append("")
    lines.append("## Must Not Do")
    for item in scenario.get("expectations", {}).get("mustNotDo", []):
        lines.append(f"- [ ] {item}")
    lines.append("")
    lines.append("## Success Criteria")
    for item in scenario.get("successCriteria", []):
        lines.append(f"- [ ] {item}")
    lines.append("")
    lines.append("## Evaluator Notes")
    lines.append("- [ ] Notes: ")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run static checks for agent scenarios"
    )
    parser.add_argument(
        "--no-output", action="store_true", help="Skip writing markdown outputs"
    )
    args = parser.parse_args()

    agents = load_json_files(ECOSYSTEM_ROOT / "agents")
    toolsets = load_json_files(ECOSYSTEM_ROOT / "toolsets")
    stacks = load_json_files(ECOSYSTEM_ROOT / "stacks")  # reserved for future use
    contracts = load_contracts()

    schema = load_schema()

    all_errors: List[str] = []
    all_warnings: List[str] = []
    summary: List[str] = []

    if args.no_output:
        output_dir = None
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_dir = OUTPUT_DIR

    for path in sorted(SCENARIO_DIR.glob("*.yaml")):
        scenario = yaml.safe_load(path.read_text(encoding="utf-8"))
        errs = []
        errs.extend(validate_against_schema(scenario, schema, path))
        errs.extend(
            validate_cross_references(scenario, agents, toolsets, contracts, path)
        )

        warnings = []
        if not errs:
            warnings = check_contract_warnings(
                scenario, contracts.get(scenario.get("agentId")), path
            )
            all_warnings.extend(warnings)

        status = "OK" if not errs else "FAIL"
        notes = ""
        if errs:
            all_errors.extend(errs)
            notes = f"{len(errs)} error(s)"
        elif warnings:
            notes = f"{len(warnings)} warning(s)"
        summary.append(f"{path.stem} | {scenario.get('agentId')} | {status} | {notes}")

        if not errs and output_dir:
            agent = agents.get(scenario["agentId"], {})
            md = render_checklist(scenario, agent)
            (output_dir / f"{path.stem}.md").write_text(md, encoding="utf-8")

    print("SCENARIO ID | AGENT | STATUS | NOTES")
    for row in summary:
        print(row)

    if all_errors:
        print("Errors:")
        for e in all_errors:
            print(f"- {e}")
        return 1

    if all_warnings:
        print("Warnings:")
        for w in all_warnings:
            print(f"- {w}")

    print("All scenarios validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
