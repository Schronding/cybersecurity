# Handoff — building the final `deliverable.md`

> **Purpose.** This file is written for a fresh Claude session that will write the complete
> `deliverable.md` without the prior conversation. It is a map of what exists, what each file
> holds, and what still has to be written. It asserts nothing new; every figure below is
> traceable to an evidence file in this repo.

## What to read first
1. **`evaluacion.md`** — the assignment. Part 2 is the exact report template and the grading
   rubric. The final `deliverable.md` must follow that structure. It is in Spanish.
2. **`deliverable.md`** — partial draft (Spanish). Modules 1–2 are mostly filled; several
   sections are marked `_Pendiente_`. Build the final report on top of this, not from scratch.
3. **`doubts.md`** — 76 numbered entries. This is the reasoning behind every finding: the
   HTTP-level root causes, why each tool behaved as it did, and the student's own analysis with
   corrections. The detailed write-ups in §5 of the report come from here. Entries are tagged
   `[Mechanism]` / `[Lookup]` / `[Correct]`; the ones about Modules 2–3 run roughly from entry 46.
4. **`report.md`** — the student's raw lab notebook (narration + pasted tool output). Primary
   source; `doubts.md` already distilled it.

## Environment (for §2, ID.AM)
- Target: OWASP Juice Shop `20.4.0-SNAPSHOT`, Docker image
  `bkimminich/juice-shop@sha256:adaf6a6ca50f772dff7d2fe56972c659e81a61e0dbbe607c2b39fefd436e6153`.
- Stack: Angular SPA + Node.js/Express + SQLite `3.44.2` (engine confirmed by sqlmap).
- Endpoint: reached both as `http://127.0.0.1:3000` (Nuclei) and `http://localhost:3000` (ZAP).
  Same instance; ZAP treats them as two sites, so all ZAP work uses `localhost:3000`.
- Host: NixOS on WSL2; tools from the repo `flake.nix` (`nuclei`, `zap`, `firefox`,
  `geckodriver`, `sqlmap`).
- Scope note: during Modules 1–2 the container was published on all interfaces (`0.0.0.0:3000`);
  it was relaunched on `127.0.0.1:3000` before Module 3 (doubts entry 67).

## Module 1 — Nuclei  (STATUS: scan done; findings table half-classified)
- Tool: Nuclei `v3.11.1`, templates `v10.5.2`. Command and flag rationale: `doubts.md` entry 35,
  `deliverable.md` §B.2.
- Result: **14 matches**. Raw evidence with request/response per finding:
  `nuclei_juice.jsonl` (14 lines) and `nuclei_md/` (14 finding files + `index.md`).
