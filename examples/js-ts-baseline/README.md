# JS/TS baseline sample

Tiny JavaScript sample to try inside the devcontainer/Codespaces environment. It uses the built-in Node test runner.

## Run

```bash
cd examples/js-ts-baseline
npm install
npm test
```

There is an intentional off-by-one bug in `src/sum.js`. Fix it and re-run `npm test`, then re-run `bash scripts/validate-all.sh --fast` from the repository root to mirror CI.

## Notes

- No external dependencies are required.
- This sample is optional and not part of `scripts/validate-all.sh`.
