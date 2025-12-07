# Toolsets

Toolsets define reusable capability bundles for agents. They describe MCP servers, Copilot tools, and the expected security posture so agents inherit a consistent least-privilege setup.

## Included exemplars

- `toolset.local-dev.json`: Read-write workspace access for day-to-day development. MCP: GitHub (repo read/write), Context7 docs, Sonatype dependency audit. Copilot tools: workspace search, run command, test runner. Security: read-write; keep network constrained and tokens least-privilege.
- `toolset.review-only.json`: Read-only review posture. MCP: GitHub (read), Context7 docs, Elastic search (read-only). Copilot tools: workspace search and diagnostics; no run-command. Security: read-only.

## Safety note

MCP servers can be risky if over-privileged. Always verify provenance, audit server code, and scope permissions appropriately before enabling. Use read-only where possible and prefer local stdio transports over remote endpoints for sensitive work.
