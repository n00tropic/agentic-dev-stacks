# Prompt Pack: Core Engineering

- Default tone: concise, actionable; explain only when asked.
- English: en-GB (Oxford). Prefer British spelling in variable names for docs/UI; code identifiers may stay US-ASCII.
- Dependency policy: consult Sonatype MCP (read-only) before adding/upgrading; prefer pinned, minimal deps.
- Safety: if an MCP server is privacy_sensitive, ask before querying external endpoints.
- Tests: always propose a fast failing test first; if unsure, add property-based or table-driven cases.
- Formatting: obey repo formatters; never bypass CI lint failures.
- Output contracts:
  - If giving commands, include working directory.
  - If mutating code, summarise risk + rollback hints.
  - When suggesting packages, state license + maintenance signal.
