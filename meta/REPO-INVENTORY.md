# Repository Inventory

Short map of key directories and their roles.

- `vscode/`: Source of truth for VS Code packs (profiles, extensions, settings, MCP manifests), scripts, exports, and devcontainer assets.
- `agents/`: Authoritative Copilot agent definitions per stack (copied into bundles/workspaces).
- `agent-ecosystems/`: Circuits, toolchains, bundles, and validation harness for agent scenarios.
- `prompts/`: Prompt packs per stack and shared instructions for agents.
- `codex/`: Docs and guidance for configuring Codex/MCP safely on user machines.
- `docs/`: Antora-based documentation site (includes UI bundle under `docs/ui/agentic-neon-ui`).
- `scripts/`: Top-level helper scripts (QA, validation, installer scaffolds) alongside per-stack installers in `scripts/install/`.
- `dist/`: Release-ready artefacts (metadata, bundle zips) produced by CI/pipelines.
- `.github/`: Repo-level automation, instructions, and templates (workflows, issue/PR templates).
- `CONTROL.md`, `PROFILE_DIST.md`, `AGENTS.md`, `GOVERNANCE.md`: Governance for profile budgets, profile exports, and agent/MCP safety rules.
