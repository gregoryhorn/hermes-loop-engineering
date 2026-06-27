# Example: Service Health Watchdog Loop

This example is best implemented as a script-only Hermes cron job that prints only on state changes.

## Purpose

Check local service health and notify only when state changes from healthy to unhealthy or recovers.

## Suggested script behavior

- read previous state from `~/.hermes/state/loops/service-health.json`
- check one or more endpoints/processes
- write new state
- print a message only when health changes
- exit non-zero only when the watchdog itself failed

## Example Hermes cron shape

```text
Schedule: every 5m
Script: scripts/check_service_health.py
no_agent: true
Deliver: origin or your preferred channel
```

## Boundaries

- No automatic restarts by default.
- No destructive cleanup.
- No config changes.
- Escalate repeated failures.

## Output format when changed

```markdown
Service health changed: API went from healthy to failing.
- Check: GET http://localhost:8080/health
- Error: connection refused
- Suggested action: inspect service logs
```
