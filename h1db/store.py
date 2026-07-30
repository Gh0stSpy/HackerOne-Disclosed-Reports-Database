"""Local state for the puller: a small SQLite index of every known report.

The markdown files under ``reports/`` are the deliverable; this database is just
bookkeeping so the puller is resumable and idempotent. Each report moves through
``fetch_state``:

* ``listed``  — seen in the hacktivity feed, body not yet fetched
* ``ok``      — body fetched and a markdown file written
* ``empty``   — disclosed but no body (content lived in the comment thread)
* ``gone``    — the .json 404'd; never retried

Storing progress here rather than inferring it from the filesystem means a run
can be killed at any point and resumed without re-fetching or re-listing.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Iterable

logger = logging.getLogger("h1db.store")

LISTED, OK, EMPTY, GONE = "listed", "ok", "empty", "gone"

_SCHEMA = """
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS reports (
    id                INTEGER PRIMARY KEY,
    title             TEXT,
    program           TEXT,
    program_handle    TEXT,
    reporter          TEXT,
    weakness          TEXT,
    cwe               TEXT,
    severity          TEXT,
    bounty            REAL,
    cve_ids           TEXT,
    substate          TEXT,
    disclosed_at      TEXT,
    votes             INTEGER,
    fetch_state       TEXT NOT NULL DEFAULT 'listed',
    body_chars        INTEGER,
    first_seen        TEXT,
    fetched_at        TEXT
);
CREATE INDEX IF NOT EXISTS idx_state    ON reports(fetch_state);
CREATE INDEX IF NOT EXISTS idx_weakness ON reports(weakness);
CREATE INDEX IF NOT EXISTS idx_program  ON reports(program_handle);
CREATE INDEX IF NOT EXISTS idx_disc     ON reports(disclosed_at);

CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def upsert_listing(conn: sqlite3.Connection, row: dict[str, Any], now: str) -> bool:
    """Insert a freshly listed report, or refresh its metadata if already known.

    Returns True if this id was not previously in the database — i.e. a genuinely
    newly disclosed report, which is what the Discord notifier keys off.
    """
    existing = conn.execute(
        "SELECT fetch_state FROM reports WHERE id = ?", (row["id"],)
    ).fetchone()

    if existing is None:
        conn.execute(
            """INSERT INTO reports
               (id, title, program, program_handle, reporter, weakness, cwe,
                severity, bounty, cve_ids, substate, disclosed_at, votes,
                fetch_state, first_seen)
               VALUES
               (:id, :title, :program, :program_handle, :reporter, :weakness, :cwe,
                :severity, :bounty, :cve_ids, :substate, :disclosed_at, :votes,
                'listed', :now)""",
            {**row, "now": now},
        )
        return True

    # Keep metadata fresh (votes/bounty/severity can change) without disturbing
    # fetch_state, so we don't re-fetch a body we already have.
    conn.execute(
        """UPDATE reports SET
             title=:title, program=:program, program_handle=:program_handle,
             reporter=:reporter, weakness=:weakness, cwe=:cwe, severity=:severity,
             bounty=:bounty, cve_ids=:cve_ids, substate=:substate,
             disclosed_at=:disclosed_at, votes=:votes
           WHERE id=:id""",
        row,
    )
    return False


def mark(conn: sqlite3.Connection, report_id: int, state: str,
         now: str, body_chars: int | None = None) -> None:
    conn.execute(
        "UPDATE reports SET fetch_state=?, body_chars=?, fetched_at=? WHERE id=?",
        (state, body_chars, now, report_id),
    )


def pending_ids(conn: sqlite3.Connection, limit: int | None = None) -> list[int]:
    """Report ids that have been listed but whose body is not yet fetched."""
    # limit=None means "no cap"; limit=0 means "none", which is what a caller
    # asking for zero bodies actually wants. Treating 0 as falsy would silently
    # fetch the entire backlog.
    if limit is not None and limit <= 0:
        return []
    sql = "SELECT id FROM reports WHERE fetch_state = 'listed' ORDER BY id DESC"
    if limit is not None:
        sql += f" LIMIT {int(limit)}"
    return [r["id"] for r in conn.execute(sql)]


def all_reports(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Every report with a body, richest metadata first — used by the indexer."""
    return [
        dict(r) for r in conn.execute(
            "SELECT * FROM reports WHERE fetch_state IN ('ok','empty') "
            "ORDER BY (bounty IS NULL), bounty DESC, votes DESC"
        )
    ]


def counts(conn: sqlite3.Connection) -> dict[str, int]:
    out = {r["fetch_state"]: r["n"] for r in conn.execute(
        "SELECT fetch_state, COUNT(*) n FROM reports GROUP BY fetch_state")}
    out["total"] = conn.execute("SELECT COUNT(*) n FROM reports").fetchone()["n"]
    return out


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta(key,value) VALUES(?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))


def get_meta(conn: sqlite3.Connection, key: str, default: str | None = None):
    row = conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def dump_jsonl(reports: Iterable[dict[str, Any]], path: str | Path) -> int:
    """Write reports as newline-delimited JSON — the git-friendly data export."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ("id", "title", "program", "program_handle", "reporter", "weakness",
              "cwe", "severity", "bounty", "cve_ids", "substate", "disclosed_at",
              "votes", "body_chars")
    n = 0
    with path.open("w", encoding="utf-8") as fh:
        for r in reports:
            record = {k: r.get(k) for k in fields}
            if isinstance(record.get("cve_ids"), str):
                try:
                    record["cve_ids"] = json.loads(record["cve_ids"])
                except (json.JSONDecodeError, TypeError):
                    record["cve_ids"] = []
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            n += 1
    return n
