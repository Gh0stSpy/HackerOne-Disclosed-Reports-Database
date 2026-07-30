#!/usr/bin/env bash
# Install the auto-updater on Kali/WSL so it runs when you open the machine.
#
# WSL has no real boot and often no running cron, so "on open" is implemented as
# a guarded hook in your shell rc: the first shell of the day kicks off a
# detached update, and later shells do nothing. That keeps terminal startup
# instant — you never wait on the network.
#
#   ./scripts/install-wsl.sh            # install (idempotent)
#   ./scripts/install-wsl.sh --cron     # also add a 6-hourly cron entry
#   ./scripts/install-wsl.sh --remove   # uninstall
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
MARKER_BEGIN="# >>> h1db auto-update >>>"
MARKER_END="# <<< h1db auto-update <<<"

rc_file() {
  case "${SHELL##*/}" in
    zsh)  echo "$HOME/.zshrc" ;;
    *)    echo "$HOME/.bashrc" ;;
  esac
}
RC="$(rc_file)"

remove_block() {
  [ -f "$RC" ] || return 0
  if grep -qF "$MARKER_BEGIN" "$RC"; then
    sed -i "/$(printf '%s' "$MARKER_BEGIN" | sed 's/[][\.*^$/]/\\&/g')/,/$(printf '%s' "$MARKER_END" | sed 's/[][\.*^$/]/\\&/g')/d" "$RC"
    echo "removed existing block from $RC"
  fi
}

if [ "${1:-}" = "--remove" ]; then
  remove_block
  crontab -l 2>/dev/null | grep -v "h1db/update.sh" | crontab - 2>/dev/null || true
  echo "uninstalled."
  exit 0
fi

command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
chmod +x "$REPO/update.sh"

remove_block
cat >> "$RC" <<EOF
$MARKER_BEGIN
# Runs at most once per day, detached, so the shell never blocks on it.
h1db_auto_update() {
  local repo="$REPO"
  local stamp="\$repo/.last-auto-update"
  local today; today="\$(date -u +%Y-%m-%d)"
  [ -f "\$stamp" ] && [ "\$(cat "\$stamp" 2>/dev/null)" = "\$today" ] && return 0
  echo "\$today" > "\$stamp"
  ( setsid nohup "\$repo/update.sh" >> "\$repo/logs/auto-update.log" 2>&1 & ) >/dev/null 2>&1
}
h1db_auto_update
$MARKER_END
EOF

mkdir -p "$REPO/logs"
grep -qxF 'logs/' "$REPO/.gitignore" 2>/dev/null || echo 'logs/' >> "$REPO/.gitignore"

echo "installed shell hook in $RC"

if [ "${1:-}" = "--cron" ]; then
  if command -v crontab >/dev/null; then
    ( crontab -l 2>/dev/null | grep -v "h1db/update.sh"
      echo "0 */6 * * * cd $REPO && ./update.sh >> $REPO/logs/cron.log 2>&1" ) | crontab -
    echo "added 6-hourly cron entry"
    service cron status >/dev/null 2>&1 || \
      echo "NOTE: cron isn't running. Start it with: sudo service cron start"
  else
    echo "crontab not available; skipping cron entry"
  fi
fi

cat <<EOF

Done. Next steps:
  1. Set your Discord webhook (never commit it):
       echo 'DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...' > $REPO/.env
  2. Test it:
       cd $REPO && python3 -m h1db notify --test
  3. Seed the database (long, one time — run it in tmux/screen):
       cd $REPO && ./update.sh --full
  4. Open a new shell to activate the hook.

Logs: $REPO/logs/auto-update.log
EOF
