# Safe vs Danger Modes for MCP Servers and Codex

This guide explains how to reason about **“safe”** vs **“danger”** modes when using Model Context Protocol (MCP) servers with Codex, and how to configure your `config.toml` so you always know what level of power you are giving to agents.

It focuses on:

- Sandbox / execution modes in Codex (`sandbox_mode`, network access).
- Read-only vs full-access behaviour for MCP servers.
- How to apply the safety flags from this repo’s MCP manifests.
- Practical configuration examples and decision rules.

---

## 1. Mental model

There are two orthogonal dimensions to keep in mind:

1. **Codex sandbox / execution mode**  
   How much power Codex has over your filesystem, shell, and network from this machine.

2. **MCP server capabilities and configuration**  
   What each MCP server is _allowed_ to do (read-only, read–write, external APIs, cloud mutations, etc.).

A “dangerous” setup usually means **both**:

- Codex is running in a permissive sandbox (e.g. `danger-full-access` with network access), **and**
- You have MCP servers enabled that can mutate things you care about (files, clusters, cloud accounts, third‑party services).

A “safe” setup is one where at least one of these is strongly constrained.

---

## 2. Safe mode patterns (read‑only / reduced blast radius)

Safe mode is about **minimising irreversible actions**. Typical characteristics:

- Codex:
  - Uses a more restrictive `sandbox_mode` (or at least lacks blanket network access).
  - Is used primarily for review, analysis, and inspection tasks.
- MCP servers:
  - Are configured in read‑only mode where possible.
  - Focus on introspection: docs, search, analysis, logs, metadata.
  - Avoid write operations, deployments, or destructive actions.

### 2.1 When to use safe mode

Use safe mode by default when:

- Reviewing unfamiliar repositories.
- Working in **multi‑user** or shared environments.
- Auditing, refactoring, or learning from sensitive/private codebases.
- Interacting with:
  - Production clusters and databases.
  - Accounts you cannot easily roll back.

### 2.2 Example: safer Codex config (conceptual)

In your personal `~/.codex/config.toml` you might use:

```toml
approval_policy = "always"            # or "sometimes", to force confirmation
sandbox_mode = "workspace-write"      # or another restricted mode

[features]
rmcp_client = true
web_search_request = false            # disable ambient web search by default

[sandbox_workspace_write]
network_access = false                # no arbitrary outbound network calls
```

In this mode:

- Codex can edit files in the workspace but not run arbitrary networked commands.
- Any MCP servers that rely on external HTTP APIs will typically:
  - Not work, or
  - Require explicit enabling in a more permissive configuration.
- You can still run read‑only MCP servers that operate on local state (filesystem, git, static analysis, etc.) so long as their commands do not depend on network access.

> **Important:** This repository does not set your sandbox mode. It only helps you scope **which** MCP servers you enable per profile; you remain responsible for the global safety posture in `config.toml`.

---

## 3. Danger mode patterns (full access / trusted workspace)

“Danger mode” is not inherently bad; it simply means you are choosing to give Codex and its MCP servers **maximum power** on purpose.

Typical characteristics:

- `sandbox_mode = "danger-full-access"`.
- Network access is enabled for both the workspace and the danger sandbox.
- MCP servers may:
  - Edit files across the repository.
  - Execute commands (build, test, deploy).
  - Talk to external services and cloud APIs.

### 3.1 When to use danger mode

It is reasonable to use a high‑power configuration when:

- You are working on your **own** repositories and fully trust their contents.
- You are doing:
  - Active feature development.
  - Large‑scale automated refactoring.
  - Build, test, or deploy orchestration.
- The configured MCP servers are:
  - Ones you chose intentionally (from this repo’s manifests).
  - Properly authenticated where required.
  - Understood in terms of their blast radius.

### 3.2 Example: high‑power Codex config (conceptual)

A typical powerful configuration looks like:

```toml
approval_policy = "never"               # no confirmation prompts
sandbox_mode = "danger-full-access"

[features]
rmcp_client = true
web_search_request = true

[sandbox_danger_full_access]
network_access = true

[sandbox_workspace_write]
network_access = true
```

This combined with:

- MCP servers that can:
  - Run `docker` builds.
  - Trigger CI pipelines.
  - Interact with Kubernetes clusters.
  - Modify remote services (e.g. AWS, DBs, SaaS APIs).

…gives Codex a lot of leverage. You should treat this like a powerful automation account: useful, but only safe in **trusted** contexts.

---

## 4. Using MCP manifest safety flags

Each MCP manifest in:

```text
vscode/packs/*/mcp/servers.<slug>.json
```

includes fields like:

