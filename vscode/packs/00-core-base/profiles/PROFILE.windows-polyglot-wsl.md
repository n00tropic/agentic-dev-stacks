# Profile: Windows – Polyglot + WSL

Slug: `windows-polyglot-wsl`  
Pack: `00-core-base`

## Intent

Windows profile optimised for WSL, PowerShell, and polyglot development.

## Canonical files

- Extensions list: `extensions.windows-polyglot-wsl.txt`
- Settings override: `settings.windows-polyglot-wsl.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Windows – Polyglot + WSL"
  ```

- Merge `settings.windows-polyglot-wsl.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.windows-polyglot-wsl.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.windows-polyglot-wsl.json`
