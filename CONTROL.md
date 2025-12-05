# VS Code Profile Control Plane

VS Code enforces a hard limit of 20 profiles per installation. This file tracks
how we budget those profiles across domains and platforms.

## Summary

- Total allowed profiles per installation: **20**
- Profiles defined in this scaffold: **16**
- Free slots remaining for future specialisations: **4**

## Canonical profiles

| #   | Pack                       | Slug                  | Human name                              | Cross-cutting | Language/domain        | Platform-specific |
| --- | -------------------------- | --------------------- | --------------------------------------- | ------------- | ---------------------- | ----------------- |
| 1   | 00-core-base               | core-base-dev         | Core / Base Dev                         | Yes           | General                | No                |
| 2   | 00-core-base               | qa-static-analysis    | QA / Static Analysis                    | Yes           | General / QA           | No                |
| 3   | 40-docs-knowledge          | docs-librarian        | Docs & Librarian                        | Yes           | Docs / Knowledge       | No                |
| 4   | 00-core-base               | gitops-code-review    | GitOps & Code Review                    | Yes           | GitOps / Review        | No                |
| 5   | 50-experimental-playground | experimental-preview  | Experimental / Preview                  | Yes           | Experimental           | No                |
| 6   | 10-fullstack-js-ts         | fullstack-js-ts       | Fullstack JS/TS – Web & API             | No            | JS/TS fullstack        | No                |
| 7   | 10-fullstack-js-ts         | frontend-ux-ui        | Frontend UX/UI – React / Storybook / DX | No            | JS/TS frontend         | No                |
| 8   | 10-fullstack-js-ts         | node-backend-services | Node / Backend Services – TS/Node       | No            | JS/TS backend          | No                |
| 9   | 20-python-data-ml          | python-services-clis  | Python Services & CLIs                  | No            | Python services / CLIs | No                |
| 10  | 20-python-data-ml          | python-data-ml        | Python Data & ML                        | No            | Python data / ML       | No                |
| 11  | 30-infra-devops-platform   | infra-devops          | Infra & DevOps (Docker/K8s/Terraform)   | No            | Infra / DevOps         | No                |
| 12  | 30-infra-devops-platform   | data-db-analytics     | Data / DB & Analytics                   | No            | Databases / Analytics  | No                |
| 13  | 10-fullstack-js-ts         | desktop-gui-cross     | Desktop & GUI – Swift / TS / Python     | No            | Desktop / GUI          | No                |
| 14  | 00-core-base               | macos-apple-platforms | macOS – Apple Platforms & Tooling       | No            | Multi                  | Yes (macOS)       |
| 15  | 00-core-base               | windows-polyglot-wsl  | Windows – Polyglot + WSL                | No            | Multi                  | Yes (Windows)     |
| 16  | 30-infra-devops-platform   | linux-ci-headless     | Linux – CI/Headless                     | No            | Multi                  | Yes (Linux)       |

## Budget by platform (recommended)

On each platform, start with these:

- **macOS**: core-base-dev, qa-static-analysis, docs-librarian, fullstack-js-ts,
  frontend-ux-ui, python-services-clis, macos-apple-platforms
- **Windows**: core-base-dev, qa-static-analysis, docs-librarian, fullstack-js-ts,
  node-backend-services, windows-polyglot-wsl
- **Linux (desktop)**: core-base-dev, qa-static-analysis, infra-devops, data-db-analytics,
  linux-ci-headless
- **Linux (CI/headless)**: linux-ci-headless only, or a minimal subset

You still have free slots on each installation for future specialisations (e.g. Rust,
security/SAST, AI-agent-dev). Keep this file updated if you add or remove profiles.
