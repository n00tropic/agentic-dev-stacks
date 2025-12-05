# Profile: Infra & DevOps (Docker/K8s/Terraform)

Slug: `infra-devops`  
Pack: `30-infra-devops-platform`

## Intent

Docker, Kubernetes, Terraform, CI/CD, YAML-heavy workflows.

## Canonical files

- Extensions list: `extensions.infra-devops.txt`
- Settings override: `settings.infra-devops.json`

## Usage

- Install extensions via VS Code CLI, for example:

  ```bash
  code --install-extension publisher.extension --profile "Infra & DevOps (Docker/K8s/Terraform)"
  ```

- Merge `settings.infra-devops.json` into your user `settings.json` using the root-level merge scripts:
  - macOS/Linux: `scripts/macos/merge-settings.sh path/to/settings.infra-devops.json`
  - Windows: `scripts/windows/Merge-Settings.ps1 -OverridePath path\to\settings.infra-devops.json`
