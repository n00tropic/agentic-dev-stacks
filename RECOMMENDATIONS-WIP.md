# WIP Recommendations (Agent Ecosystems)

- Export and track the JS/TS profile at `vscode/profiles-dist/fullstack-js-ts.code-profile` via VS Code “Export Profile…”.
- Ensure `vscode/.devcontainer/devcontainer.json` exists and matches the stack expectation, or update `fullstack-js-ts.stack.json` to the correct path.
- Install and configure MCP commands referenced by toolsets/bundles with least-privilege credentials:
  - `github-mcp` (repo read/write for local-dev; read-only for review-only)
  - `context7-mcp` (docs)
  - `sonatype-mcp` (dependency audit)
  - `elastic-mcp` (read-only search)
- Keep MCP tokens/keys out of VCS; prefer env vars or secrets managers per `codex/docs/config-guides.md`.
- Flesh out OS installer scripts to perform real setup once devcontainer/profile artefacts are finalised.
- Re-run `python3 agent-ecosystems/scripts/validate-ecosystem-configs.py` after any schema or config change.