- `optional` – not strictly required; you choose if/when to enable it.
- `experimental` – early‑stage or less battle‑tested servers.
- `privacy_sensitive` – may send code, prompts, or metadata to third‑party services.
- `recommended_read_only` – safer to run in read‑only mode (e.g. `get/list/watch` only).
- `category` – hints at the server’s role (dependency‑intelligence, docs, database, search, cloud, etc.).

### 4.1 How to use these flags in practice

When you copy `[mcp_servers.*]` blocks from `codex-mcp.generated.toml` into `config.toml`:

- **If `optional = true`:**
  - It is safe to leave the block out entirely.
  - Add it only when you’re sure you need that specific capability.

- **If `experimental = true`:**
  - Prefer enabling it only in:
    - `experimental-preview` profiles, or
    - Separate, non‑critical environments.

- **If `privacy_sensitive = true`:**
  - Assume requests and/or data may be logged by the provider.
  - Only enable in:
    - Personal or non‑sensitive projects.
    - Contexts where external logging is acceptable.

- **If `recommended_read_only = true`:**
  - Consult the server’s docs to see how to:
    - Limit operations to read‑only.
    - Use flags or configuration to disable mutating actions.
  - For cluster and DB MCPs, prefer:
    - `get/list/watch` operations only in most cases.
    - Explicit, manual workflows for writes/deletes.

---

## 5. Example: read‑only vs full‑access MCP configuration

Below are conceptual patterns; you will need to adapt them using the official docs for each server.

### 5.1 Read‑only pattern for a cluster MCP

```toml
# Example: Kubernetes MCP in read‑only mode (conceptual)
[mcp_servers.kubernetes-ro]
# command and args come from official server docs
command = "<TO_FILL>"
# args = ["--read-only"]      # if supported by the implementation
# env = { "KUBECONFIG" = "/path/to/readonly/kubeconfig" }
```

In addition, you might:

- Use a dedicated, read‑only kubeconfig.
- Limit to a non‑production cluster for everyday development.

### 5.2 Full‑access pattern for a trusted environment

```toml
# Example: Kubernetes MCP with write access (trusted environment only)
[mcp_servers.kubernetes-rw]
command = "<TO_FILL>"
# args = ["--allow-writes"]   # if supported, see server docs
# env = { "KUBECONFIG" = "/path/to/admin/kubeconfig" }
```

Only enable such a server when:

- You are in a trusted repo and cluster.
- You are comfortable with Codex performing real mutations under your credentials.

---

## 6. Practical decision rules

When deciding whether to run in a “safe” vs “danger” mode, and which MCP servers to enable, use these questions:

1. **Do I trust this repo?**
   - If **no**, prefer:
     - More restrictive sandbox.
     - Minimal MCP set (local + read‑only only).
   - If **yes**, you may consider danger mode for speed.

2. **Could an error here cause real damage?**
   - Production clusters, core databases, and cloud infra → be conservative.

3. **Does this MCP server have write or external powers?**
   - If it can deploy, delete, or modify external systems, treat it as high‑risk.

4. **Is this an “always‑on” need or a one‑off task?**
   - Prefer enabling powerful MCP servers only for the duration of a task, then disabling them.

5. **What do the manifest flags say?**
   - If `optional`, `experimental`, or `privacy_sensitive` are true, treat them as feature flags that need an explicit “yes”.

---

## 7. Recommended workflow for this repo

A practical, low‑friction approach:

1. **Keep two Codex configs:**
   - `config.toml` – your normal, perhaps more powerful working config.
   - `config.safe.toml` – a stripped‑down, read‑only‑oriented version for untrusted repos.

2. **Use this repo only for the _structure_ of power:**
   - Profile‑level MCP manifests.
   - Scripts (`merge-mcp-fragments.py`) that generate candidate configs.
   - Documentation (this file and `config-guides.md`).

3. **For each machine or role:**
   - Pull latest from `agentic-dev-stacks`.
   - Run the merge script for relevant profile slugs.
   - Decide which `[mcp_servers.*]` blocks belong in:
     - Your normal config.
     - Your safe config (if you maintain one).

4. **When in doubt, fall back to safe:**
   - If you are not sure what an MCP server does, or how it is configured, either:
     - Leave it disabled, or
     - Enable it only in an experimental profile and safe sandbox.

---

## 8. Related documents

- [`codex/docs/config-guides.md`](./config-guides.md) – how to integrate MCP fragments from this repo into `~/.codex/config.toml`.
- Profile‑specific MCP manifests under:

  ```text
  vscode/packs/*/mcp/servers.<slug>.json
  ```

  for safety flags such as:
  - `recommended_read_only`
  - `privacy_sensitive`
  - `optional`
  - `experimental`
