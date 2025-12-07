# Governance

Authoritative controls for profiles, agents, and MCP configuration in this repository.

## Sources of truth

- Profiles, settings, extensions, and MCP manifests live under `vscode/packs/**`.
- Profile budget and slug registry live in `CONTROL.md` (honour the ~20-profile VS Code limit per installation).
- Agent instructions live in `agents/<slug>/*.agent.md`; bundles copy them into `.github/agents/`.
- Guardrails and operating rules: `AGENTS.md`.

## Profiles and budgets

- Do not invent new slugs without updating `CONTROL.md`.
- Dist exports (`vscode/profiles-dist/*.code-profile`) must be regenerated via VS Code **Export Profile…**; never hand-edit.
- Keep installs non-destructive: installers live under `scripts/install/**` and `vscode/scripts/install-*.sh|ps1`; host dotfiles remain untouched.

## Agent instructions

- En-GB spelling by default; store authoritative prompts/agents under `agents/` and `prompts/`.
- When updating an agent, ensure the matching stack bundle copies it (via `vscode/scripts/build-bundles.py`).
- Validate scenario circuits with `python3 agent-ecosystems/scripts/run-agent-scenarios.py --list-circuits` as needed.

## MCP selection and safety

- Only use servers declared in `vscode/packs/*/mcp/servers.*.json`; new servers must be added there with provenance.
- Respect flags: `optional`, `experimental`, `privacy_sensitive`, `recommended_read_only`.
- Keep credentials out of git. Config fragments use `<TO_FILL>` placeholders; users merge into `~/.codex/config.toml` per `codex/docs/config-guides.md`.
- Prefer read-only posture for infra/cloud servers by default; opt-in for write access.

## QA expectations

- Before PRs or releases: `bash scripts/qa-preflight.sh` (extension validation, MCP JSON, shell lint, metadata, agent ecosystems checks).
- Per-pack extension validation: `cd vscode && ./scripts/helpers/validate-extensions.sh` (or PowerShell equivalent).
- Bundle validation: `cd vscode && bash scripts/validate-all-bundles.sh`.
- Document MCP manifests and profile budgets in any change descriptions so reviewers can confirm alignment with `CONTROL.md` and `AGENTS.md`.
