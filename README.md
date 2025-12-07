<!-- vale off -->

# Agentic Dev Stacks

Scoped, cross-OS VS Code packs plus MCP manifests and devcontainers, aimed at teams that want governed, reproducible AI-ready setups (not ad-hoc dotfiles or one-off machines).

## What is this?

Agentic development stacks built as a compiler: packs in `vscode/packs/**`, agents in `agents/**`, MCP manifests under `vscode/packs/*/mcp/`, and reproducible exports under `vscode/exports/**` (git-ignored). Dist profile exports live in `vscode/profiles-dist/*.code-profile` (never hand-edit; regenerate via VS Code **Export Profile…**).

Why this exists

- Onboard a new machine or hire with one governed VS Code profile per persona.
- Keep agent + MCP setup reproducible across macOS, Windows, and Linux.
- Respect profile budgets and safety flags (`CONTROL.md`, `AGENTS.md`), with devcontainer-first flows to avoid host dotfiles.

## Hero quickstart (Codespaces or devcontainer)

- Codespaces: open this repo in GitHub Codespaces (default devcontainer) and wait for build; then run `bash scripts/qa-preflight.sh`.
- Local devcontainer: `devcontainer up --workspace-folder .` (requires Docker/Podman + Dev Containers extension), then `bash scripts/qa-preflight.sh`.
- Prefer the Core / Base Dev flow below for the quickest local install per OS.

## Quickstart: Core / Base Dev (3 minutes)

Prereqs: VS Code with `code` CLI enabled, Git, Python 3.

```bash
# macOS / Linux
git clone https://github.com/n00tropic/agentic-dev-stacks.git
cd agentic-dev-stacks/vscode
./scripts/install-core-base-dev.sh
```

```powershell
# Windows (PowerShell)
git clone https://github.com/n00tropic/agentic-dev-stacks.git
cd agentic-dev-stacks\vscode
./scripts/Install-CoreBaseDev.ps1
```

What you get: the `Core / Base Dev` profile appears in VS Code, extensions install via CLI, and the exported workspace opens under that profile (`vscode/exports/workspaces/core-base-dev/core-base-dev.code-workspace`).

## 5-minute trial: Fullstack JS/TS

Prereqs: VS Code with `code` CLI, Git, Python 3; Docker/Podman + Dev Containers extension if you want the containerised toolchain.

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
./scripts/install/fullstack-js-ts-windows.ps1
```

What happens:

- Builds the `fullstack-js-ts` export via `vscode/scripts/export-packs.py`.
- Installs extensions into the `Fullstack JS/TS – Web & API` profile via the VS Code CLI.
- Opens the exported workspace at `vscode/exports/workspaces/fullstack-js-ts/fullstack-js-ts.code-workspace`.
- Leaves global settings untouched. Optional: import a vetted profile export from `vscode/profiles-dist/fullstack-js-ts.code-profile` once you have generated a real export.
- Verify: `code --profile "Fullstack JS/TS – Web & API" --list-extensions | wc -l` (PowerShell: `... | measure-object`) and optionally `python scripts/validate-mcp-config.py` from repo root.

Mini golden path (JS/TS)

- Open Copilot Chat and select the `refactor-surgeon` agent.
- Paste: "Propose a small refactor plan for <file>, keeping behaviour unchanged."
- Expect: a short plan and diff; then switch to `test-writer` with "Add/adjust tests for the changes in <file>" and run the suggested test command.

## Golden paths

- JS/TS refactor + tests: `docs/golden-paths/js-ts-refactor.md`
- Incident review + postmortem: `docs/golden-paths/incident-postmortem.md`
- Docs site: <https://n00tropic.github.io/agentic-dev-stacks> (hero path: JS/TS refactor + tests)

## Stacks you can install

| Stack                 | Persona                      | Status     | Supported OSes          | Agents & toolsets (high level)                                               | Quickstart                                                                                       |
| --------------------- | ---------------------------- | ---------- | ----------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| core-base-dev         | Core / Base Dev              | Production | macOS / Windows / Linux | Baseline extensions and settings; no MCP by default                          | `cd vscode && ./scripts/install-core-base-dev.sh` (Windows: `./scripts/Install-CoreBaseDev.ps1`) |
| fullstack-js-ts       | Full-stack JS/TS – Web & API | Production | macOS / Windows / Linux | refactor-surgeon, test-writer, doc-surgeon; local-dev + review-only toolsets | `./scripts/install/fullstack-js-ts-<os>.sh`                                                      |
| python-data-analytics | Data/ML/analytics            | Beta       | macOS / Windows / Linux | data-explorer, pipeline-refactorer, doc-surgeon; local-dev + review-only     | `./scripts/install/python-data-analytics-<os>.sh`                                                |
| infra-ops-sre         | Infra / SRE                  | Beta       | macOS / Windows / Linux | infra-reviewer, incident-scribe, doc-surgeon; review-only                    | `./scripts/install/infra-ops-sre-<os>.sh`                                                        |

More detail: `docs/stack-catalogue.md` (personas, MCP servers, prompts).

Status: JS/TS and Core are production-quality; other stacks are in active development while `.code-profile` exports and MCP manifests are refined.

## Governance and safety

- Profile budget: tracked in `CONTROL.md` (VS Code limits ~20 profiles per installation).
- No dotfile edits: profiles, MCP manifests, and prompts are authored under `vscode/**` and `agents/**`; generated artefacts in `vscode/exports/**` stay untracked.
- Secrets stay out of git: MCP manifests use `<TO_FILL>` placeholders; copy generated TOML into `~/.codex/config.toml` per `codex/docs/config-guides.md`.
- Dist profiles: `.code-profile` files are regenerated via VS Code **Export Profile…**; never hand-edit.
- See `GOVERNANCE.md` and `AGENTS.md` for invariants and reviewer expectations.

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
- License: MIT (see `LICENSE`).
- Community: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`.

For any new agent/toolset/stack/bundle, add at least one scenario under `agent-ecosystems/tests/scenarios/` and ensure `scripts/check-agent-ecosystems.sh` passes.

## Safety notes

- Do not edit `~/.codex/config.toml` or VS Code global settings from this repository; copy snippets instead.
- Never hand-edit `.code-profile` files; always regenerate via VS Code Export Profile.
- Do not commit generated files (`vscode/exports/**`, `vscode/codex-mcp.generated.toml`).
- MCP manifests must use placeholders for secrets/paths; avoid adding credentials.

<!-- vale on -->
