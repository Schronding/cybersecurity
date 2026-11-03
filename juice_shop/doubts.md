## juice_shop.md

Comments are the four prose paragraphs, numbered 0–3 in order of appearance.

### 0. nmap finds ports; it doesn't open them, and targets carry no port (juice_shop.md - comments 0, 3) [Mechanism]
#### User's Discovery/Doubt:
> I don't even remember what nmap was for...

> It didn't work the way I expected
#### Verdict:
Wrong - the command treats `IP:port` like a URL, but an nmap target is a host only. Ports go in their own option, and you reach the app with a browser.
#### Explanation:
nmap is a **network scanner**. It sends probes and reports which hosts are up and which ports are open, closed or filtered. It never connects you to the service. nmap reads everything after the options as a **target specification** (hostname, IP, CIDR or range). So it took `132.248.185.212:3000` as a hostname, the DNS lookup failed, and it scanned 0 hosts. You choose ports with `nmap -p <ports> <target>`. Next pitfall (verified): nmap quits if you pass `-F` and `-p` together. Verified with one request: `http://132.248.185.212:3000/` serves the page titled "OWASP Juice Shop".

### 1. A bare IP is a complete target (juice_shop.md - comment 1) [Mechanism]
#### User's Discovery/Doubt:
> Is it enough that I put the plain ip? Don't I need to add a red segment?
#### Verdict:
Wrong - you don't need a segment. A bare IP scans exactly that host, and CIDR notation only widens the target to a range.
#### Explanation:
`/24` fixes the first 24 bits, so it covers all 256 addresses from 132.248.185.0 to .255. Your first output already shows that the bare IP worked: "1 IP address (1 host up)". Adding the segment produced the second output, with 256 addresses and 90 hosts up. Ranges are for discovery when you don't yet know which host you want.

### 2. Repeated open ports aren't copies of Juice Shop (juice_shop.md - comment 2) [Mechanism]
#### User's Discovery/Doubt:
> It is interesting that it is scanning the whole red segment, so I believe the professor must have just copied a version of the Juice Shop. Then I think I should just access the specific port
#### Verdict:
Partly correct - going to the specific port is right. But the ports that repeat across hosts are not copies of Juice Shop. Juice Shop is the port 3000 service, and only .212 shows it.
#### Explanation:
Juice Shop is a Node.js app that listens on **TCP 3000** by default. nmap's SERVICE column is a lookup by port number in its `nmap-services` table, not a detection. The table lists 3000 as "ppp" (verified). Ports 2000 and 5060 show as open on almost every host, including the router at .254. That fits a firewall doing SCCP/SIP inspection that answers on behalf of the hosts behind it. This part is inferred, not verified. Version detection (`-sV`) on those ports of one host would settle it.

### 3. Unprompted correction: `-oA` overwrites (juice_shop.md) [Mechanism]
#### User's Discovery/Doubt:
> (no comment; every run reuses `-oA sneaky_scan`)
#### Verdict:
Wrong - reusing one `-oA` basename doesn't keep earlier results. Each run overwrites all three files.
#### Explanation:
`-oA <basename>` writes `.nmap`, `.gnmap` and `.xml` files and overwrites any that exist. Verified: the files in this folder hold only the failed 08:55 run. The 08:50 scan that found port 3000 now exists only in your notes. `--append-output` changes this, but appended XML generally won't parse.

### 4. The `'` probe and the `[object Object]` on the form (juice_shop.md - comment 4) [Mechanism]
#### User's Discovery/Doubt:
> I remember the trick of my professor of using ' in order to see if there was the possibility of SQL injection. When I put a ' both in the Email and the Password I got

> [object Object]

> on top of the form
#### Verdict:
Partly correct - using `'` to probe for SQL injection is right; the belief to fix is that `[object Object]` is the SQL error. It is the browser stringifying a JavaScript error object, which only indirectly confirms your input reached the backend.
#### Explanation:
A single quote is the string delimiter in SQL. If the app pastes your input straight into a query, an odd quote breaks the syntax and the database raises an error — the classic signal that the field may be injectable. What you saw is one step removed from that. The frontend received an error object from the server and rendered it with JavaScript's default string conversion, which for a plain object is the literal text `[object Object]`. So you learned the server threw an error on the quote (promising) but the message itself was swallowed by the UI. The standard next move is to read the real error: open the browser devtools Network tab and look at the failing request's JSON response body, which usually carries the raw SQL message. This is the general behaviour of JS objects, not something specific to this app.

### 5. Whether the scans were pointless given one target (juice_shop.md - comment 5) [Mechanism]
#### User's Discovery/Doubt:
> So for what I understand there is no point in doing the nmap scans, as I just have one address that interests me.
#### Verdict:
Partly correct - host *discovery* across a range is indeed moot once you know the host, but scanning that one host is still the point: it tells you which ports and service versions are exposed.
#### Explanation:
There are two jobs people call "scanning". One is discovery: sweeping a `/24` to find which hosts exist. That you no longer need. The other is enumeration of a known host: which ports are open, and what software and version answers on each (`-sV`). For a web target that second job is where the value is — it confirms the app is on 3000 and can reveal the stack behind it. The exploitation itself then happens in the browser, not in nmap.

