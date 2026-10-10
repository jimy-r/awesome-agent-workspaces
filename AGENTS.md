# AGENTS.md

Instructions for any coding agent working in this repository, in the
[agents.md](https://agents.md/) format. Runtime-neutral by design. Claude Code
reads [`CLAUDE.md`](CLAUDE.md) as well, and the two carry the same rules.
Humans should start at [`README.md`](README.md), contributors at
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## What this repository is

A curated Awesome list of resources for building **agent workspaces**: the
roles, routines, hooks, memory and task coordination that make a repository
legible to a coding agent. It is a single `README.md` plus the CI that keeps it
honest. Nothing is published from it and nothing runs on its own.

## The checks

```bash
npx awesome-lint                      # list format, what CI enforces
python scripts/check_maintained.py    # each entry's last push date, read-only
```

`check_maintained.py` reports two markers. `STALE` at 90 days is early warning;
`BREACH` at 365 days, and `UNREACHABLE`, mean the README's maintained bar has
actually been crossed. The weekly workflow posts every run's report, clean or
not, to one standing review issue and to the job summary, and never pushes to
the repo. Adding an entry does not require running it.

Link checking runs in CI against live URLs, so run it there rather than locally.

## Adding or changing an entry

Three tests decide inclusion, stated in full under "The three criteria" in
[`CONTRIBUTING.md`](CONTRIBUTING.md) and summarised at the top of
[`README.md`](README.md): the resource is *maintained* (real activity within
roughly twelve months), *documented* (a reader can tell what it does without
cloning it), and about *workspace durability* rather than agent capability. One
entry per pull request. Self-submissions are welcome and held to the same bar.

Every rejection gets a one-line reason in [`REJECTIONS.md`](REJECTIONS.md). Add
it there rather than closing a pull request silently.

## Conventions

- **Always branch.** Never commit to `main`.
- **One focused change per pull request.**
- **[Conventional Commits](https://www.conventionalcommits.org/):** `feat:`,
  `fix:`, `docs:`, `chore:`.
- **Include a `Co-Authored-By:` trailer** on agent-assisted commits.
- **Pin third-party actions to a commit SHA** with the version as a trailing
  comment. A moving tag lets someone else change what runs under this repo's
  token, and the maintained-check job's token can write issues.
- Entry descriptions are one line, sentence case, no marketing adjectives.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full mechanics and
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for the participation rules.
