#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SKILL_DIR="$HERMES_HOME/skills/loop-engineering"
PACK_DIR="$HERMES_HOME/loop-engineering"

mkdir -p "$SKILL_DIR" "$PACK_DIR/examples" "$PACK_DIR/templates" "$PACK_DIR/docs"
cp "$REPO_DIR/skill/SKILL.md" "$SKILL_DIR/SKILL.md"
cp -R "$REPO_DIR/examples/." "$PACK_DIR/examples/"
cp -R "$REPO_DIR/templates/." "$PACK_DIR/templates/"
cp -R "$REPO_DIR/docs/." "$PACK_DIR/docs/"

cat <<MSG
Installed Hermes Loop Engineering skill:
  $SKILL_DIR/SKILL.md

Copied starter pack:
  $PACK_DIR

Next steps:
  1. Start a fresh Hermes session or run /reload-skills if available.
  2. Ask Hermes: "Use the loop-engineering skill to create an L1 report-only loop from $PACK_DIR/examples/daily-project-triage.prompt.md"
  3. Keep the first loop report-only until you have reviewed its state and noise level.
MSG