### 6. Is the OS worth knowing (juice_shop.md - comment 6) [Correct]
#### User's Discovery/Doubt:
> I don't know if I need to know the OS, but it seems like valuable information
#### Verdict:
Correct - the OS is standard recon. For a web-app task like Juice Shop it is usually marginal, since the vulnerabilities live in the application, not the kernel.

### 7. Why OS and SYN scans need sudo (juice_shop.md - comment 7) [Lookup]
#### User's Discovery/Doubt:
> Again I got that first of all I need to use sudo, why is that?
#### Verdict:
No prior assumption - you asked without proposing an answer.
#### Explanation:
`-O` (OS detection) and `-sS` (SYN scan) build raw IP/TCP packets and read raw replies rather than going through the normal connect() system call. Opening a raw socket is a privileged operation on Linux, so the kernel requires root (or the `CAP_NET_RAW` capability). Without it nmap falls back to `-sT`, which needs no privilege but is slower and more visible.

### 8. The scan ran against the wrong host (juice_shop.md - comment 8) [Mechanism]
#### User's Discovery/Doubt:
> Afterwards I got the problem again that I can scan the port
#### Verdict:
Wrong - two separate failures: `IP:3000` fails as before, and the address you fell back to is not the Juice Shop host at all.
#### Explanation:
Appending `:3000` failed for the reason in entry 0 — a port is not part of an nmap target. The second command dropped the port but typed `132.248.212`, three octets instead of four. nmap pads a short dotted address by inserting zeros before the last octet, so it became `132.248.0.212` — verified here with `nmap -sL`. That is a different machine from the Juice Shop at `132.248.185.212`. The open ports it found (21, 25, 80, 110, 143, 443) look like a mail/web server, and port 3000 is absent, which is the tell that you scanned the wrong host. Every `?` after a service name (`ftp?`, `http?`) means `-sV` could not confirm the service from its banner, only guess from the port number.

### 9. How nmap guesses the OS, and why it couldn't here (juice_shop.md - comment 9 and the "Rocky Linux / docker" note) [Mechanism]
#### User's Discovery/Doubt:
> How does nmap even know what OS is attacking? What are the telltale signs?

> I assume the reason why it can't guess is that my professor put it in a docker container (which is probably Rocky Linux) but as it didn't went too far (I think to avoid detection) it could not be sure.
#### Verdict:
Wrong - the failure is not a container hiding, nor a deliberately shallow scan; nmap simply lacked enough open+closed ports to fingerprint, partly because this was the wrong host.
#### Explanation:
OS detection is TCP/IP **stack fingerprinting**. nmap sends about sixteen crafted probes and measures how the stack replies: the TCP initial sequence number pattern, default window size, which TCP options appear and in what order, the IP TTL, the don't-fragment bit, and specific ICMP behaviours. It matches that signature against `nmap-os-db`. The method needs at least one open and one closed port to calibrate; "test conditions non-ideal" means it didn't get that clean pair. A container doesn't hide this — a Docker container shares the host's Linux kernel, so it would fingerprint *as* that kernel, not mask it. The "Linux 3.X" guess is also suspect precisely because you scanned `132.248.0.212`, not the Juice Shop host.

### 10. What profinet is (juice_shop.md - comment 10) [Lookup]
#### User's Discovery/Doubt:
> What are profinet devices?
#### Verdict:
No prior assumption - a definition question.
#### Explanation:
PROFINET is an industrial Ethernet protocol used in factory and process automation to talk to PLCs and other control hardware (originally Siemens). A `safe` script probed for it and reported none on your subnet, which is expected — you are on an office/lab network, not an industrial control one.

### 11. What `--script safe` actually guarantees (juice_shop.md - comment 11) [Mechanism]
#### User's Discovery/Doubt:
> For what I recall the command script safe was used so the requests of nmap would not serve as an unintended DOS.
#### Verdict:
Partly correct - `safe` does avoid harming the target, but the guarantee is about script *behaviour*, not request *volume*; it is not a rate limiter against DoS.
#### Explanation:
NSE scripts are tagged by category. `safe` is the set whose authors judged they won't crash services, exploit anything, use large resources, or otherwise be seen as hostile — the opposite category is `intrusive`. So `--script safe` won't *do* something damaging to the target. It does not throttle how fast packets go out; flooding a fragile host is controlled by the timing templates (`-T0`..`-T5`) and `--max-rate`, not by the script category. Your instinct — "don't accidentally break it" — is right; the mechanism is script selection, not traffic shaping.

