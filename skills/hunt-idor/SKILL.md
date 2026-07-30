---
name: hunt-idor
description: Find insecure direct object reference (IDOR) / broken object-level authorization in web apps and APIs — which identifiers to tamper, where authz checks go missing, and how disclosed reports turned an ID swap into account-level impact. Use when testing an app or API for access-control bugs, reviewing an endpoint that takes an object ID, or triaging a suspected IDOR.
---

# Hunting IDOR

Synthesised from 28 disclosed, resolved HackerOne IDOR reports (2019–2026,
$25k+ in bounties). Every technique cites its source as `H1#<id>` →
`hackerone.com/reports/<id>`. Read those before trusting a claim.

> The source reports are third-party write-ups. This skill distils them; it is
> not a licence to test systems you are not authorised to test. IDOR testing
> touches other users' data — only ever use accounts and objects you control.

## The one idea

IDOR is an **authorization** bug, not an authentication one. The app checks
*who you are* but not *whether this object is yours*. You find it by taking a
request that legitimately references one of **your** objects, swapping the
identifier for someone else's, and seeing if the server complies. The whole game
is: which identifier, and does the server re-check ownership.

## Where the identifiers hide

Don't just look at `?id=` in URLs. In this set the tampered identifier lived in:

- **GraphQL operation variables** — the single richest source here (7 of 28).
  A node/record id inside a mutation or query, e.g. `deleteStorySnaps(ids:)`
  (`H1#1819832`, Snapchat, delete anyone's Spotlight video, **$15,000**) and
  `BillDetails`/`BillingDocumentDownload` leaking other merchants' invoices,
  addresses and card data (`H1#2207248`, Shopify, $5,000).
- **REST path / body IDs**, often **incremental and guessable** — model
  registry IDs (`H1#2528293`, GitLab, "exposes all ML models", $1,160).
- **Relationship parameters** — a `parent_id`/`epic_id` that links *your* new
  object to *someone else's* parent across tenants (`H1#1892200`, GitLab child
  epics, $1,160). Tampering the *link*, not just the fetch.
- **Signed/asset URLs that outlive the session** — Rails Active Storage URLs
  reachable unauthenticated, no guessing needed because the app hands them out
  in HTML (`H1#3467641`, Basecamp/fizzy.do).
- **Filenames, document IDs, request IDs** echoed back in responses — harvest
  these from your own traffic to use as swap targets.

Recon: proxy your own session, then inventory every request that carries an
object identifier — numeric IDs, UUIDs, GraphQL `gid://…/29`, invoice numbers,
filenames. Each is a candidate.

## How to test it

1. **Two accounts.** Do the action as User A, capture the request, replay it
   from User B's session (swap cookies/tokens, keep A's object ID). If B
   succeeds, it's IDOR. Nearly every report in the set used this.
2. **Get the victim ID legitimately.** You rarely need to brute force. IDs leak
   in URLs (`H1#1819832` read the Spotlight ID out of the share URL), in page
   source (`H1#1892200` grepped `gid://gitlab/Epic/29` from HTML), or they're
   incremental so you just decrement/increment (`H1#2528293`).
3. **Test every verb, not just read.** The biggest bounty here was a *delete*
   (`H1#1819832`), not a read. Try GET, then the state-changing ones —
   edit/delete/create-linked — which pay more because impact is higher.
4. **Confirm with a clean session.** For asset-URL IDOR, open the URL in an
   unauthenticated browser to prove it isn't your cookies serving it
   (`H1#3467641`).

## Patterns that keep recurring

- **GraphQL trusts the node ID.** Resolvers fetch by global ID and skip the
  object-level authz check that the REST equivalent has. Enumerate the schema's
  queries/mutations and try each with an ID you shouldn't own.
- **"Guessable + no check" = full disclosure.** Incremental IDs turn a single IDOR
  into bulk extraction ("all models", "all invoices"). Note the multiplier when
  reporting.
- **Cross-tenant *writes* via relationship fields.** Some endpoints validate you
  own the object you're creating but not the parent you attach it to.
- **Object references that escape the auth boundary** — signed URLs, export
  links, preview endpoints — are IDOR even when there's nothing to "increment".

## What made the high-bounty ones land

- **State-changing impact beats read.** Delete/modify another user's content, or
  bulk-extract via guessable IDs, pays multiples of a single-record read.
- **Show the sensitive fields, not just "200 OK."** `H1#2207248` enumerated
  exactly what leaked (email, address, card last-4) — that specificity is what
  made it $5k.
- **Demonstrate scale.** "IDs are incremental, so this exposes *all* X"
  (`H1#2528293`) reframes a medium as a systemic break.
- **Stay in your lane.** Prove it with your own two accounts / a private object
  you created; never pull real victims' data to demonstrate.

## Fast checklist

1. Proxy your session; inventory every object identifier (REST + GraphQL + URLs).
2. Replay each cross-account (A's object, B's session).
3. Source the victim ID legitimately: share URLs, page source, increment.
4. Test read **and** write verbs; note if IDs are guessable (→ bulk).
5. Report with the exact fields exposed and the blast radius.

---
*Generated by [h1db](https://github.com/Gh0stSpy/HackerOne-Disclosed-Reports-Database)
from disclosed reports. Regenerate with `python -m h1db set idor` then re-synthesise.*
