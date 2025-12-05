# GitHub Copilot – Repository Instructions

## What this repo is

This repo defines:

- VS Code packs under `vscode/packs/**` (profiles, extensions, settings, MCP manifests).
- Export tooling and generated workspaces under `vscode/exports/**` (gitignored, reproducible).
- Dist profile exports (`vscode/profiles-dist/*.code-profile`) plus mapping in `PROFILE_DIST.md`.
- Validation and merge scripts (`export-packs.py`, `merge-mcp-fragments.py`, helpers).

Use it to keep dev environments and MCP configs consistent across macOS, Windows, and Linux.

## When working in this repo, always:

1. Read `AGENTS.md` and obey all invariants.
2. Prefer editing under `vscode/` only:
   - `vscode/packs/**/profiles/PROFILE.*.md`
   - `vscode/packs/**/extensions/extensions.*.txt`
   - `vscode/packs/**/settings/settings.*.json`
   - `vscode/packs/**/mcp/servers.*.json`
   - `vscode/scripts/**`
3. Never edit my home dotfiles (`~/.codex/config.toml`, VS Code global settings) directly.
4. When a change affects MCP or profiles, propose:
   - A short plan.
   - Commands to run locally, e.g.:
     - `python scripts/export-packs.py <slug> [<slug> ...]`
     - `python scripts/merge-mcp-fragments.py <slug> [<slug> ...]`
     - Extension installs from `exports/workspaces/<slug>/.vscode/extensions.list` via `code --install-extension` (optionally `--profile "<Name>"`).

## Evergreening and validation

When I ask you to “refresh” or “re-sync” this system, by default:

1. Run and fix:
   - `./scripts/helpers/validate-extensions.sh` (or `.\\scripts\\helpers\\Validate-Extensions.ps1` on Windows).
2. If MCP manifests changed:
   - Suggest a `merge-mcp-fragments.py` run and remind me not to commit `codex-mcp.generated.toml`.
3. If you add or modify profiles:
   - Ensure `CONTROL.md` stays consistent with the actual profile list.
   - Adjust the 20-profile budget notes if needed.

## MCP usage

- Assume core MCP servers (Sonatype, Context7, GitHub, filesystem, git, etc.) are configured outside this repo.
- Treat `vscode/packs/**/mcp/servers.*.json` as the **only** source of truth for:
  - Which servers are recommended per profile.
  - Which are optional / experimental / privacy-sensitive.
- Do NOT invent new MCP servers; if you propose one, add it to a manifest with appropriate flags and notes.

## Task patterns

- “Add a new profile” → follow the workflow in `AGENTS.md` (“Add or change a profile”).
- “Update MCP for X” → edit `vscode/packs/**/mcp/servers.<slug>.json` and show an updated `merge-mcp-fragments.py` command.
- “Prepare a workspace for profile <slug>” → edit nothing; instead:
  - Suggest `python scripts/export-packs.py <slug>` (run from `vscode/`).
  - Use `exports/workspaces/<slug>/.vscode/extensions.list` with `code --install-extension` (optionally `--profile "<Name>"`).
  - Open `exports/workspaces/<slug>/<slug>.code-workspace` (optionally with `--profile "<Name>"`).
- “Publish a profile for import” → follow `PROFILE_DIST.md` checklist; never hand-edit `.code-profile` files.

## Safety

- This repo may reference MCP servers with write capabilities. When suggesting MCP usage:
  - Prefer read-only tools unless I explicitly ask for write operations.
  - Call out any privacy-sensitive or cloud-dependent servers (AWS, Apify, etc.) and the fact that credentials are needed.
