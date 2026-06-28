# Setting up loops in Hermes

This guide assumes Hermes Agent is already installed and configured. This repository is for shaping recurring Hermes work into safe, stateful loops.

## Prerequisites

- A working Hermes Agent setup
- Hermes cron or the `cronjob` tool available
- The toolsets your loop needs, usually some of:
  - `file`
  - `terminal`
  - `web`
  - `session_search`
  - GitHub or relevant MCP tools

Sanity check your local Hermes environment:

```bash
hermes doctor
hermes tools list
hermes cron list
```

## Install the Loop Engineering skill

From this repository:

```bash
./scripts/install-hermes-loop-skill.sh
```

This copies `skill/SKILL.md` into:

```text
$HERMES_HOME/skills/loop-engineering/SKILL.md
```

If `HERMES_HOME` is unset, it defaults to `~/.hermes`.

Start a fresh Hermes session or reload skills before using it.

## Create a state file

```bash
mkdir -p ~/.hermes/state/loops
cp templates/state.example.json ~/.hermes/state/loops/example-loop.json
```

Edit the copied file for your loop, then validate it:

```bash
python scripts/validate_loop_state.py ~/.hermes/state/loops/example-loop.json
```

The validator is permissive by design. Missing required core fields fail. Missing recommended operational fields warn.

## Create a loop from Hermes chat

Start with one of the example prompts:

```text
Use the loop-engineering skill. Create a new L1 report-only Hermes cron loop from examples/daily-project-triage.prompt.md.

Use ~/.hermes/state/loops/example-loop.json as durable state.
Do not mutate code or external systems.
Deliver only on state changes, blockers, risky decisions, or completed artifacts.
```

## Create a loop manually

Hermes cron prompts should be self-contained because future runs start without your current chat context.

Use your Hermes cron interface or CLI, then paste and customize an example prompt:

```bash
hermes cron create "0 9 * * 1-5"
```

Customize:

- loop name
- schedule
- state path
- watched scope
- allowed tools
- forbidden actions
- delivery behavior
- escalation rule
- kill switch

## First-run smoke check

Before trusting the schedule, run once and inspect the result.

A good first run should either:

- update the state file with a useful baseline
- report one clear blocker with evidence
- stay quiet or produce a one-line no-change summary

Check state syntax:

```bash
python -m json.tool ~/.hermes/state/loops/example-loop.json >/dev/null
```

## Recommended delivery rule

A good recurring loop is quiet when nothing changed.

Use this rule in prompts:

```text
If there are no state changes, blockers, risky decisions, or completed deliverables, update the state file and produce no user-facing alert if the platform supports quiet runs. If quiet runs are not supported, return a one-line "No actionable change" summary.
```

## Updating a loop

When a loop is wrong, update the loop prompt and the state schema before changing cadence or permissions.

When a loop discovers a reusable procedure, save it as a Hermes skill rather than burying it in chat history.
