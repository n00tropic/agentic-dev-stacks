# Profile dist map: code-profile and gist exports

This file maps internal profile slugs to their dist exports for quick import via VS Code **Import Profile…**. Dist artefacts live in `vscode/profiles-dist/*.code-profile` (exported from VS Code) for local/offline use, and may also have optional secret gist URLs for one-click import.

> Dist files are **generated** via VS Code “Export Profile…”; do **not** hand-edit them. If a file or gist is missing, treat it as `<TO_FILL>` and regenerate.

## Profiles

- **core-base-dev**
  - Pack: `00-core-base`
  - VS Code profile name: `Core / Base Dev`
  - Local dist: `vscode/profiles-dist/core-base-dev.code-profile` (generated)
  - Gist URL: <https://gist.github.com/IAmJonoBo/777fc47859c4160611f8f2051e774ed0>

- **qa-static-analysis**
  - Pack: `00-core-base`
  - VS Code profile name: `QA / Static Analysis`
  - Local dist: `vscode/profiles-dist/qa-static-analysis.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/ccabda93275d90c2230e68c8d5fc3bde>

- **docs-librarian**
  - Pack: `40-docs-knowledge`
  - VS Code profile name: `Docs & Librarian`
  - Local dist: `vscode/profiles-dist/docs-librarian.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/8ce4274f319aace82069bfb409228252>

- **gitops-code-review**
  - Pack: `00-core-base`
  - VS Code profile name: `GitOps & Code Review`
  - Local dist: `vscode/profiles-dist/gitops-code-review.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/8d887e698b20eef584772ad881643867>

- **experimental-preview**
  - Pack: `50-experimental-playground`
  - VS Code profile name: `Experimental / Preview`
  - Local dist: `vscode/profiles-dist/experimental-preview.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/8549aed6b90c79b0bb7eab738b833d92>

- **fullstack-js-ts**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Fullstack JS/TS – Web & API`
  - Local dist: `vscode/profiles-dist/fullstack-js-ts.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/e9167998659b5d4a26d86b75b5572cd2>

- **frontend-ux-ui**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Frontend UX/UI – React / Storybook / DX`
  - Local dist: `vscode/profiles-dist/frontend-ux-ui.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/2a9af2bc4ea6b435b36b627e68ca6dd5>

- **node-backend-services**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Node / Backend Services – TS/Node`
  - Local dist: `vscode/profiles-dist/node-backend-services.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/bc847dc8a0561fed50502afc75721478>

- **python-services-clis**
  - Pack: `20-python-data-ml`
  - VS Code profile name: `Python Services & CLIs`
  - Local dist: `vscode/profiles-dist/python-services-clis.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/ea546ad3f4c382c3a28eac4c1c3b8803>

- **python-data-ml**
  - Pack: `20-python-data-ml`
  - VS Code profile name: `Python Data & ML`
  - Local dist: `vscode/profiles-dist/python-data-ml.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/8a9c3b702c1b95a369d35ea9aa871ef8>

- **infra-devops**
  - Pack: `30-infra-devops-platform`
  - VS Code profile name: `Infra & DevOps (Docker/K8s/Terraform)`
  - Local dist: `vscode/profiles-dist/infra-devops.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/518ddeae59c1e247cdc012fa8e573da2>

- **data-db-analytics**
  - Pack: `30-infra-devops-platform`
  - VS Code profile name: `Data / DB & Analytics`
  - Local dist: `vscode/profiles-dist/data-db-analytics.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/f1701cdb20a20096d99b804491be364c>

- **desktop-gui-cross**
  - Pack: `10-fullstack-js-ts`
  - VS Code profile name: `Desktop & GUI – Swift / TS / Python`
  - Local dist: `vscode/profiles-dist/desktop-gui-cross.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/1f15aa21c6fc30be4a64ecb68a584f96>

- **macos-apple-platforms**
  - Pack: `00-core-base`
  - VS Code profile name: `macOS – Apple Platforms & Tooling`
  - Local dist: `vscode/profiles-dist/macos-apple-platforms.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/5061fddf9fda8e280aa164444e8c1f02>

- **windows-polyglot-wsl**
  - Pack: `00-core-base`
  - VS Code profile name: `Windows – Polyglot + WSL`
  - Local dist: `vscode/profiles-dist/windows-polyglot-wsl.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/6bb67a0522f4520e9da90c377df82f86>

- **linux-ci-headless**
  - Pack: `30-infra-devops-platform`
  - VS Code profile name: `Linux – CI/Headless`
  - Local dist: `vscode/profiles-dist/linux-ci-headless.code-profile`
  - Gist URL: <https://gist.github.com/IAmJonoBo/84ba182e2be3dd9246bf82bccc983367>

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
