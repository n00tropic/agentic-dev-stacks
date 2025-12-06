# Agentic Dev Stacks

Scoped, cross-OS VS Code packs plus MCP manifests, designed as a **compiler**: packs (source) → reproducible exports → importable profiles.

## Layout (truths up front)

- **Root**
  - Governance/agent docs: `AGENTS.md`, `CONTROL.md`, `copilot-instructions.md`, `agent-instructions.md`.
  - Profile dist map: `PROFILE_DIST.md` (slug → profile name → `.code-profile` → gist URL placeholders).
- **`vscode/`**
  - Packs (source of truth):
    - `packs/<pack>/profiles/PROFILE.<slug>.md`
    - `packs/<pack>/extensions/extensions.<slug>.txt`
    - `packs/<pack>/settings/settings.<slug>.json`
    - `packs/<pack>/mcp/servers.<slug>.json`
  - Custom agents SSoT: `../agents/<slug>/*.agent.md` (copied into bundles under `.github/agents/`)
  - Tooling: `scripts/**`
  - Exports (gitignored, reproducible): `exports/workspaces/<slug>/...`
  - Dist exports (versioned if present): `profiles-dist/*.code-profile` (never hand-edit)
- **`codex/`** – docs for configuring Codex and MCP safely (`config-guides.md`, `safe-vs-danger-modes.md`).
- **`prompts/`** – prompt packs for Copilot/sub-agents (copy into workspaces; en-GB spelling).

## Compiler pipeline (source → exports → dist)

1. Author in packs: edit `vscode/packs/**` (profiles, extensions, settings, MCP manifests).
2. Export reproducible workspaces (generated, safe to delete):
   ```bash
   cd vscode
   python scripts/export-packs.py <slug> [<slug> ...]
   ```
3. Materialise on a machine with official VS Code CLI:
   ```bash
   code --profile "<Profile Name>"
   cat exports/workspaces/<slug>/.vscode/extensions.list | xargs -n1 code --install-extension --profile "<Profile Name>"
   code exports/workspaces/<slug>/<slug>.code-workspace --profile "<Profile Name>"
   ```
4. Export a “good” profile back out from VS Code:
   - **Export Profile…** → save `.code-profile` to `vscode/profiles-dist/<slug>.code-profile` (do not hand-edit).
   - Optional: export to secret gist for one-click import.
5. Record mapping in `PROFILE_DIST.md` (slug, profile name, dist path, gist URL or `<TO_FILL>`).

## Golden paths

- **Repo-aware machines** (Mac/Windows/Linux): follow steps 2–3 above; reuse `vscode/scripts/{macos,linux}/install-profiles.sh` or `vscode/scripts/windows/Install-Profiles.ps1` to automate installing extensions per profile from the exports.
- **No-repo machines**: in VS Code, run **Import Profile…** and paste the gist URL listed in `PROFILE_DIST.md` (when populated). VS Code expects a gist containing a single `.code-profile` file; import URL format: `https://vscode.dev/editor/profile/github/<gist_id>`.

## Development container (preferred automation)

- Open in VS Code with the Development Containers extension or run `devcontainer up` (uses `.devcontainer/devcontainer.json`).
- Post-create runs: `pip3 install --user pyyaml toml && python3 vscode/scripts/build-bundles.py && bash vscode/scripts/validate-all-bundles.sh`.
- Result: fresh bundles + zips under `vscode/exports/bundles/**`, validated without touching host dot files.

## Safety notes

- Do not edit `~/.codex/config.toml` or VS Code global settings from this repo; copy snippets instead.
- Never hand-edit `.code-profile` files; always regenerate via VS Code Export Profile.
- Do not commit generated files (`vscode/exports/**`, `vscode/codex-mcp.generated.toml`).
- MCP manifests must use placeholders for secrets/paths; avoid adding credentials.
