# Release Checklist

## Before tagging a release

- [ ] Confirm current PHP security advisory and fixed-version thresholds.
- [ ] Test `nmap --script-help http-php2shell-version` on current Nmap.
- [ ] Run `nmap --script-updatedb` successfully on Linux and Windows if possible.
- [ ] Start both Docker lab controls.
- [ ] Confirm PHP 8.3.35 returns `LIKELY VULNERABLE`.
- [ ] Confirm PHP 8.3.36 returns `NOT VULNERABLE` with `vulns.showall`.
- [ ] Test a server with PHP version disclosure disabled.
- [ ] Review all network requests and confirm no exploit-style request was added.
- [ ] Review CHANGELOG.md.
- [ ] Confirm LICENSE and NSE `license` metadata remain consistent.
- [ ] Remove real IP addresses, hostnames, credentials, and private scan output.

## Suggested first tag

```text
v0.1.0-beta
```
