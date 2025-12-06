#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
npx -y -p @antora/cli@3.1.14 -p @antora/site-generator@3.1.14 antora antora-playbook.yml
