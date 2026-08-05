# By program: Monero

**13 reports** · published bounties — *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [3307874](../../reports/3307874.md) | Critical Deadlock Vulnerability in Monero RPC Leading to Complete Node Paralysis | Uncontrolled Resource Consumption | Critical | — | 93 |
| 2 | [3185083](../../reports/3185083.md) | Connection Count Bug in Monero Node Enables Outbound Peer Reset Attack | Privacy Violation | — | — | 39 |
| 3 | [3621606](../../reports/3621606.md) | ZMQ RPC Log Injection and Untrusted Payload Persistence | CRLF Injection | Medium | — | 29 |
| 4 | [3240792](../../reports/3240792.md) | Reported RPC Overflow | Integer Overflow | — | — | 25 |
| 5 | [876530](../../reports/876530.md) | Remote node DOS | Uncontrolled Resource Consumption | Medium | — | 23 |
| 6 | [3241102](../../reports/3241102.md) | Reported Denial of Service | Uncontrolled Resource Consumption | — | — | 23 |
| 7 | [3547349](../../reports/3547349.md) | Inverted ternary in peerlist_manager::filter() allows unlimited whitelist entries per host | — | — | — | 18 |
| 8 | [3687543](../../reports/3687543.md) | `relay_tx` wallet-rpc skips `--restricted-rpc` guard and lets any caller corrupt wallet st | Improper Access Control - Generic | Critical | — | 7 |
| 9 | [3699522](../../reports/3699522.md) | `check_reserve_proof` counts duplicate entries: one output can inflate `total` | Business Logic Errors | Medium | — | 4 |
| 10 | [3693636](../../reports/3693636.md) | wallet-rpc crash via malformed /gettransactions response (empty txs → vector::front() in c | NULL Pointer Dereference | High | — | 3 |
| 11 | [3723315](../../reports/3723315.md) | wallet-rpc describe_transfer uses real_output_in_tx_index instead of real_output: cold-wal | Array Index Underflow | Medium | — | 3 |
| 12 | [3700036](../../reports/3700036.md) | SpendProofV1 txid-substitution: get_spend_proof/check_spend_proof do not verify returned t | Missing Required Cryptographic Step | Medium | — | 2 |
| 13 | [3698862](../../reports/3698862.md) | `check_reserve_proof` sums RingCT ECDH amounts without checking the output commitment | Missing Required Cryptographic Step | Medium | — | 1 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
