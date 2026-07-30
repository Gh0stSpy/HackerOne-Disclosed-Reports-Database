"""Polite, dependency-free HTTP with retries.

Both HackerOne endpoints we use are public and unmetered from our side, so the
default posture is one request per second, single-threaded, honest User-Agent.
There is no upside to going faster: the first full pull is a one-off, and every
run after it fetches a handful of new reports.

A 404 is a *fact* (the report is not publicly visible), not a transient error,
so it is surfaced as :class:`NotFound` and recorded permanently by callers.
"""

from __future__ import annotations

import gzip
import json
import logging
import random
import time
import urllib.error
import urllib.request
from typing import Any

logger = logging.getLogger("h1db.http")

USER_AGENT = "h1db/1.0 (+https://github.com/Gh0stSpy/HackerOne-Disclosed-Reports-Database)"
MAX_RESPONSE_BYTES = 64 * 1024 * 1024


class HttpError(Exception):
    """A request failed after exhausting retries."""

    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.code = code


class NotFound(HttpError):
    """The resource does not exist or is not publicly visible (404/410)."""


class RateLimiter:
    """Enforce a minimum interval between requests across all callers."""

    def __init__(self, delay: float = 1.0) -> None:
        self.delay = max(0.0, delay)
        self._last = 0.0

    def wait(self) -> None:
        if self.delay <= 0:
            return
        gap = time.monotonic() - self._last
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last = time.monotonic()


def get_bytes(
    url: str,
    *,
    limiter: RateLimiter | None = None,
    timeout: float = 30.0,
    retries: int = 4,
) -> bytes:
    """Fetch ``url``; raise :class:`NotFound` on 404/410, retry 429/5xx/network."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, */*",
            "Accept-Encoding": "gzip",
        },
    )
    last = "unknown error"
    for attempt in range(retries + 1):
        if limiter is not None:
            limiter.wait()
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw) > MAX_RESPONSE_BYTES:
                    raise HttpError(f"{url} exceeded the response size cap")
                if response.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 410):
                raise NotFound(f"{url} -> {exc.code}") from exc
            if exc.code == 429 or 500 <= exc.code < 600:
                last = f"HTTP {exc.code}"
                delay = _backoff(attempt, exc.headers.get("Retry-After"))
                logger.warning("%s on %s; retry in %.0fs", last, url, delay)
                time.sleep(delay)
                continue
            raise HttpError(f"{url} -> HTTP {exc.code}", code=exc.code) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = str(exc)
            if attempt >= retries:
                break
            delay = _backoff(attempt, None)
            logger.warning("%s on %s; retry in %.0fs", last, url, delay)
            time.sleep(delay)
    raise HttpError(f"{url} failed after {retries + 1} attempt(s): {last}")


def get_json(url: str, **kwargs: Any) -> Any:
    """Fetch ``url`` and decode JSON."""
    raw = get_bytes(url, **kwargs)
    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except json.JSONDecodeError as exc:
        raise HttpError(f"{url} did not return valid JSON: {exc}") from exc


def _backoff(attempt: int, retry_after: str | None) -> float:
    if retry_after:
        try:
            return min(120.0, max(1.0, float(retry_after)))
        except ValueError:
            pass
    return min(60.0, 2.0 ** attempt) + random.uniform(0.0, 1.0)
