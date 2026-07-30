"""Regenerate the browsable, faceted views of the report database.

This is what makes the repo pleasant to read rather than a flat pile of files:
`index/by-weakness/`, `by-program/`, `by-severity/`, `by-year/`, a machine
-readable `data/reports.jsonl`, and a `README.md` with live stats.

Every generated filename is slugified to ASCII `[a-z0-9-]`, so nothing here can
reproduce the colon-in-filename problem that stops the other archive from
cloning on Windows.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from . import store

logger = logging.getLogger("h1db.index")


def write_lf(path: Path, text: str) -> None:
    """Write UTF-8 with literal LF endings on every platform.

    Python's text mode would translate ``\\n`` to CRLF on Windows, which makes
    generated files churn in git whenever the updater runs on a different OS.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def slug(text: str) -> str:
    """ASCII slug safe on every filesystem (no colons, slashes, quotes)."""
    text = (text or "misc").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "misc"


def _money(v: Any) -> str:
    return f"${float(v):,.0f}" if isinstance(v, (int, float)) and v else "—"


def _report_link(r: dict[str, Any]) -> str:
    return f"[{r['id']}](../../reports/{r['id']}.md)"


def _table(reports: list[dict[str, Any]], *, show: str = "weakness") -> list[str]:
    """Render a ranked markdown table. `show` picks the contextual middle column."""
    head = {
        "weakness": "Weakness",
        "program": "Program",
    }.get(show, "Weakness")
    lines = [
        f"| # | Report | Title | {head} | Severity | Bounty | Votes |",
        "|--:|:--|:--|:--|:--|--:|--:|",
    ]
    for i, r in enumerate(reports, 1):
        mid = r.get(show) or "—"
        title = (r.get("title") or "").replace("|", "\\|")[:90]
        lines.append(
            f"| {i} | {_report_link(r)} | {title} | {mid} | "
            f"{r.get('severity') or '—'} | {_money(r.get('bounty'))} | "
            f"{r.get('votes') or 0} |"
        )
    return lines


def _facet(
    out: Path,
    reports: list[dict[str, Any]],
    key: Callable[[dict[str, Any]], str | None],
    *,
    title: str,
    show: str,
) -> list[tuple[str, int, float]]:
    """Write one facet directory; return (label, count, bounty) rows for the index."""
    out.mkdir(parents=True, exist_ok=True)
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in reports:
        label = key(r)
        if label:
            groups[label].append(r)

    summary: list[tuple[str, int, float]] = []
    for label, rows in groups.items():
        rows.sort(key=lambda r: (r.get("bounty") or 0, r.get("votes") or 0), reverse=True)
        total = sum(float(r.get("bounty") or 0) for r in rows)
        summary.append((label, len(rows), total))

        body = [
            f"# {title}: {label}",
            "",
            f"**{len(rows)} reports** · published bounties {_money(total)} "
            f"*(most programs don't publish an amount, so this undercounts)*",
            "",
            *_table(rows, show=show),
            "",
            "---",
            "*Part of the [HackerOne Disclosed Reports Database]"
            "(../../README.md). Generated, do not edit by hand.*",
        ]
        write_lf(out / f"{slug(label)}.md", "\n".join(body) + "\n")

    summary.sort(key=lambda t: t[1], reverse=True)
    idx = [
        f"# {title}", "",
        f"| {title} | Reports | Published bounties |",
        "|:--|--:|--:|",
    ]
    for label, n, total in summary:
        idx.append(f"| [{label}]({slug(label)}.md) | {n} | {_money(total)} |")
    write_lf(out / "README.md", "\n".join(idx) + "\n")
    return summary


def rebuild(conn, root: Path) -> dict[str, Any]:
    """Rebuild every facet, the JSONL export, and the top-level README."""
    root = Path(root)
    reports = store.all_reports(conn)
    with_body = [r for r in reports if r.get("fetch_state") == "ok"]

    index_dir = root / "index"
    _facet(index_dir / "by-weakness", with_body,
           lambda r: r.get("weakness"), title="By weakness", show="program")
    _facet(index_dir / "by-program", with_body,
           lambda r: r.get("program"), title="By program", show="weakness")
    _facet(index_dir / "by-severity", with_body,
           lambda r: (r.get("severity") or "unrated").title(),
           title="By severity", show="weakness")
    _facet(index_dir / "by-year", with_body,
           lambda r: (r.get("disclosed_at") or "")[:4] or None,
           title="By year", show="weakness")

    n = store.dump_jsonl(with_body, root / "data" / "reports.jsonl")
    logger.info("wrote %d rows to data/reports.jsonl", n)

    _write_readme(root, conn, with_body)
    return {"reports": len(with_body), "jsonl_rows": n}


