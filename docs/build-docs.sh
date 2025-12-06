#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
npx @antora/site-generator@latest antora-playbook.yml
