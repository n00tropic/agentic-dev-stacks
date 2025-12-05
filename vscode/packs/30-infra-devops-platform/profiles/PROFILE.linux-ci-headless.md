# Profile: Linux – CI/Headless

Slug: `linux-ci-headless`  
Pack: `30-infra-devops-platform`

## Intent

Minimal profile mirroring a typical Linux CI/headless agent environment.

## Canonical files

- Extensions list: `extensions.linux-ci-headless.txt`
- Settings override: `settings.linux-ci-headless.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Linux – CI/Headless"
  ```

- Merge `settings.linux-ci-headless.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.linux-ci-headless.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.linux-ci-headless.json`
