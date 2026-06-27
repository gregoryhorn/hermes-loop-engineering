# Hermes Loop Engineering

![Hermes Loop Engineering banner](assets/hermes-loop-engineering-banner.svg)

[![validate](https://github.com/gregoryhorn/hermes-loop-engineering/actions/workflows/validate.yml/badge.svg)](https://github.com/gregoryhorn/hermes-loop-engineering/actions/workflows/validate.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-22d3ee)
![Loop level](https://img.shields.io/badge/default-L1%20report--first-34d399)

**Keywords:** Hermes Agent automation, AI agent cron jobs, agentic workflows, loop engineering, scheduled AI agents, stateful AI workflows, LLMOps, MCP automation, prompt runbooks, safe AI automation.

**Hermes Loop Engineering** is a public, reusable starter kit for turning repeated Hermes Agent work into **safe, stateful, scheduled, verified AI-agent loops**.

Instead of manually prompting an agent every time, you design a small operating system around the work:

> **prompt/runbook → durable state → scheduler → verification → escalation gate**

This repository contains:

- an installable Hermes skill (`skill/SKILL.md`)
- public-safe loop templates
- example loop prompts for common use cases
- state schemas and checklists
- a small readiness checker
- visual diagrams and a GitHub social preview for explaining the system

It does **not** contain anyone's private loops, credentials, social accounts, personal schedules, or internal state.

## Why this exists

A recurring agent workflow becomes risky when it has no memory, no scope, no stop criteria, and no verification. Loop engineering fixes that by making every recurring workflow explicit:

- What is the loop allowed to inspect?
- What is it allowed to change, if anything?
- Where does state live outside the chat?
- What evidence proves success?
- When should it stop and ask a human?
- How do you pause or kill it?

## Visual model

![Hermes loop architecture diagram](assets/hermes-loop-architecture.svg)

## The Hermes mapping

| Loop concept | Hermes primitive |
|---|---|
| Schedule / automation | `hermes cron` / `/cron` / `cronjob` tool |
| Reusable operating knowledge | Hermes skills |
| Short maker/checker split | `delegate_task` |
| Long-running bounded jobs | `terminal(background=true, notify_on_complete=true)` |
| Durable state | JSON/Markdown state file, wiki page, or Kanban board |
| External tools | Hermes toolsets, MCP servers, browser/web/file/terminal tools |
| Human gate | final report, approval batch, issue, PR, or message |

## Quick start

### 1. Install Hermes Agent

Follow the official Hermes docs: <https://hermes-agent.nousresearch.com/docs>

At minimum you should have:

```bash
hermes doctor
hermes cron list
hermes skills list
```

### 2. Install this loop engineering skill

Clone the repo and run the installer:

```bash
git clone https://github.com/gregoryhorn/hermes-loop-engineering.git
cd hermes-loop-engineering
./scripts/install-hermes-loop-skill.sh
```

Then start a fresh Hermes session or run `/reload-skills` if available.

### 3. Create your first L1 report-only loop

Copy a template:

```bash
mkdir -p ~/.hermes/state/loops
cp templates/state.example.json ~/.hermes/state/loops/my-first-loop.json
cp templates/LOOP.example.md ./LOOP.md
```

Ask Hermes to create a cron job using one of the example prompts, or paste the prompt into `/cron`:

```text
Create a Hermes cron loop from examples/daily-project-triage.prompt.md.
Keep it L1 report-only. Use ~/.hermes/state/loops/my-first-loop.json as durable state.
Deliver only on state changes, blockers, or decisions.
```

### 4. Keep week one report-only

Do not start by letting the loop edit code, publish, merge, delete, or mutate infrastructure. First prove that it can inspect, summarize, update state, and escalate accurately.

## Readiness levels

| Level | Meaning | Minimum bar |
|---|---|---|
| **L0 Draft** | documented intent only | purpose, non-goals, scope, owner, no scheduler |
| **L1 Report** | scheduled/read-only reporting | durable state, scoped inspection, no mutation |
| **L2 Assisted** | narrow changes with verification | isolated worktree or narrow path scope, maker/checker, real command output |
| **L3 Unattended** | allowed to act without supervision | explicit allowlist, budget, attempt caps, kill switch, verifier, human gates |

Most loops should live at **L1** longer than your optimism wants.

## Example loop cases

Public-safe examples are in [`examples/`](examples/):

- [`daily-project-triage.prompt.md`](examples/daily-project-triage.prompt.md) — read-only scan of a project workspace
- [`pr-ci-babysitter.prompt.md`](examples/pr-ci-babysitter.prompt.md) — watch PR/CI state, classify failures, escalate
- [`knowledge-base-maintenance.prompt.md`](examples/knowledge-base-maintenance.prompt.md) — validate docs/wiki links and suggest fixes
- [`dependency-watch.prompt.md`](examples/dependency-watch.prompt.md) — watch outdated dependencies, propose safe updates
- [`content-pipeline-monitor.prompt.md`](examples/content-pipeline-monitor.prompt.md) — check local media/content artifacts without publishing
- [`service-health-watchdog.prompt.md`](examples/service-health-watchdog.prompt.md) — script-first state-change watchdog
- [`hermes-loop-engineering-rd.prompt.md`](examples/hermes-loop-engineering-rd.prompt.md) — improve this starter repo over time with validation and public-safety gates

These are intentionally generic. Replace paths, commands, schedules, and boundaries with your own.

## Core safety rules

1. **No state, no loop.** Every loop reads and writes a durable state file or board.
2. **Report-only first.** L1 before L2/L3 unless a human explicitly overrides.
3. **No heartbeat spam.** Notify on changes, blockers, risky decisions, or deliverables.
4. **Implementer does not grade itself.** Use a separate verifier for mutations.
5. **Cron trigger is not completion.** Completion requires evidence from tools or checks.
6. **No broad write scope.** Use narrow allowlists and explicit denylisted areas.
7. **Human-gate risky work.** Auth, secrets, payments, infra, publishing, deletion, and PII stay gated.

## Discoverability

This repository is optimized for people searching for **Hermes Agent automation**, **AI agent cron jobs**, **agentic workflows**, **loop engineering**, **stateful agent workflows**, **scheduled AI agents**, **safe AI automation**, **LLMOps**, and **MCP automation**. See [`docs/discoverability.md`](docs/discoverability.md).

## Repository contents

```text
assets/        Visual diagrams and banner SVGs
docs/          Concepts, setup, safety, and operation docs
examples/      Public-safe example loop prompts
skill/         Installable Hermes skill
scripts/       Installer and readiness checker
templates/     LOOP.md and state templates
```

## Maintain and improve the starter

Use [`docs/r-and-d-loop.md`](docs/r-and-d-loop.md) and [`examples/hermes-loop-engineering-rd.prompt.md`](examples/hermes-loop-engineering-rd.prompt.md) to set up a recurring R&D loop that improves functionality, documentation, examples, validation, and discoverability while keeping private/local loops gated.

## Validate a loop spec

The readiness checker is intentionally lightweight. It catches missing basics before you schedule something risky:

```bash
python scripts/loop_readiness.py templates/LOOP.example.md
```

## License

MIT. See [`LICENSE`](LICENSE).

## Acknowledgements

Inspired by the broader loop-engineering discussion in the agent community and adapted specifically for Hermes Agent primitives.
