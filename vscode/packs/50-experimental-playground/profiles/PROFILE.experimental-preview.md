# Profile: Experimental / Preview

Slug: `experimental-preview`  
Pack: `50-experimental-playground`

## Intent

Try new or heavy extensions and AI agents here, isolated from production profiles.

## Canonical files

- Extensions list: `extensions.experimental-preview.txt`
- Settings override: `settings.experimental-preview.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Experimental / Preview"
  ```

- Merge `settings.experimental-preview.json` into your user `settings.json` using the root-level merge scripts:

  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.experimental-preview.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.experimental-preview.json`
