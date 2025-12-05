# Profile: Data / DB & Analytics

Slug: `data-db-analytics`  
Pack: `30-infra-devops-platform`

## Intent

SQL, schema design, migrations, and analytics scripting.

## Canonical files

- Extensions list: `extensions.data-db-analytics.txt`
- Settings override: `settings.data-db-analytics.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Data / DB & Analytics"
  ```

- Merge `settings.data-db-analytics.json` into your user `settings.json` using the root-level merge scripts:

  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.data-db-analytics.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.data-db-analytics.json`
