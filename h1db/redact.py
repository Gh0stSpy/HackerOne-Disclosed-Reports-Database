"""Strip live credentials out of report bodies before they are written to disk.

Disclosed reports routinely contain real secrets: an SSRF proof-of-concept that
dumps EC2 instance credentials, a leaked API key quoted verbatim, a JWT captured
mid-session. HackerOne hosts that content, but re-publishing it in a git repo is
a different act — the secret becomes trivially greppable, permanently, in a
place credential scanners already crawl. GitHub push protection blocks it, and
that block is correct.

So each body is scrubbed on the way in. The goal is to keep the report *useful*
— you can still see that a key was leaked, its type, and its prefix — while
removing the exploitable material. Patterns are conservative: they target
high-confidence credential shapes rather than anything that looks random, so
payloads, hashes and example values survive intact.
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger("h1db.redact")

PLACEHOLDER = "[REDACTED-{kind}]"

#: (name, compiled pattern, group holding the secret). Where a pattern has a
#: prefix group we keep the prefix, which preserves the teaching value.
_RULES: list[tuple[str, re.Pattern[str], int]] = [
    # --- cloud ---
    ("AWS-KEY-ID", re.compile(r"\b((?:AKIA|ASIA|AIDA|AROA|AGPA|ANPA|ANVA|APKA)[A-Z0-9]{16})\b"), 1),
    # The label-to-value gap allows up to 8 non-word chars so quoted JSON
    # (`"SecretAccessKey" : "`) and YAML/env forms all match.
    ("AWS-SECRET", re.compile(
        r"(?i)(?:secret[_-]?access[_-]?key|aws[_-]?secret)\W{0,8}([A-Za-z0-9/+=]{40})"), 1),
    ("AWS-SESSION-TOKEN", re.compile(
        r"(?i)(?:session[_-]?token|aws[_-]?session[_-]?token|\"Token\")\W{0,8}([A-Za-z0-9/+=]{100,})"), 1),
    ("GCP-KEY", re.compile(r"\b(AIza[0-9A-Za-z_\-]{35})\b"), 1),
    ("AZURE-SAS", re.compile(r"(?i)\b(sig=[A-Za-z0-9%/+=]{40,})"), 1),

    # --- source forges / package registries ---
    ("GITHUB-TOKEN", re.compile(r"\b((?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,})\b"), 1),
    ("GITHUB-PAT", re.compile(r"\b(github_pat_[A-Za-z0-9_]{60,})\b"), 1),
    ("GITLAB-TOKEN", re.compile(r"\b(glpat-[A-Za-z0-9_\-]{20,})\b"), 1),
    ("NPM-TOKEN", re.compile(r"\b(npm_[A-Za-z0-9]{36})\b"), 1),

    # --- SaaS ---
    ("SLACK-TOKEN", re.compile(r"\b(xox[baprs]-[A-Za-z0-9\-]{10,})\b"), 1),
    ("SLACK-WEBHOOK", re.compile(r"(https://hooks\.slack\.com/services/[A-Za-z0-9/]{20,})"), 1),
    ("DISCORD-WEBHOOK", re.compile(
        r"(https://(?:canary\.|ptb\.)?discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_\-]{20,})"), 1),
    ("STRIPE-KEY", re.compile(r"\b((?:sk|rk)_live_[A-Za-z0-9]{20,})\b"), 1),
    ("SENDGRID-KEY", re.compile(r"\b(SG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,})\b"), 1),
    ("TWILIO-SID", re.compile(r"\b(AC[a-f0-9]{32})\b"), 1),
    ("MAILGUN-KEY", re.compile(r"\b(key-[a-f0-9]{32})\b"), 1),
    ("OPENAI-KEY", re.compile(r"\b(sk-(?:proj-)?[A-Za-z0-9_\-]{32,})\b"), 1),
    ("WAKATIME-KEY", re.compile(r"\b(waka_[0-9a-fA-F]{8}-[0-9a-fA-F\-]{20,})\b"), 1),
    # Salesforce session IDs: org id, "!", then the token. Also matches the
    # URL-encoded "%21" form that shows up inside captured Cookie headers.
    ("SALESFORCE-SESSION", re.compile(
        r"\b(00D[A-Za-z0-9]{5,20}(?:!|%21)[A-Za-z0-9._%\-]{20,})"), 1),

    # --- generic ---
    ("PRIVATE-KEY", re.compile(
        r"(-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----)"
        r"[\s\S]{0,4000}?"
        r"(-----END (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----)"), 0),
    ("JWT", re.compile(r"\b(eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,})\b"), 1),
]


def scrub(text: str) -> tuple[str, dict[str, int]]:
    """Redact credentials in ``text``.

    Returns the scrubbed text and a ``{kind: count}`` tally. Idempotent: running
    it over already-scrubbed text is a no-op.
    """
    if not text:
        return text, {}

    tally: dict[str, int] = {}

    for kind, pattern, group in _RULES:
        placeholder = PLACEHOLDER.format(kind=kind)

        def _replace(match: re.Match[str], _kind=kind, _group=group,
                     _ph=placeholder) -> str:
            tally[_kind] = tally.get(_kind, 0) + 1
            if _kind == "PRIVATE-KEY":
                # Keep the BEGIN/END envelope so the reader still sees what leaked.
                return f"{match.group(1)}\n{_ph}\n{match.group(2)}"
            secret = match.group(_group)
            whole = match.group(0)
            # Preserve any label/prefix the pattern matched around the secret.
            return whole.replace(secret, _ph)

        text = pattern.sub(_replace, text)

    return text, tally


def scrub_file(path, dry_run: bool = False) -> dict[str, int]:
    """Scrub a markdown file in place. Returns the tally of what was redacted."""
    from pathlib import Path
    path = Path(path)
    original = path.read_text(encoding="utf-8", errors="replace")
    cleaned, tally = scrub(original)
    if tally and not dry_run and cleaned != original:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(cleaned)
    return tally
