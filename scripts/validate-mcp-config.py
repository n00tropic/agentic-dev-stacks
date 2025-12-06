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


def validate_server(name: str, srv: Dict[str, Any]) -> None:
    required = ["command", "args", "env"]
    for key in required:
        if key not in srv:
            sys.stderr.write(f"ERROR: server '{name}' missing '{key}'\n")
            sys.exit(1)
    if not isinstance(srv["command"], str):
        sys.stderr.write(f"ERROR: server '{name}' command must be string\n")
        sys.exit(1)
    if not isinstance(srv["args"], list) or not all(
        isinstance(a, str) for a in srv["args"]
    ):
        sys.stderr.write(f"ERROR: server '{name}' args must be list[str]\n")
        sys.exit(1)
    if not isinstance(srv["env"], dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in srv["env"].items()
    ):
        sys.stderr.write(
            f"ERROR: server '{name}' env must be object of string values\n"
        )
        sys.exit(1)

    # Warnings (non-fatal)
    if srv["command"] != "/bin/sh":
        sys.stderr.write(
            f"WARN: server '{name}' command is not /bin/sh (got '{srv['command']}')\n"
        )
    if not (len(srv["args"]) >= 2 and srv["args"][0] == "-c"):
        sys.stderr.write(f"WARN: server '{name}' args do not start with ['-c', ...]\n")
    for k, v in srv["env"].items():
        if looks_like_secret(v):
            sys.stderr.write(
                f"WARN: server '{name}' env '{k}' looks like inline secret; prefer env vars\n"
            )


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
