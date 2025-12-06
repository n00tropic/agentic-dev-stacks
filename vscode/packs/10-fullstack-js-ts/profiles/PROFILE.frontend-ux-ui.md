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

## Workflow tips

- Biome runs formatting + linting for JS/TS/React files; run it locally when Storybook/Nx/Turbo repos enforce CI parity:

  ```bash
  pnpm biome check apps/ui
  ```

- Prettier only triggers when a repo ships its own config, so you can mix component libraries without unexpected defaults.
- Storybook + Vitest: use the Storybook VS Code extension for snippets + controls, while Vitest Explorer and Jest Runner let you pin targeted suites during component work.
- CSS/Design systems: Tailwind IntelliSense + Stylelint keep tokens consistent; Auto Rename Tag avoids JSX/HTML drift.
- API collaboration: Thunder Client + REST Client ship by default so you can mirror Figma handoff flows with mocked APIs; export collections into repo `/docs/api/` when possible.
- Remote collaboration: Live Share and Remote Repositories let you pair on design reviews or run demos without cloning, remember to close sessions once done.
- MCP servers: keep Sonatype + Context7 always-on, but default MongoDB/Elastic servers to read-only credentials when pointing at shared staging data.
