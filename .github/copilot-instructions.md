# Copilot Instructions for agentic-dev-stacks

- Agent ecosystem source of truth lives in `agent-ecosystems/` (agents, toolsets, stacks, bundles, contracts, scenarios, circuits).
- Validate/build commands:
  - `bash scripts/check-agent-ecosystems.sh --with-bundles`
  - `bash scripts/qa-preflight.sh`
  - `python3 agent-ecosystems/scripts/run-agent-scenarios.py --no-output`
- Stacks:
  - Fullstack JS/TS (hero), Python Data & Analytics (beta), Infra Ops / SRE (beta). See `docs/stack-catalogue.md`.
- Agents must respect contracts (`agent-ecosystems/contracts/*.contract.json`) and structured outputs when defined.
- Prompt packs per stack live in `prompts/stacks/` for starter requests.
- No secrets in repo; use env vars for MCP tokens; keep toolsets least-privilege.
