# Profile: Python Services & CLIs

Slug: `python-services-clis`  
Pack: `20-python-data-ml`

## Intent

APIs, services, and CLI utilities in Python (non-notebook first).

## Canonical files

- Extensions list: `extensions.python-services-clis.txt`
- Settings override: `settings.python-services-clis.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Python Services & CLIs"
  ```

- Merge `settings.python-services-clis.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.python-services-clis.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.python-services-clis.json`

## Workflow tips

- Use Docker + Ansible extensions for service deployment smoke tests and automation experiments without touching your base profile.
- Ruff + Black + isort are pre-installed; run the trio via Trunk or directly before committing:

  ```bash
  trunk check
  black . && ruff check . && isort .
  ```

- With type checking set to `strict`, keep `pyrightconfig.json` (or `pyproject.toml`/`mypy.ini`) aligned so diagnostics match VS Code output.
- Point the Postgres MCP server at read-only replicas to inspect schema/state from within VS Code while developing CLI flows.
