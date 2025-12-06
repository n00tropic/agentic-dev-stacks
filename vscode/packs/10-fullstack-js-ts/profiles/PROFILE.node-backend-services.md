# Profile: Node / Backend Services – TS/Node

Slug: `node-backend-services`  
Pack: `10-fullstack-js-ts`

## Intent

Backend services, APIs, workers, and CLIs built with TS/Node.

## Canonical files

- Extensions list: `extensions.node-backend-services.txt`
- Settings override: `settings.node-backend-services.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Node / Backend Services – TS/Node"
  ```

- Merge `settings.node-backend-services.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.node-backend-services.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.node-backend-services.json`

## Workflow tips

- JS/TS formatting + linting runs via Biome (editors) and Trunk (CLI). Keep CI parity with:

  ```bash
  trunk install
  trunk check
  ```

- Testing: Vitest Explorer + Jest Runner cover mixed monorepos. Wire `pnpm test --watch` scripts into VS Code Test Explorer for quick iterates.
- API development: Thunder Client + REST Client let you capture request/response pairs in `/docs/api/`. Treat `.thunder` collections as source-controlled fixtures.
- Debugging: JS Debug Nightly plus Docker extension support Node attach in containers. Add `launch.json` entries referencing the `node` attach template.
- Remote/Pairing: Dev Containers, Remote Repositories, and Live Share ship by default; close sessions when done to avoid lingering credentials.
- MCP usage: Sonatype/Context7 are baseline. MongoDB + Elasticsearch servers must run with read-only DSNs for staging data unless you explicitly opt into a writable sandbox.
