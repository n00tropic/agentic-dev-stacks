# Profile: GitOps & Code Review

Slug: `gitops-code-review`  
Pack: `00-core-base`

## Intent

Code review, Git history, and GitOps operations with minimal language noise.

## Canonical files

- Extensions list: `extensions.gitops-code-review.txt`
- Settings override: `settings.gitops-code-review.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "GitOps & Code Review"
  ```

- Merge `settings.gitops-code-review.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.gitops-code-review.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.gitops-code-review.json`

## Workflow tips

- Use GitLens + Git Graph for timeline review, and the Git Extension Pack for quick access to stash/rebase/pick workflows.
- Keep Context7 MCP pointed at the docs relevant to the repo you are reviewing, so inline questions on APIs can be resolved without leaving VS Code.
- Run Sonatype MCP checks (or `trunk check` if the repo wires Sonatype via Trunk) before approving dependency bumps.
- Pair Trunk with built-in diff editors: stage hunks via GitLens, then run `trunk check` to confirm lint/tests before final approval.
