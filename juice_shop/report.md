# My report

I do have docker installed in my NixOS machine

```
 docker --version
Docker version 29.6.2, build v29.6.2
```

```
docker pull bkimminich/juice-shop
```

And I got 

```
Digest: sha256:adaf6a6ca50f772dff7d2fe56972c659e81a61e0dbbe607c2b39fefd436e6153
Status: Downloaded newer image for bkimminich/juice-shop:latest
docker.io/bkimminich/juice-shop:latest
```

```
docker run \--rm \-p 127.0.0.1:3000:3000 bkimminich/juice-shop
```

Now it works and I have it open in localhost

```
info: Server listening on port 3000
```

Now I need to install nuclei, which I should just put in my flake.nix if I am not mistaken. 

Everything seems to be working well

```
 nuclei -update-templates

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

                projectdiscovery.io

[INF] nuclei-templates are not installed, installing...
[INF] Successfully installed nuclei-templates at /home/nixos/nuclei-templates
[INF] No new updates found for nuclei templates
```

What are the relevant templates I need to have? 

I am checking at a guide some years ago and I found this

```
 nuclei -t https://example.com -t ~/nuclei-templates/

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

                projectdiscovery.io

[FTL] Could not run nuclei: Could not create loader.: Remote template URL host (example.com) is not present in the `remote-template-domain` list in nuclei config
```

So at least that command doesn't work

I ran 

```
nuclei -u https://127.0.0.1:3000 -t ~/nuclei-templates/
```

and its taking quite some time, so I assume it is working. 

There are a lot of templates to choose from, and indeed it seems I download them all

```
cd ~/nuclei-templates/
direnv: unloading

[nixos@nixos:~/nuclei-templates]$ ls
cloud                   network
code                    profiles
CODE_OF_CONDUCT.md      PULL_REQUEST_TEMPLATE.md
CONTRIBUTING.md         README_CN.md
contributors.json       README_JA.md
cves.json               README_KR.md
cves.json-checksum.txt  ssl
dast                    TEMPLATE-CREATION-GUIDE.md
dns                     TEMPLATE-REVIEW-GUIDE.md
file                    templates-checksum.txt
headless                TEMPLATES-STATS.json
helpers                 TEMPLATES-STATS.md
http                    TOP-10.md
javascript              websocket
LICENSE.md              workflows
```

For what it seems I am scanning with all the templates instead of the relevant ones... that was a mistake. 

I don't know where I got lost but I was waiting for the command to stop running when it had a long time ago 

```
nuclei -u https://127.0.0.1:3000 -t ~/nuclei-templates/

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

                projectdiscovery.io

[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.2 (latest)
[INF] New templates added in latest release: 121
[INF] Templates loaded for current scan: 11330
[INF] Executing 11330 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 2737 (Reduced 2602 Requests)
[INF] Skipped 127.0.0.1:5814 from target list as found unresponsive permanently: Get "https://127.0.0.1:5814/autopass": cause="port closed or filtered" address=127.0.0.1:5814 chain="connection refused"
[INF] Skipped 127.0.0.1:4040 from target list as found unresponsive permanently: cause="port closed or filtered" address=127.0.0.1:4040 chain="connection refused; got err while executing https://127.0.0.1:4040/jobs/"
[INF] Scan completed in 7m. 0 matches found.
[INF] HTTP connections: 4 total, 3 new, 1 reused (25.0%)
```

I did it again... but this should be a mistake, doesn't it? the juice shop is full of vulnerabilities and it found none 

```
nuclei -u http:127.0.0.1:3000

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

                projectdiscovery.io

[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.2 (latest)
[INF] New templates added in latest release: 121
[INF] Templates loaded for current scan: 11330
[INF] Executing 11330 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[INF] Running httpx on input host
[INF] Found 0 URL from httpx
[INF] Templates clustered: 2737 (Reduced 2602 Requests)
[INF] Scan completed in 26.494100109s. No results found.
```

Indeed I just need to use the folders that will most likely help me, so coming back to the templates I have 

```
[nixos@nixos:~/nuclei-templates]$ ls
cloud                   network
code                    profiles
CODE_OF_CONDUCT.md      PULL_REQUEST_TEMPLATE.md
CONTRIBUTING.md         README_CN.md
contributors.json       README_JA.md
cves.json               README_KR.md
cves.json-checksum.txt  ssl
dast                    TEMPLATE-CREATION-GUIDE.md
dns                     TEMPLATE-REVIEW-GUIDE.md
file                    templates-checksum.txt
headless                TEMPLATES-STATS.json
helpers                 TEMPLATES-STATS.md
http                    TOP-10.md
javascript              websocket
LICENSE.md              workflows
```

The ones that seem the most relevant are dns, headless, websocket. 

The professor says that `-jsonl` is to save it in JSONL and with `-o` I gave the file the name. 

The categories that seem to be the most relevant are the ones that run with this scan

