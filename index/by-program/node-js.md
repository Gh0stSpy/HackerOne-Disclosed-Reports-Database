# By program: Node.js

**27 reports** · published bounties — *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [2319584](../../reports/2319584.md) | "Assertion failed" in node::http2::Http2Session::~Http2Session() leads to HTTP/2 server cr | Uncontrolled Resource Consumption | High | — | 65 |
| 2 | [2084280](../../reports/2084280.md) | WASI sandbox escape via symlink | Privilege Escalation | Medium | — | 44 |
| 3 | [2079103](../../reports/2079103.md) | Permission model improperly processes UNC paths | Privilege Escalation | Low | — | 35 |
| 4 | [3648681](../../reports/3648681.md) | Improper Input Validation — HTTP Response Parser Unconditionally Accepts Bare CR in Status | HTTP Request Smuggling | Medium | — | 26 |
| 5 | [3456148](../../reports/3456148.md) | Unbounded decompression chain in HTTP responses on Node.js Fetch API via Content-Encoding  | — | — | — | 25 |
| 6 | [2913312](../../reports/2913312.md) | Usage of unsafe random function in undici for choosing boundary | Use of Insufficiently Random Values | Medium | — | 23 |
| 7 | [1763817](../../reports/1763817.md) | Take over subdomain undici.nodejs.org.cdn.cloudflare.net | Array Index Underflow | Medium | — | 22 |
| 8 | [2237099](../../reports/2237099.md) | HTTP Request Smuggling via Content Length Obfuscation | HTTP Request Smuggling | Medium | — | 18 |
| 9 | [2352957](../../reports/2352957.md) | Proxy-Authorization header is not cleared in cross-domain redirect in undici | Information Disclosure | Low | — | 18 |
| 10 | [1820955](../../reports/1820955.md) | CRLF Injection in Nodejs ‘undici’ via host | CRLF Injection | Medium | — | 11 |
| 11 | [2377760](../../reports/2377760.md) | fetch with integrity option is too lax when algorithm is specified but hash value is in in | Violation of Secure Design Principles | — | — | 11 |
| 12 | [2408074](../../reports/2408074.md) | Proxy-Authorization header not cleared on cross-origin redirect in undici.request | Insufficiently Protected Credentials | Low | — | 9 |
| 13 | [1877919](../../reports/1877919.md) | The use of __proto__ in process.mainModule.__proto__.require() bypasses the permission sys | Privilege Escalation | High | — | 8 |
| 14 | [2051224](../../reports/2051224.md) | fs.statfs bypasses Permission Model | Improper Access Control - Generic | Low | — | 8 |
| 15 | [2051257](../../reports/2051257.md) | process.binding() can bypass the permission model through path traversal | Path Traversal | High | — | 8 |
| 16 | [1747642](../../reports/1747642.md) | Permissions policies can be bypassed via process.mainModule | Privilege Escalation | High | — | 7 |
| 17 | [1927480](../../reports/1927480.md) | DiffieHellman doesn't generate keys after setting a key | Inconsistency Between Implementation and Documented Design | Medium | — | 7 |
| 18 | [2001873](../../reports/2001873.md) | HTTP Request Smuggling via Empty headers separated by CR | HTTP Request Smuggling | Medium | — | 7 |
| 19 | [1962701](../../reports/1962701.md) | Process-based permissions can be bypassed with the "inspector" module. | Improper Access Control - Generic | High | — | 6 |
| 20 | [1966492](../../reports/1966492.md) | fs.openAsBlob() bypasses permission system | Improper Access Control - Generic | Medium | — | 6 |
| 21 | [1808596](../../reports/1808596.md) | Multiple OpenSSL error handling issues in nodejs crypto library | Cryptographic Issues - Generic | Medium | — | 5 |
| 22 | [1952978](../../reports/1952978.md) | Filesystem experimental permissions policy does not handle path traversal cases. | Path Traversal | High | — | 5 |
| 23 | [1966499](../../reports/1966499.md) | fs module's file watching is not restricted by --allow-fs-read | Improper Access Control - Generic | Medium | — | 5 |
| 24 | [1710652](../../reports/1710652.md) | DNS rebinding in --inspect via invalid octal IP address | OS Command Injection | Medium | — | 4 |
| 25 | [1954535](../../reports/1954535.md) | OpenSSL engines can be used to bypass and/or disable the permission model | Privilege Escalation | Medium | — | 4 |
| 26 | [1784449](../../reports/1784449.md) | Regular Expression Denial of Service in Headers | Uncontrolled Resource Consumption | Low | — | 3 |
| 27 | [1884159](../../reports/1884159.md) | node.js process aborts when processing x509 certs with invalid public key information | Uncontrolled Resource Consumption | Medium | — | 2 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
