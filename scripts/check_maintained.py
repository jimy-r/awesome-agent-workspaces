#!/usr/bin/env python3
"""Flag README entries whose upstream repo has gone quiet, been archived or moved.

Two thresholds, reported as two distinct markers, because they answer two
different questions.

STALE (90 days) is the early-warning signal: worth a look, not yet a
problem. A healthy curated list has entries in this band at all times.

BREACH (365 days), plus UNREACHABLE, is the "maintained" bar from README.md's
inclusion criteria actually being crossed: roughly twelve months with no real
activity, judged by hand at review time. The final call stays human; this is
the machine saying which entries the human has to look at.

Keeping them apart is what keeps the weekly report readable. The workflow
posts every run's report to a standing review issue, and the reviewer has to
see at a glance which entries need a decision now and which are only worth a
look. Under one combined flag every run would read as a problem, because the
90-day band is never empty.

Two more markers come from the same API call, because a push date cannot see
either case. ARCHIVED sits with BREACH: an archived repo keeps the push date
it had, so the age check passes while the project is closed. MOVED sits with
STALE: the API answers a renamed or transferred repo under its old path, so
the entry still resolves while the list carries a path that is no longer the
canonical one.

EXEMPTIONS below carries entries that fail the age heuristic by design: a
reference essay or specification whose value doesn't depend on ongoing
commits, not a tool that rots without them. An exempted entry is never
checked against the push-date thresholds and reports as EXEMPT, never as
STALE or BREACH. It is still read for ARCHIVED, MOVED and UNREACHABLE, which
say nothing about age. It still has to clear CONTRIBUTING.md's other two
criteria; this dict only carries the "maintained" one and records why.

Usage:
    python scripts/check_maintained.py            # human-readable report
    python scripts/check_maintained.py --json      # machine-readable
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
README = REPO / "README.md"
STALE_DAYS = 90
BREACH_DAYS = 365

# "owner/repo" -> the recorded reason it's exempt from the age check. Add an
# entry here only for a reference text (an essay or specification) whose
# content is stable by design, per CONTRIBUTING.md's exemption note. Keep the
# reason short; it's printed as-is in both report formats.
EXEMPTIONS: dict[str, str] = {
    "humanlayer/12-factor-agents": (
        "reference essay; the content is stable by design, not a tool that rots"
    ),
}

# An entry is a list item whose link points at a GitHub repo. Anything after
# owner/repo (a path into the tree, a fragment, a query) is allowed and
# ignored, so an entry that deep-links into a repo is checked against that
# repo instead of being skipped.
ENTRY_RE = re.compile(
    r"^-\s+\[([^\]]+)\]\(https://github\.com/([^/)\s]+)/([^/)\s#?]+)(?:[/#?][^)]*)?\)"
)


def find_entries() -> list[tuple[str, str, str]]:
    """Return (display_name, owner, repo) for every GitHub entry in README.md."""
    entries = []
    for line in README.read_text(encoding="utf-8").splitlines():
        m = ENTRY_RE.match(line)
        if m:
            entries.append((m.group(1), m.group(2), m.group(3)))
    return entries


def repo_state(owner: str, repo: str) -> dict | None:
    """Return the repo's pushed_at, archived and full_name, or None.

    One API call carries all three. None means the call failed or came back
    without a push date, and the entry is reported as UNREACHABLE.
    """
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{owner}/{repo}",
            "--jq",
            "{pushed_at, archived, full_name}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        state = json.loads(result.stdout)
    except ValueError:
        return None
    if not isinstance(state, dict) or not state.get("pushed_at"):
        return None
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    entries = find_entries()
    now = datetime.now(timezone.utc)
    stale: list[tuple[str, str, str, int]] = []
    breached: list[tuple[str, str, str, int]] = []
    unreachable: list[str] = []
    archived: list[tuple[str, str, str]] = []
    moved: list[tuple[str, str, str, str]] = []
    exempt: list[tuple[str, str, str, str]] = []
    # Two entries can point into one repo (its root and a page inside it), so
    # each repo is asked for once.
    states: dict[str, dict | None] = {}

    for name, owner, repo in entries:
        slug = f"{owner}/{repo}"
        reason = EXEMPTIONS.get(slug)
        if reason is not None:
            exempt.append((name, owner, repo, reason))
        if slug.lower() not in states:
            states[slug.lower()] = repo_state(owner, repo)
        state = states[slug.lower()]
        if state is None:
            unreachable.append(f"{name} ({slug})")
            continue
        # GitHub paths are case-insensitive, so only a different path counts.
        full_name = state.get("full_name") or slug
        if full_name.lower() != slug.lower():
            moved.append((name, owner, repo, full_name))
        if state.get("archived"):
            # An archived repo's push date is frozen, so its age says nothing
            # the ARCHIVED marker has not already said.
            archived.append((name, owner, repo))
            continue
        if reason is not None:
            continue
        pushed = datetime.strptime(state["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        age_days = (now - pushed).days
        if age_days > BREACH_DAYS:
            breached.append((name, owner, repo, age_days))
        elif age_days > STALE_DAYS:
            stale.append((name, owner, repo, age_days))

    checked = len(entries) - len(exempt)
    bar_crossed = bool(breached or archived or unreachable)

    if args.json:
        print(
            json.dumps(
                {
                    "checked": checked,
                    "stale_days_threshold": STALE_DAYS,
                    "breach_days_threshold": BREACH_DAYS,
                    "stale": [
                        {"name": n, "owner": o, "repo": r, "days_since_push": d}
                        for n, o, r, d in stale
                    ],
                    "breached": [
                        {"name": n, "owner": o, "repo": r, "days_since_push": d}
                        for n, o, r, d in breached
                    ],
                    "unreachable": unreachable,
                    "archived": [
                        {"name": n, "owner": o, "repo": r} for n, o, r in archived
                    ],
                    "moved": [
                        {"name": n, "owner": o, "repo": r, "now": full}
                        for n, o, r, full in moved
                    ],
                    "exempt": [
                        {"name": n, "owner": o, "repo": r, "reason": reason}
                        for n, o, r, reason in exempt
                    ],
                }
            )
        )
    else:
        if not bar_crossed and not stale and not moved:
            suffix = f" ({len(exempt)} exempt from the age check.)" if exempt else ""
            print(
                f"All {checked} entries pushed within the last {STALE_DAYS} days.{suffix}"
            )
        elif not bar_crossed:
            look = []
            if stale:
                look.append(
                    f"{len(stale)} of {checked} are quieter than {STALE_DAYS} days "
                    "and worth a look."
                )
            if moved:
                look.append(f"{len(moved)} listed under a path that has moved.")
            print(
                f"No entry has breached the {BREACH_DAYS}-day maintained bar. "
                + " ".join(look)
            )
        for name, owner, repo, age_days in sorted(breached, key=lambda x: -x[3]):
            print(
                f"BREACH ({age_days}d since last push, bar is {BREACH_DAYS}d): "
                f"{name} -- https://github.com/{owner}/{repo}"
            )
        for name, owner, repo in archived:
            print(
                f"ARCHIVED (upstream is read-only): {name} -- https://github.com/{owner}/{repo}"
            )
        for u in unreachable:
            print(f"UNREACHABLE (api call failed): {u}")
        for name, owner, repo, age_days in sorted(stale, key=lambda x: -x[3]):
            print(
                f"STALE ({age_days}d since last push): {name} -- https://github.com/{owner}/{repo}"
            )
        for name, owner, repo, full_name in moved:
            print(
                f"MOVED (now https://github.com/{full_name}): "
                f"{name} -- https://github.com/{owner}/{repo}"
            )
        for name, owner, repo, reason in exempt:
            print(f"EXEMPT ({reason}): {name} -- https://github.com/{owner}/{repo}")

    # Advisory only, every marker. Exit 0 regardless; the workflow step greps
    # the markers into its outputs and posts the whole report to the standing
    # review issue every run.
    return 0


if __name__ == "__main__":
    sys.exit(main())
