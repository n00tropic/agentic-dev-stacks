# Agentic Dev Stacks

Scoped, cross-OS VS Code packs plus MCP manifests, designed for human + AI agent workflows (macOS, Windows, Linux).

## What lives where

- **Root** – governance and agent docs: `AGENTS.md`, `CONTROL.md`, `copilot-instructions.md`, `agent-instructions.md`.
- **`vscode/`** – source of truth for packs (profiles, extensions, settings, MCP), export tooling, and gitignored exports.
- **`codex/`** – docs and examples for wiring MCP into Codex (`config-guides.md`, `safe-vs-danger-modes.md`).

## Golden Path (new machine)

1. Clone repo, then `cd vscode`.
2. Generate exports: `python scripts/export-packs.py <slug> [<slug> ...]`.
3. Install extensions from each export: `cat exports/workspaces/<slug>/.vscode/extensions.list | xargs -L1 code --install-extension` (add `--profile "<Profile Name>"` if you want it scoped).
4. Open the workspace: `code exports/workspaces/<slug>/<slug>.code-workspace --profile "<Profile Name>"`.

## Golden Path (just profiles)

- Import a `.code-profile` or gist via VS Code **Import Profile…**.
- See `PROFILE_DIST.md` for slug → profile name → dist artifact mapping (local exports and optional secret gists may be `<TO_FILL>` placeholders).

## Structure (sources → exports → dist)

- Source packs live in `vscode/packs/<pack>/`:
  - `profiles/PROFILE.<slug>.md`
  - `extensions/extensions.<slug>.txt`
  - `settings/settings.<slug>.json`
  - `mcp/servers.<slug>.json`
  - `workspace-templates/` examples
- Exports are generated to `vscode/exports/**` (gitignored) via `scripts/export-packs.py`.
- Dist profile exports (optional) go in `vscode/profiles-dist/*.code-profile` and are catalogued in `PROFILE_DIST.md`.

## Safety notes

- Never edit `~/.codex/config.toml` or VS Code global settings from this repo; copy blocks instead.
- Do not commit generated files (`vscode/exports/**`, `vscode/codex-mcp.generated.toml`).
- Profiles ship with GitHub/Copilot support but remain usable offline; align future changes accordingly.
