# Profile dist map: code-profile and gist exports

This file maps internal profile slugs to their dist exports for quick import via VS Code **Import Profile…**. Dist artefacts live in `vscode/profiles-dist/*.code-profile` (exported from VS Code) for local/offline use, and may also have optional secret gist URLs for one-click import.

> Dist files are **generated** via VS Code “Export Profile…”; do **not** hand-edit them. If a file or gist is missing, treat it as `<TO_FILL>` and regenerate.

## Profiles

- **core-base-dev**
  - Pack: `00-core-base`
  - VS Code profile name: `Core / Base Dev`
  - Local dist: `vscode/profiles-dist/core-base-dev.code-profile` (generated)
  - Gist URL: `<TO_FILL>`

- **qa-static-analysis**
  - Pack: `00-core-base`
  - VS Code profile name: `QA / Static Analysis`
  - Local dist: `vscode/profiles-dist/qa-static-analysis.code-profile`
  - Gist URL: `<TO_FILL>`

- **docs-librarian**
  - Pack: `40-docs-knowledge`
  - VS Code profile name: `Docs & Librarian`
  - Local dist: `vscode/profiles-dist/docs-librarian.code-profile`
  - Gist URL: `<TO_FILL>`

- **gitops-code-review**
  - Pack: `00-core-base`
  - VS Code profile name: `GitOps & Code Review`
  - Local dist: `vscode/profiles-dist/gitops-code-review.code-profile`
  - Gist URL: `<TO_FILL>`

- **experimental-preview**
  - Pack: `50-experimental-playground`
  - VS Code profile name: `Experimental / Preview`
  - Local dist: `vscode/profiles-dist/experimental-preview.code-profile`
  - Gist URL: `<TO_FILL>`

- **fullstack-js-ts**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Fullstack JS/TS – Web & API`
  - Local dist: `vscode/profiles-dist/fullstack-js-ts.code-profile`
  - Gist URL: `<TO_FILL>`

- **frontend-ux-ui**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Frontend UX/UI – React / Storybook / DX`
  - Local dist: `vscode/profiles-dist/frontend-ux-ui.code-profile`
  - Gist URL: `<TO_FILL>`

- **node-backend-services**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Node / Backend Services – TS/Node`
  - Local dist: `vscode/profiles-dist/node-backend-services.code-profile`
  - Gist URL: `<TO_FILL>`

- **python-services-clis**
  - Pack: `20-python-data-ml`
  - VS Code profile name: `Python Services & CLIs`
  - Local dist: `vscode/profiles-dist/python-services-clis.code-profile`
  - Gist URL: `<TO_FILL>`

- **python-data-ml**
  - Pack: `20-python-data-ml`
  - VS Code profile name: `Python Data & ML`
  - Local dist: `vscode/profiles-dist/python-data-ml.code-profile`
  - Gist URL: `<TO_FILL>`

- **infra-devops**
  - Pack: `30-infra-devops-platform`
  - VS Code profile name: `Infra & DevOps (Docker/K8s/Terraform)`
  - Local dist: `vscode/profiles-dist/infra-devops.code-profile`
  - Gist URL: `<TO_FILL>`

- **data-db-analytics**
  - Pack: `30-infra-devops-platform`
  - VS Code profile name: `Data / DB & Analytics`
  - Local dist: `vscode/profiles-dist/data-db-analytics.code-profile`
  - Gist URL: `<TO_FILL>`

- **desktop-gui-cross**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Desktop & GUI – Swift / TS / Python`
  - Local dist: `vscode/profiles-dist/desktop-gui-cross.code-profile`
  - Gist URL: `<TO_FILL>`

- **macos-apple-platforms**
  - Pack: `00-core-base`
  - VS Code profile name: `macOS – Apple Platforms & Tooling`
  - Local dist: `vscode/profiles-dist/macos-apple-platforms.code-profile`
  - Gist URL: `<TO_FILL>`

- **windows-polyglot-wsl**
  - Pack: `00-core-base`
  - VS Code profile name: `Windows – Polyglot + WSL`
  - Local dist: `vscode/profiles-dist/windows-polyglot-wsl.code-profile`
  - Gist URL: `<TO_FILL>`

- **linux-ci-headless**
  - Pack: `30-infra-devops-platform`
  - VS Code profile name: `Linux – CI/Headless`
  - Local dist: `vscode/profiles-dist/linux-ci-headless.code-profile`
  - Gist URL: `<TO_FILL>`

## Publishing checklist (dist refresh)

1. Update packs under `vscode/packs/**` as needed.
2. Regenerate exports: `cd vscode && python scripts/export-packs.py <slugs...>`.
3. Open the exported workspace for each slug and refine if needed.
4. In VS Code, **Export Profile…** for the profile name above:
   - Save the `.code-profile` to `vscode/profiles-dist/<slug>.code-profile` (overwrite allowed).
   - Publish a **secret** gist via the export dialog; paste the URL above.
5. Commit updated docs and dist `.code-profile` files (never edit them manually).

### Publish via GitHub Actions (optional)

- Trigger `Export profile to gist` workflow (`workflow_dispatch`) with `slug` (and optional `gist_id`).
- Workflow generates the workspace archive and uploads to a secret gist using `secrets.GIST_TOKEN` (scope: `gist` only).
- Artifacts are also stored as workflow artifacts for review.

### Publish via SSH (manual, existing gist)

- Create a (secret) gist once in the GitHub UI and note its ID.
- Ensure your SSH key has gist write access.
- Run from the repository root:

  ```bash
  cd vscode
  python scripts/export-packs.py <slug>
  ./scripts/helpers/export-gist-ssh.sh <slug> <gist_id>
  ```