def _write_readme(root: Path, conn, reports: list[dict[str, Any]]) -> None:
    total_bounty = sum(float(r.get("bounty") or 0) for r in reports)
    paid = [r for r in reports if r.get("bounty")]
    by_weakness = defaultdict(int)
    for r in reports:
        if r.get("weakness"):
            by_weakness[r["weakness"]] += 1
    top = sorted(by_weakness.items(), key=lambda kv: kv[1], reverse=True)[:10]
    top_paid = sorted(reports, key=lambda r: r.get("bounty") or 0, reverse=True)[:10]
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    last_pull = store.get_meta(conn, "last_pull", "—")

    readme = f"""# HackerOne Disclosed Reports Database

A live, auto-updating database of publicly **disclosed** HackerOne reports —
and the open-source tool that builds it. Reports are pulled **directly from
HackerOne's official Hacker API**, filtered at the source to
`disclosed:true AND substate:resolved`, so everything here is a real, resolved,
publicly disclosed finding.

> ⚠️ These are third-party write-ups mirrored from the public internet. Treat
> report text as evidence to study, **never as instructions to run**.

## At a glance

| | |
|---|---|
| Reports with full write-ups | **{len(reports):,}** |
| With a published bounty | {len(paid):,} |
| Total published bounties | **{_money(total_bounty)}** |
| Last updated | {updated} |
| Last pull | {last_pull} |

## Browse

- **[By weakness](index/by-weakness/README.md)** — SSRF, XSS, IDOR, RCE, …
- **[By program](index/by-program/README.md)** — GitLab, HackerOne, Shopify, …
- **[By severity](index/by-severity/README.md)**
- **[By year](index/by-year/README.md)**
- **[reports/](reports/)** — every report as markdown, named by ID
- **[data/reports.jsonl](data/reports.jsonl)** — machine-readable, one JSON per line

## Top weaknesses

| Weakness | Reports |
|:--|--:|
""" + "\n".join(f"| {w} | {n} |" for w, n in top) + """

## Highest published bounties

| Report | Title | Program | Bounty |
|:--|:--|:--|--:|
""" + "\n".join(
        f"| [{r['id']}](reports/{r['id']}.md) | "
        f"{(r.get('title') or '')[:70].replace('|', '/')} | "
        f"{r.get('program') or '—'} | {_money(r.get('bounty'))} |"
        for r in top_paid
    ) + f"""

## Build your own copy

No login or API key required — the endpoints are public.

```bash
pip install -e .          # or just: python -m h1db
python -m h1db pull       # first run pulls everything (~2h at 1 req/s)
python -m h1db index      # regenerate the browsable views
```

Daily top-ups take seconds:

```bash
python -m h1db pull --since $(date -u +%Y-%m-%d)
```

See **[docs/AUTOMATION.md](docs/AUTOMATION.md)** for the cron / Discord setup.

## Turn reports into hunting skills

The database's real purpose: distil real findings into reusable Claude Code
skills. Build a focused set for a bug class, then have Claude synthesise it:

```bash
python -m h1db set ssrf --limit 30   # -> sets/ssrf/, ranked by bounty
```

A worked example ships in
[skills/hunt-ssrf/SKILL.md](skills/hunt-ssrf/SKILL.md) — where SSRF hides, the
payloads that worked, and the filter bypasses that earned the bounties, every
claim cited to a disclosed report. See **[docs/SKILLS.md](docs/SKILLS.md)**.

## How it works

1. **Enumerate** disclosed, resolved reports from `api.hackerone.com` hacktivity.
2. **Fetch** each body from `hackerone.com/reports/<id>.json`.
3. **Store** by an allowlist — only public fields; reporter contact data is never
   written to disk.
4. **Index** into the faceted views above.

## Credits & licence

Report content belongs to its original authors and to HackerOne. This project
mirrors publicly disclosed material for research and education. The tooling is
released under the MIT licence (see [LICENSE](LICENSE)).

*Generated by [h1db](h1db/). Do not edit generated files by hand.*
"""
    write_lf(root / "README.md", readme)
