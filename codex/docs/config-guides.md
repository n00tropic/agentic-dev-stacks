# Codex Configuration Guides

This guide explains how to configure Codex for use with the `agentic-dev-stacks` profiles, with a focus on:

- Where Codex reads its configuration from.
- How to safely wire Model Context Protocol (MCP) servers.
- How to merge profile-based MCP fragments from this repo into your local `config.toml`.
- Recommended patterns and troubleshooting tips.

---

## 1. Where Codex stores configuration

Codex reads its configuration from a single TOML file:

- **macOS / Linux:** `~/.codex/config.toml`
- **Windows:** `%USERPROFILE%\.codex\config.toml`

This file is shared between:

- The **Codex CLI** (`codex` in your terminal).
- The **Codex IDE extension** (e.g. in VS Code).

Use it to configure:

- Default model and reasoning effort.
- Approval policy and sandbox / execpolicy.
- MCP servers Codex should have access to.

> **Tip:** From the Codex IDE extension you can usually open this file via a “Config” or “Settings” link in the UI, which jumps directly to `config.toml`. Refer to the official Codex configuration docs if this entry point moves in future versions.

---

## 2. Baseline `config.toml` structure

Codex expects a TOML file with sections such as:

```toml
approval_policy = "never"
model = "gpt-5.1-codex-max"
model_reasoning_effort = "high"
sandbox_mode = "danger-full-access"

[features]
rmcp_client = true
web_search_request = true

[sandbox_workspace_write]
network_access = true

[sandbox_danger_full_access]
network_access = true

# MCP servers go under [mcp_servers.*] blocks
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

The exact keys available and their meaning are documented in the official Codex configuration and CLI reference.

In this repo we intentionally **do not** maintain your personal `config.toml`. Instead, we:

- Keep **profile-level MCP manifests** in `vscode/packs/**/mcp/servers.*.json`.
- Generate a **temporary** `codex-mcp.generated.toml` from those manifests.
- Ask you to copy only the blocks you want into your own `config.toml`.

---

## 3. Generating MCP fragments from profiles

This repo includes a helper script that merges profile-level MCP manifests into a single TOML file you can paste into `config.toml`.

From the repo root:

```bash
cd vscode
python scripts/merge-mcp-fragments.py core-base-dev fullstack-js-ts infra-devops docs-librarian
```

What this does:

- Looks for `servers.<slug>.json` under `vscode/packs/*/mcp/` for each slug:
  - `core-base-dev`
  - `fullstack-js-ts`
  - `infra-devops`
  - `docs-librarian`
- Validates their basic structure (`profile_slug`, `servers`, `config_fragments.codex_config_toml`, etc.).
- Deduplicates servers by ID (e.g. `sonatype-deps`, `context7-docs`, `github`, `postgres`, etc.).
- Writes a merged file at:

  ```text
  vscode/codex-mcp.generated.toml
  ```

The generated file contains one or more blocks like:

```toml
# MCP server: Sonatype Dependency Management MCP (id: sonatype-deps)
# Categories: dependency-intelligence
# From profiles: core-base-dev, fullstack-js-ts
# Source: github https://github.com/sonatype/dependency-management-mcp-server
# Optional: false
# Experimental: false
# Privacy sensitive: false
# Recommended read-only: false
[mcp_servers.sonatype-deps]
# Refer to official Sonatype MCP setup for the correct command/args.
command = "<TO_FILL>"
```

> **Do not commit** `codex-mcp.generated.toml`. It is a local working artefact for your machine.

---

## 4. Applying MCP configuration to Codex

Once you have generated `vscode/codex-mcp.generated.toml`:

1. **Open your local config:**
   - macOS/Linux: `~/.codex/config.toml`
   - Windows: `%USERPROFILE%\.codex\config.toml`

2. **Locate the MCP section** in your config, where your current `[mcp_servers.*]` blocks live.

3. **Review the generated file** and copy only the servers you want to enable, for example:

   ```toml
   # -------------------------------------------------------------------
   # MCP servers derived from agentic-dev-stacks profiles
   # -------------------------------------------------------------------

   # MCP server: Sonatype Dependency Management MCP (id: sonatype-deps)
   [mcp_servers.sonatype-deps]
   command = "<TO_FILL>"
   ```

4. **Fill in any `<TO_FILL>` placeholders** using the official server documentation (e.g. GitHub or vendor docs). This typically means:
   - Replacing `command` with the actual executable (e.g. `npx`, `uvx`, or a local binary).
   - Supplying `args = [...]` and environment variables if required.

5. **Save `config.toml`** and, if necessary, restart your Codex CLI or IDE extension so the new MCP servers are picked up.

> **Important:** This repo never ships real commands, secrets, or machine-specific paths in MCP fragments. Always consult the official docs for each MCP server and your own environment.

---

## 5. Profile-specific patterns

Each profile in `vscode/packs/**` has a corresponding MCP manifest that recommends a small, opinionated set of servers. At a high level:

- **Core / base profiles** (`core-base-dev`, `qa-static-analysis`, `gitops-code-review`):
  - Core MCPs for dependency intelligence (e.g. Sonatype), documentation (Context7), and GitHub access.
- **JS/TS & frontend** (`fullstack-js-ts`, `frontend-ux-ui`, `node-backend-services`, `desktop-gui-cross`):
  - Web and API stacks: context/doc servers, database MCPs (e.g. MongoDB), and optionally search/analytics (Elasticsearch).
- **Python services & data/ML** (`python-services-clis`, `python-data-ml`):
  - SQL/DB servers (e.g. Postgres MCP), analytics/search, and documentation MCPs.
- **Infra / DevOps / data** (`infra-devops`, `data-db-analytics`, `linux-ci-headless`):
  - GitHub MCP, Kubernetes/infra MCPs, SQL/DB, search/logging MCPs (Elasticsearch).
- **Docs & librarian** (`docs-librarian`):
  - Documentation-focused servers (Context7, docs/search MCPs), with optional web-search MCPs explicitly marked as privacy-sensitive.
- **Experimental** (`experimental-preview`):
  - Core trio only by default, plus any optional/experimental servers clearly marked as such.

> Track MCP spec and SDK releases (Context7, Sonatype, official Java/TS/Python SDKs). When the spec adds features like OAuth or structured tool outputs, rerun `merge-mcp-fragments.py` and refresh your local `config.toml`.

For concrete details, read the relevant `servers.<slug>.json` in:

```text
vscode/packs/<pack>/mcp/servers.<slug>.json
```

Each manifest includes:

- `servers[].id` (MCP server ID)
- `human_name`, `category`, `source`
- Usage notes and safety flags:
  - `optional`
  - `experimental`
  - `privacy_sensitive`
  - `recommended_read_only`

Use these flags to decide which servers to actually enable in your local config.

---

## 6. Sandbox and safety considerations

Codex supports different sandbox and approval modes controlled by `config.toml` and CLI flags. A common high-power configuration looks like:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"

[sandbox_danger_full_access]
network_access = true

[sandbox_workspace_write]
network_access = true
```

This is powerful but assumes:

- You trust the current repository and workspace.
- You understand that Codex can:
  - Edit files.
  - Run commands.
  - Access the network.

For **untrusted or unknown repositories**, consider:

- Switching to a safer sandbox mode (e.g. workspace-only).
- Temporarily disabling high-risk MCP servers (e.g. those with write or cloud access).
- Keeping only a minimal, read-only set of MCP tools enabled.

When in doubt, favour:

- Read-only operations (e.g. `get/list/watch` for Kubernetes MCPs).
- Local-only tools (filesystem, git) over remote/cloud MCPs.

---

## 7. Troubleshooting common issues

### 7.1 TOML syntax errors

Symptoms:

- Codex refuses to start.
- The CLI reports configuration parse errors.

Checks:

- Ensure the file is valid TOML:
  - Keys should not be duplicated within the same table.
  - Strings must be quoted (`"value"`).
  - Comments begin with `#`.
- If you are unsure, paste the file into a TOML validator or library (locally) and fix any reported issues.

### 7.2 MCP server not appearing or not connecting

Symptoms:

- MCP server does not show up in Codex tools.
- Codex logs indicate it can’t start or connect to a server.

Checks:

1. Verify the `[mcp_servers.<id>]` block is present and not commented out.
2. Ensure `command` points to a real executable available on your `PATH` (or provide an absolute path).
3. If using `npx` or `uvx`, confirm the package name and version are correct.
4. Check network requirements for any HTTP/remote MCP server:
   - Proxies, firewalls, or VPNs may prevent connection.
5. If only the CLI sees the server but the IDE doesn’t:
   - Confirm the IDE extension is using the same `config.toml`.
   - Restart the IDE after making changes.

### 7.3 Conflicting MCP configuration between profiles

Because `merge-mcp-fragments.py` deduplicates by server ID:

- If two profiles specify different TOML fragments for the same `id`, the script keeps the first and logs a warning as a comment.
- If you need different behaviour per machine:
  - Adjust the merged block manually in `config.toml`.
  - Or run the generator with a narrower set of profile slugs.

---

## 8. Keeping Codex and this repo aligned

When you change profiles or MCP manifests in this repo:

1. Commit and push your changes as normal.
2. On your machines:
   - Pull latest changes.
   - Re-run `merge-mcp-fragments.py` with the profile slugs you care about.
   - Inspect the new `codex-mcp.generated.toml`.
   - Manually bring your `~/.codex/config.toml` up to date.

This keeps your Codex environment in sync with the versioned, profile-based configuration in `agentic-dev-stacks` without tightly coupling your personal config file to the repo.
