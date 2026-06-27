# Operating model

## Lifecycle

1. Define purpose and non-goals.
2. Define watched scope.
3. Choose durable state.
4. Write the loop prompt as a self-contained runbook.
5. Start L1 report-only.
6. Run a few manual/smoke runs.
7. Review false positives and noise.
8. Add verification.
9. Promote only if the allowed action set is narrow and useful.

## State schema

A minimal loop state records:

- loop name
- level
- last run time
- watched scope
- current findings
- decisions waiting on humans
- attempt counters
- recent run summaries
- pause criteria

Use `templates/state.example.json` as a starting point.

## Promotion checklist

Before L2/L3:

- [ ] L1 output was useful and not noisy
- [ ] state file is populated and reviewed
- [ ] allowed actions are narrow
- [ ] forbidden actions are explicit
- [ ] verifier exists
- [ ] verification commands are real
- [ ] attempt cap is encoded
- [ ] kill switch is documented
- [ ] human escalation paths are clear

## Anti-patterns

- loop with no state
- loop that pings every run
- cron trigger treated as completion
- implementer marking its own work complete
- no attempt cap
- broad write permissions
- auto-fix before report-only baseline
- task progress stored in long-term memory