- Deliverable table `§B.3` lists all 14. Only **2 are classified** so far:
  `fingerprinthub:qm-system` = false positive, `tech-detect:google-font-api` = real
  (reasoning in doubts entry 44). **TODO: classify the other 12** using the jsonl (open each
  finding's response and decide real vs false positive). Juice Shop returns its index page with
  `200` for any unknown path, so treat "exposed file" hits as suspect until the response shows
  real content (doubts entry 35).

## Module 2 — OWASP ZAP  (STATUS: all scans done; comparison table 1 row short)
Tool: OWASP ZAP `2.17.0`. Deliverable 1 (Site Tree) and the passive analysis are complete;
the active-vs-passive table needs its second active row written.

**Site Tree (deliverable 1):** screenshots `m2_site_tree_root.png`, `m2_site_tree_rest.png`,
`m2_site_tree_api.png`. Full URL list: `zap_snapshot/site_tree_urls_2026-11-24_localhost.txt`
(1966 URLs). Traditional Spider: 1409 in-scope URLs (`zap_snapshot/spider_results_*_localhost.json`).
AJAX Spider added no new routes (Angular uses `#` fragments; doubts entry 55, 54).

**Passive alerts:** 16 types / 4124 instances. Full data:
`zap_snapshot/passive_alerts_2026-11-24_localhost.json`. Count table in `deliverable.md §C.3`.
Three chosen and explained at HTTP level (root causes in doubts 58, 60, 61; drafts in §C.3):
- P1 CSP Header Not Set (10038, Medium, CWE-693) — no `Content-Security-Policy` on any response.
- P2 Cross-Domain Misconfiguration (10098, Medium, CWE-264) — `Access-Control-Allow-Origin: *`.
- P3 JWT in Browser localStorage (120002, Medium, CWE-922) — token in JSON body, no `Set-Cookie`;
  bonus: JWT payload carries an unsalted MD5 password hash (CWE-916), doubts 61 & 75.

**Active scans** (`zap_snapshot/active_scan_alerts_*.json`, policy `Moderada.policy` = threshold
Medium / strength Low):
- Scan 0 search `GET /rest/products/search?q=` — 0 alerts (double-insertion; doubts 68).
- Scan 1 login `POST /rest/user/login` — **SQL Injection** (40018, High/Low) on `email`, attack `'`,
  evidence `500` + `SQLITE_ERROR` (msg 4396); plus 12× User Agent Fuzzer (Informational).
- Re-scan search at strength Medium (policy `Moderada-Media.policy`,
  `active_scan_search_medium_alerts_*.json`) — now **SQL Injection** (High/Low) on `q`, attack `'(`,
  evidence `500` + `SQLITE_ERROR: near "(": syntax error`; the response body leaks the full SQL
  statement (doubts 69, 70, 71, 72). This is the A2 row, already filled in `§C.5`.
- **TODO: write the A1 row** (login SQLi) in the `§C.5` comparison table — same flaw, different
  query shape: login quotes the input once so a single `'` breaks it; search inserts it twice
  (doubts 68, 74).

**Why active ≠ passive (for the table's framing):** passive alerts come from ZAP reading traffic
that was going to be sent anyway; active alerts only appear after ZAP sends its own attack
requests (doubts 54).

## Module 3 — sqlmap  (STATUS: done)
- Confirmed non-invasively that `POST /rest/user/login`, parameter `email`, is injectable.
- Technique: **boolean-based blind** (`OR ... WHERE/HAVING (NOT)`). Engine: **SQLite 3.44.2**.
  Proof payload: `test@juice.local' OR NOT 8716=8716-- LYYb`. 115 requests, no data dumped.
- Evidence: `sqlmap_out/sqlmap_console_login_2026-11-24.txt` (annotated console) and
  `sqlmap_out/localhost/{log,target.txt,session.sqlite}`.
- Full reasoning, the three failed low-setting runs, and why `--level/--risk` had to rise, plus
  the theory for the report: **doubts entry 76** (and 68 for the search's immunity at level 1).
- Non-invasive compliance: `--technique=B` only, no `--dump/--tables/--columns`, `--banner` reads
  only the version string (the "banner básico" the guide permits).

## The vulnerability chain to feature in §4/§5
The SQL injection is confirmed by three independent methods, a strong lead finding:
ZAP active scan → the application's own leaked error/SQL statement → sqlmap. Endpoint
`POST /rest/user/login`, param `email`, A03:2021 / CWE-89. Suggested CVSS and the NIST CSF 2.0
mapping are NOT yet written.

## Still to write in `deliverable.md` — ✅ DONE (2026-11-24)
All sections below are now written; `deliverable.md` is at Version 1.0 (no `_Pendiente_` left).
1. ✅ §B.3 — all 14 nuclei findings classified (13 real incl. tech/info, 1 false positive = qm-system).
2. ✅ §C.4 login analysis + §C.5 row A1 (login SQLi) written.
3. ✅ §1 Executive summary + Governance (GV); §3 Risk model (CVSS bands + probability×impact
   matrix); §4 consolidated matrix (7 VULNs); §5 detailed cards (VULN-01…07); §6 NIST CSF 2.0
   remediation plan (all 6 functions). Annex D (sqlmap) written in full.
4. ✅ Severity totals for §1: Crítica 1 / Alta 0 / Media 6 / Baja 2 / Informativa 7.

**Judgment calls made while writing (worth a glance):**
- Consolidated matrix = 7 prioritized VULNs; the many ZAP passive Medium/Low alerts are folded
  into the relevant VULN (headers→VULN-02, CORS→VULN-03, JWT→VULN-04, error disclosure→VULN-06)
  rather than listed as separate rows.
- Off-site Redirect: ZAP labeled its 1 instance High; re-rated to **Medio** (needs user
  interaction, no confidentiality impact). Exact param/allowlist-bypass left unconfirmed
  (out of non-invasive scope). This is the one finding not independently re-verified.
- CVSS vectors/scores are my estimates per finding (VULN-01 = 9.8; others 4.3–6.5).
- Fecha de Evaluación set to 23–24/11/2026 (Nuclei ran 23rd; ZAP+sqlmap 24th).
- `[Nombres y Matrículas]` and institution name left as placeholders for the student.

## Evidence integrity
- All real session JWTs were scrubbed to `eyJ.<JWT-SCRUBBED>` across `report.md`, the 4 `.har`
  files, both `passive_alerts*.json`, and `zap_report_*.md` (1385 replacements; none remain).
- Passwords/hashes were left as-is on the student's instruction (intentional throwaway values).
- `zap_snapshot/*.har` total ~40 MB; keep or `.gitignore` per preference — they are raw traffic,
  not required to write the report (the JSON alert exports are the usable evidence).
