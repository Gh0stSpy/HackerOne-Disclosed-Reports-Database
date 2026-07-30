#!/usr/bin/env bash
# Pull new disclosed reports, rebuild the indexes, commit, push, notify Discord.
#
# This is what cron runs. It is safe to run repeatedly: pulling is incremental,
# indexing is deterministic, and it exits quietly when nothing changed.
#
#   ./update.sh            incremental (default) — seconds once seeded
#   ./update.sh --full     walk the entire feed, e.g. a first run
#   ./update.sh --no-push  build locally, don't touch the remote
set -euo pipefail

cd "$(dirname "$0")"

# Pick an interpreter: python3 on Linux/Kali, the py launcher on Git Bash.
# Windows ships a python3.exe stub that exists on PATH but only advertises the
# Microsoft Store, so presence is not enough — each candidate must actually run.
if [ -z "${PYTHON:-}" ]; then
  for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1 &&
       "$candidate" -c 'import sys; sys.exit(0)' >/dev/null 2>&1; then
      PYTHON="$candidate"
      break
    fi
  done
fi
if [ -z "${PYTHON:-}" ]; then
  echo "no working Python found (tried python3, python, py)" >&2
  exit 1
fi
DELAY="${H1DB_DELAY:-1.0}"
BODIES="${H1DB_BODIES:-500}"     # cap bodies per run so a cron tick stays short
PUSH=1
PAGES="--max-pages 6"            # ~300 newest reports; plenty for a daily check

for arg in "$@"; do
  case "$arg" in
    --full)    PAGES="" ; BODIES="${H1DB_BODIES:-100000}" ;;
    --no-push) PUSH=0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

# Single-instance lock: a slow full run must not overlap the next cron tick.
LOCK=".update.lock"
if [ -e "$LOCK" ] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  echo "update already running (pid $(cat "$LOCK")); exiting"
  exit 0
fi
echo $$ > "$LOCK"
trap 'rm -f "$LOCK"' EXIT

# A failed pull or index must never reach the commit step — committing a broken
# or half-written state is worse than doing nothing.
echo "==> pulling new reports"
# shellcheck disable=SC2086
if ! "$PYTHON" -m h1db pull $PAGES --limit-bodies "$BODIES" --delay "$DELAY"; then
  echo "pull failed; leaving the repo untouched" >&2
  exit 1
fi

echo "==> rebuilding indexes"
if ! "$PYTHON" -m h1db index; then
  echo "index failed; leaving the repo untouched" >&2
  exit 1
fi

if [ -d .git ]; then
  if [ -n "$(git status --porcelain)" ]; then
    echo "==> committing"
    git add -A
    git commit -q -m "Update disclosed reports ($(date -u +%Y-%m-%d\ %H:%M) UTC)"
    if [ "$PUSH" -eq 1 ]; then
      echo "==> pushing"
      git push -q || echo "   push failed (check credentials); commit is local"
    fi
  else
    echo "==> no changes"
  fi
fi

echo "==> notifying"
"$PYTHON" -m h1db notify

echo "==> done"
"$PYTHON" -m h1db stats
