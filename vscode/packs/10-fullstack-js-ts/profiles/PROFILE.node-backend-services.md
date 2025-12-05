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
