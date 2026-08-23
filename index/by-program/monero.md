# By program: Monero

**22 reports** · published bounties — *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [3307874](../../reports/3307874.md) | Critical Deadlock Vulnerability in Monero RPC Leading to Complete Node Paralysis | Uncontrolled Resource Consumption | Critical | — | 94 |
| 2 | [3620006](../../reports/3620006.md) | Wallet RPC Restricted-Mode Policy Bypass | Improper Authentication - Generic | High | — | 43 |
| 3 | [3693636](../../reports/3693636.md) | wallet-rpc crash via malformed /gettransactions response (empty txs → vector::front() in c | NULL Pointer Dereference | High | — | 43 |
| 4 | [3699522](../../reports/3699522.md) | `check_reserve_proof` counts duplicate entries: one output can inflate `total` | Business Logic Errors | Medium | — | 41 |
| 5 | [3185083](../../reports/3185083.md) | Connection Count Bug in Monero Node Enables Outbound Peer Reset Attack | Privacy Violation | — | — | 39 |
| 6 | [3698862](../../reports/3698862.md) | `check_reserve_proof` sums RingCT ECDH amounts without checking the output commitment | Missing Required Cryptographic Step | Medium | — | 36 |
| 7 | [3601469](../../reports/3601469.md) | Restricted RPC Policy Bypass on ZMQ JSON-RPC Allows Unauthenticated Remote Admin Actions | Improper Authentication - Generic | High | — | 32 |
| 8 | [3621606](../../reports/3621606.md) | ZMQ RPC Log Injection and Untrusted Payload Persistence | CRLF Injection | Medium | — | 30 |
| 9 | [3700036](../../reports/3700036.md) | SpendProofV1 txid-substitution: get_spend_proof/check_spend_proof do not verify returned t | Missing Required Cryptographic Step | Medium | — | 27 |
| 10 | [3240792](../../reports/3240792.md) | Reported RPC Overflow | Integer Overflow | — | — | 25 |
| 11 | [876530](../../reports/876530.md) | Remote node DOS | Uncontrolled Resource Consumption | Medium | — | 24 |
| 12 | [3241102](../../reports/3241102.md) | Reported Denial of Service | Uncontrolled Resource Consumption | — | — | 23 |
| 13 | [3619409](../../reports/3619409.md) | Windows installer grants low-privileged users write access to executable P2Pool directory, | Improper Access Control - Generic | High | — | 20 |
| 14 | [3687543](../../reports/3687543.md) | `relay_tx` wallet-rpc skips `--restricted-rpc` guard and lets any caller corrupt wallet st | Improper Access Control - Generic | Low | — | 19 |
| 15 | [3547349](../../reports/3547349.md) | Inverted ternary in peerlist_manager::filter() allows unlimited whitelist entries per host | — | — | — | 18 |
| 16 | [3723315](../../reports/3723315.md) | wallet-rpc describe_transfer uses real_output_in_tx_index instead of real_output: cold-wal | Array Index Underflow | Medium | — | 18 |
| 17 | [3819475](../../reports/3819475.md) | Monero GUI OpenAlias DNSSEC-invalid resolution still writes spoofable address into recipie | — | Medium | — | 18 |
| 18 | [3686283](../../reports/3686283.md) | View-only offline transaction creation bypasses the long-payment-ID privacy block | Information Disclosure | Medium | — | 16 |
| 19 | [3679471](../../reports/3679471.md) | HTML Injection in Transaction Confirmation Dialog via Address Book Description Enables UI  | Code Injection | Medium | — | 15 |
| 20 | [3648638](../../reports/3648638.md) | monero:// deeplink parsing accepts tx_amount=(all) and can trigger send-all transaction mo | Business Logic Errors | Medium | — | 14 |
| 21 | [3515557](../../reports/3515557.md) | Loss of multisig funds through single malicious participant's deliberate deception | Business Logic Errors | Medium | — | 10 |
| 22 | [3686259](../../reports/3686259.md) | `set_daemon` wallet-rpc silently ignores `ssl_allowed_fingerprints` → pinning bypassed, wa | Improper Certificate Validation | High | — | 5 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
