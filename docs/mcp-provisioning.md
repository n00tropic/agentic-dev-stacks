# MCP provisioning for this workspace

Use this checklist to provision MCP servers safely, drawing from reputable curated lists and the existing profile fragments in `vscode/packs/*/mcp/`.

## Curated sources to pull candidates from

- `https://github.com/punkpeye/awesome-mcp-servers` (large, active catalogue).
- `https://github.com/wong2/awesome-mcp-servers` (concise curation).
- `https://github.com/appcypher/awesome-mcp-servers` (general-purpose).
- `https://github.com/rohitg00/awesome-devops-mcp-servers` (DevOps-focused).
- `https://github.com/jaw9c/awesome-remote-mcp-servers` (remote/SaaS-friendly).

## Recommended baseline servers (already defined in pack fragments)

- `sonatype-deps` — dependency/security intelligence.
- `context7-docs` — versioned library/framework docs.
- `github` — GitHub repo/PR/issue access.

## How to generate a local MCP config for this workspace

1. From repo root, merge the desired fragments (example: base + QA):

   ```bash
   cd vscode
   python scripts/merge-mcp-fragments.py core-base-dev qa-static-analysis gitops-code-review macos-apple-platforms
   ```

2. This writes `vscode/codex-mcp.generated.toml` (gitignored). Copy the `[mcp_servers.*]` blocks you want into your local `~/.codex/config.toml` (do **not** commit generated files).
3. Fill in each server’s `command`/`args`/env placeholders per its upstream README. Keep secrets out of version control.

## Adding new servers safely

- Only add servers with clear provenance (official repos or well-known vendors) and licences.
- Mark flags in JSON fragments: `optional` for non-essential/remote, `privacy_sensitive` if requests may leak code/data, `experimental` if beta.
- Place new entries in the appropriate `vscode/packs/<pack>/mcp/servers.<slug>.json` and re-run the merge command above.

## Suggested next candidates to consider (pending validation)

- DevOps/infra: pick 1–2 from `rohitg00/awesome-devops-mcp-servers` (e.g., cloud inventory/monitoring) and add to `servers.infra-devops.json` as optional + privacy_sensitive.
- Code search/insight: a GitHub- or sourcegraph-backed code search MCP (optional, privacy_sensitive) for `core-base-dev`/`gitops-code-review`.
- API/reference: a stable public docs MCP (read-only) for `qa-static-analysis`.

## Validation

- Keep `vscode/codex-mcp.generated.toml` out of git; rerun merge after JSON edits.
- Run `python scripts/validate_extensions.py` if updated scripts start validating MCP JSON (future-proof hook).
