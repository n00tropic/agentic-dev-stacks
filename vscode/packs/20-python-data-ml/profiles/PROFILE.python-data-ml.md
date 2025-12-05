# Profile: Python Data & ML

Slug: `python-data-ml`  
Pack: `20-python-data-ml`

## Intent

Notebook-heavy data exploration and ML experimentation.

## Canonical files

- Extensions list: `extensions.python-data-ml.txt`
- Settings override: `settings.python-data-ml.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Python Data & ML"
  ```

- Merge `settings.python-data-ml.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.python-data-ml.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.python-data-ml.json`
