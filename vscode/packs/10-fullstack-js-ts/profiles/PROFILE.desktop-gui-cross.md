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

## Workflow tips

- JS/TS frontends: Biome handles formatting + linting. When wiring Tauri or Electron UI code, enable HMR via `pnpm tauri dev -- --watch` and attach JS Debug Nightly to `localhost:9222`.
- Swift targets: Swift Development Environment + SwiftLint ship together; run linting outside VS Code with `swiftlint --strict`. Use LLDB configs produced by the extension pack for native debugging.
- Python UIs: Ruff + Black default formatters keep CLI tooling consistent. Add `.python-version` files (pyenv) so Pylance picks the correct interpreter.
- API + device testing: Thunder Client + REST Client help script bridge endpoints, while Playwright integration lets you preview multi-window UI flows.
- Remote pairing: Dev Containers, Remote SSH, Remote Repositories, and Live Share all come preinstalled; keep container definitions in `workspace-templates/desktop-gui-cross/` when sharing with the team.
- MCP servers: Sonatype + Context7 baseline, MongoDB for data inspection. Use separate credentials per platform (Swift vs JS) and keep them read-only when pointing at staging data.
