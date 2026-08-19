# By program: Monero

**16 reports** · published bounties — *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [3307874](../../reports/3307874.md) | Critical Deadlock Vulnerability in Monero RPC Leading to Complete Node Paralysis | Uncontrolled Resource Consumption | Critical | — | 94 |
| 2 | [3693636](../../reports/3693636.md) | wallet-rpc crash via malformed /gettransactions response (empty txs → vector::front() in c | NULL Pointer Dereference | High | — | 43 |
| 3 | [3185083](../../reports/3185083.md) | Connection Count Bug in Monero Node Enables Outbound Peer Reset Attack | Privacy Violation | — | — | 39 |
| 4 | [3699522](../../reports/3699522.md) | `check_reserve_proof` counts duplicate entries: one output can inflate `total` | Business Logic Errors | Medium | — | 39 |
| 5 | [3698862](../../reports/3698862.md) | `check_reserve_proof` sums RingCT ECDH amounts without checking the output commitment | Missing Required Cryptographic Step | Medium | — | 34 |
| 6 | [3621606](../../reports/3621606.md) | ZMQ RPC Log Injection and Untrusted Payload Persistence | CRLF Injection | Medium | — | 30 |
| 7 | [3620006](../../reports/3620006.md) | Wallet RPC Restricted-Mode Policy Bypass | Improper Authentication - Generic | High | — | 29 |
| 8 | [3700036](../../reports/3700036.md) | SpendProofV1 txid-substitution: get_spend_proof/check_spend_proof do not verify returned t | Missing Required Cryptographic Step | Medium | — | 26 |
| 9 | [3240792](../../reports/3240792.md) | Reported RPC Overflow | Integer Overflow | — | — | 25 |
| 10 | [876530](../../reports/876530.md) | Remote node DOS | Uncontrolled Resource Consumption | Medium | — | 24 |
| 11 | [3241102](../../reports/3241102.md) | Reported Denial of Service | Uncontrolled Resource Consumption | — | — | 23 |
| 12 | [3601469](../../reports/3601469.md) | Restricted RPC Policy Bypass on ZMQ JSON-RPC Allows Unauthenticated Remote Admin Actions | Improper Authentication - Generic | High | — | 21 |
| 13 | [3687543](../../reports/3687543.md) | `relay_tx` wallet-rpc skips `--restricted-rpc` guard and lets any caller corrupt wallet st | Improper Access Control - Generic | Low | — | 19 |
| 14 | [3547349](../../reports/3547349.md) | Inverted ternary in peerlist_manager::filter() allows unlimited whitelist entries per host | — | — | — | 18 |
| 15 | [3723315](../../reports/3723315.md) | wallet-rpc describe_transfer uses real_output_in_tx_index instead of real_output: cold-wal | Array Index Underflow | Medium | — | 17 |
| 16 | [3686259](../../reports/3686259.md) | `set_daemon` wallet-rpc silently ignores `ssl_allowed_fingerprints` → pinning bypassed, wa | Improper Certificate Validation | High | — | 5 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
