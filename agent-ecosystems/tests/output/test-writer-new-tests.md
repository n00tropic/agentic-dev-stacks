# Scenario: test-writer-new-tests

Agent: Test Writer (test-writer)
Description: Add new unit tests for an existing module without altering implementation logic.

## Inputs

- Add unit tests covering edge cases for the user serializer.
- Do not change the serializer implementation; focus on tests only.

## Must Do

- [ ] Locate existing tests or create new ones alongside the module.
- [ ] Add tests for happy path and at least one edge case.
- [ ] Keep production code untouched unless a tiny seam is absolutely required.

## Must Not Do

- [ ] Must not refactor or rewrite implementation logic.
- [ ] Must not add new dependencies without approval.

## Success Criteria

- [ ] New tests run under the existing test runner.
- [ ] Coverage improves around the serializer’s edge cases.
- [ ] No production code changes beyond minimal seams (if any).

## Evaluator Notes

- [ ] Notes:
