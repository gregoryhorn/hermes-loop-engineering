# LOOP.md — Example Hermes Loop Spec

## Name

Example Daily Project Triage

## Level

L1 Report

## Purpose

Inspect a bounded project workspace and surface actionable changes without mutating code or external systems.

## Non-goals

- Do not edit code.
- Do not create PRs/issues.
- Do not install dependencies.
- Do not publish, deploy, or delete anything.

## Watched scope

- Project path: `/path/to/project`
- Branch: `main`
- State file: `~/.hermes/state/loops/example-project-triage.json`

## Schedule

Weekdays at 09:00 local time.

## Required tools

- file
- terminal
- optionally web/github for public issue/CI inspection

## Durable state

State schema follows `templates/state.example.json`.

The loop must read state at start and write state before finishing.

## Verification evidence

For L1:

- current git status
- changed finding IDs
- validation command output when configured

For L2+:

- real test/lint/build command output
- verifier summary
- diff summary

## Notification rule

Notify only on state changes, blockers, risky decisions, or completed deliverables.

## Human escalation triggers

- auth/secrets/PII/infra/publishing/deletion involved
- same issue repeats 3 times
- validation command fails unexpectedly
- scope expansion needed

## Kill switch

Pause the Hermes cron job:

```bash
hermes cron pause <job_id>
```

## Promotion checklist

- [ ] L1 has run successfully several times
- [ ] False positive rate is acceptable
- [ ] State is populated and pruned
- [ ] Allowed action set is narrow
- [ ] Verifier exists
- [ ] Attempt caps are set
- [ ] Human gates are documented
