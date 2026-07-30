"""Pull disclosed HackerOne reports directly from the official Hacker API.

Enumeration uses ``api.hackerone.com/v1/hackers/hacktivity`` with the Lucene
filter ``disclosed:true AND substate:resolved``. That endpoint answers
unauthenticated, so only valid, resolved, publicly disclosed reports are ever
listed — the "only pull valid disclosed reports" requirement is enforced at the
source, not by filtering afterwards.

Bodies are fetched separately from ``hackerone.com/reports/<id>.json``, because
hacktivity deliberately omits ``vulnerability_information``.

Fields are copied by *allowlist*. The report JSON carries full ``reporter`` and
``voters`` objects, and that endpoint has a history of over-disclosing personal
detail, so nothing beyond the public byline is stored or written to disk.
"""

from __future__ import annotations

import json
import logging
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from . import http, redact, store

logger = logging.getLogger("h1db.pull")

HACKTIVITY = "https://api.hackerone.com/v1/hackers/hacktivity"
REPORT_JSON = "https://hackerone.com/reports/{id}.json"

#: The API caps page size at 50 regardless of what we request.
PAGE_SIZE = 50

#: HackerOne rejects offsets beyond 10,000 rows (page 200 at size 50) with a
#: 400. That is the practical ceiling on how many reports this endpoint exposes.
MAX_OFFSET_PAGE = 200


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _query(weakness: str | None, program: str | None, since: str | None) -> str:
    parts = ["disclosed:true", "substate:resolved"]
    if weakness:
        # The working Lucene field is `cwe` and it takes HackerOne's *full*
        # weakness display name, e.g. cwe:"Server-Side Request Forgery (SSRF)".
        # Most workflows skip this and filter locally after a full pull, since
        # the whole disclosed+resolved set is only a few thousand reports.
        parts.append(f'cwe:"{weakness}"')
    if program:
        parts.append(f"program:{program}")
    if since:
        parts.append(f"disclosed_at:>={since}")
    return " AND ".join(parts)


def enumerate_reports(
    *,
    weakness: str | None = None,
    program: str | None = None,
    since: str | None = None,
    max_pages: int | None = None,
    limiter: http.RateLimiter,
) -> Iterator[dict[str, Any]]:
    """Yield normalised listing rows for every matching disclosed report."""
    query = _query(weakness, program, since)
    logger.info("hacktivity query: %s", query)
    page = 1
    while True:
        if max_pages and page > max_pages:
            return
        if page >= MAX_OFFSET_PAGE:
            logger.info("reached HackerOne's pagination ceiling (page %d)", page)
            return
        params = urllib.parse.urlencode({
            "queryString": query,
            "sort": "-latest_disclosable_activity_at",
            "page[number]": page,
            "page[size]": PAGE_SIZE,
        })
        try:
            payload = http.get_json(f"{HACKTIVITY}?{params}", limiter=limiter)
        except http.HttpError as exc:
            # A 400 here is the offset ceiling, i.e. the end of the feed.
            if exc.code == 400:
                logger.info("feed ended at page %d (HTTP 400 offset cap)", page)
                return
            raise
        items = payload.get("data") if isinstance(payload, dict) else None
        if not items:
            return
        for item in items:
            row = _listing_row(item)
            if row is not None:
                yield row
        page += 1


