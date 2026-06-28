# Loop artifact flow

Hermes loops should keep full audit evidence while making the latest useful result easy to inspect.

## Artifact classes

| Artifact | Purpose | Recommended location | Retention |
|---|---|---|---|
| Loop state | Compact durable state and current health | `~/.hermes/state/loops/<loop>.json` | Long-lived |
| Full cron output | Complete scheduler transcript for audit/debugging | `~/.hermes/cron/output/<job_id>/<timestamp>.md` | Time-limited or archived |
| Compact response | Human-readable final response without prompt/skill preamble | `~/.hermes/state/loops/<loop>-last-response.md` | Keep latest, optionally history |
| Health summary | Machine-readable latest status/blocker/next action | `~/.hermes/state/loops/<loop>-health.json` | Keep latest |
| Deliverable artifact | Report, diff, validation log, screenshot, media, etc. | Loop-specific artifact directory | Project-specific |

## Minimal health fields

```json
{
  "kind": "hermes_loop_health",
  "loop_id": "example-loop",
  "job_id": "abc123",
  "state_path": "/home/user/.hermes/state/loops/example-loop.json",
  "last_status": "ok",
  "last_output_path": "/home/user/.hermes/cron/output/abc123/2026-06-28_10-00-00.md",
  "last_response_path": "/home/user/.hermes/state/loops/example-loop-last-response.md",
  "last_response_line": 120,
  "last_blocker_id": null,
  "next_safe_action": "review compact response"
}
```

## Extracting compact responses

Use the central extractor to keep cron outputs auditable while writing compact state artifacts:

```bash
python scripts/extract_cron_response.py \
  ~/.hermes/cron/output/<job_id>/<timestamp>.md \
  --loop-id example-loop \
  --job-id <job_id> \
  --state-path ~/.hermes/state/loops/example-loop.json \
  --write-response ~/.hermes/state/loops/example-loop-last-response.md \
  --write-health ~/.hermes/state/loops/example-loop-health.json
```

The extractor looks for a `## Response` or `# Response` marker and falls back to the whole file for script-only outputs.

## Alert hygiene

- Notify on blocker opened/resolved/repeated, validation failure, approval need, or delivered artifact.
- Stay silent on unchanged/no-op runs when the scheduler can suppress delivery.
- Keep full outputs for audit, but point operators to compact response/health files first.
- Do not put private local paths, job IDs, account names, or secrets in public examples unless they are placeholders.
