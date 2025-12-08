# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately using GitHub Security Advisories (Security tab → “Report a vulnerability”) so maintainers can triage and patch before public disclosure. Avoid filing public issues for security reports. We aim to acknowledge within 2 business days and provide status updates weekly until resolution.

## Scope and expectations

- This repository ships devcontainers, VS Code profiles, MCP manifests, and agent configurations. These are configuration assets and validation scripts, not production services.
- Secrets must not be committed. Use environment variables, GitHub Actions secrets, or local secret stores when configuring MCP servers or agents.
- Treat MCP/agent manifests as infrastructure-as-code: review diffs before enabling, prefer least-privilege/read-only servers, and fill placeholders (`<TO_FILL>`) locally.
- Prefer isolated environments (devcontainers/Codespaces) when running MCP servers; avoid pointing servers at sensitive production data.

For deeper MCP-specific guidance, see [docs/modules/ROOT/pages/mcp-security.adoc](docs/modules/ROOT/pages/mcp-security.adoc). If you discover insecure defaults or unsafe MCP/server guidance in this project, please report it via the private channel above.
