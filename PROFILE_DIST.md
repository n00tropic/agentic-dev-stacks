# Profile dist map: code-profile and gist exports

This file maps internal profile slugs to their dist exports for quick import via VS Code **Import Profile… (VS Code expects a single .code-profile file)**. Dist artefacts live in `vscode/profiles-dist/*.code-profile` (exported from VS Code) for local/offline use, and may also have optional secret gist URLs for one-click import.

> Dist files are **generated** via VS Code “Export Profile…”; do **not** hand-edit them. If a file or gist is missing, treat it as `<TO_FILL>` and regenerate.

<!-- vale off -->

## Profiles

| Slug                  | Pack                       | VS Code profile                         | Local dist                                                | Gist URL    |
| --------------------- | -------------------------- | --------------------------------------- | --------------------------------------------------------- | ----------- |
| core-base-dev         | 00-core-base               | Core / Base Dev                         | `vscode/profiles-dist/core-base-dev.code-profile`         | `<TO_FILL>` |
| qa-static-analysis    | 00-core-base               | QA / Static Analysis                    | `vscode/profiles-dist/qa-static-analysis.code-profile`    | `<TO_FILL>` |
| docs-librarian        | 40-docs-knowledge          | Docs & Librarian                        | `vscode/profiles-dist/docs-librarian.code-profile`        | `<TO_FILL>` |
| gitops-code-review    | 00-core-base               | GitOps & Code Review                    | `vscode/profiles-dist/gitops-code-review.code-profile`    | `<TO_FILL>` |
| experimental-preview  | 50-experimental-playground | Experimental / Preview                  | `vscode/profiles-dist/experimental-preview.code-profile`  | `<TO_FILL>` |
| fullstack-js-ts       | 10-fullstack-js-ts         | Fullstack JS/TS – Web & API             | `vscode/profiles-dist/fullstack-js-ts.code-profile`       | `<TO_FILL>` |
| frontend-ux-ui        | 10-fullstack-js-ts         | Frontend UX/UI – React / Storybook / DX | `vscode/profiles-dist/frontend-ux-ui.code-profile`        | `<TO_FILL>` |
| node-backend-services | 10-fullstack-js-ts         | Node / Backend Services – TS/Node       | `vscode/profiles-dist/node-backend-services.code-profile` | `<TO_FILL>` |
| python-services-clis  | 20-python-data-ml          | Python Services & CLIs                  | `vscode/profiles-dist/python-services-clis.code-profile`  | `<TO_FILL>` |
| python-data-ml        | 20-python-data-ml          | Python Data & ML                        | `vscode/profiles-dist/python-data-ml.code-profile`        | `<TO_FILL>` |
| python-data-analytics | <TO_FILL>                  | Python Data & Analytics                 | `vscode/profiles-dist/python-data-analytics.code-profile` | `<TO_FILL>` |
| infra-devops          | 30-infra-devops-platform   | Infra & DevOps (Docker/K8s/Terraform)   | `vscode/profiles-dist/infra-devops.code-profile`          | `<TO_FILL>` |
| infra-ops-sre         | <TO_FILL>                  | Infra Ops / SRE                         | `vscode/profiles-dist/infra-ops-sre.code-profile`         | `<TO_FILL>` |
| data-db-analytics     | 30-infra-devops-platform   | Data / DB & Analytics                   | `vscode/profiles-dist/data-db-analytics.code-profile`     | `<TO_FILL>` |
| desktop-gui-cross     | 10-fullstack-js-ts         | Desktop & GUI – Swift / TS / Python     | `vscode/profiles-dist/desktop-gui-cross.code-profile`     | `<TO_FILL>` |
| macos-apple-platforms | 00-core-base               | macOS – Apple Platforms & Tooling       | `vscode/profiles-dist/macos-apple-platforms.code-profile` | `<TO_FILL>` |
| windows-polyglot-wsl  | 00-core-base               | Windows – Polyglot + WSL                | `vscode/profiles-dist/windows-polyglot-wsl.code-profile`  | `<TO_FILL>` |
| linux-ci-headless     | 30-infra-devops-platform   | Linux – CI/Headless                     | `vscode/profiles-dist/linux-ci-headless.code-profile`     | `<TO_FILL>` |

Validation: `python3 scripts/check-profile-dist.py` fails if any production stack in `README.md` is missing a mapped `.code-profile` file. Set `SKIP_PROFILE_DIST_CHECK=1` to bypass when dist exports are intentionally absent during development.

<!-- vale on -->

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
