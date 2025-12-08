# Generated profile exports

This folder holds **generated** `.code-profile` files built from pack sources via `vscode/scripts/generate-code-profiles.py`. They are minimal, machine-agnostic profiles derived from the extensions and settings under `vscode/packs/**`.

- These do **not** replace the reviewed exports in `vscode/profiles-dist/`; they are an optional fast path for bulk profile creation.
- Regenerate anytime: `python3 vscode/scripts/generate-code-profiles.py` (optionally `--slug <profile>`).
- Files are safe to overwrite; they contain no global state or machine-specific paths.
