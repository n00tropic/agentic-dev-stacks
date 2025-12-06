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

## Workflow tips

- Biome is the default formatter for JS/TS/React. Keep it honest with the CLI before pushes:

  ```bash
  pnpm biome check src
  ```

  Prettier only fires when a project config exists (`prettier.requireConfig = true`).

- Use Trunk to orchestrate monorepo checks (Nx/Turbo + lint/test) so CI and editors stay in sync:

  ```bash
  trunk install
  trunk check
  ```

- Tests: `Vitest Explorer` covers component/unit specs while `Jest Runner` handles legacy suites; pin run configs so React/Vitest projects stay fast.
- API work: `Thunder Client` ships with the profile for REST flows alongside `Humao REST Client` in project repos; sync saved collections into source control when possible.
- Collaboration: Live Share + Remote Repositories let you pair or review without recloning; exit sessions once finished to keep access scoped.
- MCP usage: Sonatype + Context7 stay baseline. MongoDB and Elasticsearch servers should use read-only creds unless you explicitly enable writes for dev sandboxes.
