# R&D loop for Hermes Loop Engineering

This page describes a reusable research-and-development loop for improving a public Hermes Loop Engineering starter repository over time.

The loop is designed for maintainers who want their starter kit to keep improving without turning into an unsafe unattended publisher.

## Objective

Continuously improve:

- functionality and setup ergonomics
- documentation quality
- example prompt usefulness
- validation and safety checks
- discoverability / SEO
- adoption paths for new Hermes users

## Recommended readiness level

Start at **L2 Assisted** for this repository class:

- The loop may make narrow public-repo changes.
- It must run validation before committing.
- It may push only if the worktree is clean except for its intended files and all checks pass.
- It must stop and notify the maintainer when a change is risky, broad, ambiguous, or requires external credentials.

Use **L1 Report** if you want recommendations only.

## Durable state

Use a local private state file, not the public repository, for run history:

```text
~/.hermes/state/loops/hermes-loop-engineering-rd.json
```

The public repo includes `templates/rnd-state.example.json` so users can create their own private state file.

## Allowed actions

Within the public starter repository only, the loop may:

- improve README clarity and onboarding
- add or refine public-safe example prompts
- improve templates and state schemas
- improve validator/readiness checks
- add documentation pages
- improve SEO/discoverability metadata
- run local validation and GitHub Actions readback
- commit and push one small improvement batch per run, if checks pass

## Forbidden actions

The loop must not:

- include private loop prompts, schedules, state files, account workflows, personal paths, channel IDs, or credentials
- edit unrelated repositories
- mutate the user's real production/personal loops without explicit approval
- create noisy alerts on unchanged runs
- delete files unless the deletion is clearly part of the public starter and validated
- change GitHub visibility/private settings
- publish packages/releases without explicit approval

## Existing loop improvement policy

The loop may inspect the maintainer's local loop registry/status to identify weaknesses in existing loops, but it should treat private loops as private operations:

- For public starter repo improvements: it may implement and push safe changes.
- For private/local loop improvements: it should write recommendations and ask for approval before changing cron jobs, private prompts, or state files.

## Suggested cadence

Weekly is usually enough:

```cron
0 10 * * 4
```

For an active launch period, twice weekly is reasonable.

## Notification policy

Notify the maintainer when:

- a commit was pushed
- validation failed
- GitHub Actions failed
- a blocker or risky decision exists
- private loop improvements require approval
- a new high-value opportunity was found

Do not notify on unchanged/no-op runs unless the scheduler cannot stay silent.

## Validation checklist

Before pushing, run at minimum:

```bash
python scripts/loop_readiness.py templates/LOOP.example.md
bash -n scripts/install-hermes-loop-skill.sh
python -m py_compile scripts/loop_readiness.py scripts/check_markdown_links.py scripts/validate_loop_state.py scripts/extract_cron_response.py scripts/check_assets.py scripts/public_release_check.py
python scripts/validate_loop_state.py templates/state.example.json
python scripts/validate_loop_state.py templates/rnd-state.example.json
python scripts/check_assets.py
python scripts/public_release_check.py
python scripts/check_markdown_links.py .
python -m unittest discover -s tests -v
```

Also scan for private leakage terms appropriate to your environment before pushing. Keep those environment-specific terms in the private loop prompt or state, not in the public repository.

After pushing, verify:

```bash
git rev-list --left-right --count @{u}...HEAD
gh run list --repo OWNER/REPO --limit 3
gh repo view OWNER/REPO --json nameWithOwner,visibility,url,description,isTemplate,repositoryTopics
```

## Promotion ideas

Good future improvements include:

- generated `hermes cron create` command examples
- stricter JSON schema validation modes for state files
- automated private-leakage scanner with configurable patterns
- install smoke test in a temporary `HERMES_HOME`
- example dashboards for loop health
- a GitHub issue template for proposed loop patterns
- documentation for using this starter with MCP servers
