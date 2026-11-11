# By program: MariaDB

**44 reports** · published bounties — *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [3788482](../../reports/3788482.md) | Stack Buffer Overflow in mariadb-dump quote_name() Allows Malicious Server to Execute Arbi | Stack Overflow | Critical | — | 51 |
| 2 | [3897914](../../reports/3897914.md) | Out-of-bounds read in MariaDB .frm parsing enables RCE via vtable hijacking | Out-of-bounds Read | High | — | 43 |
| 3 | [3876430](../../reports/3876430.md) | MariaDB GRANT PROXY permits unauthorized authentication changes and administrator account  | Improper Access Control - Generic | High | — | 35 |
| 4 | [3872239](../../reports/3872239.md) | Connector/J: malicious server crashes client JVM via unbounded result-set field-count allo | Uncontrolled Resource Consumption | Medium | — | 31 |
| 5 | [3896671](../../reports/3896671.md) | Connector/C Out-of-bounds read in `unpack_fields()` from short metadata field | Out-of-bounds Read | — | — | 31 |
| 6 | [3678395](../../reports/3678395.md) | Path Traversal in mbstream Extract | Path Traversal | High | — | 29 |
| 7 | [3849007](../../reports/3849007.md) | MariaDB CLI Utility Issues | SQL Injection | — | — | 27 |
| 8 | [3766217](../../reports/3766217.md) | libmariadb ( mariadb-connector-c ): stack overflow via server-controlled field->length in  | Stack Overflow | Medium | — | 23 |
| 9 | [3782405](../../reports/3782405.md) | Stack Buffer-Overflow in MariaDB Charset_collation_map_st::insert_or_replace() | Stack Overflow | — | — | 23 |
| 10 | [3867363](../../reports/3867363.md) | MariaDB HandlerSocket Improper Request Field-Count Validation Causes Server Crash | Uncontrolled Resource Consumption | Medium | — | 23 |
| 11 | [3908943](../../reports/3908943.md) | DROP PACKAGE leaves PACKAGE BODY grant in mysql.procs_priv causing privilege escalation | Improper Access Control - Generic | High | — | 19 |
| 12 | [3769676](../../reports/3769676.md) | Stack Overflow DoS in ST_GeomFromGeoJSON Allows Any Authenticated User to Crash the Entire | Stack Overflow | Medium | — | 18 |
| 13 | [3896507](../../reports/3896507.md) | Server crash (stack-overflow DoS) via unbounded recursion in MariaDB WKB GEOMETRYCOLLECTIO | — | Medium | — | 18 |
| 14 | [3896617](../../reports/3896617.md) | Connector/C TLS auth-switch bypass exposes plaintext password on hostname verification fai | Improper Certificate Validation | — | — | 17 |
| 15 | [3771139](../../reports/3771139.md) | Heap Memory Disclosure via Integer Underflow in Item_func_json_arrayagg::cut_max_length in | Buffer Over-read | — | — | 16 |
| 16 | [3867358](../../reports/3867358.md) | MariaDB Low-Privilege User Can Exhaust Memory Through a Formatting Function and Crash the  | Uncontrolled Resource Consumption | Medium | — | 16 |
| 17 | [3910393](../../reports/3910393.md) | Stack Buffer Overflow in MariaDB CONNECT storage engine when reading DOUBLE columns from T | Stack Overflow | — | — | 16 |
| 18 | [3781201](../../reports/3781201.md) | Pre-authentication `size_t` integer underflow → out-of-bounds read / server crash in Maria | Integer Underflow | Medium | — | 14 |
| 19 | [3836021](../../reports/3836021.md) | Missing FILE-privilege enforcement in CONNECT file UDFs allows server-side file read and w | Improper Access Control - Generic | High | — | 14 |
| 20 | [3856148](../../reports/3856148.md) | Low-privilege RCE in MariaDB: SYS_REFCURSOR cursor-array use-after-free chained with an ST | Use After Free | Critical | — | 14 |
| 21 | [3771144](../../reports/3771144.md) | Use-After-Free in BTREE Index Traversal via Stale key_version in heap_update() in MariaDB  | Use After Free | — | — | 12 |
| 22 | [3771147](../../reports/3771147.md) | Stack Buffer Overflow via Crafted keyseg->start/ keyseg->length in .MYI File (MariaDB MyIS | Classic Buffer Overflow | — | — | 11 |
| 23 | [3896684](../../reports/3896684.md) | Connector/C Out-of-bounds read from unterminated GSSAPI SPN in `parse_server_packet()` | Out-of-bounds Read | — | — | 10 |
| 24 | [3897588](../../reports/3897588.md) | KILL authorization trusts the presented login name instead of the authenticated anonymous  | Incorrect Calculation of Buffer Size | — | — | 9 |
| 25 | [3920633](../../reports/3920633.md) | Connector/ODBC: SqlwcsOctetLen sizes UTF-16 with a byte-oriented helper, reading past the  | Out-of-bounds Read | Medium | — | 9 |
| 26 | [3920647](../../reports/3920647.md) | Connector/ODBC: MADB_Stmt::ArrayOffset is not reset when an exception unwinds out of MADB_ | Out-of-bounds Read | Medium | — | 9 |
| 27 | [3849025](../../reports/3849025.md) | DATA / INDEX DIRECTORY Abuse | — | — | — | 8 |
| 28 | [3889667](../../reports/3889667.md) | ACL cache collision lets a role inherit privileges from a same-named socket user | Improper Authentication - Generic | Medium | — | 8 |
| 29 | [3871977](../../reports/3871977.md) | Connector/ODBC: malicious server's long version string wraps size_t PrefixLen via negative | Memory Corruption - Generic | Medium | — | 7 |
| 30 | [3871740](../../reports/3871740.md) | r2dbc-mariadb Parsec auth: server-controlled PBKDF2 iteration count causes CPU-exhaustion  | Uncontrolled Resource Consumption | Medium | — | 6 |
| 31 | [3872248](../../reports/3872248.md) | Connector/C++: heap out-of-bounds read when malicious server field length exceeds declared | Out-of-bounds Read | Medium | — | 6 |
| 32 | [3880451](../../reports/3880451.md) | Privilege escalation via user controlled usernames / roles and views | — | — | — | 6 |
| 33 | [3890289](../../reports/3890289.md) | Connector/C++ string escaper re-escapes its own output, enabling SQL injection | SQL Injection | Medium | — | 6 |
| 34 | [3890329](../../reports/3890329.md) | Connector/C++ ignores allowMultiQueries and injects savepoint names into SQL | SQL Injection | Medium | — | 6 |
| 35 | [3909248](../../reports/3909248.md) | MariaDB: heap buffer overflow in ha_tina::chain_append() lets a low-privileged user crash  | Heap Overflow | Medium | — | 6 |
| 36 | [3915935](../../reports/3915935.md) | Heap Use-After-Free in Materialized_cursor::open via SYS_REFCURSOR Array Reallocation | Use After Free | High | — | 6 |
| 37 | [3920629](../../reports/3920629.md) | r2dbc-mariadb: server message accepted with no command in flight desynchronises the connec | Information Disclosure | Medium | — | 6 |
| 38 | [3848978](../../reports/3848978.md) | `SHOW [CREATE\|GRANTS] ...` / `mariadb-dump` Unescaped SQL Generation | SQL Injection | — | — | 5 |
| 39 | [3849040](../../reports/3849040.md) | #mysql50# legacy alias / stale table cache identity mismatch | — | — | — | 5 |
| 40 | [3849051](../../reports/3849051.md) | #mysql50# legacy alias / internal table collisions | — | — | — | 5 |
| 41 | [3890352](../../reports/3890352.md) | Connector/C++ aborts client process on server session-tracking packet via std::stoi | Uncontrolled Resource Consumption | Medium | — | 5 |
| 42 | [3891319](../../reports/3891319.md) | Stack buffer overflow in 9 of 10 Connector/ODBC catalog functions via unbounded name | Stack Overflow | Medium | — | 5 |
| 43 | [3891337](../../reports/3891337.md) | Connector/ODBC SQLGetDescRec treats descriptor handle as statement handle, heap OOB write  | Type Confusion | Medium | — | 5 |
| 44 | [3891779](../../reports/3891779.md) | Connector/ODBC injects unquoted column names into positioned DELETE and UPDATE via MADB_Dy | SQL Injection | Medium | — | 4 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
