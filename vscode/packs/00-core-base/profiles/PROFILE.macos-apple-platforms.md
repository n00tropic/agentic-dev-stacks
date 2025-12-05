# Profile: macOS – Apple Platforms & Tooling

Slug: `macos-apple-platforms`  
Pack: `00-core-base`

## Intent

macOS and Apple platforms profile, tuned for Swift/Xcode-adjacent workflows.

## Canonical files

- Extensions list: `extensions.macos-apple-platforms.txt`
- Settings override: `settings.macos-apple-platforms.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "macOS – Apple Platforms & Tooling"
  ```

- Merge `settings.macos-apple-platforms.json` into your user `settings.json` using the root-level merge scripts:

  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.macos-apple-platforms.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.macos-apple-platforms.json`
