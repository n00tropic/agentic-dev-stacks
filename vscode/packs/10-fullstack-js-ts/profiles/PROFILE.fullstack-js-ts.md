# Profile: Fullstack JS/TS – Web & API

Slug: `fullstack-js-ts`  
Pack: `10-fullstack-js-ts`

## Intent

React/Next.js, Node APIs, and monorepo tooling (pnpm/Nx/Turbo).

## Canonical files

- Extensions list: `extensions.fullstack-js-ts.txt`
- Settings override: `settings.fullstack-js-ts.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Fullstack JS/TS – Web & API"
  ```

- Merge `settings.fullstack-js-ts.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.fullstack-js-ts.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.fullstack-js-ts.json`
