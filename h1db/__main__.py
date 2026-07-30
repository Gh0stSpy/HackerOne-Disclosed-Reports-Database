"""Command-line entry point: ``python -m h1db <command>``.

Commands:
    pull    fetch newly disclosed reports from HackerOne
    index   regenerate the browsable views and README
    notify  send pending new-report notifications to Discord
    update  pull + index + notify, i.e. what cron runs
    stats   show what is in the local database
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import index_site, notify, redact, sets, store
from .pull import pull

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "state.db"
DEFAULT_REPORTS = ROOT / "reports"

#: New reports found by `pull` are queued here so `notify` can run as a separate
#: step (useful in CI, where posting happens only after a successful commit).
PENDING_NOTIFY = ROOT / ".pending-notify.json"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="h1db",
        description="Build a database of disclosed HackerOne reports, "
                    "direct from HackerOne's official API.",
    )
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--reports", type=Path, default=DEFAULT_REPORTS)
    p.add_argument("--root", type=Path, default=ROOT)
    sub = p.add_subparsers(dest="command", required=True)

    for name, help_text in (("pull", "fetch newly disclosed reports"),
                            ("update", "pull + index + notify (what cron runs)")):
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("--weakness", help='e.g. "Server-Side Request Forgery (SSRF)"')
        sp.add_argument("--program", help="program handle, e.g. gitlab")
        sp.add_argument("--since", metavar="YYYY-MM-DD")
        sp.add_argument("--max-pages", type=int,
                        help="limit listing pages (50 each); -1 skips enumeration")
        sp.add_argument("--limit-bodies", type=int, help="fetch at most N bodies")
        sp.add_argument("--list-only", action="store_true")
        sp.add_argument("--delay", type=float, default=1.0)

    st = sub.add_parser("set", help="build a working set of reports for a bug class")
    st.add_argument("presets", nargs="*", metavar="PRESET",
                    help="e.g. ssrf idor xss (omit with --list to see all)")
    st.add_argument("--weakness", action="append", default=[], metavar="TEXT",
                    help="match weakness names containing TEXT (repeatable)")
    st.add_argument("--list", action="store_true", help="show presets and counts")
    st.add_argument("--limit", type=int, default=30,
                    help="reports per set (default 30; 25-40 suits one skill)")
    st.add_argument("--min-bounty", type=float, default=0.0)
    st.add_argument("--since", metavar="YYYY-MM-DD")
    st.add_argument("--sort", choices=("bounty", "newest", "votes"), default="bounty")
    st.add_argument("--out", type=Path, default=ROOT / "sets")

    sub.add_parser("index", help="regenerate browsable views and README")
    sub.add_parser("stats", help="show database contents")
    rd = sub.add_parser("redact",
                        help="scrub credentials from already-downloaded reports")
    rd.add_argument("--dry-run", action="store_true",
                    help="report what would be redacted without writing")
    n = sub.add_parser("notify", help="send queued new-report notifications")
    n.add_argument("--test", action="store_true",
                   help="send a sample notification to verify the webhook")
    return p


def _do_pull(args, conn) -> dict:
    summary = pull(
        conn, args.reports,
        weakness=args.weakness, program=args.program, since=args.since,
        max_pages=args.max_pages, limit_bodies=args.limit_bodies,
        delay=args.delay, list_only=args.list_only,
    )
    print(f"listed {summary['listed']}, new {len(summary['new'])}, "
          f"fetched {summary['fetched']}, no-body {summary['empty']}, "
          f"gone {summary['gone']}")
    if summary["new"]:
        PENDING_NOTIFY.write_text(
            json.dumps(summary["new"], ensure_ascii=False), encoding="utf-8")
    return summary


def _do_notify(root: Path) -> bool:
    if not PENDING_NOTIFY.exists():
        print("nothing queued to notify")
        return False
    try:
        pending = json.loads(PENDING_NOTIFY.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("could not read pending notifications")
        return False
    sent = notify.send_new_reports(pending, root=root)
    if sent:
        PENDING_NOTIFY.unlink(missing_ok=True)
    return sent


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s",
                        datefmt="%H:%M:%S")
    conn = store.connect(args.db)

    if args.command == "stats":
        c = store.counts(conn)
        print(f"reports known:  {c.get('total', 0):,}")
        print(f"  with body:    {c.get('ok', 0):,}")
        print(f"  no body:      {c.get('empty', 0):,}")
        print(f"  pending:      {c.get('listed', 0):,}")
        print(f"  gone (404):   {c.get('gone', 0):,}")
        print(f"last pull:      {store.get_meta(conn, 'last_pull', 'never')}")
        return 0

    if args.command == "set":
        if args.list:
            print(f"\n{'preset':<11} {'reports':>8}  weakness match")
            print("-" * 66)
            for name, n in sets.available(conn):
                print(f"{name:<11} {n:>8}  {', '.join(sets.PRESETS[name])}")
            print("\nThen:  python -m h1db set ssrf --limit 30")
            return 0

        groups = [(p.lower(), sets.PRESETS[p.lower()])
                  for p in args.presets if p.lower() in sets.PRESETS]
        unknown = [p for p in args.presets if p.lower() not in sets.PRESETS]
        if unknown:
            print(f"unknown preset(s): {', '.join(unknown)}", file=sys.stderr)
            print(f"options: {', '.join(sets.PRESETS)}", file=sys.stderr)
            return 2
        groups += [(t, [t]) for t in args.weakness]
        if not groups:
            print("nothing selected. Try: python -m h1db set --list", file=sys.stderr)
            return 2

        all_reports = store.all_reports(conn)
        for label, patterns in groups:
            chosen = sets.select(all_reports, patterns, min_bounty=args.min_bounty,
                                 since=args.since, limit=args.limit, sort=args.sort)
            if not chosen:
                print(f"{label}: nothing matched")
                continue
            folder, n = sets.build(chosen, label, args.reports, args.out)
            print(f"{label}: {n} reports -> {folder}")
        return 0

    if args.command == "redact":
        files = sorted(Path(args.reports).glob("*.md"))
        totals: dict[str, int] = {}
        touched = 0
        for path in files:
            tally = redact.scrub_file(path, dry_run=args.dry_run)
            if tally:
                touched += 1
                for kind, n in tally.items():
                    totals[kind] = totals.get(kind, 0) + n
        verb = "would redact" if args.dry_run else "redacted"
        print(f"{verb} secrets in {touched} of {len(files)} report(s)")
        for kind, n in sorted(totals.items(), key=lambda kv: -kv[1]):
            print(f"  {n:>4}  {kind}")
        return 0

    if args.command == "index":
        result = index_site.rebuild(conn, args.root)
        print(f"indexed {result['reports']:,} reports, "
              f"{result['jsonl_rows']:,} rows in data/reports.jsonl")
        return 0

    if args.command == "notify":
        if args.test:
            ok = notify.send_new_reports(
                [{"id": 826361, "title": "Test — h1db webhook check",
                  "program": "gitlab", "weakness": "Server-Side Request Forgery (SSRF)",
                  "severity": "high", "bounty": 10000, "disclosed_at": "2020-06-07"}],
                root=args.root)
            print("test notification sent" if ok else
                  "not sent — is DISCORD_WEBHOOK_URL set?")
            return 0 if ok else 1
        return 0 if _do_notify(args.root) else 0

    if args.command == "pull":
        _do_pull(args, conn)
        return 0

    if args.command == "update":
        _do_pull(args, conn)
        result = index_site.rebuild(conn, args.root)
        print(f"indexed {result['reports']:,} reports")
        _do_notify(args.root)
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
