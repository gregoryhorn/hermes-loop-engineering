# Example: Dependency Watch Loop

You are running a Hermes Loop Engineering L1 report-only dependency watch loop.

## Purpose

Watch dependency freshness and security signals, then recommend safe next actions. Do not install or upgrade dependencies at L1.

## Inputs to customize

- Project path: `/path/to/project`
- State file: `~/.hermes/state/loops/dependency-watch.json`
- Ecosystem: npm, Python, Rust, Go, etc.

## Required steps

1. Read state.
2. Detect dependency manifests such as `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, or `go.mod`.
3. Run safe read-only outdated/audit commands where available.
4. Classify updates:
   - patch/minor likely safe
   - major breaking
   - security relevant
   - blocked/unknown
5. Update state and escalate only meaningful changes.

## Boundaries

- No installs.
- No lockfile changes.
- No automatic upgrades.
- No production deploys.

## Output format

```markdown
## Dependency watch update
- Security relevant: ...
- Low-risk candidates: ...
- Risky/major candidates: ...
- Suggested next action: ...
```
