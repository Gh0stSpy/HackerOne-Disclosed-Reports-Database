"""Tooling for building a local database of disclosed HackerOne reports.

Two data sources, both public and unauthenticated:

* The report *list* comes from HackerOne's official Hacker API hacktivity
  endpoint, filtered to ``disclosed:true AND substate:resolved`` so only valid,
  resolved, publicly disclosed reports are ever pulled.
* The report *body* comes from ``hackerone.com/reports/<id>.json``.

Everything is resumable and rate-limited; see :mod:`h1db.pull`.
"""

from __future__ import annotations

__version__ = "1.0.0"
