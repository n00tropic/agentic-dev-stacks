# Python Data & Analytics Prompt Pack

Persona: Data/ML/analytics engineers working with notebooks, ETL, and tests.

## Explore data (use: data-explorer)

- "Summarise what this notebook does and data it touches."
- "List validation checks we should run on this dataset."
- "Map inputs/outputs for this ETL script; suggest sanity checks."

## Refactor pipelines (use: pipeline-refactorer)

- "Refactor pipelines/daily_ingest.py for readability; preserve outputs."
- "Improve error handling in this job without changing contracts."
- "Suggest minimal tests to cover this pipeline."

## Docs (use: doc-surgeon)

- "Update data README with setup steps and validation guidance."
- "Add notes on data lineage for this pipeline."

Preconditions: keep outputs/schemas unchanged; avoid new deps without approval; read-first posture on data.
