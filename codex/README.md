# Codex Configuration

This directory contains Codex-specific configuration examples and documentation for wiring MCP servers into your local Codex setup.

## Structure

- `examples/`  
  Sample Codex configuration files (safe to commit). These are **illustrative only** and never contain real secrets, machine-specific paths, or live credentials.
- `docs/`  
  Documentation for Codex configuration, sandbox modes, and recommended usage patterns.

## Usage

Use this directory as the bridge between the versioned repo and your local Codex configuration in `~/.codex/config.toml`.

### 1. Generate MCP config from profiles

From the repository root (or from `vscode/` if you prefer), run:

```bash
cd vscode
python scripts/merge-mcp-fragments.py core-base-dev fullstack-js-ts infra-devops docs-librarian
```

This reads the per-profile MCP manifests under:

- `vscode/packs/*/mcp/servers.<slug>.json`

and writes a merged file at:

- `vscode/codex-mcp.generated.toml` (or wherever you have configured it to write)

The generated file contains `[mcp_servers.*]` blocks that you can copy into your personal `~/.codex/config.toml`.

> **Important:** Do **not** commit `codex-mcp.generated.toml` to version control. It is a working artefact for your machine.

### 2. Update your local Codex config

Open `~/.codex/config.toml` and:

1. Keep your core settings (model, approval_policy, sandbox_mode, features) as-is.
2. Identify the section where your MCP servers are defined (the `[mcp_servers.*]` blocks).
3. From the generated `codex-mcp.generated.toml`, copy only the `[mcp_servers.*]` entries you actually want to enable on this machine.
4. Paste them into `~/.codex/config.toml`, ideally grouped under a comment such as:

   ```toml
   # -------------------------------------------------------------------
   # MCP servers derived from agentic-dev-stacks profiles
   # -------------------------------------------------------------------
   ```

5. Save and, if needed, restart Codex or your editor so the new MCP servers are picked up.

### 3. Safety and sandboxing

The examples and docs in this directory assume you understand the trade-offs of Codex sandbox modes, in particular:

- `sandbox_mode = 'danger-full-access'` with network access enabled is powerful but assumes you fully trust the repo and workspace where Codex is running.
- For untrusted or unknown repositories, you should:
  - Use a safer sandbox mode (e.g. workspace-write only).
  - Limit the number of MCP servers you enable, especially anything with write or cloud capabilities.

Whenever you adopt new MCP servers from this repo:

- Check their `servers.<slug>.json` metadata (optional, experimental, privacy_sensitive, recommended_read_only, etc.).
- Prefer read-only or low-impact modes unless you explicitly need mutating actions.

### 4. Keeping things evergreen

When MCP manifests or profiles change in this repository:

1. Pull the latest changes from the repo.
2. Re-run `merge-mcp-fragments.py` with the relevant profile slugs.
3. Review the new `codex-mcp.generated.toml` output.
4. Manually update your `~/.codex/config.toml` with any new or changed `[mcp_servers.*]` blocks you want to adopt.

You should periodically repeat this process to keep your Codex environment aligned with the latest profile definitions.

## Related

See `../vscode/scripts/merge-mcp-fragments.py` for generating Codex MCP configuration from profile manifests, and the documents under `docs/` for more detailed guidance on safe vs. “danger-full-access” configurations.
