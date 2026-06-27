# Safety model

## Default denylist

Loops should not mutate these areas without explicit human approval:

```text
.env
.env.*
**/secrets/**
**/credentials/**
**/*_key*
**/*_secret*
**/auth/**
**/payments/**
**/billing/**
**/production/**
**/terraform/**
**/k8s/**
```

## Always human-gate

- secrets and credentials
- authentication / authorization
- payments and billing
- PII handling
- public publishing
- deletes and destructive cleanup
- production infrastructure
- broad dependency upgrades
- third failed attempt on the same item

## Notification hygiene

Notify on:

- new actionable finding
- state change
- blocker
- repeated failure
- risky decision
- completed deliverable

Do not notify on:

- routine heartbeat
- unchanged watchlists
- low-confidence speculation
- repeated duplicate findings

## Attempt caps

Every L2/L3 loop needs attempt caps.

Example:

```text
Max attempts per item: 2
On third failure: stop, write blocker, escalate to human
```

## Kill switch

Every scheduled loop should document exactly how to pause it:

```bash
hermes cron pause <job_id>
```

The loop state should also contain:

```json
{
  "kill_switch": "hermes cron pause <job_id>",
  "pause_if": ["budget exceeded", "same blocker repeated", "human says stop"]
}
```
