---
name: loop-engineering
description: Design safe scheduled/stateful Hermes loops with durable state, report-only rollout, verification, and human gates.
version: 1.0.0
author: Hermes Agent contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, cron, loops, automation, safety, skills, delegation]
    homepage: https://github.com/gregoryhorn/hermes-loop-engineering
---

# Loop Engineering for Hermes

Use this skill when creating, reviewing, upgrading, or troubleshooting recurring Hermes work such as cron jobs, watchdogs, project triage, CI babysitters, knowledge-base maintenance, content pipeline monitors, or multi-agent routines.

## Definition

Loop engineering means designing the system that prompts, schedules, verifies, records, and escalates agent work, rather than manually prompting the agent each time.

## Mandatory defaults

1. Start new loops as **L1 report-only** unless the user explicitly approves mutation.
2. Every loop needs durable state outside chat.
3. Prompts for scheduled loops must be self-contained.
4. Notify only on state changes, blockers, risky decisions, or completed deliverables.
5. Use maker/checker verification before L2/L3 actions.
6. Human-gate secrets, auth, payments, PII, infra, publishing, deletion, and broad dependency upgrades.
7. Do not write transient run logs into long-term memory.

## Hermes primitive mapping

| Need | Hermes primitive |
|---|---|
| durable schedule | `hermes cron` / cronjob tool |
| quick maker/checker split | `delegate_task` |
| long bounded job | `terminal(background=true, notify_on_complete=true)` |
| durable state | JSON/Markdown/Kanban/wiki |
| reusable procedure | Hermes skill |
| external integrations | toolsets / MCP / browser / web / terminal |

## Loop design checklist

Before scheduling, capture:

- purpose
- non-goals
- watched scope
- schedule and first-run behavior
- state file or board
- required tools
- read/write boundaries
- verification evidence
- attempt caps and budget limits
- escalation triggers
- kill switch

## Readiness levels

- **L0 Draft:** documented intent only.
- **L1 Report:** inspect/update state/report; no mutation.
- **L2 Assisted:** small scoped changes with verifier and human-visible output.
- **L3 Unattended:** narrow allowlist, state, budget, verifier, kill switch, and human gates.

## Recommended prompt shape

```text
You are running the <name> Hermes loop.
Level: L1 Report.
Purpose: ...
Non-goals: ...
State file: ...
Watched scope: ...
Steps:
1. Read state.
2. Inspect bounded signals.
3. Compare with previous state.
4. Update state.
5. Report only changes/blockers/decisions/deliverables.
Forbidden: ...
Escalate when: ...
```

## Review stance

When reviewing a proposed loop, look for:

- missing state
- vague scope
- no kill switch
- noisy notification rule
- mutation at L1
- no verifier
- no attempt cap
- broad connectors or write permissions
- private data accidentally embedded in prompt/examples

Prefer smaller, quieter loops over ambitious autonomous ones.
