# Golden Path: JS/TS Refactor with Tests

Persona: Full-stack JS/TS engineers using the `fullstack-js-ts` stack.

Prerequisites

- Run the stack installer for your OS (e.g. `./scripts/install/fullstack-js-ts-macos.sh`).
- Open the workspace: `code vscode/exports/workspaces/fullstack-js-ts/fullstack-js-ts.code-workspace --profile "Fullstack JS/TS – Web & API"`.
- Optional: import the vetted profile export at `vscode/profiles-dist/fullstack-js-ts.code-profile` if you have generated one via **Export Profile…**.

Flow (10–15 minutes)

1. Pick a target module/component to refactor. Ensure tests run locally (e.g. `npm test`, `pnpm test`, or `npm run lint`).
2. Open Copilot Chat (or your agent runner) and select the `refactor-surgeon` agent.
   - Prompt: "Propose a small refactor plan for <file>, keeping behaviour unchanged."
   - Inspect the plan; ask for a tighter, incremental diff if it is too broad.
3. Let `refactor-surgeon` apply the refactor. Keep changes small; stop if it proposes sweeping rewrites.
4. Switch to the `test-writer` agent.
   - Prompt: "Add/adjust tests for the changes in <file>; prefer minimal new seams."
   - Run the suggested test command locally. Example: `npm test -- <pattern>`.
5. If docs need tweaking, ask `doc-surgeon` for a short README/update snippet tied to the refactor.
6. Review the diff in VS Code source control. Keep/adjust; discard anything noisy.
7. Optional automation check: run the scenario harness for this circuit:
   ```bash
   python3 agent-ecosystems/scripts/run-agent-scenarios.py --circuit js-refactor-and-test --stack fullstack-js-ts
   ```

MCP servers (all optional, align with manifest)

- `context7-docs` (docs lookup, read-only): ask for API usage across versions.
- `github` (VCS, token required): read issues/PRs, avoid mutating actions unless scoped.
- `sonatype-deps` (dependency insight): ask for license/security notes on a package before upgrading.
- `elasticsearch`/`mongodb` (data/search): keep to read-only queries in shared environments.

Expected outcome

- A small, behaviour-safe refactor plus targeted tests.
- A short doc/update if needed.
- Diff is reviewable and scoped; MCP usage stayed read-only unless explicitly opted into write operations.
