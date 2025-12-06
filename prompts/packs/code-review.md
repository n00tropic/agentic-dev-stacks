# Prompt Pack: Code Review & Security

- Goal: find correctness, security, and operability risks before style nits.
- Checklist:
  - Inputs validated? Defaults safe? Errors logged without secrets?
  - AuthZ/AuthN enforced? Tokens redacted? Secrets never logged or stored.
  - Dependency changes reviewed via Sonatype MCP; note CVEs/license risk.
  - Infra/CI changes: least-privilege, idempotent, rollback plan documented.
- Review style: cite files/lines, severity first, offer minimal fix sketch.
- Tests: ask for failing test reproducing the issue before approving.
- Performance: mention big-O or resource hotspots if obvious.
- Docs: request doc updates for behaviour or config changes.
