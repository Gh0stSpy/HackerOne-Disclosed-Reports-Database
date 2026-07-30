# By program: Nextcloud

**85 reports** · published bounties $4,200 *(most programs don't publish an amount, so this undercounts)*

| # | Report | Title | Weakness | Severity | Bounty | Votes |
|--:|:--|:--|:--|:--|--:|--:|
| 1 | [1878381](../../reports/1878381.md) | CSRF protection on OIDC login is broken | Cross-Site Request Forgery (CSRF) | Medium | $500 | 77 |
| 2 | [1724016](../../reports/1724016.md) | Download permissions can be changed by resharer | Improper Access Control - Generic | Medium | $500 | 49 |
| 3 | [1987062](../../reports/1987062.md) | Password reset endpoint is not brute force protected | Improper Restriction of Authentication Attempts | High | $500 | 46 |
| 4 | [1914115](../../reports/1914115.md) | End-to-end encrypted file-drops can be made inaccessible | Improper Access Control - Generic | High | $400 | 43 |
| 5 | [2380133](../../reports/2380133.md) | Can download files on Android app without permission | Improper Access Control - Generic | Low | $250 | 46 |
| 6 | [3400143](../../reports/3400143.md) | Credential Disclosure via Unvalidated directDownloadUrl (Missing DontAddCredentialsAttribu | Insufficiently Protected Credentials | Medium | $250 | 37 |
| 7 | [1702864](../../reports/1702864.md) | SSRF via filter bypass due to lax checking on IPs | Server-Side Request Forgery (SSRF) | Medium | $250 | 33 |
| 8 | [1965156](../../reports/1965156.md) | Text does not respect 'Allow download' permissions | Improper Access Control - Generic | Low | $250 | 12 |
| 9 | [2067572](../../reports/2067572.md) | New AppPassword can be generated without password confirmation | Improper Access Control - Generic | High | $250 | 11 |
| 10 | [2021684](../../reports/2021684.md) | Issuer not verified from obtained token in user_oidc | — | Medium | $250 | 1 |
| 11 | [1724021](../../reports/1724021.md) | Secure view trivial to bypass | Improper Access Control - Generic | Medium | $150 | 13 |
| 12 | [1977222](../../reports/1977222.md) | Open redirect on "Unsupported browser" warning | Open Redirect | Medium | $150 | 8 |
| 13 | [2388183](../../reports/2388183.md) | Easy way to create a new Deck board without permission | Improper Access Control - Generic | — | $100 | 56 |
| 14 | [1784162](../../reports/1784162.md) | OAuth2 "authorization_code" is valid indefinetly | Violation of Secure Design Principles | Low | $100 | 45 |
| 15 | [1994324](../../reports/1994324.md) | OAuth2 client_secret stored in plain text in the database | Cleartext Storage in a File or on Disk | Medium | $100 | 31 |
| 16 | [2120667](../../reports/2120667.md) | Bypass password confirmation via Context-dependent access control (CDCA) | Improper Access Control - Generic | Medium | $100 | 31 |
| 17 | [2107934](../../reports/2107934.md) | Admins can change authentication details of user configured external storage | Improper Access Control - Generic | Low | $100 | 30 |
| 18 | [2946927](../../reports/2946927.md) | Sensitive Information Disclosure via Back Button Post Logout on https://apps.nextcloud.com | — | Low | — | 113 |
| 19 | [2248328](../../reports/2248328.md) | RCE on Wordpress website | Deserialization of Untrusted Data | Critical | — | 82 |
| 20 | [2311179](../../reports/2311179.md) | Directory Listing of publicly available assets | Information Exposure Through Directory Listing | Medium | — | 70 |
| 21 | [2376929](../../reports/2376929.md) | ID4me feature of OpenID connect app available even when disabled | Improper Access Control - Generic | Medium | — | 66 |
| 22 | [3399016](../../reports/3399016.md) | Improper input validation On Exported deep-link handler crashes `FileDisplayActivity` on c | Improper Null Termination | — | — | 64 |
| 23 | [1879549](../../reports/1879549.md) | Basic auth header on WebDAV requests is not bruteforce protected | Improper Restriction of Authentication Attempts | High | — | 53 |
| 24 | [3486747](../../reports/3486747.md) | SVG filter primitives bypass remote image blocking, enabling email tracking without consen | Privacy Violation | Medium | — | 53 |
| 25 | [2778441](../../reports/2778441.md) | Exposing debug.log file leads to server full path disclosure | Business Logic Errors | Medium | — | 47 |
| 26 | [2058337](../../reports/2058337.md) | Inviting excessive long email addresses to a calendar event makes the server unresponsive | Uncontrolled Resource Consumption | Medium | — | 46 |
| 27 | [3443563](../../reports/3443563.md) | Roundcube Webmail Style Sanitizer can be bypassed using CSS Character Escapes | Information Disclosure | Medium | — | 46 |
| 28 | [2212627](../../reports/2212627.md) | Delete external storage of any user | Improper Access Control - Generic | High | — | 44 |
| 29 | [3590586](../../reports/3590586.md) | position: fixed !important bypasses CSS sanitizer's fixed-position mitigation, enabling fu | Resource Injection | Medium | — | 44 |
| 30 | [2305880](../../reports/2305880.md) | Email not verified when changing afterwards on apps.nextcloud.com | Violation of Secure Design Principles | Low | — | 42 |
| 31 | [2299069](../../reports/2299069.md) | xmlrpc.php &wp-cron.php files are enabled, and will used for (DDOS),(DOS) and broutforce u | XML External Entities (XXE) | — | — | 41 |
| 32 | [2247457](../../reports/2247457.md) | Can download files by zipping the folder | Improper Access Control - Generic | Medium | — | 40 |
| 33 | [1727424](../../reports/1727424.md) | No password length limit when creating a user as an administrator | Uncontrolled Resource Consumption | Low | — | 39 |
| 34 | [3594137](../../reports/3594137.md) | Stored XSS in attachment-display exploitable through SameSite | Cross-site Scripting (XSS) - Stored | Medium | — | 39 |
| 35 | [3367676](../../reports/3367676.md) | tabnabbing in roundcube webmail | — | — | — | 37 |
| 36 | [2446531](../../reports/2446531.md) | Weak ssh algorithms and CVE-2023-48795 Discovered on various subdomains of nextcloud.com | Use of a Broken or Risky Cryptographic Algorithm | Medium | — | 36 |
| 37 | [3590583](../../reports/3590583.md) | Unquoted body background attribute enables CSS injection that bypasses remote image blocki | Resource Injection | Medium | — | 34 |
| 38 | [2230915](../../reports/2230915.md) | Bruteforce protection in password verification can be bypassed | Improper Restriction of Authentication Attempts | Medium | — | 31 |
| 39 | [2210038](../../reports/2210038.md) | HTML injection in search UI when selecting a circle with HTML in the display name | Cross-site Scripting (XSS) - Stored | Low | — | 30 |
| 40 | [2245437](../../reports/2245437.md) | App PIN code can be bypassed in Files iOS | Improper Authentication - Generic | Low | — | 30 |
| 41 | [1784645](../../reports/1784645.md) | Passcode bypass on Talk Android app | Improper Access Control - Generic | Low | — | 29 |
| 42 | [2112973](../../reports/2112973.md) | Enabling Birthday Contact to any user | Insecure Direct Object Reference (IDOR) | Medium | — | 29 |
| 43 | [2376909](../../reports/2376909.md) | Possible to enumerate valid files in password protected shares/files drop shares as well a | Information Disclosure | Low | — | 29 |
| 44 | [2101165](../../reports/2101165.md) | user_ldap app logs user passwords in the log file on level debug | Cleartext Storage of Sensitive Information | Medium | — | 28 |
| 45 | [2094473](../../reports/2094473.md) | Password of talk conversations can be bruteforced | Improper Restriction of Authentication Attempts | Medium | — | 27 |
| 46 | [3590576](../../reports/3590576.md) | SMIL values and by attributes bypass remote image blocking via unvalidated resource-loadin | Remote File Inclusion | Medium | — | 26 |
| 47 | [1741430](../../reports/1741430.md) | CSRF vulnerability in Nextcloud Desktop Client 3.6.1 on Windows when clicking malicious li | Cross-Site Request Forgery (CSRF) | Medium | — | 24 |
| 48 | [1841408](../../reports/1841408.md) | Error in  Booking an appointment reveals the full path of the website | Improper Access Control - Generic | Low | — | 24 |
| 49 | [1842114](../../reports/1842114.md) | Missing brute force protection on password confirmation modal | Improper Restriction of Authentication Attempts | Medium | — | 24 |
| 50 | [1755555](../../reports/1755555.md) | Possibility to delete files attached to deck cards of other users | Insecure Direct Object Reference (IDOR) | Low | — | 21 |
| 51 | [2058556](../../reports/2058556.md) | Self XSS when sending HTML as a comment in the Deck app | Cross-site Scripting (XSS) - Generic | — | — | 20 |
| 52 | [2211561](../../reports/2211561.md) | Self XSS when pasting HTML into Text app with Ctrl+Shift+V | Cross-site Scripting (XSS) - DOM | Medium | — | 20 |
| 53 | [2110945](../../reports/2110945.md) | Memcached used as RateLimiter backend is no-op | Improper Restriction of Authentication Attempts | Medium | — | 19 |
| 54 | [1745766](../../reports/1745766.md) | Disabled download shares still allow download through preview images | Improper Access Control - Generic | Low | — | 18 |
| 55 | [1720822](../../reports/1720822.md) | Suspicious login app ships old league/flysystem version | Violation of Secure Design Principles | — | — | 17 |
| 56 | [1850407](../../reports/1850407.md) | Chat room member disclosure via autocomplete API | Improper Access Control - Generic | Medium | — | 17 |
| 57 | [1894653](../../reports/1894653.md) | Missing brute force protection for passwords of password protected share links | Improper Restriction of Authentication Attempts | Low | — | 17 |
| 58 | [2108342](../../reports/2108342.md) | Error when editing a calendar appointment returns stacktrace and query | Information Disclosure | Medium | — | 16 |
| 59 | [1706248](../../reports/1706248.md) | Guests can continue to receive video streams from call after being removed from a conversa | Privacy Violation | Medium | — | 15 |
| 60 | [1767439](../../reports/1767439.md) | Exposed Log File Lead to Full Internal path disclosure at [https://nextcloud.com/wp-conten | Information Disclosure | Low | — | 15 |
| 61 | [1784310](../../reports/1784310.md) | Messages can still be seen on conversation after expiring when cron is misconfigured | Privacy Violation | Low | — | 15 |
| 62 | [1916565](../../reports/1916565.md) | Twitter Account hijack @nextcloudfrance | — | Medium | — | 15 |
| 63 | [1767503](../../reports/1767503.md) | Reference caching can leak data to unauthorized users | Insecure Storage of Sensitive Information | Medium | — | 14 |
| 64 | [1720043](../../reports/1720043.md) | Desktop client can be tricked into opening/executing local files when clicking a nc://open | Code Injection | Medium | — | 13 |
| 65 | [1893186](../../reports/1893186.md) | Reflected XSS vulnerability with full CSP bypass in Nextcloud installations using recommen | Cross-site Scripting (XSS) - Reflected | Medium | — | 13 |
| 66 | [1736390](../../reports/1736390.md) | Mail app - blind SSRF via imapHost parameter | Server-Side Request Forgery (SSRF) | Low | — | 12 |
| 67 | [1806275](../../reports/1806275.md) | Mail app stores cleartext password in database until OAUTH2 setup is done | Plaintext Storage of a Password | Low | — | 12 |
| 68 | [1820864](../../reports/1820864.md) | No password length restriction in reset password endpoint | Uncontrolled Resource Consumption | Low | — | 12 |
| 69 | [1741525](../../reports/1741525.md) | Mail app - Blind SSRF via Sierve server fonctionnality and sieveHost parameter | Server-Side Request Forgery (SSRF) | Low | — | 11 |
| 70 | [1745755](../../reports/1745755.md) | Hide download previews are accessible without a watermark | Improper Access Control - Generic | Low | — | 11 |
| 71 | [2047168](../../reports/2047168.md) | Any (non-admin) user from an instance can destroy any (user and/or global) external filesy | Improper Access Control - Generic | Medium | — | 11 |
| 72 | [1746582](../../reports/1746582.md) | Mail app - blind SSRF via smtpHost parameter | Server-Side Request Forgery (SSRF) | Low | — | 10 |
| 73 | [1765631](../../reports/1765631.md) | Potential directory traversal in OC\Files\Node\Folder::getFullPath | Path Traversal: 'dir\..\..\filename' | Medium | — | 10 |
| 74 | [2052795](../../reports/2052795.md) | No Rate Limit On Forgot Password on https://apps.nextcloud.com | Improper Authentication - Generic | — | — | 10 |
| 75 | [1708873](../../reports/1708873.md) | Vulnerable moment-timezone version shipped | Cleartext Transmission of Sensitive Information | — | — | 9 |
| 76 | [1712329](../../reports/1712329.md) | [nextcloud/server] Moment.js vulnerable to Inefficient Regular Expression Complexity | Improper Authentication - Generic | — | — | 9 |
| 77 | [1726445](../../reports/1726445.md) | A vulnerability classified as critical has been found in gsi-openssh-server 7.9p1 on Fedor | — | Low | — | 6 |
| 78 | [1781751](../../reports/1781751.md) | Ability to control the filename when uploading a logo or favicon on theming | Violation of Secure Design Principles | Low | — | 6 |
| 79 | [1707977](../../reports/1707977.md) | XSS in Desktop Client via user status and information | Resource Injection | Low | — | 5 |
| 80 | [1745702](../../reports/1745702.md) | Insecure randomness for default password in file sharing when password policy app is disab | Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) | Low | — | 5 |
| 81 | [1711847](../../reports/1711847.md) | XSS in Desktop Client in call notification popup | Resource Injection | Low | — | 4 |
| 82 | [1794462](../../reports/1794462.md) | Website PHP source code returned in javascript | — | Medium | — | 4 |
| 83 | [1806223](../../reports/1806223.md) | Reference fetch can saturate the server bandwidth for 10 seconds | Uncontrolled Resource Consumption | Medium | — | 4 |
| 84 | [1954711](../../reports/1954711.md) | user_oidc app is missing bruteforce protection | Improper Restriction of Authentication Attempts | Medium | — | 4 |
| 85 | [1994328](../../reports/1994328.md) | App stores client secret unencrypted in database | Missing Encryption of Sensitive Data | Low | — | 3 |

---
*Part of the [HackerOne Disclosed Reports Database](../../README.md). Generated, do not edit by hand.*
