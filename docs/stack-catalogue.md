# Stack Catalogue

Stacks combine a devcontainer, VS Code profile, agents, toolsets, and bundles into installable “Agent Packs” for specific personas. Profiles are exported from VS Code; devcontainers keep tooling reproducible; agents and toolsets are wired via JSON configs and prompts in this repo.

| Stack                 | Persona                               | What you get                                                                                                                                                                | How to install                                                                                                                                                                                                                                                                                   |
| --------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| fullstack-js-ts       | Full-stack JS/TS developers (web/API) | Devcontainer (Node/TypeScript), profile export placeholder to replace after first run, agents: refactor-surgeon, test-writer, doc-surgeon; toolsets: local-dev, review-only | Run OS installer script (e.g. `scripts/install/fullstack-js-ts-macos.sh`). It builds the export, installs extensions into the `Fullstack JS/TS – Web & API` profile, and opens the workspace. Optionally import `vscode/profiles-dist/fullstack-js-ts.code-profile` once you have a real export. |
| python-data-analytics | Data/ML/analytics engineers (Python)  | Devcontainer (Python), profile export placeholder to replace after first run, agents: data-explorer, pipeline-refactorer, doc-surgeon; toolsets: local-dev, review-only     | Run OS installer script (e.g. `scripts/install/python-data-analytics-macos.sh`). It builds the export, installs extensions into the profile, and opens the workspace. Optionally import `vscode/profiles-dist/python-data-analytics.code-profile` once you have a real export.                   |
| infra-ops-sre         | Infra/Platform/SRE engineers          | Devcontainer (infra tooling), profile export placeholder to replace after first run, agents: infra-reviewer, incident-scribe, doc-surgeon; toolsets: review-only            | Run OS installer script (e.g. `scripts/install/infra-ops-sre-macos.sh`). It builds the export, installs extensions into the profile, and opens the workspace. Optionally import `vscode/profiles-dist/infra-ops-sre.code-profile` once you have a real export.                                   |

Notes

- Profile placeholders (e.g. `vscode/profiles-dist/fullstack-js-ts.code-profile`) exist for wiring; overwrite them with real VS Code exports via “Export Profile…” when using a stack seriously.
- Installer scripts are non-destructive; they build exports, install extensions into the profile, and open the workspace without touching host dotfiles. Profile import is optional if you already have a `.code-profile` export.

## Stack details

### Fullstack JS/TS

- What you get: Node/TypeScript devcontainer, placeholder profile, agents (refactor-surgeon, test-writer, doc-surgeon), toolsets (local-dev, review-only).
- Who it’s for: Web/API engineers.
- How to install: run the OS script under `scripts/install/fullstack-js-ts-*.sh|ps1`, then import the `.code-profile` via VS Code.
- Prompts: See `prompts/stacks/fullstack-js-ts.prompts.md`.

### Python Data & Analytics

- What you get: Python devcontainer, placeholder profile, agents (data-explorer, pipeline-refactorer, doc-surgeon), toolsets (local-dev, review-only).
- Who it’s for: Data/ML/analytics engineers.
- How to install: run `scripts/install/python-data-analytics-*.sh|ps1`, then import the `.code-profile` via VS Code.
- Prompts: See `prompts/stacks/python-data-analytics.prompts.md`.

### Infra Ops / SRE

- What you get: Infra-focused devcontainer, placeholder profile, agents (infra-reviewer, incident-scribe, doc-surgeon), toolsets (review-only).
- Who it’s for: Infra/platform/SRE engineers.
- How to install: run `scripts/install/infra-ops-sre-*.sh|ps1`, then import the `.code-profile` via VS Code.
- Prompts: See `prompts/stacks/infra-ops-sre.prompts.md`.
