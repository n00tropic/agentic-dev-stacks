# GitHub Copilot – Repository Instructions

## What this repo is

This repo defines:

- VS Code “packs” for scoped profiles and workspaces.
- MCP server manifests per profile.
- Validation and merge scripts (e.g. `validate-extensions`, `merge-mcp-fragments`).

Use it to keep my dev environments and MCP configs consistent across macOS, Windows, and Linux.

## When working in this repo, always:

1. Read `AGENTS.md` and obey all invariants.
2. Prefer editing:
   - `packs/**/profiles/PROFILE.*.md`
   - `packs/**/extensions/extensions.*.txt`
   - `packs/**/settings/settings.*.json`
   - `packs/**/mcp/servers.*.json`
     and the `scripts/` directory.
3. Never edit my home dotfiles (`~/.codex/config.toml`, VS Code global settings) directly.
4. When a change affects MCP or profiles, propose:
   - A short plan.
   - The commands I should run locally (e.g. `python scripts/merge-mcp-fragments.py ...`, `./apply-profile.sh <slug>`).

## Evergreening and validation

When I ask you to “refresh” or “re-sync” this system, by default:

1. Run and fix:
   - `./validate-extensions.sh` (or `.\Validate-Extensions.ps1` on Windows).
2. If MCP manifests changed:
   - Suggest a `merge-mcp-fragments.py` run and remind me not to commit `codex-mcp.generated.toml`.
3. If you add or modify profiles:
   - Ensure `CONTROL.md` stays consistent with the actual profile list.
   - Adjust the 20-profile budget notes if needed.

## MCP usage

- Assume core MCP servers (Sonatype, Context7, GitHub, filesystem, git, etc.) are configured outside this repo.
- Treat `packs/**/mcp/servers.*.json` as the **only** source of truth for:
  - Which servers are recommended per profile.
  - Which are optional / experimental / privacy-sensitive.
- Do NOT invent new MCP servers; if you propose one, add it to a manifest with appropriate flags and notes.

## Task patterns

- “Add a new profile” → follow the workflow in `AGENTS.md` (“Add or change a profile”).
- “Update MCP for X” → edit the appropriate `servers.<slug>.json` and show me an updated `merge-mcp-fragments.py` command.
- “Prepare a workspace for profile <slug>” → edit nothing; instead:
  - Read the relevant profile + extensions + settings + manifest.
  - Output the commands for applying them (from the `scripts/` helpers).

## Safety

- This repo may reference MCP servers with write capabilities. When suggesting MCP usage:
  - Prefer read-only tools unless I explicitly ask for write operations.
  - Call out any privacy-sensitive or cloud-dependent servers (AWS, Apify, etc.) and the fact that credentials are needed.