```
nuclei -u http://127.0.0.1:3000 -pt http \
  -tags exposure,misconfig,headers,tech \
  -etags intrusive,default-login \
  -s info,low,medium,high \
  -ni -rl 10 -c 5 \
  -jle nuclei_juice.jsonl -me nuclei_md
```

What does the `-pt` flag mean? I understand that it only runs http but what `-pt` stands for? 

I assume the `jle` and `me` mean something like "JSONL extend" and "Markdown extend", so we can have just one file that grows through time instead of being constantly replaced. 

It went through! 

```
nuclei -u http://127.0.0.1:3000 -pt http \
  -tags exposure,misconfig,headers,tech \
  -etags intrusive,default-login \
  -s info,low,medium,high \
  -ni -rl 10 -c 5 \
  -jle nuclei_juice.jsonl -me nuclei_md

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v3.11.1

                projectdiscovery.io

[INF] Current nuclei version: v3.11.1 (latest)
[INF] Current nuclei-templates version: v10.5.2 (latest)
[INF] New templates added in latest release: 121
[INF] Templates loaded for current scan: 3021
[INF] Executing 3021 signed templates from projectdiscovery/nuclei-templates
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 1199 (Reduced 1137 Requests)
[swagger-api] [http] [info] http://127.0.0.1:3000/api-docs/swagger.json [paths="/api-docs/swagger.json"]
[http-missing-security-headers:content-security-policy] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:permissions-policy] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:x-permitted-cross-domain-policies] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:referrer-policy] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:cross-origin-embedder-policy] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:cross-origin-opener-policy] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:cross-origin-resource-policy] [http] [info] http://127.0.0.1:3000
[http-missing-security-headers:strict-transport-security] [http] [info] http://127.0.0.1:3000
[INF] Skipped 127.0.0.1:5814 from target list as found unresponsive permanently: Get "https://127.0.0.1:5814/autopass": cause="port closed or filtered" address=127.0.0.1:5814 chain="connection refused"
[prometheus-metrics] [http] [medium] http://127.0.0.1:3000/metrics
[fingerprinthub-web-fingerprints:qm-system] [http] [info] http://127.0.0.1:3000
[tech-detect:google-font-api] [http] [info] http://127.0.0.1:3000
[deprecated-feature-policy] [http] [info] http://127.0.0.1:3000 ["payment 'self'"]
[owasp-juice-shop-detect] [http] [info] http://127.0.0.1:3000
[INF] Scan completed in 9m. 14 matches found.
[INF] HTTP connections: 5107 total, 1582 new, 3525 reused (69.0%)
```

But I don't see the `nuclei_juice.jsonl` or `nuclei_md` files anywhere. 

It seems that I have done everything that was required in this first part

I need to install `zaproxy` so back to the `flake.nix` file. 

It didn't work, that probably isn't the name

```
nix-direnv: /home/nixos/repos/cybersecurity/flake.nix
error:
       … while calling the 'derivationStrict' builtin
         at «nix-internal»/derivation-internal.nix:37:12:
           36|
           37|   strict = derivationStrict drvAttrs;
             |            ^
           38|

       … while evaluating derivation 'nix-shell'
         whose name attribute is located at «github:NixOS/nixpkgs/dc5d91f840324650bac8c379428c7037a416959a?narHash=sha256-VaWGJ6%2BcIYN2erfSecbRV%2B4ljI185Ty2wUrXyvQbgOw%3D»/pkgs/stdenv/generic/make-derivation.nix:651:11

       … while evaluating attribute 'nativeBuildInputs' of derivation 'nix-shell'
         at «github:NixOS/nixpkgs/dc5d91f840324650bac8c379428c7037a416959a?narHash=sha256-VaWGJ6%2BcIYN2erfSecbRV%2B4ljI185Ty2wUrXyvQbgOw%3D»/pkgs/stdenv/generic/make-derivation.nix:719:11:
          718|           depsBuildBuild = buildBuildOutputs;
          719|           nativeBuildInputs = buildHostOutputs;
             |           ^
          720|           depsBuildTarget = buildTargetOutputs;

       (stack trace truncated; use '--show-trace' to show the full, detailed trace)

       error: undefined variable 'zaproxy'
       at /home/nixos/repos/cybersecurity/flake.nix:12:11:
           11|           nuclei
           12|           zaproxy
             |           ^
           13|           unzip
```

With zap I am struggling a lot in finding the tools that Claude tells me, I have version 2.17, the latest, and I went to tools > client spider and selected the following 

![client spider](image-5.png)

It doesn't allow me to run, as it says I need a valid starting point along with the protocol

![error spider scan](image-6.png)

I think the problem is that I am not putting the complete address 

Now it works, and it seems it went through everything fairly quickly, which is suspicious for me as my computer is not that powerful. Maybe AJAX will require more power

I went through

![AJAX spider](image-7.png)

but it is telling me that 

![error ajax spider scan](image-8.png)

What is the scope in this scenario? I will uncheck that mark for now 

Now it is working

IT seems it broke somewhere along the way, could this be by the poor hardware power of my machine? 

![error during ajax spider scan](image-9.png)

