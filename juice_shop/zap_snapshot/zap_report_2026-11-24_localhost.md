# OWASP Juice Shop - ZAP (localhost:3000)

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 2 |
| Medium | 6 |
| Low | 4 |
| Informational | 6 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 29    |
| Info | Informational | http://localhost:3000 | Percentage of responses with status code 1xx | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of responses with status code 2xx | 72 % |
| Info | Informational | http://localhost:3000 | Percentage of responses with status code 3xx | 11 % |
| Info | Exceeded Low | http://localhost:3000 | Percentage of responses with status code 4xx | 10 % |
| Info | Exceeded Low | http://localhost:3000 | Percentage of responses with status code 5xx | 5 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type application/javascript | 2 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type application/json | 4 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type application/pdf | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type font/woff | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type font/woff2 | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type image/avif | 2 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type image/jpeg | 3 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type image/png | 2 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type image/x-icon | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type text/css | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type text/event-stream | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type text/html | 87 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with content type text/plain | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with method GET | 98 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with method POST | 1 % |
| Info | Informational | http://localhost:3000 | Percentage of endpoints with method PUT | 1 % |
| Info | Informational | http://localhost:3000 | Count of total endpoints | 1,523    |
| Info | Informational | http://localhost:3000 | Percentage of slow responses | 4 % |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Off-site Redirect | High | 1 |
| SQL Injection | High | 1 |
| CSP: Failure to Define Directive with No Fallback | Medium | Systemic |
| Content Security Policy (CSP) Header Not Set | Medium | Systemic |
| Cross-Domain Misconfiguration | Medium | Systemic |
| Information Disclosure - JWT in Browser localStorage | Medium | 1 |
| Missing Anti-clickjacking Header | Medium | 1 |
| Session ID in URL Rewrite | Medium | Systemic |
| Application Error Disclosure | Low | 56 |
| Private IP Disclosure | Low | 2 |
| Timestamp Disclosure - Unix | Low | Systemic |
| X-Content-Type-Options Header Missing | Low | 3 |
| Authentication Request Identified | Informational | 2 |
| Information Disclosure - Information in Browser localStorage | Informational | 2 |
| Information Disclosure - Information in Browser sessionStorage | Informational | 5 |
| Modern Web Application | Informational | Systemic |
| Session Management Response Identified | Informational | 5 |
| User Agent Fuzzer | Informational | Systemic |




## Alert Detail



### [ Off-site Redirect ](https://www.zaproxy.org/docs/alerts/10028/)



##### High (Medium)

### Description

