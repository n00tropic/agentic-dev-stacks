# Linters and formatters

Configuration for linters, formatters, and test runners.

## Vale

- `vale.ini.sample` is the reference config. Copy it into your docs project and adjust paths and alert levels as needed.
- After copying, run `vale sync` (from the workspace root) to hydrate `styles/Packages` with the pinned packages referenced in the config.
- Keep the resulting `.vale.ini` plus `styles/` tree under version control so every contributor + CI uses the exact same rule versions.
