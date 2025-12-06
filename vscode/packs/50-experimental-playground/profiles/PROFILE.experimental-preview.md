# Profile: Experimental / Preview

Slug: `experimental-preview`  
Pack: `50-experimental-playground`

## Intent

Try new or heavy extensions and AI agents here, isolated from production profiles.

## Canonical files

- Extensions list: `extensions.experimental-preview.txt`
- Settings override: `settings.experimental-preview.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Experimental / Preview"
  ```

- Merge `settings.experimental-preview.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.experimental-preview.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.experimental-preview.json`

## Workflow tips

- AI copilots: Continue, Codeium, and Tabnine are installed here so you can trial different LLM backends without touching production profiles. Keep API keys/env vars outside this repo and prefer `.env.local` + VS Code Secret Storage.
- Remote-first experiments: Remote Repositories + Live Share let you try preview features or pair-programming flows without cloning locally; enable only when you trust the target host.
- MCP mix: Sonatype + Context7 remain baseline; Apify Web Search stays optional/consent-driven for privacy. Use this profile to verify new MCP servers before promoting them into other packs.
- Clean exits: disable or uninstall any preview extension once you finish testing so the profile remains snappy for the next experiment.
