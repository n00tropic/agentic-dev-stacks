# Docs workflow

- Build the site: `cd docs && ./build-docs.sh` (outputs to `build/site/`; open `build/site/index.html` locally).
- Link checks (requires a built site):
  - Offline/local only (anchors and local assets): `cd docs && ./check-links.sh`.
  - External HTTP/HTTPS (opt-in, uses network): `cd docs && CHECK_EXTERNAL=1 ./check-links.sh`.
- Tooling notes: Antora uses the vendored UI at `docs/ui/ui-bundle.zip`; lychee is downloaded on demand if not already installed.
