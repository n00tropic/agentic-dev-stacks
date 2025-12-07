# Stacks

Workspace stacks pair devcontainers, VS Code profiles, and default agents/toolsets for a given workflow or language family.

## Included

- `fullstack-js-ts.stack.json`: Targets JavaScript/TypeScript fullstack work. Uses `vscode/.devcontainer/devcontainer.json` (node-based devcontainer) and expects a `vscode/profiles-dist/fullstack-js-ts.code-profile` export containing core JS/TS extensions, Copilot, Copilot Chat, and MCP integration. Default agents: refactor-surgeon, test-writer, doc-surgeon. Default toolsets: `toolset.local-dev`, `toolset.review-only`. Tags: javascript, typescript, ai-heavy, default.
- `python-data-analytics.stack.json`: Targets Python data/analytics engineers. Uses `vscode/.devcontainer/python-data-analytics/devcontainer.json` and expects `vscode/profiles-dist/python-data-analytics.code-profile` (placeholder) with Python/Jupyter extensions. Default agents: data-explorer, pipeline-refactorer, doc-surgeon. Default toolsets: `toolset.local-dev`, `toolset.review-only`. Tags: python, data, analytics, ai-heavy.
- `infra-ops-sre.stack.json`: Targets infra/platform/SRE engineers. Uses `vscode/.devcontainer/infra-ops-sre/devcontainer.json` and expects `vscode/profiles-dist/infra-ops-sre.code-profile` (placeholder). Default agents: infra-reviewer, incident-scribe, doc-surgeon. Default toolsets: `toolset.review-only`. Tags: infra, ops, sre, ai-heavy.

Stacks tie into existing profile/export flows—use VS Code profile exports for `profilePath` and existing devcontainer definitions to avoid duplicating configuration.
