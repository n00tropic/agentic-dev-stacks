# Scenario: refactor-surgeon-small-refactor

Agent: Refactor Surgeon (refactor-surgeon)
Description: Small refactor of an existing function to improve readability without behaviour change.

## Inputs

- Please refactor the data fetching helper to be more readable. Keep behaviour the same.
- Limit changes to the existing file unless strictly necessary.

## Must Do

- [ ] Use workspace search or navigation to locate the function before editing.
- [ ] Keep diff small and focused; avoid API changes.
- [ ] Preserve behaviour and existing tests.

## Must Not Do

- [ ] Must not introduce new features or endpoints.
- [ ] Must not modify more than a couple of files without asking.

## Success Criteria

- [ ] Refactor improves clarity/structure without changing behaviour.
- [ ] Diff stays small and reviewable.
- [ ] No new breaking changes; tests still pass in principle.

## Evaluator Notes

- [ ] Notes:
