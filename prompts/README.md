# Prompt Packs

Reusable, copy-pasteable prompts for Copilot Chat and other sub-agents. Keep them lightweight, profile-aware, and vendor-neutral.

## How to use

- Copy a prompt pack into your workspace (e.g., `prompts/packs/*.md` → `exports/workspaces/<slug>/prompts/`).
- Add key snippets to `.copilot/custom-instructions.md` (or Copilot Chat “Custom instructions”) so they apply automatically.
- Stick to en-GB/Oxford English for wording to align with LTeX and spell-check defaults in our profiles.

## Packs

- `core-engineering.md` — coding conventions, safety rails, dependency policy.
- `code-review.md` — review & security triage flow.
- `docs-author.md` — docs/knowledge writing guidance.

Feel free to fork/extend per profile, but keep sources of truth under `prompts/packs/`.
