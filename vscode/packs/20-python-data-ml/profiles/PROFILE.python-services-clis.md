# Profile: Python Services & CLIs

Slug: `python-services-clis`  
Pack: `20-python-data-ml`

## Intent

APIs, services, and CLI utilities in Python (non-notebook first).

## Canonical files

- Extensions list: `extensions.python-services-clis.txt`
- Settings override: `settings.python-services-clis.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Python Services & CLIs"
  ```

- Merge `settings.python-services-clis.json` into your user `settings.json` using the root-level merge scripts:

  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.python-services-clis.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.python-services-clis.json`
