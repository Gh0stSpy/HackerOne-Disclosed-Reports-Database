"""Discord notifications for newly disclosed reports.

The webhook URL is read from the ``DISCORD_WEBHOOK_URL`` environment variable
(or a gitignored ``.env`` beside the repo root). It is never committed, never
logged, and never echoed back — a Discord webhook is a bearer credential: anyone
holding it can post to the channel.

If no webhook is configured this degrades to a no-op, so cron jobs and CI runs
work fine without one.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger("h1db.notify")

ENV_VAR = "DISCORD_WEBHOOK_URL"

#: Discord hard-limits embeds per message.
MAX_EMBEDS = 10

SEVERITY_COLOUR = {
    "critical": 0x992D22,
    "high": 0xE74C3C,
    "medium": 0xE67E22,
    "low": 0xF1C40F,
    "none": 0x95A5A6,
}


def webhook_url(root: Path | None = None) -> str | None:
    """Resolve the webhook from the environment, falling back to a local .env."""
    url = os.environ.get(ENV_VAR, "").strip()
    if url:
        return url
    if root:
        env_file = Path(root) / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith(f"{ENV_VAR}=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip().strip("'\"") or None
    return None


def _embed(report: dict[str, Any]) -> dict[str, Any]:
    rid = report.get("id")
    bounty = report.get("bounty")
    fields = [
        {"name": "Program", "value": str(report.get("program") or "—"), "inline": True},
        {"name": "Weakness", "value": str(report.get("weakness") or "—"), "inline": True},
        {"name": "Severity", "value": str(report.get("severity") or "—"), "inline": True},
    ]
    if bounty:
        fields.append({"name": "Bounty", "value": f"${float(bounty):,.0f}", "inline": True})
    return {
        "title": (report.get("title") or "(untitled)")[:250],
        "url": f"https://hackerone.com/reports/{rid}",
        "color": SEVERITY_COLOUR.get(str(report.get("severity") or "").lower(), 0x5865F2),
        "fields": fields,
        "footer": {"text": f"Report #{rid} · disclosed {report.get('disclosed_at') or '—'}"},
    }


def send_new_reports(
    reports: list[dict[str, Any]],
    *,
    root: Path | None = None,
    url: str | None = None,
    max_items: int = 10,
) -> bool:
    """Post newly disclosed reports to Discord. Returns True if anything was sent.

    A no-op (returning False) when there is nothing new or no webhook is set.
    """
    if not reports:
        logger.info("no new reports; nothing to notify")
        return False

    url = url or webhook_url(root)
    if not url:
        logger.info("no %s configured; skipping Discord notification", ENV_VAR)
        return False

    # Highest bounty first so the most interesting ones survive the cap.
    ranked = sorted(reports, key=lambda r: (r.get("bounty") or 0), reverse=True)
    shown, extra = ranked[:max_items][:MAX_EMBEDS], max(0, len(ranked) - MAX_EMBEDS)

    content = f"**{len(reports)} newly disclosed HackerOne report(s)**"
    if extra:
        content += f" — showing top {len(shown)}, {extra} more in the repo"

    payload = {
        "content": content,
        "embeds": [_embed(r) for r in shown],
        "allowed_mentions": {"parse": []},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "h1db/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            logger.info("Discord notified (%d embeds, HTTP %s)",
                        len(shown), response.status)
            return True
    except Exception as exc:  # noqa: BLE001 - notification must never break a pull
        # Deliberately does not include the URL in the message.
        logger.warning("Discord notification failed: %s", type(exc).__name__)
        return False
