# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately using GitHub Security Advisories (Security tab → “Report a vulnerability”) so maintainers can triage and patch before public disclosure. Avoid filing public issues for security reports.

## Scope and expectations

- This repository ships devcontainers, VS Code profiles, MCP manifests, and agent configurations. These are configuration assets, not production services.
- Do not add secrets to the repository. Use environment variables, GitHub Actions secrets, or local secret stores when configuring MCP servers or agents.
- MCP servers should be enabled with least-privilege credentials (read-only by default where possible) and reviewed before use. Placeholders like `<TO_FILL>` must be replaced locally, not committed.

If you discover insecure defaults or unsafe MCP/server guidance in this project, please report it via the same private channel.
