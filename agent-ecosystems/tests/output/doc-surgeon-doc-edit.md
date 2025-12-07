# Scenario: doc-surgeon-doc-edit

Agent: Doc Surgeon (doc-surgeon)
Description: Update documentation to clarify setup steps and link to related ADRs without touching code.

## Inputs

- Improve the setup section to mention the devcontainer and profile export.
- Add links to any ADRs related to tooling or MCP usage.

## Must Do

- [ ] Edit only documentation files.
- [ ] Keep style/tone aligned with existing docs.
- [ ] Add cross-links where they aid discoverability.

## Must Not Do

- [ ] Must not modify source code or configs.
- [ ] Must not add speculative behaviour changes.

## Success Criteria

- [ ] Docs clearly describe setup steps (devcontainer, profile export).
- [ ] Relevant ADRs or docs are linked.
- [ ] No code changes.

## Evaluator Notes

- [ ] Notes:
