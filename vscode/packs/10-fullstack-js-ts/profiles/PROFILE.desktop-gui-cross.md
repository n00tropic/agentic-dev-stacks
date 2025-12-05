# Profile: Desktop & GUI – Swift / TS / Python

Slug: `desktop-gui-cross`  
Pack: `10-fullstack-js-ts`

## Intent

Cross-platform desktop and GUI app development (SwiftUI, Tauri/Electron, Python UIs).

## Canonical files

- Extensions list: `extensions.desktop-gui-cross.txt`
- Settings override: `settings.desktop-gui-cross.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Desktop & GUI – Swift / TS / Python"
  ```

- Merge `settings.desktop-gui-cross.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.desktop-gui-cross.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.desktop-gui-cross.json`
