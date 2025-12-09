# Visual Studio Code packs: source to exports

This directory holds the **source-of-truth packs** and the tooling to generate reproducible, workspace-ready exports. Nothing here touches your global VS Code settings; all outputs land under `exports/`.

## Structure

- `packs/<pack>/profiles/PROFILE.<slug>.md`: profile descriptor.
- `packs/<pack>/extensions/extensions.<slug>.txt`: curated extensions.
- `packs/<pack>/settings/settings.<slug>.json`: settings overlay for the profile.
- `packs/<pack>/mcp/servers.<slug>.json`: Model Context Protocol (MCP) manifest for the profile.
- Optional per-profile assets (pulled into exports when present):
  - `packs/<pack>/tasks/tasks.<slug>.json`
  - `packs/<pack>/launch/launch.<slug>.json`
  - `packs/<pack>/snippets/snippets.<slug>.code-snippets`
  - `packs/<pack>/keybindings/keybindings.<slug>.json`
  - `packs/<pack>/workspace-templates/<slug>.code-workspace` (overrides the default export)
- `scripts/`: export and validation tooling (`export-packs.py`, `merge-mcp-fragments.py`, helpers).
- `export-map.yaml`: slug → pack → export paths → display name mapping.
- `exports/`: **generated, gitignored** workspaces and install aids (safe to delete/regenerate).
- `prompts/packs/**`: reusable prompt packs you can copy into exports or Copilot custom instructions (keep en-GB spelling).

## How to export workspaces (source → exports)

```bash
cd vscode
python scripts/export-packs.py <slug> [<slug> ...]
```

- Reads pack data via `export-map.yaml`.
- Writes to `exports/workspaces/<slug>/` (all optional except settings/extensions):
  - `.vscode/extensions.list`
  - `.vscode/settings.json`
  - `.vscode/tasks.json`
  - `.vscode/launch.json`
  - `.vscode/keybindings.json`
  - `.vscode/snippets/*.code-snippets`
  - `<slug>.code-workspace` (overridden by `workspace-templates/<slug>.code-workspace` if present)
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

### Post-import helper (apply-profile-assets)

After importing a `.code-profile`, preview or apply extra assets (tasks/launch/snippets/keybindings) and print MCP TOML for a slug:

```bash
python scripts/apply-profile-assets.py --slug fullstack-js-ts --dry-run
# Or apply into another workspace
python scripts/apply-profile-assets.py --slug fullstack-js-ts --apply --target-dir /path/to/workspace
```

> Fast path: `scripts/macos/install-profiles.sh`, `scripts/linux/install-profiles.sh`, or `scripts/windows/Install-Profiles.ps1` will loop through slugs (or the ones you pass) using `export-map.yaml`, ensure the profile exists, install extensions, and open the workspace once.

## Installation script generators

Generate standalone and pack-level installation scripts from source:

```bash
# Generate standalone installation scripts for all profiles
python scripts/generate-install-scripts.py              # all 16 profiles
python scripts/generate-install-scripts.py slug1 slug2  # specific profiles

# Generate pack-level installation scripts for all packs
python scripts/generate-pack-scripts.py                 # all 6 packs
python scripts/generate-pack-scripts.py pack1 pack2     # specific packs
```

- Standalone scripts: `scripts/install-<slug>.sh` and `scripts/Install-<Slug>.ps1`
- Pack-level scripts: `packs/<pack>/scripts/{linux,macos,windows}/install-profiles.sh` (or `.ps1`)
- Idempotent: safe to regenerate; scripts read from `export-map.yaml` for metadata
- Generated scripts are committed to the repository for easy distribution

## Validation reminders

- Keep source packs in `packs/**` aligned with `CONTROL.md`.
- After changing extensions: run `./scripts/helpers/validate-extensions.sh` (or `.\scripts\helpers\Validate-Extensions.ps1` on Windows).
- After MCP manifest changes: consider `python scripts/merge-mcp-fragments.py ...` to stage `codex-mcp.generated.toml` locally (never commit generated files).
- Optional publishing: use `Export profile to gist` workflow (`workflow_dispatch`) with `slug` (and optional `gist_id`) plus `secrets.GIST_TOKEN` (scope: gist) to ship the `.code-profile` export for that slug. VS Code imports via `https://vscode.dev/editor/profile/github/<gist_id>`.
- SSH alternative: create a gist in the UI, then run `./scripts/helpers/export-gist-ssh.sh <slug> <gist_id>` (SSH key with gist access required; expects `vscode/profiles-dist/<slug>.code-profile`).
