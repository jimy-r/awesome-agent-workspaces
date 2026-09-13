#!/usr/bin/env python3
"""Flag README entries whose upstream repo has gone quiet.

Two thresholds, reported as two distinct markers, because they answer two
different questions.

STALE (90 days) is the early-warning signal: worth a look, not yet a
problem. A healthy curated list has entries in this band at all times.

BREACH (365 days), plus UNREACHABLE, is the "maintained" bar from README.md's
inclusion criteria actually being crossed: roughly twelve months with no real
activity, judged by hand at review time. The final call stays human; this is
the machine saying which entries the human has to look at.

Keeping them apart is what lets the workflow gate two things separately: it
files the review issue on either marker, and it restamps the README's
verified-on date only when nothing has breached. Under one combined flag the
restamp could never fire, because the 90-day band is never empty.

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

ENTRY_RE = re.compile(r"^-\s+\[([^\]]+)\]\(https://github\.com/([^/]+)/([^/)]+)\)")


def find_entries() -> list[tuple[str, str, str]]:
    """Return (display_name, owner, repo) for every GitHub entry in README.md."""
    entries = []
    for line in README.read_text(encoding="utf-8").splitlines():
        m = ENTRY_RE.match(line)
        if m:
            entries.append((m.group(1), m.group(2), m.group(3)))
    return entries


def pushed_at(owner: str, repo: str) -> str | None:
    result = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}", "--jq", ".pushed_at"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    entries = find_entries()
    now = datetime.now(timezone.utc)
    stale: list[tuple[str, str, str, int]] = []
    breached: list[tuple[str, str, str, int]] = []
    unreachable: list[str] = []

    for name, owner, repo in entries:
        ts = pushed_at(owner, repo)
        if ts is None:
            unreachable.append(f"{name} ({owner}/{repo})")
            continue
        pushed = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        age_days = (now - pushed).days
        if age_days > BREACH_DAYS:
            breached.append((name, owner, repo, age_days))
        elif age_days > STALE_DAYS:
            stale.append((name, owner, repo, age_days))

    if args.json:
        print(
            json.dumps(
                {
                    "checked": len(entries),
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
                }
            )
        )
    else:
        if not stale and not breached and not unreachable:
            print(
                f"All {len(entries)} entries pushed within the last {STALE_DAYS} days."
            )
        elif not breached and not unreachable:
            print(
                f"No entry has breached the {BREACH_DAYS}-day maintained bar. "
                f"{len(stale)} of {len(entries)} are quieter than {STALE_DAYS} days "
                "and worth a look."
            )
        for name, owner, repo, age_days in sorted(breached, key=lambda x: -x[3]):
            print(
                f"BREACH ({age_days}d since last push, bar is {BREACH_DAYS}d): "
                f"{name} -- https://github.com/{owner}/{repo}"
            )
        for u in unreachable:
            print(f"UNREACHABLE (api call failed): {u}")
        for name, owner, repo, age_days in sorted(stale, key=lambda x: -x[3]):
            print(
                f"STALE ({age_days}d since last push): {name} -- https://github.com/{owner}/{repo}"
            )

    # Advisory only, both markers. Exit 0 regardless; the workflow step reads
    # the markers and decides what to file and whether to restamp.
    return 0


if __name__ == "__main__":
    sys.exit(main())
