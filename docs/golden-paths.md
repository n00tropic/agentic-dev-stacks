# Golden Paths (Circuits)

Repeatable, multi-agent workflows mapped to stacks. Detailed guides:

- JS/TS refactor + tests: `docs/golden-paths/js-ts-refactor.md`
- Incident review + postmortem: `docs/golden-paths/incident-postmortem.md`

Source of truth for circuits lives in `agent-ecosystems/circuits/*.circuit.yaml`.

Scenario harness:

```bash
python3 agent-ecosystems/scripts/run-agent-scenarios.py --list-circuits
```

Run a circuit directly (example):

```bash
python3 agent-ecosystems/scripts/run-agent-scenarios.py --circuit js-refactor-and-test --stack fullstack-js-ts
```
