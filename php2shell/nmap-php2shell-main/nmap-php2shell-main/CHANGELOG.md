# Changelog

All notable changes to this project will be documented in this file.

The project uses semantic-style release numbering while the detector matures.

## [0.1.0-beta] - 2026-10-22

### Added

- Initial public beta of `http-php2shell-version.nse`.
- Safe version-based checks for CVE-2026-109618 and CVE-2026-109619.
- Upstream fixed-version thresholds:
  - PHP 8.2.35
  - PHP 8.3.36
  - PHP 8.4.27
  - PHP 8.5.12
- Nmap `vulns` library integration using `LIKELY_VULN` for version-only findings.
- HEAD-first HTTP probing with GET fallback.
- Optional custom-path scanning through `http-php2shell-version.paths`.
- Evidence-source and confidence reporting.
- Explicit warning for vendor/distribution backports.
- Reproducible Docker validation lab with pre-fix and fixed PHP 8.3 containers.
- Sample Nmap/Zenmap output.

### Safety

- No exploit attempt is performed.
- No memory-exhaustion or large multipart request is sent.
- Detection is based on remotely observable PHP version information only.
