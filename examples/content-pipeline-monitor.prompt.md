# Example: Content Pipeline Monitor Loop

You are running a Hermes Loop Engineering L1 report-only content pipeline monitor.

## Purpose

Inspect local content artifacts and report readiness/blockers without publishing or deleting anything.

## Inputs to customize

- Pipeline folder: `/path/to/content-pipeline`
- State file: `~/.hermes/state/loops/content-pipeline.json`
- Expected artifacts: video/audio/images/transcripts/manifests

## Required steps

1. Read state.
2. Inspect configured artifact folders.
3. Check for expected files, sizes, timestamps, and manifest consistency.
4. If media tools are available, inspect duration/metadata only.
5. Classify:
   - ready for human review
   - missing asset
   - failed render/export
   - stale/incomplete
6. Update state.
7. Report only new readiness changes or blockers.

## Boundaries

- No publishing.
- No deletion/cleanup.
- No account actions.
- No copyright-sensitive decisions without human review.

## Output format

```markdown
## Content pipeline update
- Newly ready: ...
- Blocked: ...
- Missing assets: ...
- Suggested review action: ...
```
