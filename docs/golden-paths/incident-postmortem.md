# Golden Path: Incident Review and Postmortem

Persona: Infra/SRE engineers using the `infra-ops-sre` stack.

Prerequisites

- Run the stack installer for your OS (e.g. `./scripts/install/infra-ops-sre-macos.sh`).
- Open the workspace: `code vscode/exports/workspaces/infra-ops-sre/infra-ops-sre.code-workspace --profile "Infra Ops / SRE"`.
- Optional: import the vetted profile export at `vscode/profiles-dist/infra-ops-sre.code-profile` if you have generated one via **Export Profile…**.
- Gather artefacts: incident notes, logs, timeline, relevant diffs.

Flow (15–20 minutes)

1. Set posture: read-only on cloud/cluster MCP servers; do not run apply/deploy actions.
2. Open Copilot Chat (or your agent runner) and select the `infra-reviewer` agent.
   - Prompt: "Review these infra changes/logs for contributing factors to incident <id>. Call out risks and suspected root causes." Attach log snippets or paths.
3. If Kubernetes context is relevant, use `kubernetes` MCP (read-only verbs) to list resources/events:
   - Example prompt: "Using kubernetes MCP, list events for namespace <ns> around <timestamp>; do not mutate resources."
4. For logs/search, use `elasticsearch` MCP with tight queries:
   - Prompt: "Query Elasticsearch index <idx> for error rates between <t1> and <t2>; return top 5 messages."
5. Switch to the `incident-scribe` agent.
   - Prompt: "Draft an incident summary with timeline, impact, detected by, and follow-up actions based on these notes and findings." Provide reviewer output and log snippets.
6. Review the draft; edit for tone and accuracy. Add follow-ups with owners and due dates.
7. Optional automation check: run the scenario harness for this circuit:
   ```bash
   python3 agent-ecosystems/scripts/run-agent-scenarios.py --circuit incident-review-and-postmortem --stack infra-ops-sre
   ```

MCP servers (respect manifest flags)

- `github` (VCS): read issues/PRs for context; avoid mutating actions unless narrowly scoped.
- `elasticsearch` (logs/search): use read-only queries.
- `kubernetes` (cloud): keep to get/list/watch; ensure kubeconfig uses least-privilege.
- `sonatype-deps` and `context7-docs`: dependency/docs lookups; no secrets.
- `aws` (optional): only if explicitly enabled with read-only IAM; treat as opt-in per manifest.

Expected outcome

- Contributing factors identified and documented.
- A neutral postmortem draft with timeline and concrete follow-ups.
- No unintended writes to infra; MCP usage remains least-privilege and opt-in for cloud access.
