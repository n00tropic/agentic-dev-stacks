# MCP Bundles (.mcpb)

`.mcpb` bundles package an MCP server (manifest + assets) into a portable artefact so users can import the server without copying bespoke shell commands. See the Model Context Protocol guidance for background and tooling.<sup>[1](https://blog.modelcontextprotocol.io/posts/2025-11-20-adopting-mcpb/)</sup>

## How this repo treats bundles

- Source of truth stays in `vscode/packs/*/mcp/servers.<slug>.json` (ids, safety flags, provenance).
- Generated TOML remains command-based with `<TO_FILL>` placeholders; keep secrets out of git.
- If you publish a `.mcpb` externally, keep the server id, name, and safety flags in sync with the manifest here so agents stay compatible.

## Plugging an existing `.mcpb` into a stack

1. Run the stack installer (for example `./scripts/install/fullstack-js-ts-macos.sh`) to generate exports and workspace wiring.
2. Import your `.mcpb` using your MCP-aware client (Codex or another agent runtime). For Codex, follow `codex/docs/config-guides.md` and add a `[mcp_servers.<id>]` block that points to the bundle path on disk instead of the command-based fragment. Use placeholder paths (e.g. `<PATH_TO_BUNDLE>`) in any shared snippets.
3. Leave the manifest JSON untouched; it remains the compatibility contract between agents and the runtime regardless of how the server is shipped.

## Building `.mcpb` packages (optional)

If you want to publish a bundle for a server defined here:

- Use the official MCP bundle tooling to package the server, keeping the `id` identical to the manifest entry. Example (adjust to the CLI you install):

  ```bash
  mcpb pack path/to/server --output ./dist/<id>.mcpb
  ```

- Document provenance and safety flags alongside the bundle download (mirroring `servers.<slug>.json`).
- Treat the bundle as a distributable artefact; do not commit it. Ship it alongside release assets or via your preferred registry.

Bundle-ready servers in this repo (keep ids aligned with manifests):

- `github`, `context7-docs`, `sonatype-deps`, `elasticsearch`, `mongodb` (fullstack-js-ts)
- `kubernetes`, `aws` (optional/opt-in), plus the above where relevant (infra/devops)

This keeps the repo authoritative for ids, flags, and wiring, while letting teams distribute `.mcpb` files when that better suits their environment.
