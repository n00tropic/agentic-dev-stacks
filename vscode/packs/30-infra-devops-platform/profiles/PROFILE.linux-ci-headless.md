# Profile: Linux – CI/Headless

Slug: `linux-ci-headless`  
Pack: `30-infra-devops-platform`

## Intent

Minimal profile mirroring a typical Linux CI/headless agent environment.

## Canonical files

- Extensions list: `extensions.linux-ci-headless.txt`
- Settings override: `settings.linux-ci-headless.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Linux – CI/Headless"
  ```

- Merge `settings.linux-ci-headless.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.linux-ci-headless.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.linux-ci-headless.json`

## Workflow tips

- Purposefully light: only the shared baseline extensions, remote tooling, Tokyo Night, and Trunk ship with this profile so editor behavior mirrors CI/headless nodes closely.
- Remote-first: Remote SSH/Containers/Repositories let you attach to build agents or containers that have the same OS + toolchain as CI. Keep `~/.ssh/config` entries out of this repo.
- Debugging: Docker + Live Share are included strictly for troubleshooting; uninstall locally if you want a completely bare profile.
- MCP notes: Sonatype + Context7 help inspect dependencies/logs without installing extra tooling on target hosts. Kubernetes server is read-only—avoid enabling mutating verbs when mirroring CI.
