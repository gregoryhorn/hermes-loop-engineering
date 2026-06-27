# Concepts

## Loop engineering

Loop engineering is the practice of designing the system that prompts, schedules, verifies, records, and escalates agent work.

A loop is not just a prompt. A loop has:

- a purpose
- non-goals
- watched scope
- durable state
- a schedule or trigger
- operating boundaries
- verification evidence
- escalation rules
- a kill switch

## Harness vs loop

A harness is the environment for one agent run: model, tools, context, permissions, and instructions.

A loop is the harness plus recurrence, state, verification, and human handoff.

```text
Harness = one safe agent run
Loop    = harness + schedule + state + verification + escalation
```

## Durable state

Hermes chats are not durable loop state. Store loop state in one of:

- `~/.hermes/state/loops/<name>.json`
- a repo-local `LOOP.md` or `STATE.md`
- a Kanban board
- a wiki/documentation page

Mnemosyne/Hermes memory is best for compact pointers and preferences, not run logs.

## Maker/checker

If a loop performs a mutation, split roles:

- maker: proposes or implements the smallest scoped change
- checker: tries to reject it by running real verification commands

The checker should report evidence, not vibes.
