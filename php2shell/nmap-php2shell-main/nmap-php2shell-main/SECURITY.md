# Security Policy

## Reporting a security issue in this project

If you find a security issue in the NSE script, lab configuration, or repository
content, please avoid publishing exploit details in a public issue before the
maintainer has had an opportunity to review them.

Use GitHub's private vulnerability reporting feature for this repository when it
is enabled. If private reporting is unavailable, open a minimal public issue that
describes the affected project component without including sensitive exploit
material, and ask the maintainer for a private reporting channel.

## Scope

This repository is a defensive detection utility. The NSE script performs
version fingerprinting and does not attempt to exploit CVE-2026-109618 or
CVE-2026-109619.

Security reports about PHP itself should be directed to the PHP project rather
than this repository.

## Safe-use expectation

Only scan systems you own or are explicitly authorized to assess. The included
Docker lab is intended for local validation and should not be exposed directly
to the public Internet.
