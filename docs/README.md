# Docs workflow

- Build the site: `cd docs && ./build-docs.sh` (outputs to `build/site/`; open `build/site/index.html` locally).
- Link checks (requires a built site):
  - Offline/local only (anchors and local assets): `cd docs && ./check-links.sh`.
  - External HTTP/HTTPS (opt-in, uses network): `cd docs && CHECK_EXTERNAL=1 ./check-links.sh`.
- Tooling notes:
  - The docs site uses the custom Agentic Neon UI at `docs/ui/agentic-neon-ui` (built automatically by `build-docs.sh`).
  - GitHub Pages must use “GitHub Actions” as the source so the `docs-antora.yml` workflow can deploy `docs/build/site/` (via `actions/deploy-pages`). If Pages reverts to “Deploy from a branch”, the site will fall back to the default Jekyll view.
  - Lychee is downloaded on demand if not already installed.
