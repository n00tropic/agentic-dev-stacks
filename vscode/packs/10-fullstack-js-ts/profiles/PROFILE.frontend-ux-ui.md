# Profile: Frontend UX/UI – React / Storybook / DX

Slug: `frontend-ux-ui`  
Pack: `10-fullstack-js-ts`

## Intent

UI/UX-heavy work: Storybook, components, CSS/Tailwind, and DX helpers.

## Canonical files

- Extensions list: `extensions.frontend-ux-ui.txt`
- Settings override: `settings.frontend-ux-ui.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Frontend UX/UI – React / Storybook / DX"
  ```

- Merge `settings.frontend-ux-ui.json` into your user `settings.json` using the root-level merge scripts:

  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.frontend-ux-ui.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.frontend-ux-ui.json`
