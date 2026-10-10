# By program: MariaDB

**27 reports** · published bounties — *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [3788482](../../reports/3788482.md) | Stack Buffer Overflow in mariadb-dump quote_name() Allows Malicious Server to Execute Arbi | Stack Overflow | Critical | — | 50 |
| 2 | [3897914](../../reports/3897914.md) | Out-of-bounds read in MariaDB .frm parsing enables RCE via vtable hijacking | Out-of-bounds Read | High | — | 43 |
| 3 | [3876430](../../reports/3876430.md) | MariaDB GRANT PROXY permits unauthorized authentication changes and administrator account  | Improper Access Control - Generic | High | — | 35 |
| 4 | [3872239](../../reports/3872239.md) | Connector/J: malicious server crashes client JVM via unbounded result-set field-count allo | Uncontrolled Resource Consumption | Medium | — | 30 |
| 5 | [3896671](../../reports/3896671.md) | Connector/C Out-of-bounds read in `unpack_fields()` from short metadata field | Out-of-bounds Read | — | — | 30 |
| 6 | [3678395](../../reports/3678395.md) | Path Traversal in mbstream Extract | Path Traversal | High | — | 27 |
| 7 | [3782405](../../reports/3782405.md) | Stack Buffer-Overflow in MariaDB Charset_collation_map_st::insert_or_replace() | Stack Overflow | — | — | 23 |
| 8 | [3766217](../../reports/3766217.md) | libmariadb ( mariadb-connector-c ): stack overflow via server-controlled field->length in  | Stack Overflow | Medium | — | 22 |
| 9 | [3769676](../../reports/3769676.md) | Stack Overflow DoS in ST_GeomFromGeoJSON Allows Any Authenticated User to Crash the Entire | Stack Overflow | Medium | — | 18 |
| 10 | [3771139](../../reports/3771139.md) | Heap Memory Disclosure via Integer Underflow in Item_func_json_arrayagg::cut_max_length in | Buffer Over-read | — | — | 16 |
| 11 | [3867363](../../reports/3867363.md) | MariaDB HandlerSocket Improper Request Field-Count Validation Causes Server Crash | Uncontrolled Resource Consumption | Medium | — | 16 |
| 12 | [3771144](../../reports/3771144.md) | Use-After-Free in BTREE Index Traversal via Stale key_version in heap_update() in MariaDB  | Use After Free | — | — | 12 |
| 13 | [3771147](../../reports/3771147.md) | Stack Buffer Overflow via Crafted keyseg->start/ keyseg->length in .MYI File (MariaDB MyIS | Classic Buffer Overflow | — | — | 11 |
| 14 | [3867358](../../reports/3867358.md) | MariaDB Low-Privilege User Can Exhaust Memory Through a Formatting Function and Crash the  | Uncontrolled Resource Consumption | Medium | — | 10 |
| 15 | [3908943](../../reports/3908943.md) | DROP PACKAGE leaves PACKAGE BODY grant in mysql.procs_priv causing privilege escalation | Improper Access Control - Generic | High | — | 10 |
| 16 | [3897588](../../reports/3897588.md) | KILL authorization trusts the presented login name instead of the authenticated anonymous  | Incorrect Calculation of Buffer Size | — | — | 9 |
| 17 | [3781201](../../reports/3781201.md) | Pre-authentication `size_t` integer underflow → out-of-bounds read / server crash in Maria | Integer Underflow | Medium | — | 8 |
| 18 | [3889667](../../reports/3889667.md) | ACL cache collision lets a role inherit privileges from a same-named socket user | Improper Authentication - Generic | Medium | — | 8 |
| 19 | [3836021](../../reports/3836021.md) | Missing FILE-privilege enforcement in CONNECT file UDFs allows server-side file read and w | Improper Access Control - Generic | High | — | 7 |
| 20 | [3909248](../../reports/3909248.md) | MariaDB: heap buffer overflow in ha_tina::chain_append() lets a low-privileged user crash  | Heap Overflow | Medium | — | 6 |
| 21 | [3915935](../../reports/3915935.md) | Heap Use-After-Free in Materialized_cursor::open via SYS_REFCURSOR Array Reallocation | Use After Free | High | — | 5 |
| 22 | [3849025](../../reports/3849025.md) | DATA / INDEX DIRECTORY Abuse | — | — | — | 4 |
| 23 | [3856148](../../reports/3856148.md) | Low-privilege RCE in MariaDB: SYS_REFCURSOR cursor-array use-after-free chained with an ST | Use After Free | Critical | — | 4 |
| 24 | [3880451](../../reports/3880451.md) | Privilege escalation via user controlled usernames / roles and views | — | — | — | 4 |
| 25 | [3848978](../../reports/3848978.md) | `SHOW [CREATE\|GRANTS] ...` / `mariadb-dump` Unescaped SQL Generation | SQL Injection | — | — | 3 |
| 26 | [3849040](../../reports/3849040.md) | #mysql50# legacy alias / stale table cache identity mismatch | — | — | — | 1 |
| 27 | [3849051](../../reports/3849051.md) | #mysql50# legacy alias / internal table collisions | — | — | — | 1 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
