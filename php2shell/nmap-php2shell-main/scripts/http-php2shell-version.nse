local http = require "http"
local shortport = require "shortport"
local stdnse = require "stdnse"
local vulns = require "vulns"

description = [[
Performs a safe, version-based check for PHP releases that may be affected by
CVE-2026-109618 and CVE-2026-109619 (commonly referred to as PHP2Shell).

The script does not attempt exploitation and does not send the large multipart
requests used by exploit-style validators. It fingerprints a remotely reported
PHP version and compares it with the upstream PHP security releases that contain
the fixes.

Upstream fixed versions:
  PHP 8.2 -> 8.2.35
  PHP 8.3 -> 8.3.36
  PHP 8.4 -> 8.4.27
  PHP 8.5 -> 8.5.12

Both vulnerabilities are rated Critical, CVSS v4.0 9.2 by the PHP project.

A LIKELY_VULN result is based only on remote version comparison. Distribution
or LTS vendors may backport fixes without changing the apparent upstream version,
and HTTP headers can be hidden, stale, or spoofed. Verify findings against the
installed package and vendor security advisory before treating them as confirmed.
]]

---
-- @usage
-- nmap -sV -p 80,443,8080 --script http-php2shell-version <target>
--
-- Show patched controls as well as likely-vulnerable results:
-- nmap -sV -p 8080,8081 --script http-php2shell-version \
--   --script-args vulns.showall <target>
--
-- Check additional application paths:
-- nmap -sV -p 80,443 --script http-php2shell-version \
--   --script-args 'http-php2shell-version.paths=/,/index.php,/phpinfo.php' <target>
--
-- @args http-php2shell-version.paths Comma-separated HTTP paths to inspect.
--       The default is only <code>/</code>. A HEAD request is attempted first;
--       a GET request is used only when additional version evidence is needed.
-- @args vulns.showall Show NOT_VULN results, including versions at or above the
--       upstream fixed release. This is provided by Nmap's vulns library.
-- @args vulns.short Use Nmap's one-line vulnerability output format.
--
-- @output
-- PORT     STATE SERVICE
-- 8080/tcp open  http
-- | http-php2shell-version:
-- |   VULNERABLE:
-- |   PHP CVE-2026-109618 - RCE via OOM corruption
-- |     State: LIKELY VULNERABLE
-- |     IDs:  CVE:CVE-2026-109618
-- |     Risk factor: High
-- |     Scores:
-- |       CVSS: 9.2
-- |     Check results:
-- |       Observed PHP version: 8.3.35
-- |       Upstream fixed version: 8.3.36
-- |       Evidence source: X-Powered-By
-- |       Confidence: MEDIUM
-- |       Detected path: /
-- |_      Assessment method: remote version comparison only
--
-- @xmloutput
-- <table key="CVE-2026-109618">...</table>

author = "dinvisible1"
license = "Simplified (2-clause) BSD license--See https://nmap.org/svn/docs/licenses/BSD-simplified"
categories = {"safe", "discovery", "vuln"}

portrule = shortport.http

local PHP_ADVISORY = "https://www.php.net/archive/2026.php#2026-10-21-5"

local FIXED = {
  [2] = 35,
  [3] = 36,
  [4] = 27,
  [5] = 12,
}

local CVES = {
  {
    id = "CVE-2026-109618",
    title = "PHP CVE-2026-109618 - RCE via OOM corruption",
    description = [[
PHP out-of-memory handling can interrupt request processing while internal
request data is only partially initialized. Cleanup may then treat invalid data
as valid, potentially resulting in unauthenticated remote code execution.]],
  },
  {
    id = "CVE-2026-109619",
    title = "PHP CVE-2026-109619 - RCE via stale global state",
    description = [[
Request-owned internal state can survive after its backing memory has been
freed. A later request handled by the same worker may use stale state before
normal initialization resets it, potentially resulting in unauthenticated
remote code execution.]],
  },
}

