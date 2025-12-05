# VS Code packs and exports

## What lives here

- `packs/` — canonical, versioned sources (profiles, extensions, settings, MCP manifests).
- `export-map.yaml` — slug → pack → export paths → display name mapping.
- `scripts/` — helper tooling (validation, MCP merge, exports).
- `exports/` — generated, gitignored workspace-ready outputs (safe to delete/regenerate).

## Generate workspace exports

```bash
cd vscode
python3 scripts/export-packs.py <slug> [<slug> ...]
```

- Uses `export-map.yaml` to locate the pack and export paths.
- Writes to `exports/workspaces/<slug>/`:
  - `.vscode/settings.json` (copied from pack settings)
  - `.vscode/extensions.list` (normalized extension IDs)
  - `<slug>.code-workspace` (standard workspace pointing one level up)
- Overwrite-safe; never writes outside `exports/`.

## Open an exported workspace

```bash
code exports/workspaces/<slug>/<slug>.code-workspace
```

You can pair this with VS Code CLI profiles if desired; no global settings are changed by the script.

## Validation reminders

- Profile content remains in `packs/**`; keep it in sync with `CONTROL.md`.
- Run `./scripts/helpers/validate-extensions.sh` from `vscode/` after modifying extensions.
- For MCP changes, use `python scripts/merge-mcp-fragments.py ...` to stage TOML locally; do not commit generated files.
