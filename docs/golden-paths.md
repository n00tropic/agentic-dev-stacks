# Golden Paths (Circuits)

Configuration-only multi-agent flows capturing repeatable workflows:

- `js-refactor-and-test` (fullstack-js-ts): refactor-surgeon then test-writer.
- `data-pipeline-hardening` (python-data-analytics): pipeline-refactorer then data-explorer for validation ideas.
- `incident-review-and-postmortem` (infra-ops-sre): infra-reviewer then incident-scribe.

Use `agent-ecosystems/circuits/*.circuit.yaml` as source of truth. The scenario harness can list circuits with `python3 agent-ecosystems/scripts/run-agent-scenarios.py --list-circuits`.
