# VS Code Packs Scaffold

Canonical VS Code configuration packs for macOS, Windows, and Linux.
Open this folder as a workspace in VS Code and let your AI assistants
(Copilot, Codex, etc.) orchestrate profile setup from here.

## Structure

- `packs/<pack-name>/profiles/` – Profile descriptors (`PROFILE.<slug>.md`) and exported profile files.
- `packs/<pack-name>/extensions/` – Curated extension lists for each profile.
- `packs/<pack-name>/settings/` – Settings overrides per profile.
- `packs/<pack-name>/qa/` – Linters, formatters, and QA tooling config.
- `packs/<pack-name>/mcp/` – MCP client/server configuration (e.g. dependency intelligence).
- `packs/<pack-name>/workspace-templates/` – Example `.code-workspace` files per pack.
- `packs/<pack-name>/scripts/` – OS-specific helper scripts for that pack.

## Automation scripts

Root-level scripts under `scripts/` help apply settings overrides in a safe, merge-friendly way:

- `scripts/macos/merge-settings.sh` – Merge a settings override JSON into the current user's VS Code settings on macOS (or generic Unix).
- `scripts/linux/merge-settings.sh` – Thin wrapper that forwards to the macOS merge script for Linux.
- `scripts/windows/Merge-Settings.ps1` – PowerShell version that merges override settings into `%APPDATA%\Code\User\settings.json`.

Each script:

- Backs up the existing `settings.json` (if it exists) with a timestamped `.bak` suffix.
- Merges the override on top of the existing settings (shallow merge, with override keys winning).
