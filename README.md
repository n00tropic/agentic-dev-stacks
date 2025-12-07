<!-- vale off -->

# Agentic Dev Stacks

Scoped, cross-OS VS Code packs plus MCP manifests and devcontainers. One repo, one truth, no host dotfiles touched.

## What is this?

Agentic development stacks built as a compiler: packs in `vscode/packs/**`, agents in `agents/**`, MCP manifests under `vscode/packs/*/mcp/`, and reproducible exports under `vscode/exports/**` (git-ignored). Dist profile exports live in `vscode/profiles-dist/*.code-profile` (never hand-edit; regenerate via VS Code **Export Profile…**).

## Why you might care

- New machines and new hires land in a governed VS Code profile within minutes.
- Reproducible agent + MCP setup across macOS, Windows, and Linux.
- Profile budgets and safety flags are explicit (see `CONTROL.md` and `AGENTS.md`).
- Devcontainer-first: keep host dotfiles clean while validating stacks end-to-end.

## 5-minute Quickstart (Fullstack JS/TS)

Prerequisites: VS Code with `code` CLI enabled, Git, Python 3; Docker/Podman + Dev Containers extension if you want the containerised toolchain.

```bash
# macOS
git clone https://github.com/n00tropic/agentic-dev-stacks.git
cd agentic-dev-stacks
./scripts/install/fullstack-js-ts-macos.sh
```

```bash
# Linux
git clone https://github.com/n00tropic/agentic-dev-stacks.git
cd agentic-dev-stacks
./scripts/install/fullstack-js-ts-linux.sh
```

```powershell
# Windows (PowerShell)
git clone https://github.com/n00tropic/agentic-dev-stacks.git
cd agentic-dev-stacks
.\scripts\install\fullstack-js-ts-windows.ps1
```

What happens:

- Builds the `fullstack-js-ts` export via `vscode/scripts/export-packs.py`.
- Installs extensions into the `Fullstack JS/TS – Web & API` profile via the VS Code CLI.
- Opens the exported workspace at `vscode/exports/workspaces/fullstack-js-ts/fullstack-js-ts.code-workspace`.
- Leaves global settings untouched. Optional: import a vetted profile export from `vscode/profiles-dist/fullstack-js-ts.code-profile` once you have generated a real export.

## Golden paths

- JS/TS refactor + tests: pair refactor-surgeon with test-writer (see `docs/golden-paths.md`).
- Incident review + postmortem: infra-reviewer then incident-scribe (see `docs/golden-paths.md`).

## Stacks you can install

| Stack                 | Persona           | Agents & toolsets (high level)                                               | Quickstart                                       |
| --------------------- | ----------------- | ---------------------------------------------------------------------------- | ------------------------------------------------ | ---- |
| fullstack-js-ts       | Full-stack JS/TS  | refactor-surgeon, test-writer, doc-surgeon; local-dev + review-only toolsets | `./scripts/install/fullstack-js-ts-<os>.sh       | ps1` |
| python-data-analytics | Data/ML/analytics | data-explorer, pipeline-refactorer, doc-surgeon; local-dev + review-only     | `./scripts/install/python-data-analytics-<os>.sh | ps1` |
| infra-ops-sre         | Infra / SRE       | infra-reviewer, incident-scribe, doc-surgeon; review-only                    | `./scripts/install/infra-ops-sre-<os>.sh         | ps1` |

More detail: `docs/stack-catalogue.md` (personas, MCP servers, prompts).

## Governance and safety

- Profile budget: tracked in `CONTROL.md` (VS Code limits ~20 profiles per installation).
- No dotfile edits: profiles, MCP manifests, and prompts are authored under `vscode/**` and `agents/**`; generated artefacts in `vscode/exports/**` stay untracked.
- Secrets stay out of git: MCP manifests use `<TO_FILL>` placeholders; copy generated TOML into `~/.codex/config.toml` per `codex/docs/config-guides.md`.
- Dist profiles: `.code-profile` files are regenerated via VS Code **Export Profile…**; never hand-edit.

## QA and validation

- Validate extensions: `cd vscode && ./scripts/helpers/validate-extensions.sh`
- Validate bundles: `cd vscode && bash scripts/validate-all-bundles.sh`
- Full preflight: `bash scripts/qa-preflight.sh` (extensions, MCP JSON, shell lint, metadata checks, agent ecosystem scenarios).

## Advanced use

- Build a distributable bundle: `cd vscode && python scripts/build-bundles.py fullstack-js-ts` (outputs to `vscode/exports/bundles/`, git-ignored).
- Author a new pack: update `vscode/packs/<pack>/` assets, then refresh exports via `python scripts/export-packs.py <slug>`; keep slugs aligned with `CONTROL.md`.
- Devcontainer automation: `devcontainer up --workspace-folder .` to build + validate in isolation (preferred for CI-like runs).
- MCP bundles: see `docs/mcp-bundles.md` for how to align existing MCP servers with `.mcpb` distribution.

## Docs and references

- Docs site: <https://n00tropic.github.io/agentic-dev-stacks> (built from `docs/`). Build locally with `cd docs && ./build-docs.sh`.
- Safe vs danger modes and Codex wiring: `codex/docs/config-guides.md`, `codex/docs/safe-vs-danger-modes.md`.
- Prompts: `prompts/stacks/*.prompts.md`; agent contracts and schemas: `agent-ecosystems/contracts/`, `agent-ecosystems/schemas/structured-outputs/`.

For any new agent/toolset/stack/bundle, add at least one scenario under `agent-ecosystems/tests/scenarios/` and ensure `scripts/check-agent-ecosystems.sh` passes.

## Safety notes

- Do not edit `~/.codex/config.toml` or VS Code global settings from this repository; copy snippets instead.
- Never hand-edit `.code-profile` files; always regenerate via VS Code Export Profile.
- Do not commit generated files (`vscode/exports/**`, `vscode/codex-mcp.generated.toml`).
- MCP manifests must use placeholders for secrets/paths; avoid adding credentials.

<!-- vale on -->
