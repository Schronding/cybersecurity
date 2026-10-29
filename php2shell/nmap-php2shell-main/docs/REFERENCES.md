# References

## PHP security advisory

PHP published the security advisory on 21 October 2026 and identifies the
following upstream releases as containing the fixes for CVE-2026-109618 and
CVE-2026-109619:

- PHP 8.2.35
- PHP 8.3.36
- PHP 8.4.27
- PHP 8.5.12

Official advisory:

- https://www.php.net/archive/2026.php#2026-10-21-5

The PHP project also notes that Linux distributions and LTS vendors may provide
backported fixes. This is why the NSE script reports an older remotely observed
version as `LIKELY_VULN`, rather than claiming confirmed exploitation.

## Nmap NSE conventions

Nmap's `vulns` library defines `LIKELY_VULN` for cases such as simple version
comparison where false positives are possible:

- https://nmap.org/nsedoc/lib/vulns.html

NSE script format and licensing guidance:

- https://nmap.org/book/nse-script-format.html

NSE documentation guidance:

- https://nmap.org/book/nsedoc.html
