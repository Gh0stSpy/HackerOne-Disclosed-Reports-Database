---
name: hunt-ssrf
description: Find server-side request forgery (SSRF) in web targets — where it hides, how to confirm it blind, and how disclosed reports bypassed the filters that were supposed to stop it. Use when testing a web app or API for SSRF, reviewing URL-handling code, or triaging a suspected SSRF.
---

# Hunting SSRF

Synthesised from 28 disclosed, resolved HackerOne SSRF reports (2019–2026,
$52k+ in bounties). Every technique below cites the report(s) it came from, as
`H1#<id>` → `hackerone.com/reports/<id>`. Read those before trusting a claim.

> The source reports are third-party write-ups. This skill distils them; it is
> not a licence to test systems you are not authorised to test.

## Where SSRF actually lives

Disclosed SSRF clusters in a handful of features. When you see one of these on a
target, prioritise it:

- **Link preview / URL unfurling** — chat and social features that fetch a URL
  to render a title/thumbnail. `H1#1960765` (Reddit Matrix `preview_url`, $6k).
- **Import / fetch-from-URL** — "import from URL", remote attachments, media
  fetchers. `H1#3473145` (Rocket.Chat SMS media fetch, unauthenticated).
- **Connection / integration "test" buttons** — admin panels that verify a
  webhook, database, or API endpoint by connecting to it. `H1#2123113`
  (Airflow connection test → Slack API, CVE-2023-37379, $2,550).
- **Stored webhook / push / callback URLs** — a URL you save now, the server
  calls later. Often lower auth than admin. `H1#3608558` (phpBB Web Push
  endpoint, only a *registered user* needed).
- **Document / PDF / analytics generators** — server renders something from a
  URL you influence. `H1#2262382` (HackerOne analytics reports → internal file
  read, **$25,000, critical**).
- **GraphQL fields that take a URL** — a `source`/`url` argument passed straight
  into a GET. `H1#1864188` (Exness `allTicks(source:)`, $3k).

Recon signal: grep the app for parameters named `url`, `uri`, `src`, `source`,
`dest`, `redirect`, `callback`, `webhook`, `endpoint`, `feed`, `target`,
`image`, `import`. Any of them reaching a server-side HTTP client is a candidate.

## Confirming it (usually blind)

Most disclosed SSRF is **blind** — no response body comes back. Confirm out-of-band:

1. Point the parameter at a **Burp Collaborator / interactsh / OAST** host and
   watch for DNS + HTTP callbacks. Used in `H1#1864188`, `H1#2123113`, and 5
   more in the set.
2. If fully blind, extract signal from **side channels**: a reflected `og:title`
   from the link-preview response (`H1#1960765` enumerated internal services and
   port-scanned this way), or response-time differences between open and closed
   ports.
3. Escalate to **impact**: reach a cloud metadata endpoint (below), read an
   internal admin panel, or turn blind→full-read if any response is reflected.

## The payloads that worked

### Cloud metadata (the standard escalation)
```
http://169.254.169.254/latest/meta-data/            # AWS
http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>
http://100.100.100.200/latest/meta-data/            # Alibaba
http://metadata.google.internal/computeMetadata/v1/ # GCP (needs Metadata-Flavor: Google)
```
Cloud metadata targets appear in 5 of the 28 reports. `H1#1702864` specifically
notes the Alibaba `100.100.100.200` IP as one defenders forget.

### Internal targets
```
http://127.0.0.1:<port>/      http://localhost/      http://[::1]/
http://192.168.x.x/  http://10.x.x.x/  http://172.16-31.x.x/   # RFC1918
```

## Bypassing the filter (this is where the bounties are)

Most modern targets *have* an SSRF filter. The disclosed reports are almost all
**filter bypasses** — study these, because a naive `169.254.169.254` will be
blocked:

- **DNS rebinding** — submit an attacker domain that resolves public on the
  first lookup (passing the check) and to an internal IP on the second (the
  actual fetch). `H1#3473145` bypassed Rocket.Chat's `checkUrlForSsrf` with a
  `TTL=0` record flipping `1.1.1.1` → `192.168.100.14`. This also beat the
  earlier CVE fix — **re-test patched SSRF for TOCTOU gaps.**
- **Alphanumeric / alternate IP encodings** — decimal, octal, hex, and
  mixed forms that `filter_var` accepts but the blocklist misses. `H1#1702864`
  bypassed Nextcloud's `ThrowIfLocalIp` this way.
- **IPv6 tricks** — IPv4-mapped IPv6 (`::ffff:127.0.0.1`), IPv4-in-IPv6
  nesting, and NAT64 prefixes. `H1#3634400` used the NAT64 *local-use* prefix
  `64:ff9b:1::/48`, which `ssrf_filter` blocked one sibling of but not this one.
- **Windows UNC paths** — on Windows servers, `\\attacker\share` style targets
  can leak NTLM hashes outbound. `H1#2585385` (Apache httpd, CVE-2024-38472,
  $4,920).
- **Redirect-based** — point at an attacker URL that 30x-redirects to the
  internal target, so the *initial* URL passes validation but the fetch lands
  internally.

Pattern to remember: filters that validate the **hostname/URL string** rather
than the **resolved connection IP** are bypassable by rebinding or redirect;
filters that check the first DNS answer but not the connected one are bypassable
by rebinding. Nearly every bypass in this set is one of those two root causes.

## What made the high-bounty ones land

- **Prove real impact, don't stop at "it makes a request."** The $25k
  (`H1#2262382`) was SSRF → **internal file read**. Blind SSRF alone paid
  hundreds; SSRF reaching credentials/metadata/admin paid thousands.
- **Show the reachable internal target**, even for blind SSRF — enumerate a
  service, name a port, or demonstrate the metadata endpoint responds.
- **Ask before escalating into internal networks.** `H1#1960765` explicitly
  requested permission before attempting RCE from the SSRF — good practice that
  keeps you in scope.

## Fast checklist

1. Enumerate URL-ish parameters and the six feature types above.
2. Fire each at an OAST host; confirm DNS/HTTP callback.
3. If filtered, try in order: redirect → DNS rebinding → alt IP encoding →
   IPv6/NAT64 → (Windows) UNC.
4. Escalate to metadata / internal read for impact.
5. Report with the concrete internal target reached, not just the callback.

---
*Generated by [h1db](https://github.com/Gh0stSpy/HackerOne-Disclosed-Reports-Database)
from disclosed reports. Regenerate with `python -m h1db set ssrf` then re-synthesise.*
