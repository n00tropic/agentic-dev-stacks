<!-- vale off -->

# Agentic Dev Stacks – Devcontainer + MCP + Copilot Sample

## What it is

Devcontainers plus curated VS Code profiles, MCP manifests, and custom Copilot agents for reproducible, AI-ready development stacks. It ships a lean Ubuntu-based devcontainer, profile packs, and MCP configurations kept as code.

## Why it’s useful as a sample

- Shows how to make devcontainers the primary environment for MCP/Copilot work (Codespaces-ready).
- Demonstrates curated VS Code profiles and bundle exports with MCP manifests kept in git.
- Provides a single validation entrypoint (`bash scripts/validate-all.sh`) and a minimal CI workflow wired to it.
- Documents an MCP security posture (least privilege, reviewable manifests, no inline secrets).

## How to try it (5-minute flow)

1. Open in GitHub Codespaces or run `devcontainer up --workspace-folder .` locally.
2. Wait for the container build (installs Python 3.12, Node 22, `requirements-dev.txt`).
3. Run `bash scripts/validate-all.sh --fast` (omit `--fast` to include docs build).

## What people can copy

- Devcontainer structure with feature-based installs and focused post-create.
- Unified validation script + CI minimal workflow.
- Packaged VS Code profiles/bundles layout under `vscode/`.
- MCP security/governance doc patterns and placeholders-first manifests.

<!-- vale on -->
