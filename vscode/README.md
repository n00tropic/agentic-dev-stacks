# VS Code Packs (source → exports)

This directory holds the **source-of-truth packs** and the tooling to generate reproducible, workspace-ready exports. Nothing here touches your global VS Code settings; all outputs land under `exports/`.

## Structure

- `packs/<pack>/profiles/PROFILE.<slug>.md` — profile descriptor.
- `packs/<pack>/extensions/extensions.<slug>.txt` — curated extensions.
- `packs/<pack>/settings/settings.<slug>.json` — settings overlay for the profile.
- `packs/<pack>/mcp/servers.<slug>.json` — MCP manifest for the profile.
- `packs/<pack>/workspace-templates/` — example `.code-workspace` files.
- `scripts/` — export + validation tooling (`export-packs.py`, `merge-mcp-fragments.py`, helpers).
- `export-map.yaml` — slug → pack → export paths → display name mapping.
- `exports/` — **generated, gitignored** workspaces and install aids (safe to delete/regenerate).

## How to export workspaces (source → exports)

```bash
cd vscode
python scripts/export-packs.py <slug> [<slug> ...]
```

- Reads pack data via `export-map.yaml`.
- Writes to `exports/workspaces/<slug>/`:
  - `.vscode/extensions.list`
  - `.vscode/settings.json`
  - `<slug>.code-workspace`
- Overwrite-safe; never writes outside `exports/`.

## How to apply exports on a new machine

1. Install extensions (optionally scoped to a profile):
   ```bash
   cd vscode
   cat exports/workspaces/<slug>/.vscode/extensions.list | xargs -L1 code --install-extension --profile "<Profile Name>"
   ```
   _On Windows PowerShell:_ `Get-Content exports/workspaces/<slug>/.vscode/extensions.list | ForEach-Object { code --install-extension $_ --profile "<Profile Name>" }`
2. Open the workspace with (or without) the profile:
   ```bash
   code exports/workspaces/<slug>/<slug>.code-workspace --profile "<Profile Name>"
   ```

## Validation reminders

- Keep source packs in `packs/**` aligned with `CONTROL.md`.
- After changing extensions: run `./scripts/helpers/validate-extensions.sh` (or `.\scripts\helpers\Validate-Extensions.ps1` on Windows).
- After MCP manifest changes: consider `python scripts/merge-mcp-fragments.py ...` to stage `codex-mcp.generated.toml` locally (never commit generated files).
