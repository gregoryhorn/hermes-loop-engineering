# Setting up loops in Hermes

## Prerequisites

- Hermes Agent installed and configured
- `cronjob` / Hermes cron available
- the required toolsets enabled for the loop, usually some of:
  - `file`
  - `terminal`
  - `web`
  - `session_search`
  - `github` or relevant MCP tools

Check your Hermes setup:

```bash
hermes doctor
hermes tools list
hermes cron list
```

## Install the skill

```bash
./scripts/install-hermes-loop-skill.sh
```

This copies `skill/SKILL.md` into:

```text
$HERMES_HOME/skills/loop-engineering/SKILL.md
```

If `HERMES_HOME` is unset, it defaults to `~/.hermes`.

## Create a state file

```bash
mkdir -p ~/.hermes/state/loops
cp templates/state.example.json ~/.hermes/state/loops/example-loop.json
```

Edit the file before running the loop.

## Create a loop from Hermes chat

Start with one of the example prompts:

```text
Use the loop-engineering skill. Create a new L1 report-only Hermes cron loop from examples/daily-project-triage.prompt.md. Use ~/.hermes/state/loops/example-loop.json as durable state. Do not mutate code or external systems.
```

## Create a loop manually

Hermes cron prompts should be self-contained because future runs start without your current chat context.

Use:

```bash
hermes cron create "0 9 * * 1-5"
```

Then paste an example prompt and customize:

- loop name
- schedule
- state path
- watched scope
- allowed tools
- forbidden actions
- delivery behavior

## Recommended delivery rule

A good recurring loop is quiet when nothing changed.

Use this rule in prompts:

```text
If there are no state changes, blockers, risky decisions, or completed deliverables, update the state file and produce no user-facing alert if the platform supports quiet runs. If quiet runs are not supported, return a one-line "No actionable change" summary.
```

## Updating a loop

When a loop is wrong, update the loop prompt and the state schema before changing cadence or permissions.

When a loop discovers a reusable procedure, save it as a Hermes skill rather than burying it in chat history.
