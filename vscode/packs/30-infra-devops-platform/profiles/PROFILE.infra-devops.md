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

## Workflow tips

- IaC defaults: Terraform, Bicep, and YAML all format via their native extensions. Keep `terraform fmt` + `terraform validate` in automation, and use Trunk to orchestrate multi-tool pipelines.
- Containers + clusters: Docker, Dev Containers, and Remote SSH let you debug k8s nodes locally; attach VS Code to pods via Kubernetes extension port-forwarding when needed.
- Multi-cloud: AWS Toolkit, Azure Terraform, and Pulumi extensions live side-by-side. Use workspace-specific settings to scope credentials (e.g., `AWS_PROFILE` or `az account set`).
- Helm/Ansible: Helm Intellisense + Red Hat Ansible provide schema validation. Add `helm lint` / `ansible-lint` tasks to `.vscode/tasks.json` for repeatable runs.
- Collaboration: Remote Repositories + Live Share help share repros quickly; tear sessions down after audits. For CI mirroring, open `vscode/exports/workspaces/infra-devops/` to share identical workspace configs.
- MCP guidance: Kubernetes server should stay read-only (get/list/watch). AWS server is optional/opt-in—highlight IAM scoping before enabling. Sonatype/Context7 remain baseline for dependency and docs insight.
