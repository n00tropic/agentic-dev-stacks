# MCP Security Notes

Expected MCP servers in exemplar toolsets:

- `github-mcp`: GitHub access. Use read-only tokens for review-only flows; use narrowly scoped repo write tokens for local-dev when needed. Avoid org-wide scopes.
- `context7-mcp`: Documentation fetcher. Configure with Context7 token via env var; no secrets in git.
- `sonatype-mcp`: Dependency auditing. Provide credentials via env vars; prefer audit/read-only roles.
- `elastic-mcp`: Elasticsearch access. Use read-only API keys; scope indices to what agents need.

Guidance

- Store credentials in environment variables or external secret managers (e.g. `GITHUB_MCP_TOKEN`, `CONTEXT7_TOKEN`, `SONATYPE_TOKEN`, `ELASTIC_API_KEY`). Never commit them.
- Prefer stdio/local transports where possible; treat remote endpoints as privacy-sensitive.
- Apply least privilege: review-only toolsets should not get write scopes; local-dev should keep write scopes limited to the current repo.
