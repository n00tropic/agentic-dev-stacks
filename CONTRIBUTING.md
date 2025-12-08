# Contributing

Thanks for helping improve Agentic Dev Stacks. This project aims to be a reference for governed, reproducible AI-ready dev environments.

## Getting set up

- **Codespaces / devcontainer (recommended):** Open in GitHub Codespaces or run `devcontainer up --workspace-folder .` locally (Docker/Podman + Dev Containers extension required). This installs tooling and isolates from host dotfiles.
- **Local setup:** Install Git, Python 3, and VS Code with the `code` CLI enabled. For stack-specific installs, use the per-OS scripts under `scripts/install/` (e.g. `./scripts/install/fullstack-js-ts-macos.sh`).

## Running validations

Before sending a PR, run:

```bash
bash scripts/validate-all.sh    # use --fast to skip docs build locally
```

This covers trunk (if installed), QA preflight (extensions, MCP config structure, scripts, metadata, agent ecosystems), and docs build (unless skipped with `--fast`).
Outside the devcontainer, install Python deps once with `pip3 install --user -r requirements-dev.txt`.

## PR expectations

- Keep diffs small and scoped; follow profile/MCP rules in `AGENTS.md`, `GOVERNANCE.md`, and `CONTROL.md`.
- Ensure `bash scripts/qa-preflight.sh` is green; build docs if you touched anything under `docs/`.
- Update docs and prompts when behaviour changes; link relevant sections in the PR description.
- Avoid committing generated artefacts (`vscode/exports/**`, `vscode/codex-mcp.generated.toml`) or secrets; use placeholders and env vars.
