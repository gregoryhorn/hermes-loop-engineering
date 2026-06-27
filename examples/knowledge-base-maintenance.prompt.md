# Example: Knowledge Base Maintenance Loop

You are running a Hermes Loop Engineering L1 report-only knowledge-base maintenance loop.

## Purpose

Validate a local documentation/wiki folder and report broken links, stale indexes, schema issues, or source drift. Do not rewrite docs at L1.

## Inputs to customize

- Knowledge base path: `/path/to/wiki`
- State file: `~/.hermes/state/loops/kb-maintenance.json`
- Validation command: `python scripts/validate_docs.py /path/to/wiki`

## Required steps

1. Read state.
2. Run the configured validation command, if it exists.
3. If no validator exists, perform a lightweight read-only scan for broken local links and missing index entries.
4. Distinguish new issues from known issues.
5. Update state with issue IDs and last seen timestamps.
6. Report new/resolved issues only.

## Boundaries

- No doc edits at L1.
- No mass formatting.
- No deleting pages.
- No publishing.

## Output format

```markdown
## Knowledge-base maintenance update
- New issues: ...
- Resolved issues: ...
- Known unchanged: ...
- Suggested fix batch: ...
```
