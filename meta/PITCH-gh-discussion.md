<!-- vale off -->

# Agentic Dev Stacks – discussion blurb

Teams keep asking how to standardise MCP + Copilot usage without leaking secrets or hand-building dev environments. This repository is an opinionated, OSS reference: devcontainer-first, curated VS Code profiles, MCP manifests as code, and a single validation/CI path.

Highlights:

- Devcontainer hero path (Codespaces-ready) with Node/Python features and focused post-create.
- Unified validation script (`bash scripts/validate-all.sh`) wired into a minimal CI workflow.
- MCP security & governance doc (least privilege, reviewed manifests, no inline secrets, sandbox-first).
- Packs/bundles that show how to ship profiles, agents, and MCP fragments together.

Ask: would linking this from your devcontainer/MCP/Copilot docs or template collections help teams looking for a governed, reproducible example?

<!-- vale on -->
