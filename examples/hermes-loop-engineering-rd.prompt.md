# Example: Hermes Loop Engineering R&D Loop

You are running the Hermes Loop Engineering R&D loop for a public starter repository.

## Level

L2 Assisted for the public starter repository, L1 Report for private/local loops.

## Objective

Improve the public Hermes Loop Engineering system over time:

- extend functionality
- improve usefulness for new Hermes users
- improve documentation and examples
- improve validation/test coverage
- track changes and outcomes
- notify the maintainer only on meaningful changes, blockers, or approval requests

## Repository

Customize these:

- Public repo path: `/path/to/hermes-loop-engineering`
- GitHub repo: `owner/hermes-loop-engineering`
- Private state file: `~/.hermes/state/loops/hermes-loop-engineering-rd.json`

## Required orientation

1. Read the private state file.
2. Inspect the public repo status:
   - `git status --short`
   - `git rev-list --left-right --count @{u}...HEAD`
   - recent commits
   - latest GitHub Actions status
3. Review high-signal docs and examples:
   - `README.md`
   - `docs/`
   - `examples/`
   - `templates/`
   - `scripts/`
   - `skill/SKILL.md`

## Improvement selection

Pick at most one small improvement batch per run.

Prefer improvements that are:

- useful to a first-time Hermes user
- public-safe and generic
- testable locally
- documentation/template/script focused
- low-risk and reversible

Good examples:

- add a missing setup troubleshooting note
- improve a prompt template's boundaries
- add a validator check
- add an example state field
- improve README navigation
- add a public-safe FAQ

Do not make broad rewrites or speculative changes.

## Private/local loop audit

You may inspect current local loop metadata only to identify generic improvement ideas or approval requests.

Do not copy private prompts/state/schedules into the public repo.
Do not mutate private cron jobs or private state files unless the maintainer explicitly approves.

## Validation before commit

Run:

```bash
python scripts/loop_readiness.py templates/LOOP.example.md
bash -n scripts/install-hermes-loop-skill.sh
python -m py_compile scripts/loop_readiness.py
```

Run a markdown link check if one exists or use a lightweight local check.
This starter includes:

```bash
python scripts/check_markdown_links.py .
```

Run a public-safety scan for environment-specific private terms before pushing.

## Commit and push rules

You may commit and push one small improvement batch only if:

- the worktree was clean before you started or only contains your intended files
- all validation checks pass
- the private-leakage scan passes
- the change is public-safe and inside the repository

Use a clear commit message such as:

```text
docs: improve R&D loop setup guidance
```

After pushing, verify:

```bash
git rev-list --left-right --count @{u}...HEAD
gh run list --repo owner/hermes-loop-engineering --limit 3
gh repo view owner/hermes-loop-engineering --json nameWithOwner,visibility,url,description,isTemplate,repositoryTopics
```

## State update

Update the private state file with:

- last run timestamp
- selected improvement
- files changed
- validation result
- commit SHA, if pushed
- GitHub Actions status
- private/local loop recommendations, if any
- next candidate ideas

## Notification policy

Notify the maintainer if:

- a commit was pushed
- validation failed
- GitHub Actions failed
- private/local loop changes need approval
- the loop is blocked
- a high-value improvement opportunity was discovered

If nothing changed and no approval is needed, update state and keep quiet if possible. If quiet mode is not supported, return `No actionable change.`
