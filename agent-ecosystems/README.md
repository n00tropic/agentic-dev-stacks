# Agent Ecosystems

This area defines the building blocks for composing agent-based developer environments. It mirrors existing repository docs but stays self-contained so you can reason about the pieces without jumping elsewhere.

- **Agent Blueprints** (under `agents/`): JSON definitions describing agent identity, role, safety posture, prompt sources, and the toolsets they depend on.
- **Toolsets** (under `toolsets/`): Shared collections of MCP servers and Copilot tools aligned to a security profile (read-only/read-write/admin) so agents inherit consistent capabilities.
- **Workspace Stacks** (under `stacks/`): Pair a devcontainer, VS Code profile export, and default agents/toolsets for a target language or workflow.
- **Bundles** (under `bundles/`): OS-specific install metadata that points at the stack artefacts and scripts for reproducible setup.

For broader context on profiles, packs, and MCP safety, see the repository `README.md` and `docs/` (notably `codex/docs/config-guides.md` and `codex/docs/safe-vs-danger-modes.md`). The ecosystem files here stay the source of truth for agent composition; generated exports and install scripts should reference these definitions.

Current stack/devcontainer/profile placeholders:

- Devcontainer: `vscode/.devcontainer/devcontainer.json` (TypeScript/Node base image with core JS/TS + Copilot extensions).
- Profile export: `vscode/profiles-dist/fullstack-js-ts.code-profile` (export via VS Code; do not hand-edit).

## Validation

Run the validator before committing changes to agents, toolsets, stacks, or bundles:

```bash
python3 agent-ecosystems/scripts/validate-ecosystem-configs.py
```

This checks all JSON files in `agent-ecosystems/{agents,toolsets,stacks,bundles}` against the schemas in `agent-ecosystems/schemas/`.

## Agent Evaluation

- Define scenarios in `agent-ecosystems/tests/scenarios/` (see `agent-ecosystems/tests/SCENARIOS.md`).
- Generate checklists and validate scenarios:

```bash
python3 agent-ecosystems/scripts/run-agent-scenarios.py
```

This performs static validation (schema + cross-references) and writes manual checklists to `agent-ecosystems/tests/output/`. Use these with Copilot Chat and the relevant stack/profile to run manual evaluations.

## Building bundles

- Build all bundles and write ZIPs to `dist/bundles/` with metadata in `dist/metadata/`:

```bash
python3 agent-ecosystems/scripts/build-ecosystem-bundles.py
```

- Wrapper script: `scripts/build-agent-ecosystem-bundles.sh`
- Combined check + optional build: `scripts/check-agent-ecosystems.sh [--with-bundles]`

Outputs follow the naming conventions documented in `dist/README.md`.

## Hero stack: Fullstack JS/TS

- **Persona:** Full-stack JS/TS developers building web and API features.
- **Default agents:** refactor-surgeon (safe refactors), test-writer (tests only), doc-surgeon (docs/ADRs). Add planning/architecture prompts via workspace prompts as needed.
- **Toolsets:** `toolset.local-dev` (repo read/write, docs, deps) and `toolset.review-only` (read-only review posture).
- **Typical tasks:** refactor services/components, add coverage for serializers/hooks, polish docs/ADRs, review changes with MCP-powered context.

## Stack catalogue

See `docs/stack-catalogue.md` for a catalogue of stacks (Fullstack JS/TS available now; others coming soon).

## Automation roadmap

See `docs/architecture/agent-ops-automation.md` for how a future “Agent Ops” agent could orchestrate validations, builds, and releases.
