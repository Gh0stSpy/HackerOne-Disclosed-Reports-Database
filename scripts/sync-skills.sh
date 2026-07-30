#!/usr/bin/env bash
# Install the generated hunting skills into a Claude Code skills directory.
#
# The canonical skills live in this repo under skills/hunt-<class>/ so they stay
# version-controlled and shareable. This copies them to where Claude Code loads
# skills, renaming hunt-<class> -> skill-hunt-<class> to match a skill-* naming
# convention. Copy (not symlink) because skills dirs are often cloud-synced,
# where symlinks break.
#
# Usage:
#   SKILLS_DIR=/home/ghost/BugBounty/Skills ./scripts/sync-skills.sh
#   ./scripts/sync-skills.sh            # defaults to ~/.claude/skills
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO/skills"
DST="${SKILLS_DIR:-$HOME/.claude/skills}"
PREFIX="${SKILL_PREFIX:-skill-}"

mkdir -p "$DST"

count=0
for dir in "$SRC"/hunt-*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"          # hunt-ssrf
    dest="$DST/${PREFIX}${name}"       # .../skill-hunt-ssrf
    rm -rf "$dest"
    cp -r "$dir" "$dest"
    echo "  installed ${PREFIX}${name}"
    count=$((count + 1))
done

echo "synced $count skill(s) -> $DST"
