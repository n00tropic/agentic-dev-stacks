# Fullstack JS/TS Prompt Pack

Persona: Full-stack web/API engineers using the JS/TS stack.

## Refactor safely (use: refactor-surgeon)

- "Refactor this module to reduce complexity; keep behaviour unchanged."
- "Tidy this React component and extract helpers; no API changes."
- "Propose a small refactor plan before touching multiple files."

## Add tests (use: test-writer)

- "Add edge-case tests for the user serializer; keep implementation intact."
- "Improve tests for this hook/component; avoid production code changes."
- "Suggest minimal seams needed for better testability."

## Docs & review (use: doc-surgeon)

- "Tighten the setup section in README; align with current devcontainer."
- "Update ADR summary with latest decision and links."
- "Cross-link related docs to improve discoverability."

Preconditions: tests/framework already present; run commands only when necessary; keep diffs small.
