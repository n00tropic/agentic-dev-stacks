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

## Workflow tips

- WSL + Remote: The profile installs Remote WSL/SSH/Containers + Remote Repositories so you can bounce between PowerShell, cmd, and Linux environments without switching VS Code windows.
- Formatting: Prettier handles JS/TS by default and PowerShell extension formats scripts—mirror the same tooling in CI for consistent output.
- Docker + JS testing: Docker Desktop + JS Debug Nightly/Playwright make it easy to test Edge/WebView apps that share code with WSL workloads.
- Collaboration: Live Share ships by default; stop sessions when finished. Keep `.vscode/settings.json` in repros to capture per-project overrides (shell, paths, etc.).
- MCP: Sonatype + Context7 remain defaults. If you point MongoDB/Elastic servers at shared infra from Windows, ensure WSL hosts share the same read-only credentials.
