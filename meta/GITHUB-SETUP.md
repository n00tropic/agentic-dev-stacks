# GitHub setup notes

- Mark the `CI – Minimal validation` workflow (from `.github/workflows/ci-minimal.yml`) as a required status check on `main` via Branch protection rules.
- Leave docs build workflows (`docs-antora.yml`, `docs-check.yml`) as separate jobs; they are not part of the minimal gate.
- Keep `validate-packs.yml` and `agent-ecosystems-release.yml` optional unless shipping a packs-specific release.

## Security & analysis

- Enable GitHub security features: `Dependabot` alerts + security updates, secret scanning, and code scanning (choose preferred engine) on `main`.
- Apply branch protection on `main` requiring `CI – Minimal validation`; optionally require docs build/deploy jobs.
- Encourage MCP manifest reviews: treat MCP JSON/TOML as IaC, ensure reviewers check flags (`optional`, `privacy_sensitive`, `experimental`) and notes.
- Set repository topics for visibility: `devcontainer`, `codespaces`, `github-copilot`, `mcp`, `ai-agents`, `developer-environment`.

## Outreach materials

- Use `meta/PITCH-devcontainers-template.md` when proposing this repository as a devcontainer/Codespaces template or sample (e.g., issues/PRs in devcontainers/templates).
- Use `meta/PITCH-gh-discussion.md` for GitHub Discussions in devcontainer/Codespaces communities.
