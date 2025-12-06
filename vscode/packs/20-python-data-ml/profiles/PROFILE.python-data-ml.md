# Profile: Python Data & ML

Slug: `python-data-ml`  
Pack: `20-python-data-ml`

## Intent

Notebook-heavy data exploration and ML experimentation.

## Canonical files

- Extensions list: `extensions.python-data-ml.txt`
- Settings override: `settings.python-data-ml.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Python Data & ML"
  ```

- Merge `settings.python-data-ml.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.python-data-ml.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.python-data-ml.json`

## Workflow tips

- Ruff + Black run on save with explicit code actions. Keep CI parity by pinning the same versions in `requirements-dev.txt` and your `pyproject.toml`.
- Jupyter defaults: Notebook renderers, theme-aware Matplotlib, and Data Wrangler are included. For reproducibility, prefer `.ipynb + .py` pairs via `jupytext` and commit `.ipynb_checkpoints` to `.gitignore`.
- Remote runtimes: Dev Containers + Remote Repositories let you bring GPU or cloud kernels closer to notebooks. Update `workspace-templates/python-data-ml/` when you add CUDA or RAPIDS images.
- Data preview: Random Fractals Data Preview + GitHub Issue Notebooks help you inspect CSV/Parquet files inline before promoting them to pipelines.
- Testing: Use `pytest -m "not slow"` for quick iterations and reserve heavy training for scheduled workflows. Wire `python.testing.pytestArgs` in project settings when needed.
- MCP servers: Sonatype + Context7 remain defaults. Postgres + Elasticsearch servers must stay read-only; drop per-env DSNs into `.env.example` and load via `direnv` or VS Code secret storage.
