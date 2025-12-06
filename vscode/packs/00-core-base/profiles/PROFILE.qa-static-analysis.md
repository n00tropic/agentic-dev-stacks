# Profile: QA / Static Analysis

Slug: `qa-static-analysis`  
Pack: `00-core-base`

## Intent

Profile focused on linting, formatting, tests, and coverage.

## Canonical files

- Extensions list: `extensions.qa-static-analysis.txt`
- Settings override: `settings.qa-static-analysis.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "QA / Static Analysis"
  ```

- Merge `settings.qa-static-analysis.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.qa-static-analysis.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.qa-static-analysis.json`

## QA workflow

- Use Biome for JS/TS formatting and linting, and Black for Python (both wired via the profile settings). Run the CLI equivalents before commits:

  ```bash
  npx biome check src
  black . && ruff check .
  ```

- Keep Trunk as the umbrella orchestrator:

  ```bash
  trunk install
  trunk check
  ```

- Leverage SonarLint for code-level insights and Context7/Sonatype MCP servers for doc + dependency validation during reviews.