Open redirects are one of the OWASP 2010 Top Ten vulnerabilities. This check looks at user-supplied input in query string parameters and POST data to identify where open redirects might be possible. Open redirects occur when an application allows user-supplied input (e.g. https://nottrusted.com) to control an off-site destination. This is generally a pretty accurate way to find where 301 or 302 redirects could be exploited by spammers or phishing attacks.

For example an attacker could supply a user with the following link: https://example.com/example.php?url=https://malicious.example.com.

NOTE: For the purposes of the passive check the authority portion of the origin and destination were compared. Manual testing may be required to validate the impact of this finding.

* URL: http://localhost:3000/redirect%3Fto=https://github.com/juice-shop/juice-shop
  * Node Name: `http://localhost:3000/redirect (to)`
  * Method: `GET`
  * Parameter: `to`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The 301 or 302 response to a request for the following URL appeared to contain user input in the location header:

http://localhost:3000/redirect?to=https://github.com/juice-shop/juice-shop

The user input found was:

to=https://github.com/juice-shop/juice-shop

The context was:

https://github.com/juice-shop/juice-shop`


Instances: 1

### Solution

To avoid the open redirect vulnerability, parameters of the application script/program must be validated before sending 302 HTTP code (redirect) to the client browser. Implement safe redirect functionality that only redirects to relative URI's, or a list of trusted domains.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
* [ https://cwe.mitre.org/data/definitions/601.html ](https://cwe.mitre.org/data/definitions/601.html)


#### CWE Id: [ 601 ](https://cwe.mitre.org/data/definitions/601.html)


#### WASC Id: 38

#### Source ID: 3

### [ SQL Injection ](https://www.zaproxy.org/docs/alerts/40018/)



##### High (Low)

### Description

SQL injection may be possible.

* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `email`
  * Attack: `'`
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``


Instances: 1

### Solution

Do not trust client side input, even if there is client side validation in place.
In general, type check all data on the server side.
If the application uses JDBC, use PreparedStatement or CallableStatement, with parameters passed by '?'
If the application uses ASP, use ADO Command Objects with strong type checking and parameterized queries.
If database Stored Procedures can be used, use them.
Do *not* concatenate strings into queries in the stored procedure, or use 'exec', 'exec immediate', or equivalent functionality!
Do not create dynamic SQL queries using simple string concatenation.
Escape all data received from the client.
Apply an 'allow list' of allowed characters, or a 'deny list' of disallowed characters in user input.
Apply the principle of least privilege by using the least privileged database user possible.
In particular, avoid using the 'sa' or 'db-owner' database users. This does not eliminate SQL injection, but minimizes its impact.
Grant the minimum database access that is necessary for the application.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)


#### CWE Id: [ 89 ](https://cwe.mitre.org/data/definitions/89.html)


#### WASC Id: 19

#### Source ID: 1

### [ CSP: Failure to Define Directive with No Fallback ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

The Content Security Policy fails to define one of the directives that has no fallback. Missing/excluding them is the same as allowing anything.

* URL: http://localhost:3000/assets
  * Node Name: `http://localhost:3000/assets`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `default-src 'none'`
  * Other Info: `The directive(s): frame-ancestors, form-action, base-uri is/are among the directives that do not fallback to default-src.`
* URL: http://localhost:3000/assets/i18n
  * Node Name: `http://localhost:3000/assets/i18n`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `default-src 'none'`
  * Other Info: `The directive(s): frame-ancestors, form-action, base-uri is/are among the directives that do not fallback to default-src.`
* URL: http://localhost:3000/assets/public
  * Node Name: `http://localhost:3000/assets/public`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `default-src 'none'`
  * Other Info: `The directive(s): frame-ancestors, form-action, base-uri is/are among the directives that do not fallback to default-src.`
* URL: http://localhost:3000/assets/public/images
  * Node Name: `http://localhost:3000/assets/public/images`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `default-src 'none'`
  * Other Info: `The directive(s): frame-ancestors, form-action, base-uri is/are among the directives that do not fallback to default-src.`
* URL: http://localhost:3000/assets/public/images/carousel
  * Node Name: `http://localhost:3000/assets/public/images/carousel`
  * Method: `GET`
  * Parameter: `Content-Security-Policy`
  * Attack: ``
  * Evidence: `default-src 'none'`
  * Other Info: `The directive(s): frame-ancestors, form-action, base-uri is/are among the directives that do not fallback to default-src.`

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Content Security Policy (CSP) Header Not Set ](https://www.zaproxy.org/docs/alerts/10038/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: http://localhost:3000/
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://localhost:3000/api/BasketItems/
  * Node Name: `http://localhost:3000/api/BasketItems/ ()({ProductId,BasketId,quantity})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apejrvu&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,t,transport)(40)`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
* [ https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://w3c.github.io/webappsec-csp/ ](https://w3c.github.io/webappsec-csp/)
* [ https://web.dev/articles/csp ](https://web.dev/articles/csp)
* [ https://caniuse.com/#feat=contentsecuritypolicy ](https://caniuse.com/#feat=contentsecuritypolicy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Cross-Domain Misconfiguration ](https://www.zaproxy.org/docs/alerts/10098/)



##### Medium (Medium)

### Description

Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.

* URL: http://localhost:3000/
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://localhost:3000/polyfills.js
  * Node Name: `http://localhost:3000/polyfills.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://localhost:3000/rolldown-runtime-kqx1xuJ_.js
  * Node Name: `http://localhost:3000/rolldown-runtime-kqx1xuJ_.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://localhost:3000/scripts.js
  * Node Name: `http://localhost:3000/scripts.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://localhost:3000/styles.css
  * Node Name: `http://localhost:3000/styles.css`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`

Instances: Systemic


### Solution

Ensure that sensitive data is not available in an unauthenticated manner (using IP address white-listing, for instance).
Configure the "Access-Control-Allow-Origin" HTTP header to a more restrictive set of domains, or remove all CORS headers entirely, to allow the web browser to enforce the Same Origin Policy (SOP) in a more restrictive manner.

### Reference


* [ https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy ](https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy)


#### CWE Id: [ 264 ](https://cwe.mitre.org/data/definitions/264.html)


#### WASC Id: 14

#### Source ID: 3

### [ Information Disclosure - JWT in Browser localStorage ](https://www.zaproxy.org/docs/alerts/120002/)



##### Medium (High)

### Description

JWT was stored in browser localStorage.
This is dangerous because data stored in localStorage does not expire. .

* URL: http://localhost:3000/%23/search
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `token`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following JWT was set:
Key: token
Header: {"typ":"JWT","alg":"RS256"}
Payload: {"data":{"id":26,"username":"","email":"juice@test.com","password":"827ccb0eea8a706c4c34a16891f84e7b","role":"customer","deluxeToken":"","lastLoginIp":"0.0.0.0","profileImage":"/assets/public/images/uploads/default.svg","totpSecret":"","isActive":true,"createdAt":"2026-11-24 22:19:28.067 +00:00","updatedAt":"2026-11-24 22:19:28.067 +00:00","deletedAt":null},"bid":6,"iat":1795558777}
Signature: bd1c38cb3d3b8fbf48a90558ca9b43e133fbb6e5e9e0e767cdd3cb0c13b1bc3eab2ec771a971e579710c2544cbff3aaf85787fd1f1bfbb53911a84ba64e46f16435c29e53eafc45abaab3b6274b0dfabdaeb5e00a6b29094d13173febfff288d1b84c769f5ed1a65a2b43fca07c589f093ec3bdc4b5b622c9db73341dfaa15a6
Note that this alert will only be raised once for each URL + key.`


Instances: 1

### Solution

This is an informational alert and no action is necessary. 

### Reference


* [ https://www.zaproxy.org/blog/2020-09-03-zap-jwt-scanner/ ](https://www.zaproxy.org/blog/2020-09-03-zap-jwt-scanner/)


#### CWE Id: [ 922 ](https://cwe.mitre.org/data/definitions/922.html)


#### WASC Id: 13

#### Source ID: 3

### [ Missing Anti-clickjacking Header ](https://www.zaproxy.org/docs/alerts/10020/)



##### Medium (Medium)

### Description

The response does not protect against 'ClickJacking' attacks. It should include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options.

* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apejrvu&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,t,transport)(40)`
  * Method: `POST`
  * Parameter: `x-frame-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``


Instances: 1

### Solution

Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.
If you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's "frame-ancestors" directive.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options)


#### CWE Id: [ 1021 ](https://cwe.mitre.org/data/definitions/1021.html)


#### WASC Id: 15

#### Source ID: 3

### [ Session ID in URL Rewrite ](https://www.zaproxy.org/docs/alerts/3/)



##### Medium (High)

### Description

URL rewrite is used to track user session ID. The session ID may be disclosed via cross-site referer header. In addition, the session ID might be stored in browser history or server logs.

* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apekco1&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,t,transport)`
  * Method: `GET`
  * Parameter: `sid`
  * Attack: ``
  * Evidence: `9u2EuC1QzOQ-1zEwAAAB`
  * Other Info: ``
* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=websocket&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,transport)`
  * Method: `GET`
  * Parameter: `sid`
  * Attack: ``
  * Evidence: `9u2EuC1QzOQ-1zEwAAAB`
  * Other Info: ``
* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apejrvu&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,t,transport)(40)`
  * Method: `POST`
  * Parameter: `sid`
  * Attack: ``
  * Evidence: `9u2EuC1QzOQ-1zEwAAAB`
  * Other Info: ``

Instances: Systemic


### Solution

For secure content, put session ID in a cookie. To be even more secure consider using a combination of cookie and URL rewrite.

### Reference


* [ https://seclists.org/webappsec/2002/q4/111 ](https://seclists.org/webappsec/2002/q4/111)


#### CWE Id: [ 598 ](https://cwe.mitre.org/data/definitions/598.html)


#### WASC Id: 13

#### Source ID: 3

### [ Application Error Disclosure ](https://www.zaproxy.org/docs/alerts/90022/)



##### Low (Medium)

### Description

This page contains an error/warning message that may disclose sensitive information like the location of the file that produced the unhandled exception. This information can be used to launch further attacks against the web application. The alert could be a false positive if the error message is found inside a documentation page.

* URL: http://localhost:3000/api
  * Node Name: `http://localhost:3000/api`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/.DS_Store
  * Node Name: `http://localhost:3000/api/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/.git/index
  * Node Name: `http://localhost:3000/api/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/.svn/entries
  * Node Name: `http://localhost:3000/api/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/.svn/wc.db
  * Node Name: `http://localhost:3000/api/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Addresss/.git/index
  * Node Name: `http://localhost:3000/api/Addresss/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Addresss/.svn/entries
  * Node Name: `http://localhost:3000/api/Addresss/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Addresss/.svn/wc.db
  * Node Name: `http://localhost:3000/api/Addresss/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Cards/.git/index
  * Node Name: `http://localhost:3000/api/Cards/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Cards/.svn/entries
  * Node Name: `http://localhost:3000/api/Cards/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Cards/.svn/wc.db
  * Node Name: `http://localhost:3000/api/Cards/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Deliverys/.git/index
  * Node Name: `http://localhost:3000/api/Deliverys/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Deliverys/.svn/entries
  * Node Name: `http://localhost:3000/api/Deliverys/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Deliverys/.svn/wc.db
  * Node Name: `http://localhost:3000/api/Deliverys/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Products/.git/index
  * Node Name: `http://localhost:3000/api/Products/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Products/.svn/entries
  * Node Name: `http://localhost:3000/api/Products/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Products/.svn/wc.db
  * Node Name: `http://localhost:3000/api/Products/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Users/.git/index
  * Node Name: `http://localhost:3000/api/Users/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Users/.svn/entries
  * Node Name: `http://localhost:3000/api/Users/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/api/Users/.svn/wc.db
  * Node Name: `http://localhost:3000/api/Users/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest
  * Node Name: `http://localhost:3000/rest`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/.DS_Store
  * Node Name: `http://localhost:3000/rest/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/.git/index
  * Node Name: `http://localhost:3000/rest/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/.svn/entries
  * Node Name: `http://localhost:3000/rest/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/admin
  * Node Name: `http://localhost:3000/rest/admin`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/admin/.DS_Store
  * Node Name: `http://localhost:3000/rest/admin/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/admin/.git/index
  * Node Name: `http://localhost:3000/rest/admin/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/admin/.svn/entries
  * Node Name: `http://localhost:3000/rest/admin/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/admin/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/admin/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/captcha/.DS_Store
  * Node Name: `http://localhost:3000/rest/captcha/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/captcha/.git/index
  * Node Name: `http://localhost:3000/rest/captcha/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/captcha/.svn/entries
  * Node Name: `http://localhost:3000/rest/captcha/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/captcha/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/captcha/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/chat
  * Node Name: `http://localhost:3000/rest/chat`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/order-history
  * Node Name: `http://localhost:3000/rest/order-history`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/products
  * Node Name: `http://localhost:3000/rest/products`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/products/.DS_Store
  * Node Name: `http://localhost:3000/rest/products/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/products/.git/index
  * Node Name: `http://localhost:3000/rest/products/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/products/.svn/entries
  * Node Name: `http://localhost:3000/rest/products/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/products/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/products/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/track-order
  * Node Name: `http://localhost:3000/rest/track-order`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/track-order/.git/index
  * Node Name: `http://localhost:3000/rest/track-order/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/track-order/.svn/entries
  * Node Name: `http://localhost:3000/rest/track-order/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/track-order/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/track-order/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/user
  * Node Name: `http://localhost:3000/rest/user`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/user/.DS_Store
  * Node Name: `http://localhost:3000/rest/user/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/user/.git/index
  * Node Name: `http://localhost:3000/rest/user/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/user/.svn/entries
  * Node Name: `http://localhost:3000/rest/user/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/user/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/user/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/wallet
  * Node Name: `http://localhost:3000/rest/wallet`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/wallet/.DS_Store
  * Node Name: `http://localhost:3000/rest/wallet/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/wallet/.git/index
  * Node Name: `http://localhost:3000/rest/wallet/.git/index`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/wallet/.svn/entries
  * Node Name: `http://localhost:3000/rest/wallet/.svn/entries`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``
* URL: http://localhost:3000/rest/wallet/.svn/wc.db
  * Node Name: `http://localhost:3000/rest/wallet/.svn/wc.db`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `HTTP/1.1 500 Internal Server Error`
  * Other Info: ``


Instances: 56

### Solution

Review the source code of this page. Implement custom error pages. Consider implementing a mechanism to provide a unique error reference/identifier to the client (browser) while logging the details on the server side and not exposing them to the user.

### Reference



#### CWE Id: [ 550 ](https://cwe.mitre.org/data/definitions/550.html)


#### WASC Id: 13

#### Source ID: 3

### [ Private IP Disclosure ](https://www.zaproxy.org/docs/alerts/2/)



##### Low (Medium)

### Description

A private IP (such as 10.x.x.x, 172.x.x.x, 192.168.x.x) or an Amazon EC2 private hostname (for example, ip-10-0-56-78) has been found in the HTTP response body. This information might be helpful for further attacks targeting internal systems.

* URL: http://localhost:3000/rest/admin/application-configuration
  * Node Name: `http://localhost:3000/rest/admin/application-configuration`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `192.168.99.100:3000`
  * Other Info: `192.168.99.100:3000
192.168.99.100:4200
`
* URL: http://localhost:3000/rest/order-history
  * Node Name: `http://localhost:3000/rest/order-history`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `172.17.0.1`
  * Other Info: `172.17.0.1
172.17.0.1
`


Instances: 2

### Solution

Remove the private IP address from the HTTP response body. For comments, use JSP/ASP/PHP comment instead of HTML/JavaScript comment which can be seen by client browsers.

### Reference


* [ https://datatracker.ietf.org/doc/html/rfc1918 ](https://datatracker.ietf.org/doc/html/rfc1918)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ Timestamp Disclosure - Unix ](https://www.zaproxy.org/docs/alerts/10096/)



##### Low (Low)

### Description

A timestamp was disclosed by the application/web server. - Unix

* URL: http://localhost:3000/rest/admin/application-configuration
  * Node Name: `http://localhost:3000/rest/admin/application-configuration`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1969196030`
  * Other Info: `1969196030, which evaluates to: 2032-05-26 08:53:50.`
* URL: http://localhost:3000/rest/admin/application-configuration
  * Node Name: `http://localhost:3000/rest/admin/application-configuration`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1970691216`
  * Other Info: `1970691216, which evaluates to: 2032-06-12 16:13:36.`
* URL: http://localhost:3000/rest/products/search%3Fq=
  * Node Name: `http://localhost:3000/rest/products/search (q)`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1969196030`
  * Other Info: `1969196030, which evaluates to: 2032-05-26 08:53:50.`
* URL: http://localhost:3000/rest/products/search%3Fq=
  * Node Name: `http://localhost:3000/rest/products/search (q)`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1970691216`
  * Other Info: `1970691216, which evaluates to: 2032-06-12 16:13:36.`

Instances: Systemic


### Solution

Manually confirm that the timestamp data is not sensitive, and that the data cannot be aggregated to disclose exploitable patterns.

### Reference


* [ https://cwe.mitre.org/data/definitions/200.html ](https://cwe.mitre.org/data/definitions/200.html)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ X-Content-Type-Options Header Missing ](https://www.zaproxy.org/docs/alerts/10021/)



##### Low (Medium)

### Description

The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.

* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apekco1&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,t,transport)`
  * Method: `GET`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`
* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apa7j6s
  * Node Name: `http://localhost:3000/socket.io/ (EIO,t,transport)`
  * Method: `GET`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`
* URL: http://localhost:3000/socket.io/%3FEIO=4&transport=polling&t=9apejrvu&sid=9u2EuC1QzOQ-1zEwAAAB
  * Node Name: `http://localhost:3000/socket.io/ (EIO,sid,t,transport)(40)`
  * Method: `POST`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`


Instances: 3

### Solution

Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.
If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.

### Reference


* [ https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/compatibility/gg622941(v=vs.85) ](https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/compatibility/gg622941(v=vs.85))
* [ https://owasp.org/www-community/Security_Headers ](https://owasp.org/www-community/Security_Headers)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Authentication Request Identified ](https://www.zaproxy.org/docs/alerts/10111/)



##### Informational (Low)

### Description

The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.

* URL: http://localhost:3000/api/Users/
  * Node Name: `http://localhost:3000/api/Users/ ()({email,password,passwordRepeat,securityQuestion:{id,question,createdAt,updatedAt},securityAnswer})`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=email
userValue=juice@test.com
passwordParam=password
referer=http://localhost:3000/`
* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=email
userValue=juice@test.com
passwordParam=password
referer=http://localhost:3000/`


Instances: 2

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/)



#### Source ID: 3

### [ Information Disclosure - Information in Browser localStorage ](https://www.zaproxy.org/docs/alerts/120000/)



##### Informational (High)

### Description

Information was stored in browser localStorage.
This is not unusual or necessarily unsafe - this informational alert has been raised to help you get a better understanding of what this app is doing. For more details see the Client tabs - this information was set directly in the browser and will therefore not necessarily appear in this form in any HTTP(S) messages.

* URL: http://localhost:3000/%23/chatbot/conversation/1795558896837_9tav6kw0
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `juiceshop_chat_conversations`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: juiceshop_chat_conversations=[{"id":"1795558896837_9tav6kw0","title":"ji","messages":[{"role":"user","content":"ji"},{"role":"assistant","content":""}],"createdAt":1795558896902,"updatedAt":1795558896902}]
Note that this alert will only be raised once for each URL + key.`
* URL: http://localhost:3000/%23/search
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `token`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: token=eyJ.<JWT-SCRUBBED>
Note that this alert will only be raised once for each URL + key.`


Instances: 2

### Solution

This is an informational alert and no action is necessary. 

### Reference



#### CWE Id: [ 359 ](https://cwe.mitre.org/data/definitions/359.html)


#### WASC Id: 13

#### Source ID: 3

### [ Information Disclosure - Information in Browser sessionStorage ](https://www.zaproxy.org/docs/alerts/120000/)



##### Informational (High)

### Description

Information was stored in browser sessionStorage.
This is not unusual or necessarily unsafe - this informational alert has been raised to help you get a better understanding of what this app is doing. For more details see the Client tabs - this information was set directly in the browser and will therefore not necessarily appear in this form in any HTTP(S) messages.

* URL: http://localhost:3000/%23/delivery-method
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `addressId`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: addressId=7
Note that this alert will only be raised once for each URL + key.`
* URL: http://localhost:3000/%23/search
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `bid`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: bid=6
Note that this alert will only be raised once for each URL + key.`
* URL: http://localhost:3000/%23/payment/shop
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `deliveryMethodId`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: deliveryMethodId=1
Note that this alert will only be raised once for each URL + key.`
* URL: http://localhost:3000/%23/basket
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `itemTotal`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: itemTotal=9.96
Note that this alert will only be raised once for each URL + key.`
* URL: http://localhost:3000/%23/order-summary
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: `paymentId`
  * Attack: ``
  * Evidence: ``
  * Other Info: `The following data (key=value) was set: paymentId=7
Note that this alert will only be raised once for each URL + key.`


Instances: 5

### Solution

This is an informational alert and no action is necessary. 

### Reference



#### CWE Id: [ 359 ](https://cwe.mitre.org/data/definitions/359.html)


#### WASC Id: 13

#### Source ID: 3

### [ Modern Web Application ](https://www.zaproxy.org/docs/alerts/10109/)



##### Informational (Medium)

### Description

The application appears to be a modern web application. If you need to explore it automatically then the Client Spider may well be more effective than the standard one.

* URL: http://localhost:3000
  * Node Name: `http://localhost:3000`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
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
  </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: http://localhost:3000/
  * Node Name: `http://localhost:3000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
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
  </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: http://localhost:3000/.DS_Store
  * Node Name: `http://localhost:3000/.DS_Store`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
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
  </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`
* URL: http://localhost:3000/sitemap.xml
  * Node Name: `http://localhost:3000/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script>
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
  </script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`

Instances: Systemic


### Solution

This is an informational alert and so no changes are required.

### Reference




#### Source ID: 3

### [ Session Management Response Identified ](https://www.zaproxy.org/docs/alerts/10112/)



##### Informational (Medium)

### Description

The given response has been identified as containing a session management token. The 'Other Info' field contains a set of header tokens that can be used in the Header Based Session Management Method. If the request is in a context which has a Session Management Method set to "Auto-Detect" then this rule will change the session management to use the tokens identified.

* URL: http://localhost:3000/rest/deluxe-membership
  * Node Name: `http://localhost:3000/rest/deluxe-membership ()({paymentMode,paymentId})`
  * Method: `POST`
  * Parameter: `data.token`
  * Attack: ``
  * Evidence: `data.token`
  * Other Info: `json:data.token`
* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `authentication.token`
  * Attack: ``
  * Evidence: `authentication.token`
  * Other Info: `json:authentication.token`
* URL: http://localhost:3000/rest/continue-code
  * Node Name: `http://localhost:3000/rest/continue-code`
  * Method: `GET`
  * Parameter: `continueCode`
  * Attack: ``
  * Evidence: `continueCode`
  * Other Info: `json:continueCode`
* URL: http://localhost:3000/rest/deluxe-membership
  * Node Name: `http://localhost:3000/rest/deluxe-membership ()({paymentMode,paymentId})`
  * Method: `POST`
  * Parameter: `data.token`
  * Attack: ``
  * Evidence: `data.token`
  * Other Info: `json:data.token`
* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `authentication.token`
  * Attack: ``
  * Evidence: `authentication.token`
  * Other Info: `json:authentication.token`


Instances: 5

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/)



#### Source ID: 3

### [ User Agent Fuzzer ](https://www.zaproxy.org/docs/alerts/10104/)



##### Informational (Medium)

### Description

Check for differences in response based on fuzzed User Agent (eg. mobile sites, access as a Search Engine Crawler). Compares the response statuscode and the hashcode of the response body with the original response.

* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)`
  * Evidence: ``
  * Other Info: ``
* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)`
  * Evidence: ``
  * Other Info: ``
* URL: http://localhost:3000/rest/user/login
  * Node Name: `http://localhost:3000/rest/user/login ()({email,password})`
  * Method: `POST`
  * Parameter: `Header User-Agent`
  * Attack: `Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)`
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution



### Reference


* [ https://owasp.org/www-project-web-security-testing-guide/ ](https://owasp.org/www-project-web-security-testing-guide/)



#### Source ID: 1


