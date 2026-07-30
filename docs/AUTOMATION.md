# Automation

How to keep the database fresh and get pinged when new reports drop.

## Quick start (Kali / WSL)

```bash
git clone https://github.com/Gh0stSpy/HackerOne-Disclosed-Reports-Database
cd HackerOne-Disclosed-Reports-Database
./scripts/install-wsl.sh --cron
```

Then seed it once (this is the long part — a few hours):

```bash
./update.sh --full
```

Run that inside `tmux` or `screen` so closing the terminal doesn't kill it.

## How "run when I open WSL" works

WSL has no real boot sequence and usually no cron daemon running, so a systemd
timer isn't reliable there. The installer instead adds a small guarded function
to your `~/.bashrc` (or `~/.zshrc`):

- The **first shell you open each day** kicks off `update.sh` **detached**, so
  your prompt returns instantly and never waits on the network.
- Every later shell that day sees the datestamp file and does nothing.
- Output goes to `logs/auto-update.log`.

Add `--cron` and you also get a 6-hourly job for machines that stay up. If cron
isn't running under WSL:

```bash
sudo service cron start
```

To make that persist across WSL restarts, add to `/etc/wsl.conf`:

```ini
[boot]
command = service cron start
```

## Discord notifications

Create a webhook (Server Settings → Integrations → Webhooks), then:

```bash
echo 'DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...' > .env
python3 -m h1db notify --test
```

You should see a test embed appear in the channel. After that, every `update.sh`
run posts an embed per newly disclosed report — title, program, weakness,
severity, bounty, and a link.

**The webhook is a bearer credential**: anyone with the URL can post to your
channel. `.env` is gitignored, the URL is never logged, and it is never included
in error messages. Don't paste it into a commit, an issue, or a screenshot.

Notifications are best-effort — if Discord is unreachable the pull still
succeeds, and the queued items retry on the next run.

## Commands

| Command | What it does |
|---|---|
| `python3 -m h1db pull` | Fetch newly disclosed reports |
| `python3 -m h1db index` | Rebuild browsable views + README |
| `python3 -m h1db notify` | Send queued notifications |
| `python3 -m h1db update` | pull → index → notify |
| `python3 -m h1db stats` | Show database contents |
| `./update.sh` | The above, plus git commit/push |
| `./update.sh --full` | Walk the entire feed (first run) |
| `./update.sh --no-push` | Build locally, don't touch the remote |

Useful environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `H1DB_DELAY` | `1.0` | Seconds between requests. Please don't lower it. |
| `H1DB_BODIES` | `500` | Max bodies fetched per run |
| `DISCORD_WEBHOOK_URL` | — | Where to post notifications |

## Rate limiting

One request per second, single-threaded, with exponential backoff on 429/5xx.
The endpoints are public and free; there is no reason to hammer them. A full
seed is ~9,800 requests (a few hours). After that, daily runs are seconds.

## Notes and limits

- HackerOne caps pagination at **10,000 rows** (page 200 × 50). That is the
  ceiling on what the hacktivity feed exposes.
- About **10% of disclosed reports have no body** — "limited disclosure", where
  the substance stayed in the comment thread. These are recorded with metadata
  and skipped for markdown. Newly disclosed reports are disproportionately in
  this group.
- Reports that 404 are remembered and never retried.
