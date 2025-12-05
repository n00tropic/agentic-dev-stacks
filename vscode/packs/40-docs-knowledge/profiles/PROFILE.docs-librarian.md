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
