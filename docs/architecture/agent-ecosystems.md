Product vision

We are not just shipping devcontainers and VS Code profiles.
We are shipping micro-ecosystems: opinionated workspace stacks that come with:
• A curated toolset layer (MCP servers + Copilot tools).
• A small retinue of custom agents (Copilot custom agents) with clear roles.
• A reproducible workspace chassis (devcontainer + VS Code profile).
• A versioned bundle/dist that users install with a single command per OS.

The developer experience should be:

“Install one bundle. Open VS Code. You now have a tailored workspace plus a handful of specialised agents already wired to the right tools. You do not configure anything; you just start using them.”

We build on:
• VS Code devcontainers for reproducible environments. ￼
• VS Code profiles for settings/extension export/import (.code-profile, gist URLs). ￼
• Prompt files + repository custom instructions for reusable workflows and repo-specific guidance. ￼
• Custom agents in VS Code for specialised AI behaviours with tools and handoffs. ￼
• Model Context Protocol (MCP) for tool and data access via standardised servers and tools. ￼

Core concepts 1. Agent Blueprints
• Machine-readable + human-readable spec for a custom agent:
• id, name, role, scope, non-goals.
• Bound toolsets (see below), allowed MCP servers/tools.
• Interaction style (tone, verbosity, when to ask for clarification).
• Safety constraints (file scopes, max diff size, destructive ops).
• Links to prompt files / instructions. 2. Toolsets
• Named bundles of:
• MCP servers (e.g. filesystem, git, github, http, jira, internal servers). ￼
• Copilot tools (run commands, search workspace, test runner). ￼
• Each toolset has:
• An ID (toolset.local-dev, toolset.review-only, toolset.ops-extended).
• A security profile (read-only vs read/write, scopes, approval model).
• Explicitly documented risk notes (MCP security, prompt injection, credential scope). ￼ 3. Workspace Stacks
• A stack is a devcontainer + VS Code profile + associated agents/toolsets:
• devcontainer.json + Dockerfile = toolchain + OS-level deps. ￼
• VS Code profile spec = extensions, settings, Copilot enablement. ￼
• A list of default agents and toolsets that are “first-class citizens” in this stack (e.g. fullstack-js-ts, python-data, infra-ops). 4. Bundles / Dists
• A bundle is a versioned, OS-specific zip that contains:
• The devcontainer config (or instructions if remote).
• The exported .code-profile for the stack. ￼
• Agent blueprints.
• Toolset definitions + MCP config.
• Install scripts per OS (macOS, Windows, Linux).
• One command per OS should install the bundle and register the profile and agents.

Hero use-cases
• Full-fat AI dev stack for JS/TS:
• Agents: Planner, Refactorer, Test Writer, Doc Surgeon.
• Toolsets: local dev + read-only GitHub + issue tracker.
• Infra / Ops stack:
• Agents: Terraform Reviewer, K8s Diagnostics, Incident Scribe.
• Toolsets: k8s MCP server, logs/metrics, CI systems (read-only by default).

Quality bar
• All stacks:
• Build cleanly in CI (devcontainer + bundle generation).
• Pass agent evaluations on scenario prompts.
• Have human-readable docs that lead with agents, not infrastructure.
