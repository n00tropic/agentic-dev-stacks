#!/usr/bin/env python3
"""Summarise agent run logs from agent-ecosystems/logs/runs/*.jsonl."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "agent-ecosystems" / "logs" / "runs"


def load_logs():
    entries = []
    if not LOG_DIR.exists():
        return entries
    for path in LOG_DIR.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                entries.append(json.loads(line))
            except Exception:
                continue
    return entries


def summarise(entries):
    by_agent = Counter()
    by_scenario = Counter()
    durations = defaultdict(list)
    statuses = Counter()
    for e in entries:
        by_agent[e.get("agentId")] += 1
        if e.get("scenarioId"):
            by_scenario[e["scenarioId"]] += 1
        statuses[e.get("status")] += 1
        durations[e.get("agentId")].append(e.get("durationMs", 0))

    print("Runs per agent:")
    for agent, count in by_agent.items():
        avg = mean(durations[agent]) if durations[agent] else 0
        print(f"- {agent}: {count} runs (avg duration {avg:.1f} ms)")

    print("\nRuns per scenario:")
    for scen, count in by_scenario.items():
        print(f"- {scen}: {count} runs")

    print("\nStatuses:")
    for status, count in statuses.items():
        print(f"- {status}: {count}")


def main() -> int:
    entries = load_logs()
    if not entries:
        print("No logs found.")
        return 0
    summarise(entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
