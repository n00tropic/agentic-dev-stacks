#!/usr/bin/env python3
"""Append a JSONL log entry for agent runs.

Usage:
  python3 agent-ecosystems/scripts/log-agent-run.py --agent <id> --stack <id> --status <status> [--scenario <id>] [--circuit <id>] [--tool-calls N] [--duration-ms N]
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "agent-ecosystems" / "logs" / "runs"
LOG_PATH = LOG_DIR / "runs.jsonl"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--stack", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--scenario")
    parser.add_argument("--circuit")
    parser.add_argument("--tool-calls", type=int, default=0)
    parser.add_argument("--duration-ms", type=int, default=0)
    args = parser.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agentId": args.agent,
        "stackId": args.stack,
        "scenarioId": args.scenario,
        "circuitId": args.circuit,
        "status": args.status,
        "toolCalls": args.tool_calls,
        "durationMs": args.duration_ms,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
