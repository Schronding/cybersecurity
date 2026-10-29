# Contributing

Contributions that improve accuracy, portability, documentation, or safe
detection are welcome.

## Design principles

Changes should preserve these properties:

1. The NSE script must remain non-exploitative and suitable for defensive use.
2. A version-only finding must not be represented as confirmed exploitation.
3. `LIKELY_VULN` should be used when exposure is inferred from version data.
4. Vendor and distribution backports must be considered when interpreting an
   older reported PHP version.
5. Network traffic should remain lightweight. Prefer HEAD requests and use GET
   only when necessary for fingerprinting.
6. New fixed-version thresholds must be supported by an authoritative PHP or
   vendor security advisory.

## Testing

Before submitting a change:

- Run `nmap --script-updatedb` after installing the script.
- Confirm `nmap --script-help http-php2shell-version` loads without an NSE error.
- Test against both containers in `lab/docker-compose.yml`.
- Confirm the pre-fix container is reported as `LIKELY VULNERABLE`.
- Run with `--script-args vulns.showall` and confirm the fixed container is
  reported as `NOT VULNERABLE` by upstream version.
- Include any relevant Nmap version and operating system details with bug reports.

## Pull requests

Keep pull requests focused. Explain what changed, why it is safe, and how the
change was validated. Do not include live third-party targets or sensitive scan
results in test evidence.
