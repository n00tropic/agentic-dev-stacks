# Agent Ops Automation (Roadmap)

Current state

- Validate + build via scripts:
  - `scripts/check-agent-ecosystems.sh` (schemas + scenarios; optional `--with-bundles`).
  - `scripts/build-agent-ecosystem-bundles.sh` (builds ZIPs + metadata under `dist/`).
- GitHub Actions workflows cover validation and bundle building.
- Profile import remains manual: VS Code exports `.code-profile` files but lacks a safe CLI import flow today.

Near-term automation

- A dedicated “Agent Ops” agent (via Copilot/MCP) could:
  - Edit/validate agents, toolsets, stacks, and bundles (JSON + schemas).
  - Run validation + build scripts through MCP shell/CI tooling.
  - Open PRs with bundle outputs and release notes summaries.
- Preconditions:
  - MCP servers expose safe shell/CI controls.
  - Least-privilege access; no broad write by default.

Longer-term automation

- If VS Code adds CLI/API for profile import, installers can auto-import `.code-profile` files and wire MCP/agents purely via config.
- Multi-agent “Agent HQ” could:
  - Watch repo changes, propose new stacks/agents via PRs.
  - Kick off CI, review scenario results, prepare releases.

Security considerations

- Use least-privilege tokens per toolset; separate read vs write scopes.
- Treat MCP servers as potentially untrusted (prompt injection/misconfig risk).
- Keep agent-ecosystems configs as policy-as-code with mandatory review.
