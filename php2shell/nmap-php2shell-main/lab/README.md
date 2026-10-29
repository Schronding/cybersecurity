# Validation Lab

This lab provides two disposable Apache/PHP containers for validating the NSE
script without testing an unrelated third-party system.

- `localhost:8080` - PHP 8.3.35 (pre-fix control)
- `localhost:8081` - PHP 8.3.36 (fixed control)

The PHP project identifies PHP 8.3.36 as the security release containing the
fixes for CVE-2026-109618 and CVE-2026-109619.

## Start the lab

From this directory:

```sh
docker compose up -d
```

Confirm the containers:

```sh
docker compose ps
```

## Browser check

Open:

```text
http://127.0.0.1:8080/
http://127.0.0.1:8081/
```

The first page should report PHP 8.3.35 and the second PHP 8.3.36.

## Nmap check

After installing the NSE script, run:

```sh
nmap -Pn -sV -p 8080,8081 \
  --script http-php2shell-version \
  --script-args vulns.showall \
  127.0.0.1
```

Expected classification:

- 8.3.35 - `LIKELY VULNERABLE`
- 8.3.36 - `NOT VULNERABLE` by reported upstream version

## Stop and remove the lab

```sh
docker compose down
```

## Important

`phpinfo()` exposes detailed server information. These containers are for local
or isolated-lab use only. Do not publish ports 8080/8081 to the Internet and do
not leave the lab running after testing.
