#!/usr/bin/env python3
"""Flag README entries whose upstream repo has gone quiet.

The "maintained" bar in README.md's inclusion criteria is a human judgment
call: real activity within roughly the last twelve months. This script is
an earlier-warning signal, not the bar itself -- it flags any GitHub entry
with no push in more than STALE_DAYS days, well before a year passes, so
staleness surfaces for review rather than being caught only once an entry
has already crossed the twelve-month line.

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
        if age_days > STALE_DAYS:
            stale.append((name, owner, repo, age_days))

    if args.json:
        print(
            json.dumps(
                {
                    "checked": len(entries),
                    "stale_days_threshold": STALE_DAYS,
                    "stale": [
                        {"name": n, "owner": o, "repo": r, "days_since_push": d}
                        for n, o, r, d in stale
                    ],
                    "unreachable": unreachable,
                }
            )
        )
    else:
        if not stale and not unreachable:
            print(
                f"All {len(entries)} entries pushed within the last {STALE_DAYS} days."
            )
        for name, owner, repo, age_days in sorted(stale, key=lambda x: -x[3]):
            print(
                f"STALE ({age_days}d since last push): {name} -- https://github.com/{owner}/{repo}"
            )
        for u in unreachable:
            print(f"UNREACHABLE (api call failed): {u}")

    # Advisory only: crossing 90 days is a "keep an eye on it" signal, not
    # the maintained bar itself (~365 days, judged by hand at review time).
    # Exit 0 regardless; the workflow step decides whether to open an issue.
    return 0


if __name__ == "__main__":
    sys.exit(main())
