# Installation

## Linux / Unix-like Nmap installation

Find the Nmap script directory. A common location is:

```text
/usr/share/nmap/scripts
```

Copy the script:

```sh
sudo cp scripts/http-php2shell-version.nse /usr/share/nmap/scripts/
sudo nmap --script-updatedb
```

Verify that Nmap can load it:

```sh
nmap --script-help http-php2shell-version
```

## Windows / Zenmap

A common installer path is:

```text
C:\Program Files (x86)\Nmap\scripts
```

Copy `scripts\http-php2shell-version.nse` into that directory using an
Administrator account, then open an elevated PowerShell or Command Prompt and
run:

```text
nmap --script-updatedb
nmap --script-help http-php2shell-version
```

Zenmap uses the same Nmap installation and NSE scripts.

## Basic scan

```sh
nmap -Pn -sV -p 80,443,8080,8443 \
  --script http-php2shell-version \
  TARGET
```

Nmap's `vulns` library normally suppresses `NOT_VULN` entries. To include
patched-version controls in output:

```sh
nmap -Pn -sV -p 80,443,8080,8443 \
  --script http-php2shell-version \
  --script-args vulns.showall \
  TARGET
```

## Additional application paths

The script checks only `/` by default. To inspect known paths:

```sh
nmap -Pn -sV -p 80,443 \
  --script http-php2shell-version \
  --script-args 'http-php2shell-version.paths=/,/index.php,/phpinfo.php' \
  TARGET
```

Only scan assets you own or are authorized to assess.
