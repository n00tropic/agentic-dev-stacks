# Agent Ecosystem Schemas

These JSON Schemas describe the core building blocks used under `agent-ecosystems/`:

- `agent.schema.json`: Agent blueprints referencing toolsets, prompts, and safety defaults.
- `toolset.schema.json`: Collections of MCP servers and Copilot tools bound to a security profile.
- `stack.schema.json`: Workspace stacks combining devcontainers, VS Code profiles, and default agents/toolsets.
- `bundle.schema.json`: OS-specific bundle metadata pointing to stack artefacts and install instructions.

## Validation

Use `agent-ecosystems/scripts/validate-ecosystem-configs.*` (added in this repo) to validate all JSON files under `agent-ecosystems/{agents,toolsets,stacks,bundles}` against these schemas. The validator resolves schemas by filename relative to `agent-ecosystems/schemas/` via their `$id` values.

When adding new JSON files, ensure they include the correct `$schema` URL pointing to the matching schema and run the validation script before committing.
