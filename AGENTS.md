# AGENTS

## Purpose

This repository is the canonical source of truth for:

- VS Code profile packs (profiles, extensions, settings).
- MCP server manifests for each profile.
- Helper scripts for validation and TOML generation.
- Documentation for configuring Codex safely with these profiles.

Any AI agent (Codex, GitHub Copilot coding agent, ChatGPT, etc.) working in this repo MUST follow these rules.

## Core invariants

1. **Single source of truth (SSoT)**
   - `CONTROL.md` is the ground truth for:
     - Profile slugs.
     - The 20-profile budget per VS Code installation.
   - Do NOT invent new slugs or packs without updating `CONTROL.md`.

2. **Scoped paths**
   - All VS Code packs and scripts live under `vscode/`.
   - Do NOT create new top-level `packs/` or `scripts/` directories outside `vscode/`.

3. **No dotfile edits**
   - Do NOT edit:
     - `~/.codex/config.toml`
     - VS Code global settings
   - Instead:
     - Update manifests and scripts in this repo.
     - Show the user the exact commands and TOML blocks they should apply locally.
     - When touching anything related to Codex configuration or MCP, consult:
       - `codex/docs/config-guides.md`
       - `codex/docs/safe-vs-danger-modes.md`

4. **No secrets**
   - Never create or commit:
     - API keys or tokens.
     - Cloud credentials.
     - Machine-specific paths or secrets.
   - MCP configuration in this repo MUST use placeholders (e.g. `<TO_FILL>`) for commands/args/env that depend on local setup.

5. **Generated files**
   - The following are treated as **throw-away artefacts** and MUST NOT be committed:
     - `vscode/codex-mcp.generated.toml`
     - Any `*.bak.*` files produced by local tooling or editors.
   - Use generated files as staging areas for the user to copy from into their own config files.

## Standard workflows

### A. Add or change a profile

When asked to create or modify a profile:

1. Update the profile assets under `vscode/packs/<pack>/`:
   - `vscode/packs/<pack>/profiles/PROFILE.<slug>.md`
   - `vscode/packs/<pack>/extensions/extensions.<slug>.txt`
   - `vscode/packs/<pack>/settings/settings.<slug>.json`
   - `vscode/packs/<pack>/mcp/servers.<slug>.json`
2. Update `CONTROL.md` if:
   - The profile list changes, or
   - The 20-profile budget / allocations per platform change.
3. Run validation scripts and fix any errors:
   - From the repo root:
     - `cd vscode`
     - `./scripts/helpers/validate-extensions.sh`  
       or on Windows: `.\scripts\helpers\Validate-Extensions.ps1`
   - Additionally, ensure MCP JSON is valid:
     - `python scripts/validate_extensions.py` (and/or a JSON validator for `servers.*.json` if implemented).
4. Do NOT touch global Codex / VS Code config. Instead, output to the user:
   - A suggested `merge-mcp-fragments.py` command, e.g.:

     ```bash
     cd vscode
     python scripts/merge-mcp-fragments.py core-base-dev fullstack-js-ts ...
     ```

   - A reminder to follow `codex/docs/config-guides.md` to copy `[mcp_servers.*]` blocks into `~/.codex/config.toml`.

### B. Before opening a PR

Before proposing or committing changes that affect packs, MCP manifests, or scripts, automatically:

1. Run extension validation from within `vscode/`:
   - `./scripts/helpers/validate-extensions.sh`  
     or `.\scripts\helpers\Validate-Extensions.ps1` on Windows.
2. Ensure all MCP manifests `vscode/packs/*/mcp/servers.<slug>.json` are:
   - Valid JSON.
   - Contain, per server:
     - `id`
     - `human_name`
     - `category`
     - `source`
     - `config_fragments`
     - Any relevant safety flags (`optional`, `experimental`, `privacy_sensitive`, `recommended_read_only`).
3. If you touched MCP manifests, propose (in your response to the user):
   - A `merge-mcp-fragments.py` command, e.g.:

     ```bash
     cd vscode
     python scripts/merge-mcp-fragments.py core-base-dev fullstack-js-ts ...
     ```

   - A reminder that `vscode/codex-mcp.generated.toml` is **not** to be committed and is only a local staging file.

## MCP-specific rules

1. **Prefer manifests**
   - Only use MCP servers that are declared in:
     - `vscode/packs/*/mcp/servers.*.json`
   - If you propose a new server:
     - Add it to the appropriate `servers.<slug>.json`.
     - Mark it with `optional`, `experimental`, and/or `privacy_sensitive` flags as appropriate.

2. **Trust and provenance**
   - Do NOT add MCP servers from random or unclear sources.
   - Only accept servers that:
     - Have official or clearly reputable origins.
     - Have documentation that can be referenced in `source.url` or similar fields.

3. **Respect safety flags from manifests**
   - If `recommended_read_only = true`:
     - Do not suggest write tools or mutating operations by default.
     - Prefer read-only usage in plans (e.g. `get/list/watch` for clusters).
   - If `privacy_sensitive = true`:
     - Explicitly mention in your plan that:
       - Requests or data may be logged by third-party services.
       - The user should only enable these servers in suitable, non-sensitive contexts.
   - If `optional = true`:
     - Treat the server as opt-in; never assume it must be enabled.
   - If `experimental = true`:
     - Prefer enabling it only via the `experimental-preview` profile or clearly marked test setups.

4. **Codex and sandbox modes**
   - When suggesting changes that depend on Codex sandbox or MCP behaviour:
     - Refer the user to:
       - `codex/docs/config-guides.md`
       - `codex/docs/safe-vs-danger-modes.md`
     - Do NOT assume they are running in `danger-full-access`; make your guidance explicit.

## How to talk to the user

When performing tasks in this repo:

- Explain what you’re going to change in a short, structured plan.
- Show diffs or file snippets, not just high-level descriptions.
- Offer the exact commands the user can run, for example:
  - Profile application scripts.
  - Validation scripts.
  - `merge-mcp-fragments.py` runs.
- Call out explicitly if a step:
  - Depends on an MCP server that is `privacy_sensitive`, `optional`, or `experimental`.
  - Assumes a powerful Codex sandbox mode (e.g. `danger-full-access`).

Your primary goals as an agent in this repo are:

1. Keep the profile and MCP configuration consistent with `CONTROL.md`.
2. Maintain a clean, validated state (extensions, manifests, scripts).
3. Help the user safely bridge from this versioned configuration to their local Codex and VS Code setups without ever committing secrets or machine-specific configuration.
