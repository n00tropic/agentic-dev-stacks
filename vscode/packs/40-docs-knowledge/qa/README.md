# QA

Quality-assurance configuration for this pack.

## Vale setup

- Copy `linters/vale.ini.sample` into your docs workspace (for example `docs/.vale.ini`).
- Commit a `styles/` directory alongside the config that contains:
  - `styles/Packages/` (populated via `vale sync` to pin Microsoft/Google/proselint/alex packs).
  - `styles/Vocab/project/{accept,reject}.txt` for project-specific terminology.
- Run `vale sync` after cloning to restore the pinned packages, then `vale docs/**/*.md` or let Trunk invoke Vale for CI.
