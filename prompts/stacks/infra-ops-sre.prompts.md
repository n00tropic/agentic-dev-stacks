# Infra Ops / SRE Prompt Pack

Persona: Infra/platform/SRE engineers reviewing IaC and documenting incidents.

## Review infra (use: infra-reviewer)

- "Review this Terraform diff for security/reliability risks; suggest minimal fixes."
- "Check these K8s manifests for misconfigurations and least-privilege gaps."
- "Call out cost or blast-radius concerns in this infra change."

## Incident docs (use: incident-scribe)

- "Draft an incident summary from these notes with timeline and impact."
- "Extract follow-up actions from this outage log."
- "Create a neutral post-mortem draft based on provided bullet points."

## Docs (use: doc-surgeon)

- "Refresh runbook section for K8s diagnostics."
- "Document rollback steps found in notes."

Preconditions: read-only posture on infra; never run deploys; keep tone factual in incident docs.
