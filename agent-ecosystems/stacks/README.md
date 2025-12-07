# Stacks

Workspace stacks pair devcontainers, VS Code profiles, and default agents/toolsets for a given workflow or language family.

## Included

- `fullstack-js-ts.stack.json`: Targets JavaScript/TypeScript fullstack work. Uses `vscode/.devcontainer/devcontainer.json` (node-based devcontainer) and expects a `vscode/profiles-dist/fullstack-js-ts.code-profile` export containing core JS/TS extensions, Copilot, Copilot Chat, and MCP integration. Default agents: refactor-surgeon, test-writer, doc-surgeon. Default toolsets: `toolset.local-dev`, `toolset.review-only`. Tags: javascript, typescript, ai-heavy, default.

Stacks tie into existing profile/export flows—use VS Code profile exports for `profilePath` and existing devcontainer definitions to avoid duplicating configuration.
