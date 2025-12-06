# MCP integration and sources of truth

- Workspace MCP SSoT (macOS/Linux): `.vscode/mcp.json`
  - Defines how to start each MCP server locally (POSIX `/bin/sh -c` pattern with env overrides).
  - Keep secrets out of the file; rely on inherited environment variables.
- Per-profile manifests: `vscode/packs/**/mcp/servers.<slug>.json`
  - Declare which MCP servers each profile cares about (and flags such as `optional`, `privacy_sensitive`, `experimental`).
- Generated Codex TOML: `vscode/codex-mcp.generated.toml` (git-ignored)
  - Built via `python scripts/merge-mcp-fragments.py ...` from the manifests; copy blocks into local `~/.codex/config.toml` as needed.
- Agents (e.g. `.github/agents/*.agent.md`, `agents/**`)
  - Should call MCP tools that are declared in the relevant profile manifest and have a corresponding launcher in `.vscode/mcp.json`.

## Adding a new MCP server (pattern)

1. Add the launcher to `.vscode/mcp.json` with `/bin/sh -c "${MCP_FOO_CMD:-default}"` and empty `env` unless passing through well-named env vars.
2. Add the server entry to the relevant `servers.<slug>.json` manifest with flags (`optional`, `privacy_sensitive`, `experimental`) as appropriate.
3. (Optional) Re-run `python scripts/merge-mcp-fragments.py <slugs...>` to regenerate local TOML for Codex.
4. Keep secrets in your shell or `.env`; never inline credentials.

## Validation

- Run `python scripts/validate-mcp-config.py` to check workspace MCP structure (command/args/env) and receive warnings on deviations from the `/bin/sh -c` pattern.
