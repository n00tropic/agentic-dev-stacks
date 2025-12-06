#!/usr/bin/env python3
"""Validate .vscode/mcp.json structure for workspace MCP config.

Checks:
- JSON parseable; top-level has "mcpServers" object.
- Each server has: command (str), args (list[str]), env (object).
Warnings (non-fatal):
- command is not /bin/sh
- args do not start with ["-c", ...]
- env values that look like inlined secrets (simple heuristic)

Exit codes:
- 0 on success
- 1 on structural errors
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
MCP_PATH = WORKSPACE_ROOT / ".vscode" / "mcp.json"


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Invalid JSON in {path}: {e}\n")
        sys.exit(1)
    except FileNotFoundError:
        sys.stderr.write(f"Missing {path}\n")
        sys.exit(1)


def looks_like_secret(val: str) -> bool:
    lower = val.lower()
    return (
        any(
            prefix in lower
            for prefix in ("sk-", "token", "secret", "api_key", "apikey")
        )
        or len(val) > 80
    )


def _assert_required_keys(name: str, obj: Dict[str, Any], keys: list[str]) -> None:
    for key in keys:
        if key not in obj:
            sys.stderr.write(f"ERROR: server '{name}' missing '{key}'\n")
            sys.exit(1)


def _assert_string_field(name: str, obj: Dict[str, Any], key: str) -> None:
    if not isinstance(obj[key], str):
        sys.stderr.write(f"ERROR: server '{name}' {key} must be string\n")
        sys.exit(1)


def _assert_list_of_strings(name: str, obj: Dict[str, Any], key: str) -> None:
    if not isinstance(obj[key], list) or not all(isinstance(a, str) for a in obj[key]):
        sys.stderr.write(f"ERROR: server '{name}' {key} must be list[str]\n")
        sys.exit(1)


def _assert_env_map(name: str, obj: Dict[str, Any], key: str) -> None:
    if not isinstance(obj[key], dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in obj[key].items()
    ):
        sys.stderr.write(
            f"ERROR: server '{name}' {key} must be object of string values\n"
        )
        sys.exit(1)


def _warn_command_not_sh(name: str, obj: Dict[str, Any]) -> None:
    if obj["command"] != "/bin/sh":
        sys.stderr.write(
            f"WARN: server '{name}' command is not /bin/sh (got '{obj['command']}')\n"
        )


def _warn_args_not_prefix(name: str, obj: Dict[str, Any]) -> None:
    if len(obj["args"]) < 2 or obj["args"][0] != "-c":
        sys.stderr.write(f"WARN: server '{name}' args do not start with ['-c', ...]\n")


def _warn_inline_secrets(name: str, obj: Dict[str, Any]) -> None:
    for k, v in obj["env"].items():
        if looks_like_secret(v):
            sys.stderr.write(
                f"WARN: server '{name}' env '{k}' looks like inline secret; prefer env vars\n"
            )


def validate_server(name: str, srv: Dict[str, Any]) -> None:
    # Validate required keys present.
    _assert_required_keys(name, srv, ["command", "args", "env"])
    _assert_string_field(name, srv, "command")
    _assert_list_of_strings(name, srv, "args")
    _assert_env_map(name, srv, "env")

    _warn_command_not_sh(name, srv)
    _warn_args_not_prefix(name, srv)
    _warn_inline_secrets(name, srv)


def main() -> None:
    data = load_json(MCP_PATH)
    if "mcpServers" not in data or not isinstance(data["mcpServers"], dict):
        sys.stderr.write("ERROR: top-level 'mcpServers' must be an object\n")
        sys.exit(1)
    for name, srv in data["mcpServers"].items():
        if not isinstance(srv, dict):
            sys.stderr.write(f"ERROR: server '{name}' must be an object\n")
            sys.exit(1)
        validate_server(name, srv)
    print("MCP config looks structurally valid.")


if __name__ == "__main__":
    main()
