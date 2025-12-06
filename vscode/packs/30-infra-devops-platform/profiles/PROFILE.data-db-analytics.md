# Profile: Data / DB & Analytics

Slug: `data-db-analytics`  
Pack: `30-infra-devops-platform`

## Intent

SQL, schema design, migrations, and analytics scripting.

## Canonical files

- Extensions list: `extensions.data-db-analytics.txt`
- Settings override: `settings.data-db-analytics.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Data / DB & Analytics"
  ```

- Merge `settings.data-db-analytics.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.data-db-analytics.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.data-db-analytics.json`

## Workflow tips

- SQL Tools: ship drivers for Postgres, MySQL, SQLite, and MSSQL. Store database connections via `~/.sqltools/connections.json` and prefer read-only roles outside local dev.
- Python analytics: Ruff + Black run automatically; add `notebooks/requirements.txt` to keep lint/test parity with CI. Use Data Wrangler + Jupyter Keymap to flip between notebook + script workflows quickly.
- Data preview + docs: Random Fractals Data Preview and GitHub Issue Notebooks make it easy to annotate datasets before codifying them in dbt or pipelines.
- Collaboration: Remote Repositories + Dev Containers share identical workspace configs; Live Share helps pair on investigations without dumping credentials.
- MCP servers: Sonatype/Context7 baseline, Postgres + Elasticsearch for read-only querying. Keep DSNs in `.env.local` and remind reviewers to disable servers when handling regulated data.
