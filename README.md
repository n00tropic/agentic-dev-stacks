<!-- vale off -->

# Agentic Dev Stacks

<!-- cspell:ignore Agentic Prereqs dotfiles Antora -->

Scoped, cross-OS VS Code packs plus MCP manifests, designed as a **compiler**: devcontainers + profiles + curated agents + MCP toolsets. Full docs: <https://n00tropic.github.io/agentic-dev-stacks>

- Before: every machine grows its own VS Code / MCP quirks.
- After: one repo, one truth; one-liner to land a vetted, agent-ready stack on macOS, Windows, or Linux.
- Guardrails: profiles are exportable, reviewable, and avoid your global dotfiles.

See vscode/prompts/phase-4-agent-ops.md for the Agent Ops meta-prompt (used with Copilot Chat).

## Why / Who

- Why: Single source of truth for reproducible, sandbox-friendly VS Code profiles and MCP manifests without touching host dotfiles.
- Who: Engineers and reviewers who need predictable, policy-aligned environments across macOS, Windows, and Linux.
- Hero stack now: Fullstack JS/TS (agents + toolsets). See `docs/stack-catalogue.md`.

## Quickstart (reference profile: Core / Base Dev)

- Prereqs: VS Code CLI `code` in PATH, Python 3, Git + curl (for docs/bundle steps).
- Exactly one first command per OS (fresh machines included):

  ```bash
  # macOS / Linux
  cd vscode && ./scripts/install-core-base-dev.sh
  ```

  ```powershell
  # Windows PowerShell
  cd vscode
  .\scripts\Install-CoreBaseDev.ps1
  ```

- What it does: ensures the `core-base-dev` export exists (runs `export-packs.py` if missing), installs extensions into the `Core / Base Dev` profile via `code --install-extension --profile`, and opens the exported workspace under that profile. No global settings or dotfiles are touched.

## Installation scripts (all profiles)

All 16 profiles have standalone installation scripts:

```bash
# macOS / Linux - install any profile
cd vscode && ./scripts/install-<slug>.sh

# Windows PowerShell
cd vscode
.\scripts\Install-<Slug>.ps1
```

Examples: `install-fullstack-js-ts.sh`, `Install-PythonDataMl.ps1`, `install-qa-static-analysis.sh`

Pack-level installers (install all profiles from a pack or specific ones):

```bash
# Install all profiles from the 10-fullstack-js-ts pack (macOS)
cd vscode/packs/10-fullstack-js-ts/scripts/macos
./install-profiles.sh

# Install specific profiles from a pack
./install-profiles.sh fullstack-js-ts frontend-ux-ui
```

## Bundle builder (for handoff)

- Build a distributable bundle (git-ignored) for any slug:

  ```bash
  cd vscode
  python3 scripts/build-bundles.py core-base-dev
  ```

- Output: `vscode/exports/bundles/<slug>/` plus `<slug>-bundle.zip` with workspace, extensions list, MCP manifest + generated TOML, prompts, agents, per-OS install scripts, and metadata.

## Documentation

- Docs site (Antora, GitHub Pages): <https://n00tropic.github.io/agentic-dev-stacks>
- Source lives in `docs/` (Antora playbook + modules). Build locally:

  ```bash
  cd docs
  ./build-docs.sh
  ```

  Output: `docs/build/site` (git-ignored).

- Workspace MCP validation (macOS/Linux):

  ```bash
  python scripts/validate-mcp-config.py
  ```

  Validates `.vscode/mcp.json` structure (command/args/env per server); warns if commands diverge from the standard `/bin/sh -c` pattern.

- Coming back online: visual walkthroughs (before/after profile import, MCP validation catching mistakes) will ship on the docs site; contributions welcome once the site is live again.

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
  - Exports (git-ignored, reproducible): `exports/workspaces/<slug>/...`
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

## Golden paths (copy-pasta)

- Solo dev on laptop (Core / Base Dev, quickest win):

  ```bash
  cd vscode && ./scripts/install-core-base-dev.sh
  ```

  ```powershell
  cd vscode
  .\scripts\Install-CoreBaseDev.ps1
  ```

- Reviewer on a locked-down machine (no repo checkout): use VS Code **Import Profile…** and paste the gist URL from `PROFILE_DIST.md` once populated (format: `https://vscode.dev/editor/profile/github/<gist_id>`). Profiles stay reviewable and avoid host dotfiles.

- Team baseline via devcontainer (repro + validation):

  ```bash
  devcontainer up --workspace-folder .
  ```

  Post-create: `pip3 install --user pyyaml toml && python3 vscode/scripts/build-bundles.py && bash vscode/scripts/validate-all-bundles.sh` (runs in container; leaves host untouched).

## Development container (preferred automation)

- Open in VS Code with the Development Containers extension or run `devcontainer up` (uses `.devcontainer/devcontainer.json`).
- Post-create runs: `pip3 install --user pyyaml toml && python3 vscode/scripts/build-bundles.py && bash vscode/scripts/validate-all-bundles.sh`.
- Result: fresh bundles + zips under `vscode/exports/bundles/**`, validated without touching host dot files.

## CI coverage

- `validate-packs`: validates extension lists and metadata on PRs/pushes touching packs/control docs.
- `docs-check`: PR link checker + docs build; `docs-antora`: deploys docs to GitHub Pages on main.
- `ci-minimal` (added): runs `trunk check --ci`, Python syntax checks, JSON/TOML validation, and agent-ecosystems checks (schemas + scenarios) to keep scripts and manifests healthy.

## Agent ecosystems release flow

- Tag: `agent-stacks-vX.Y.Z` (or trigger the workflow dispatch with a version).
- CI runs validations, scenarios, and bundle builds; outputs ZIPs to `dist/bundles/` plus metadata in `dist/metadata/`.
- GitHub Release attaches the built ZIPs and checksums.

## QA preflight (pre-release health checks)

Run comprehensive health checks before any release:

```bash
bash scripts/qa-preflight.sh
```

This validates:

- Extension lists (shell + Python validators)
- MCP configuration structure
- Python syntax across all scripts
- JSON/TOML format validation
- Shell script integrity
- Metadata consistency (CONTROL.md ↔ export-map.yaml)
- Presence of all installation scripts (standalone + pack-level)
- Agent ecosystems configs and scenarios (via `scripts/check-agent-ecosystems.sh`)

For any new agent/toolset/stack/bundle, add at least one scenario under `agent-ecosystems/tests/scenarios/` and ensure `scripts/check-agent-ecosystems.sh` passes.

## Safety notes

- Do not edit `~/.codex/config.toml` or VS Code global settings from this repository; copy snippets instead.
- Never hand-edit `.code-profile` files; always regenerate via VS Code Export Profile.
- Do not commit generated files (`vscode/exports/**`, `vscode/codex-mcp.generated.toml`).
- MCP manifests must use placeholders for secrets/paths; avoid adding credentials.

<!-- vale on -->