### 12. Are PEAP / EAP-MSCHAPv2 / EAP-TLS / EAP-TTLS all MITM-vulnerable (juice_shop.md - comment 12) [Mechanism]
#### User's Discovery/Doubt:
> I imagine PEAP, EAP-MSCHAP-V2, EAP-TLS, EAP-TTLS are protocols of communication and that one if not all of them might be vulnerable to a network sniffer (a man in the middle)
#### Verdict:
Partly correct - they are 802.1X/WPA-Enterprise authentication methods, and the "not all" caution is the key: EAP-TLS is the strong one, the others are only vulnerable under a specific misconfiguration.
#### Explanation:
These are EAP methods for network authentication, not general comms protocols. The real risk is not passive sniffing — the credential exchange runs inside a TLS tunnel — but an **evil-twin** attack where a rogue access point impersonates the real one. PEAP and EAP-TTLS wrap an inner password method (often MSCHAPv2, which is weak and crackable offline if captured). They are safe *only if* the client is configured to verify the server's certificate; if it isn't, a fake AP completes the tunnel and harvests the inner credentials. EAP-TLS is the outlier: it authenticates both sides with certificates, so there is no password for a rogue AP to steal. So "if not all" is the right hedge — EAP-TLS is the robust one.

### 13. NSE timing lines and the frozen terminal (juice_shop.md - comment 14) [Lookup]
#### User's Discovery/Doubt:
> What are these things of NSE Timing? My terminal doesn't allow me to put any other command nor to exit, and I don't know if it is actually doing something.
#### Verdict:
No prior assumption - you asked what the lines mean and whether it is stuck.
#### Explanation:
NSE is the Nmap Scripting Engine. Those lines are live progress for the script phase: percent complete and an estimated time to completion. The terminal is "stuck" because nmap holds the foreground until the scan finishes — it is working, not hung. Press any key (or Enter) to print an immediate status line; press Ctrl-C to abort. This is terminal/tool behaviour, not something about the target.

### 14. The 500 is the finding, not background noise (juice_shop.md - comment 15) [Mechanism]
#### User's Discovery/Doubt:
> It seems that I can see an error...

> Failed to load resource: the server responded with a status of 500 (Internal Server Error)

> I don't actually see anything relevant, just the loading of the necessary componentes for the page to run.
#### Verdict:
Wrong - the `500 Internal Server Error` is the relevant line; the rest are just the page's own assets loading, and the detail you want is one level inside that one request.
#### Explanation:
The Network tab lists every request the page makes, and most are what you noticed — scripts, styles and images the app pulls to render. The single line that matters is the one that returned 500. A 500 means the server-side code hit an unhandled error while processing that request, which is exactly what a malformed input is meant to provoke: the backend choked rather than rejecting you cleanly. The message you're after is not in the request list; it is in that request's own detail. Click the failing request, then open its **Response** (or **Preview**) sub-tab, which holds the body the server sent back. The `[object Object]` from entry 4 was that same body after the UI flattened it to a string — here you see it raw.

### 15. Why the earlier turn was cut off (juice_shop.md - comment 16) [Lookup]
#### User's Discovery/Doubt:
> It seems that I messed up with the host and that was probably the reason why Claude Opus 5.5 put me a guardrail.
#### Verdict:
Wrong - the cut-off came from an automated safety classifier reacting to the wording of the exchange, not from which host was scanned; the two are unrelated.
#### Explanation:
The guardrail is a separate automated system that reads the text of a turn. It has no notion of nmap targets or of a right-versus-wrong IP, so scanning `132.248.0.212` did not trigger it. Naming the setting plainly — a supervised OWASP Juice Shop lab — is what lets the explanations continue.

### 16. How you issue a GET, and what 200 OK actually means (juice_shop.md - comments 17, 19) [Mechanism]
#### User's Discovery/Doubt:
> On step one it says that "GET http://localhost:3000/rest/user?sort=price:ASC,createdAt:DESC" but where I am supposed to do this? mmm for what I know get is a way in which machines communicate, so if I get 200 OK I assume that means the database is exposed.

> It seems I cannot simply use get blindly

> GET 132.248.185.212:3000/rest/user?sort=price:ASC,createdAt:DESC
> GET: command not found
#### Verdict:
Wrong - two false beliefs: that `GET` is a shell command, and that a 200 OK means the database is exposed. GET is an HTTP method issued by an HTTP client, and 200 means only that the request succeeded.
#### Explanation:
HTTP defines request methods; GET asks a server for the resource at a URL. Your shell replied `GET: command not found` because the shell has no program by that name — the word is meaningful only inside an HTTP client. You send one by pasting the full URL, scheme included (`http://...`), into a browser's address bar, which always makes a GET; or with `curl -i 'http://host:3000/path'`; or from the devtools. Note the guide's address is `localhost:3000`, which means the machine running the app — from your side you substitute the lab host. The status code reports that one exchange: 200 = handled and a body returned, 500 = it errored. A 200 is the ordinary reply for virtually every working URL, so it says nothing about a database being "exposed." What carries meaning is the response body — for this endpoint, the JSON the API is built to return.

## Noted
- juice_shop.md (unnumbered block after comment 17) - the re-run `--script safe` scan, this time against the correct host `132.248.185.212`; narration/evidence, nothing asserted.

## Not addressed
- none
