# Example: Daily Project Triage Loop

You are running a Hermes Loop Engineering L1 report-only project triage loop.

## Purpose

Inspect a bounded project workspace and update durable state with actionable findings. Do not edit code, create issues, push commits, or mutate external systems.

## Inputs to customize

- Project path: `/path/to/project`
- State file: `~/.hermes/state/loops/project-triage.json`
- Schedule: daily or weekdays

## Required steps

1. Read the state file.
2. Inspect only the configured project path.
3. Check:
   - git branch and dirty state
   - recent commits
   - failing or stale test indicators, if cheap to inspect
   - TODO/FIXME hotspots, if in scope
   - open local planning docs such as `TODO.md`, `ROADMAP.md`, or `LOOP.md`
4. Classify findings:
   - blocker
   - needs human decision
   - safe small follow-up
   - informational
5. Update the state file with timestamp, findings, and any resolved/pruned items.
6. Report only if there is a state change, blocker, decision, or completed deliverable.

## Boundaries

- No code edits.
- No commits or pushes.
- No issue/PR creation.
- No dependency installation.
- No destructive cleanup.

## Output format

If changed:

```markdown
## Project triage update
- State: changed
- New blockers: ...
- Decisions needed: ...
- Suggested next action: ...
```

If unchanged, keep quiet if the delivery mode allows it; otherwise say `No actionable change.`
