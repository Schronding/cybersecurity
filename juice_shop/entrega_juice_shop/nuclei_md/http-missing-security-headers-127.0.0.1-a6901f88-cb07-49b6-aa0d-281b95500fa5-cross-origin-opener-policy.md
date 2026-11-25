### HTTP Missing Security Headers (http-missing-security-headers:cross-origin-opener-policy) found on 127.0.0.1

----
**Details**: **http-missing-security-headers:cross-origin-opener-policy** matched at 127.0.0.1

**Protocol**: HTTP

**Full URL**: http://127.0.0.1:3000

**Timestamp**: Mon Nov 23 09:35:34 -0600 CST 2026

**Template Information**

| Key | Value |
| --- | --- |
| Name | HTTP Missing Security Headers |
| Authors | socketz, geeknik, g4l1t0, convisoappsec, kurohost, dawid-czarnecki, forgedhallpass, jub0bs, userdehghani, celbahraoui, safejulian |
| Tags | misconfig, headers, generic, vuln |
| Severity | info |
| Description | This template searches for missing HTTP security headers. The impact of these missing headers can vary.<br> |
| CWE-ID | [CWE-693](https://cwe.mitre.org/data/definitions/693.html) |
| CVSS-Score | 0.00 |

**Request**
```http
GET / HTTP/1.1
Host: 127.0.0.1:3000
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15
Accept: */*
Accept-Language: en
Accept-Encoding: gzip


```

**Response**
```http
HTTP/1.1 200 OK
Transfer-Encoding: chunked
Accept-Ranges: bytes
Access-Control-Allow-Origin: *
Cache-Control: public, max-age=0
Connection: keep-alive
Content-Type: text/html; charset=UTF-8
Date: Mon, 23 Nov 2026 15:35:34 GMT
Etag: W/"2667-1a1f5fdc378"
Feature-Policy: payment 'self'
Keep-Alive: timeout=5
Last-Modified: Thu, 19 Nov 2026 22:46:51 GMT
Vary: Accept-Encoding
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-Recruiting: /#/jobs

<!--
  ~ Copyright (c) 2014-2026 Bjoern Kimminich & the OWASP Juice Shop contributors.
  ~ SPDX-License-Identifier: MIT
  -->

<!doctype html>
<html lang="en" data-beasties-container>
<head>
  <meta charset="utf-8">
  <title>OWASP Juice Shop</title>
  <meta name="description" content="Probably the most modern and sophisticated insecure web application">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <style>@font-face{font-family:'VT323';font-style:normal;font-weight:400;font-display:swap;src:url(https://fonts.gstatic.com/s/vt323/v18/pxiKyp0ihIEF2isQFJXGdg.woff2) format('woff2');unicode-range:U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;}@font-face{font-family:'VT323';font-style:normal;font-weight:400;font-display:swap;src:url(https://fonts.gstatic.com/s/vt323/v18/pxiKyp0ihIEF2isRFJXGdg.woff2) format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;}@font-face{font-family:'VT323';font-style:normal;font-weight:400;font-display:swap;src:url(https://fonts.gstatic.com/s/vt323/v18/pxiKyp0ihIEF2isfFJU.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}</style>
  <link id="favicon" rel="icon" type="image/x-icon" href="assets/public/favicon_js.ico">
  <script>
    window.addEventListener("load", function(){
      window.cookieconsent.initialise({
        "palette": {
          "popup": { "background": "var(--theme-primary)", "text": "var(--theme-text)" },
          "button": { "background": "var(--theme-accent)", "text": "var(--theme-text)" }
        },
        "theme": "classic",
        "position": "bottom-right",
        "content": { "message": "This website uses fruit cookies to ensure you get the juiciest tracking experience.", "dismiss": "Me want it!", "link": "But me wait!", "href": "https://www.youtube.com/watch?v=9PnbKL3wuH4" }
      })});
  </script>
<style>.bluegrey-lightgreen-theme{--mat-sys-background:#121316;--mat-sys-error:#ffb4ab;--mat-sys-error-container:#93000a;--mat-sys-inverse-on-surface:#2f3033;--mat-sys-inverse-primary:#005cbb;--mat-sys-inverse-surface:#e3e2e6;--mat-sys-on-background:#e3e2e6;--mat-sys-on-error:#690005;--mat-sys-on-error-container:#ffdad6;--mat-sys-on-primary:#002f65;--mat-sys-on-primary-container:#d7e3ff;--mat-sys-on-primary-fixed:#001b3f;--mat-sys-on-primary-fixed-variant:#00458f;--mat-sys-on-secondary:#283041;--mat-sys-on-secondary-container:#dae2f9;--mat-sys-on-secondary-fixed:#131c2b;--mat-sys-on-secondary-fixed-variant:#3e4759;--mat-sys-on-surface:#e3e2e6;--mat-sys-on-surface-variant:#e0e2ec;--mat-sys-on-tertiary:#173800;--mat-sys-on-tertiary-container:#82ff10;--mat-sys-on-tertiary-fixed:#0b2000;--mat-sys-on-tertiary-fixed-variant:#245100;--mat-sys-outline:#8e9099;--mat-sys-outline-variant:#44474e;--mat-sys-primary:#abc7ff;--mat-sys-primary-container:#00458f;--mat-sys-primary-fixed:#d7e3ff;--mat-sys-primary-fixed-dim:#abc7ff;--mat-sys-scrim:#000000;--mat-sys-secondary:#bec6dc;--mat-sys-secondary-container:#3e4759;--mat-sys-secondary-fixed:#dae2f9;--mat-sys-secondary-fixed-dim:#bec6dc;--mat-sys-shadow:#000000;--mat-sys-surface:#121316;--mat-sys-surface-bright:#38393c;--mat-sys-surface-container:#1f2022;--mat-sys-surface-container-high:#292a2c;--mat-sys-surface-container-highest:#343537;--mat-sys-surface-container-low:#1a1b1f;--mat-sys-surface-container-lowest:#0d0e11;--mat-sys-surface-dim:#121316;--mat-sys-surface-tint:#abc7ff;--mat-sys-surface-variant:#44474e;--mat-sys-tertiary:#70e000;--mat-sys-tertiary-container:#245100;--mat-sys-tertiary-fixed:#82ff10;--mat-sys-tertiary-fixed-dim:#70e000;--mat-sys-neutral-variant20:#2d3038;--mat-sys-neutral10:#1a1b1f;--mat-sys-level0:0px 0px 0px 0px rgba(0, 0, 0, .2), 0px 0px 0px 0px rgba(0, 0, 0, .14), 0px 0px 0px 0px rgba(0, 0, 0, .12);--mat-sys-level1:0px 2px 1px -1px rgba(0, 0, 0, .2), 0px 1px 1px 0px rgba(0, 0, 0, .14), 0px 1px 3px 0px rgba(0, 0, 0, .12);--mat-sys-level2:0px 3px 3px -2px rgba(0, 0, 0, .2), 0px 3px 4px 0px rgba(0, 0, 0, .14), 0px 1px 8px 0px rgba(0, 0, 0, .12);--mat-sys-level3:0px 3px 5px -1px rgba(0, 0, 0, .2), 0px 6px 10px 0px rgba(0, 0, 0, .14), 0px 1px 18px 0px rgba(0, 0, 0, .12);--m.... Truncated ....
```


**CURL command**
```sh
curl -X 'GET' -d '' -H 'Accept: */*' -H 'Accept-Language: en' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15' 'http://127.0.0.1:3000'
```

----

Generated by [Nuclei v3.11.1](https://github.com/projectdiscovery/nuclei)