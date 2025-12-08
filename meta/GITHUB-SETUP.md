# GitHub setup notes

- Mark the `CI – Minimal validation` workflow (from `.github/workflows/ci-minimal.yml`) as a required status check on `main` via Branch protection rules.
- Leave docs build workflows (`docs-antora.yml`, `docs-check.yml`) as separate jobs; they are not part of the minimal gate.
- Keep `validate-packs.yml` and `agent-ecosystems-release.yml` optional unless shipping a packs-specific release.
