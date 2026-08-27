# Contributing

Thanks for taking the list seriously enough to propose a change. The bar below is the whole product. A list anyone can get onto is worth nothing to the reader.

## The three criteria

Every entry has to clear all three.

1. **Maintained.** Real activity within roughly the last twelve months. A repo whose last commit is two years old fails, however good the idea was.
2. **Documented.** A reader can tell what it does, and how it differs from the neighbouring entry, without cloning it and running it. A README that is a logo and an install command fails.
3. **About workspace durability, not agent capability.** The list covers the things that make an agent workspace survive: persistent memory, context management, evaluation, guardrails, orchestration discipline, observability, security. A tool that makes an agent smarter, faster, or more autonomous is out of scope unless durability is the point of it.

Generic agent frameworks, prompt collections, model lists, and one-shot demos are out of scope by definition. So are forks and mirrors. List the upstream.

## How to submit

**One pull request per entry.** A PR adding six things gets closed with a request to split it. One entry per PR keeps the reasoning reviewable and keeps the rejection log honest.

Use this format, exactly:

```
- [Name](https://github.com/owner/repo) - What it uniquely solves, in one line.
```

Rules for the line:

- Plain prose. No emoji, no star counts, no badges, no marketing copy lifted from the README.
- Say what it *uniquely* solves. If your line would apply equally to three entries already on the list, the entry is redundant and will be rejected.
- Start with a capital letter, end with a full stop.
- Put it in the category it actually belongs to, alphabetically within that category is not required but keep it tidy.

## What happens next

The reviewer replies with one of two things: a merge, or a one-line reason. Rejections are recorded in [REJECTIONS.md](REJECTIONS.md) with that reason and the date. Nothing is rejected silently, and the log is public so you can argue with it.

Expect the reason to be short. "Not maintained since 2024", "generic agent framework", "duplicates an existing entry" are complete answers.

## Self-submissions

Submitting your own project is welcome and always has been. It is held to exactly the same bar, judged on the same three criteria, and rejected with the same one-line reason if it does not clear them. Say in the PR that it is yours. Entries maintained by the list author carry a visible marker for the same reason.

## Removals

Removals are contributions too. If an entry has gone stale, been archived, or turned into something else, open a PR that removes it and say why. Link rot and abandonment are caught by CI and by review, but a human noticing first is faster.

## Style

- Keep the README lint-clean. CI runs `awesome-lint` and a link check on every PR.
- Do not add a category. If you think one is missing, open an issue first; a category with fewer than two entries gets folded into its neighbour.
- Commit messages: short and descriptive.
