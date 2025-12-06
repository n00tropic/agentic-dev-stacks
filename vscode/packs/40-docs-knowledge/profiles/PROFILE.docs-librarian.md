# Profile: Docs & Librarian

Slug: `docs-librarian`  
Pack: `40-docs-knowledge`

## Intent

Technical writing, docs grooming, and knowledge curation profile.

## Canonical files

- Extensions list: `extensions.docs-librarian.txt`
- Settings override: `settings.docs-librarian.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Docs & Librarian"
  ```

- Merge `settings.docs-librarian.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.docs-librarian.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.docs-librarian.json`

## QA & style workflow

- Start by copying `qa/linters/vale.ini.sample` into your docs workspace (for example `docs/.vale.ini`) and commit it along with the `styles/` directory produced by `vale sync`.
- Keep Microsoft + Google Vale style packs synced:

  ```bash
  vale sync
  vale ls
  ```

- Point the VS Code Vale extension at your `.vale.ini` (fill the `vale.valeCLI.config` placeholder) and tune `MinAlertLevel` / `IgnoredScopes` inside the config rather than muting rules in-editor.
- Run Trunk + Vale before publishing:

  ```bash
  trunk check
  vale docs/**/*.md
  ```

- Use LTeX+ suggestions to iterate on structure and wording, then re-run Vale to confirm alignment with Microsoft/Google guidance.
