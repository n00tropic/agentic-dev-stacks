# Agent Scenarios

Scenarios describe manual evaluation cases for agents. Files live in `agent-ecosystems/tests/scenarios/` using YAML and the schema at `agent-ecosystems/tests/scenario.schema.yaml`.

## Fields

- `id`: unique slug.
- `description`: short, human-readable summary.
- `agentId`: agent under test (must match an entry in `agent-ecosystems/agents/`).
- `toolsets`: allowed/expected toolsets for this scenario.
- `workspaceHints`: paths, languages, and optional notes about the repo state.
- `inputs`: list of user prompts/messages.
- `expectations.mustDo`: required behaviours.
- `expectations.mustNotDo`: forbidden behaviours.
- `successCriteria`: checklist for what good looks like.
- `notes`: optional freeform guidance for evaluators.

## Writing new scenarios

1. Copy an existing YAML file in `scenarios/` and adjust values.
2. Keep IDs lowercase with dashes/underscores.
3. Align `agentId` and `toolsets` with existing definitions.
4. Keep prompts realistic and scoped to the agent’s role.

## Running scenarios (manual loop for now)

- Run static validation and checklist generation:
  ```bash
  python3 agent-ecosystems/scripts/run-agent-scenarios.py
  ```
- Open the generated checklist in `agent-ecosystems/tests/output/<scenario>.md`.
- In VS Code, select the appropriate stack/profile, invoke the agent in Copilot Chat, and walk through the prompts.
- Tick checkboxes and add evaluator notes manually.

Automation will plug into this format later; the current flow is intentionally manual and non-destructive.