def _listing_row(item: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    report_id = item.get("id")
    if not isinstance(report_id, int):
        return None
    attr = item.get("attributes") or {}
    rel = item.get("relationships") or {}

    program = _rel_attr(rel, "program")
    reporter = _rel_attr(rel, "reporter")
    cve = attr.get("cve_ids")

    # hacktivity returns `cwe` as the weakness *display name* string
    # ("Information Disclosure"), not an object. Older/other shapes send a dict,
    # so handle both and always land the human-readable name in `weakness`.
    raw_cwe = attr.get("cwe")
    if isinstance(raw_cwe, dict):
        weakness_name = _clean(raw_cwe.get("name"))
        cwe_id = _clean(str(raw_cwe.get("id"))) if raw_cwe.get("id") else None
    else:
        weakness_name = _clean(raw_cwe)
        cwe_id = None

    severity = _clean(attr.get("severity_rating"))
    if severity and severity.lower() == "none":
        severity = None

    return {
        "id": report_id,
        "title": _clean(attr.get("title")),
        "program": _clean(program.get("name")) or _clean(program.get("handle")),
        "program_handle": _clean(program.get("handle")),
        "reporter": _clean(reporter.get("username")),
        "weakness": weakness_name,
        "cwe": cwe_id,
        "severity": severity,
        "bounty": _num(attr.get("total_awarded_amount")),
        "cve_ids": json.dumps(cve) if isinstance(cve, list) and cve else None,
        "substate": _clean(attr.get("substate")),
        "disclosed_at": _date(attr.get("disclosed_at")
                              or attr.get("latest_disclosable_activity_at")),
        "votes": _int(attr.get("votes")),
    }


def fetch_body(report_id: int, limiter: http.RateLimiter) -> dict[str, Any]:
    """Fetch and allowlist-project one report's JSON. Raises http.NotFound on 404."""
    payload = http.get_json(REPORT_JSON.format(id=report_id), limiter=limiter)
    if not isinstance(payload, dict):
        raise http.HttpError(f"report {report_id}: unexpected JSON shape")
    return payload


def render_markdown(payload: dict[str, Any], listing: dict[str, Any]) -> str | None:
    """Render a report as markdown, or None when it has no body text."""
    body = payload.get("vulnerability_information")
    if not isinstance(body, str) or not body.strip():
        return None

    # Disclosed reports frequently quote live credentials in their PoCs. Mirror
    # the finding, not the secret.
    body, redactions = redact.scrub(body)
    if redactions:
        logger.info("report %s: redacted %s", payload.get("id"),
                    ", ".join(f"{n}x {k}" for k, n in sorted(redactions.items())))

    def sub(key: str) -> dict[str, Any]:
        v = payload.get(key)
        return v if isinstance(v, dict) else {}

    team, scope, sev, weak = sub("team"), sub("structured_scope"), sub("severity"), sub("weakness")
    rid = payload.get("id") or listing["id"]
    bounty = listing.get("bounty")
    cves = listing.get("cve_ids")
    cves = json.loads(cves) if isinstance(cves, str) and cves else (cves or [])

    rows = [
        ("Report ID", f"[{rid}](https://hackerone.com/reports/{rid})"),
        ("Program", team.get("handle") or listing.get("program_handle") or "—"),
        ("Weakness", weak.get("name") or listing.get("weakness") or "—"),
        ("Severity", (sev.get("rating") or listing.get("severity") or "—")),
        ("Bounty", f"${float(bounty):,.0f}" if bounty else "—"),
        ("Asset", scope.get("asset_identifier") or "—"),
        ("CVE", ", ".join(str(c) for c in cves) if cves else "—"),
        ("Disclosed", listing.get("disclosed_at") or "—"),
        ("Reporter", f"[{listing.get('reporter') or '—'}]"
                     f"(https://hackerone.com/{listing.get('reporter') or ''})"),
    ]
    header = "\n".join(f"| **{k}** | {v} |" for k, v in rows)
    title = payload.get("title") or listing.get("title") or "(untitled)"
    return (
        f"# {title}\n\n"
        f"| | |\n|---|---|\n{header}\n\n"
        f"## Vulnerability details\n\n{body.strip()}\n"
    )


def pull(
    conn,
    reports_dir: Path,
    *,
    weakness: str | None = None,
    program: str | None = None,
    since: str | None = None,
    max_pages: int | None = None,
    limit_bodies: int | None = None,
    delay: float = 1.0,
    list_only: bool = False,
) -> dict[str, Any]:
    """Run enumeration then body-fetch. Returns a summary incl. newly disclosed ids."""
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    limiter = http.RateLimiter(delay)
    now = _now()

    # Phase 1: enumerate. Records which ids are brand new. max_pages < 0 skips
    # enumeration entirely, so a body-only run doesn't re-walk the whole feed.
    new_ids: list[dict[str, Any]] = []
    listed = 0
    rows = () if (max_pages is not None and max_pages < 0) else enumerate_reports(
        weakness=weakness, program=program, since=since,
        max_pages=max_pages, limiter=limiter)
    for row in rows:
        listed += 1
        if store.upsert_listing(conn, row, now):
            new_ids.append(row)
        if listed % 200 == 0:
            conn.commit()
            logger.info("listed %d reports ...", listed)
    conn.commit()
    logger.info("enumeration done: %d listed, %d new", listed, len(new_ids))

    if list_only:
        return {"listed": listed, "new": new_ids, "fetched": 0, "empty": 0, "gone": 0}

    # Reconcile against the filesystem before fetching. state.db is gitignored,
    # so a fresh clone starts with no state even though reports/ is populated;
    # without this, cloning the repo would re-download every committed report.
    reconciled = 0
    for rid in store.pending_ids(conn):
        if (reports_dir / f"{rid}.md").exists():
            store.mark(conn, rid, store.OK, now,
                       (reports_dir / f"{rid}.md").stat().st_size)
            reconciled += 1
    if reconciled:
        conn.commit()
        logger.info("adopted %d report(s) already on disk", reconciled)

    # Phase 2: fetch bodies for anything still pending.
    pending = store.pending_ids(conn, limit=limit_bodies)
    fetched = empty = gone = failed = 0
    for i, rid in enumerate(pending, 1):
        listing = dict(conn.execute("SELECT * FROM reports WHERE id=?", (rid,)).fetchone())
        try:
            payload = fetch_body(rid, limiter)
        except http.NotFound:
            store.mark(conn, rid, store.GONE, _now())
            gone += 1
        except http.HttpError as exc:
            logger.warning("report %s failed: %s", rid, exc)
            failed += 1
        else:
            md = render_markdown(payload, listing)
            if md is None:
                store.mark(conn, rid, store.EMPTY, _now(), 0)
                empty += 1
            else:
                # newline="" keeps the LF we wrote; Python would otherwise
                # translate to CRLF on Windows and churn the diff on every OS swap.
                with open(reports_dir / f"{rid}.md", "w",
                          encoding="utf-8", newline="") as fh:
                    fh.write(md)
                store.mark(conn, rid, store.OK, _now(), len(md))
                fetched += 1
        if i % 50 == 0:
            conn.commit()
            logger.info("bodies %d/%d (%d ok, %d empty, %d gone)",
                        i, len(pending), fetched, empty, gone)
    store.set_meta(conn, "last_pull", now)
    conn.commit()

    return {"listed": listed, "new": new_ids, "fetched": fetched,
            "empty": empty, "gone": gone, "failed": failed}


# --- allowlist helpers -----------------------------------------------------

def _rel_attr(rel: dict[str, Any], key: str) -> dict[str, Any]:
    node = rel.get(key)
    if isinstance(node, dict):
        data = node.get("data")
        if isinstance(data, dict):
            attr = data.get("attributes")
            return attr if isinstance(attr, dict) else {}
    return {}


def _clean(v: Any) -> str | None:
    if not isinstance(v, str):
        return None
    v = v.strip()
    return v or None


def _num(v: Any) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _int(v: Any) -> int | None:
    n = _num(v)
    return int(n) if n is not None else None


def _date(v: Any) -> str | None:
    s = _clean(v)
    return s[:10] if s and len(s) >= 10 else s
