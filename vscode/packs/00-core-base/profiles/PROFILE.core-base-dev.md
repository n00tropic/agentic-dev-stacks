# Profile: Core / Base Dev

Slug: `core-base-dev`  
Pack: `00-core-base`

## Intent

Everyday coding profile: light but capable. Default for small edits and general work.

## Canonical files

- Extensions list: `extensions.core-base-dev.txt`
- Settings override: `settings.core-base-dev.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Core / Base Dev"
  ```

- Merge `settings.core-base-dev.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.core-base-dev.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.core-base-dev.json`
