# Building hunting skills from the database

The database isn't just for browsing — its point is to turn thousands of real
findings into reusable **Claude Code skills**: short markdown playbooks that tell
Claude where a bug class hides, the payloads that worked, and how disclosed
reports bypassed the filters meant to stop them.

A worked example ships in [`skills/hunt-ssrf/SKILL.md`](../skills/hunt-ssrf/SKILL.md),
built from 28 disclosed SSRF reports.

## The loop

### 1. Build a focused set

```bash
python -m h1db set --list          # bug classes and how many reports each has
python -m h1db set ssrf --limit 30 # -> sets/ssrf/ (30 reports + ranked README)
```

A "set" is just the best N reports for one class, copied into `sets/<class>/`
with a bounty-ranked README, so they can be read as one coherent batch.

Options: `--limit N` (25–40 suits one skill), `--sort bounty|newest|votes`,
`--since YYYY-MM-DD`, `--min-bounty N`, or `--weakness "free text"` for classes
without a preset.

### 2. Have Claude write the skill

In Claude Code, open this repo and give it the instructions in
[`prompts/build-skill.md`](../prompts/build-skill.md) with the class name. Claude
reads `sets/<class>/`, synthesises by technique, and writes
`skills/hunt-<class>/SKILL.md` with every claim cited to a report ID.

### 3. Review, then use

**Read the skill before trusting it.** Generated skills can overreach; the
citations exist so you can spot-check that report `H1#<id>` really shows the
claimed technique. Then copy it where Claude Code will load it:

```bash
cp -r skills/hunt-ssrf ~/.claude/skills/     # user-wide
# or into a project's .claude/skills/
```

Now "test this target for SSRF" pulls in real disclosed tradecraft instead of
generic advice.

## Why skills, not fine-tuning

A skill is a text file you can read, diff, and correct. When it gives bad
advice you see exactly which line and fix it — no retraining, no opaque weights,
no cost. The report citations keep it honest and auditable.

## Two honest limits

- **Redaction.** Many disclosed bodies black out the PoC (`█`) or put the detail
  in image attachments the JSON can't inline. Some sets are therefore rich in
  *where to look* but thin on copy-paste payloads. The prompt tells Claude to
  say so rather than fabricate.
- **Coverage.** A skill is only as good as its set. Thin classes (few disclosed
  reports) yield thin skills; check the `--list` count first.

## Automating it

Skill generation needs Claude, so it isn't part of the free `update.sh` cron.
To automate it, run [`anthropics/claude-code-action`](https://github.com/anthropics/claude-code-action)
on a schedule: build the sets, run the `build-skill.md` prompt, and open a pull
request with the new skills for review. Keep it PR-based, never auto-merge — a
bad skill silently misleads every future session.
