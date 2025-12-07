# Agent Ecosystem Logs

Log runs to JSONL under `agent-ecosystems/logs/runs/` using `agent-ecosystems/scripts/log-agent-run.py`.

Recommended fields:

- timestamp (ISO8601, UTC)
- stackId
- agentId
- scenarioId (optional)
- circuitId (optional)
- status (success|failure|partial)
- toolCalls (count)
- durationMs

Summaries: use `agent-ecosystems/scripts/summarise-logs.py` to aggregate runs per agent/scenario and basic stats.

Note: logging is opt-in; no secrets should be recorded.