local function split_paths(value)
  local paths = {}
  value = value or "/"

  for path in value:gmatch("([^,]+)") do
    path = path:gsub("^%s+", ""):gsub("%s+$", "")

    if path ~= "" then
      if path:sub(1, 1) ~= "/" then
        path = "/" .. path
      end

      paths[#paths + 1] = path
    end
  end

  if #paths == 0 then
    paths[1] = "/"
  end

  return paths
end

local function extract_php_version(value)
  if not value then
    return nil
  end

  -- Header-style disclosure: PHP/8.3.35
  local major, minor, patch =
    value:match("[Pp][Hh][Pp][/%s%-]*([0-9]+)%.([0-9]+)%.([0-9]+)")

  if major then
    return tonumber(major), tonumber(minor), tonumber(patch)
  end

  -- phpinfo()-style disclosure: PHP Version 8.3.35
  major, minor, patch =
    value:match(
      "[Pp][Hh][Pp].-[Vv]ersion[^0-9]*([0-9]+)%.([0-9]+)%.([0-9]+)"
    )

  if major then
    return tonumber(major), tonumber(minor), tonumber(patch)
  end

  return nil
end

local function inspect_headers(response)
  if not response or not response.header then
    return nil
  end

  local candidates = {
    {
      name = "X-Powered-By",
      value = response.header["x-powered-by"],
      confidence = "MEDIUM"
    },
    {
      name = "Server",
      value = response.header["server"],
      confidence = "MEDIUM"
    },
  }

  local php_seen = false

  for _, candidate in ipairs(candidates) do
    if candidate.value then

      if candidate.value:lower():find("php", 1, true) then
        php_seen = true
      end

      local major, minor, patch =
        extract_php_version(candidate.value)

      if major then
        return {
          major = major,
          minor = minor,
          patch = patch,
          source = candidate.name,
          confidence = candidate.confidence,
          php_seen = true,
        }
      end
    end
  end

  if php_seen then
    return {
      php_seen = true
    }
  end

  return nil
end

local function inspect_body(response)
  if not response or
     not response.body or
     response.body == "" then
    return nil
  end

  local major, minor, patch =
    extract_php_version(response.body)

  if major then
    return {
      major = major,
      minor = minor,
      patch = patch,
      source = "HTTP response body",
      confidence = "HIGH",
      php_seen = true,
    }
  end

  -- Only claim generic PHP detection for body patterns that resemble
  -- phpinfo() or an explicit PHP version marker.
  local lower = response.body:lower()

  if lower:find("phpinfo()", 1, true) or
     lower:find("php version", 1, true) then
    return {
      php_seen = true
    }
  end

  return nil
end

local function merge_detection(current, candidate, path)
  if not candidate then
    return current
  end

  current = current or {
    php_seen = false
  }

  current.php_seen =
    current.php_seen or candidate.php_seen

  if candidate.major and not current.major then
    current.major = candidate.major
    current.minor = candidate.minor
    current.patch = candidate.patch
    current.source = candidate.source
    current.confidence = candidate.confidence
    current.path = path
  end

  return current
end

local function detect_php(host, port, paths)
  local detection = {
    php_seen = false
  }

  local opts = {
    redirect_ok = false
  }

  for _, path in ipairs(paths) do

    -- Prefer HEAD to minimize network traffic.
    local head =
      http.head(host, port, path, opts)

    detection =
      merge_detection(
        detection,
        inspect_headers(head),
        path
      )

    if detection.major then
      return detection
    end

    -- Fall back to GET only when HEAD did not disclose a version.
    local response =
      http.get(host, port, path, opts)

    detection =
      merge_detection(
        detection,
        inspect_headers(response),
        path
      )

    detection =
      merge_detection(
        detection,
        inspect_body(response),
        path
      )

    if detection.major then
      return detection
    end
  end

  return detection
end

local function classify_version(major, minor, patch)

  if major < 8 or
     (major == 8 and minor < 2) then

    return {
      kind = "likely",
      fixed = "No upstream fixed release for this EOL branch",
      note =
        "Verify distribution/LTS vendor backports or upgrade to a supported PHP branch.",
    }
  end

  if major ~= 8 or
     not FIXED[minor] then

    return {
      kind = "unknown",
      fixed = "Unknown for this PHP branch",
      note =
        "The detected PHP branch is outside this script's fixed-version table.",
    }
  end

  local fixed_patch =
    FIXED[minor]

  local fixed_version =
    string.format(
      "8.%d.%d",
      minor,
      fixed_patch
    )

  if patch < fixed_patch then

    return {
      kind = "likely",
      fixed = fixed_version,
      note =
        "A vendor-backported fix may change the actual exposure; verify the installed package.",
    }
  end

  return {
    kind = "patched",
    fixed = fixed_version,
    note =
      "The reported upstream version is at or above the fixed release; package provenance was not independently verified.",
  }
end

local function make_vuln(
  cve,
  state,
  detection,
  classification
)

  local observed =
    string.format(
      "%d.%d.%d",
      detection.major,
      detection.minor,
      detection.patch
    )

  return {
    title = cve.title,

    state = state,

    IDS = {
      CVE = cve.id
    },

    -- Nmap's vulns library supports High, Medium and Low.
    -- PHP upstream rates both vulnerabilities Critical,
    -- CVSS v4.0 9.2.
    risk_factor = "High",

    scores = {
      CVSS = "9.2",
    },

    description = cve.description,

    dates = {
      disclosure = {
        year = 2026,
        month = 10,
        day = 21
      },
    },

    references = {
      PHP_ADVISORY,
    },

    check_results = {
      "Observed PHP version: " .. observed,
      "Upstream fixed version: " .. classification.fixed,
      "Evidence source: " .. (detection.source or "unknown"),
      "Confidence: " .. (detection.confidence or "LOW"),
      "Detected path: " .. (detection.path or "/"),
      "Assessment method: remote version comparison only",
    },

    extra_info = {
      "Upstream severity: CRITICAL - CVSS v4.0 9.2",
      classification.note,
      "This script does not attempt exploitation or intrusive multipart probing.",
    },
  }
end

local function make_unknown_output(detection)

  local output =
    stdnse.output_table()

  output["Assessment"] =
    "UNKNOWN / VERIFICATION REQUIRED"

  output["PHP detected"] =
    detection.php_seen and "yes" or "no"

  if detection.major then

    output["Observed PHP version"] =
      string.format(
        "%d.%d.%d",
        detection.major,
        detection.minor,
        detection.patch
      )

  else

    output["Observed PHP version"] =
      "not disclosed"

  end

  if detection.source then
    output["Evidence source"] =
      detection.source
  end

  if detection.path then
    output["Detected path"] =
      detection.path
  end

  output["CVE-2026-109618"] =
    "verification required"

  output["CVE-2026-109619"] =
    "verification required"

  output["Upstream severity"] =
    "CRITICAL - CVSS v4.0 9.2"

  output["Note"] =
    "Verify the installed PHP package and vendor security advisory. No exploit attempt was made."

  return output
end

action = function(host, port)

  local paths_arg =
    stdnse.get_script_args(
      SCRIPT_NAME .. ".paths"
    )

  local paths =
    split_paths(paths_arg)

  local detection =
    detect_php(
      host,
      port,
      paths
    )

  if not detection.php_seen and
     not detection.major then
    return nil
  end

  if not detection.major then
    return make_unknown_output(detection)
  end

  local classification =
    classify_version(
      detection.major,
      detection.minor,
      detection.patch
    )

  if classification.kind == "unknown" then
    return make_unknown_output(detection)
  end

  local state =
    vulns.STATE.LIKELY_VULN

  if classification.kind == "patched" then
    state =
      vulns.STATE.NOT_VULN
  end

  local vuln1 =
    make_vuln(
      CVES[1],
      state,
      detection,
      classification
    )

  local vuln2 =
    make_vuln(
      CVES[2],
      state,
      detection,
      classification
    )

  local report =
    vulns.Report:new(
      SCRIPT_NAME,
      host,
      port
    )

  return report:make_output(
    vuln1,
    vuln2
  )
end