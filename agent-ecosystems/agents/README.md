# Agents

Exemplar agent blueprints demonstrating how to wire prompts and toolsets.

- `refactor-surgeon.agent.json`: Safely refactors existing code with minimal behavioural change. Uses `toolset.local-dev`; small diffs; asks before broad changes.
- `test-writer.agent.json`: Adds and improves tests. Uses `toolset.local-dev`; avoids production code edits unless seams are approved.
- `doc-surgeon.agent.json`: Focuses on documentation, READMEs, ADRs. Uses `toolset.review-only`; read-only on code, writes only to docs paths.

Each agent references a prompt file under `prompts/agents/` aligned with VS Code prompt file guidance. Safety blocks outline allowed paths, diff size limits, and whether commands or network access are permitted.
