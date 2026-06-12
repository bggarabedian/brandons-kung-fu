<#
=============================================================================
brandons-kung-fu - dry-run skill fetcher (PowerShell 5.1)

Mirror of skill-fetch.sh. Reads skills/skills-manifest.yaml and reports what it
WOULD fetch/install.

Safety guarantees:
  - DRY-RUN BY DEFAULT. With no -Apply it makes zero network calls and zero
    writes; it only prints a plan and a summary.
  - -Apply enables network + install, but STILL prompts per skill. No bypass.
  - Copies files only. Never executes fetched content.
  - Never installs into this repo. Never reads or copies the gstack store.
  - Fails closed: un-cleared license, empty/private source, non-installable
    state, AUTH-P provenance, name collision, or unsafe target is REFUSED.

Usage:
  skill-fetch.ps1 [-Name a,b] [-Apply] [-Target DIR] [-Manifest PATH] [-Force]
=============================================================================
#>

param(
  [string[]]$Name = @(),
  [switch]$Apply,
  [switch]$Force,
  [string]$Target = "",
  [string]$Manifest = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$PFX = "[bkf]"

# --- locate repo root via marker files (never a hardcoded path)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
foreach ($marker in @("git-hooks\pre-push.sh","README.md","skills\skills-manifest.yaml")) {
  if (-not (Test-Path (Join-Path $Root $marker))) { Write-Error "$PFX not the kit root (missing $marker)."; exit 1 }
}

if ([string]::IsNullOrEmpty($Manifest)) { $Manifest = Join-Path $Root "skills\skills-manifest.yaml" }
if (-not (Test-Path $Manifest)) { Write-Error "$PFX manifest not found: $Manifest"; exit 1 }

# --- resolve gstack home and default target (runtime-resolved, never literal)
$GstackDir = $env:GSTACK_HOME; if ([string]::IsNullOrEmpty($GstackDir)) { $GstackDir = Join-Path $HOME ".gstack" }
if ([string]::IsNullOrEmpty($Target)) {
  $Target = $env:SKILL_TARGET; if ([string]::IsNullOrEmpty($Target)) { $Target = Join-Path $HOME ".claude\skills" }
}

# --- target safety: never inside the repo, never inside the gstack store
function Resolve-Abs([string]$p) {
  try { return (Resolve-Path $p -ErrorAction Stop).Path } catch { return [System.IO.Path]::GetFullPath($p) }
}
$Tabs = Resolve-Abs $Target
$Rabs = Resolve-Abs $Root
$Gabs = Resolve-Abs $GstackDir
if ($Tabs.TrimEnd('\','/') -like ($Rabs.TrimEnd('\','/') + '*')) { Write-Error "$PFX target is inside the repo - refused."; exit 1 }
if ($Tabs.TrimEnd('\','/') -like ($Gabs.TrimEnd('\','/') + '*')) { Write-Error "$PFX target is inside the gstack store - refused."; exit 1 }

# --- public host allowlist for source_url; returns $true when private (refuse)
$Allow = @("github.com","gitlab.com","codeberg.org","bitbucket.org","raw.githubusercontent.com")
function Test-PrivateUrl([string]$url) {
  # Scheme and host are lowercased before comparison so behavior matches the
  # bash mirror exactly (PowerShell operators are case-insensitive by default;
  # normalizing makes the rule explicit and consistent across both shells).
  # drive-letter / UNC shapes
  if ($url -match '^[A-Za-z]:[\\/]' -or $url -match '^(\\\\|//)') { return $true }
  # require a scheme://; anything without one (incl. scp-style git@host:path) is private
  if ($url -notmatch '://') { return $true }
  $scheme = (($url -split '://',2)[0]).ToLower()
  if ($scheme -ne 'https') { return $true }                    # only https (after lowercasing)
  $rest = ($url -split '://',2)[1]
  $host2 = ($rest -split '/')[0]
  $host2 = ($host2 -split ':')[0]
  if ($host2 -match '@') { $host2 = ($host2 -split '@')[-1] }   # drop userinfo (user@host)
  $host2 = $host2.ToLower()
  switch -regex ($host2) {
    '^(localhost|127\.0\.0\.1)$' { return $true }
    '^10\.' { return $true }
    '^192\.168\.' { return $true }
    '^172\.(1[6-9]|2[0-9]|3[01])\.' { return $true }
    '\.(local|internal|lan|corp)$' { return $true }
  }
  if ($Allow -notcontains $host2) { return $true }             # exact lowercase allowlist match; fail closed
  $dl = Join-Path $Root "git-hooks\denylist.local.txt"
  if (Test-Path $dl) {
    $lcurl = $url.ToLower()
    foreach ($term in (Get-Content $dl)) {
      $t = $term.Trim()
      if ($t -eq "" -or $t.StartsWith("#")) { continue }
      if ($lcurl -like "*$($t.ToLower())*") { return $true }    # case-insensitive: both sides lowercased
    }
  }
  return $false
}

# --- skill name validation: only [A-Za-z0-9_-], non-empty. Blocks path
#     traversal (slash, backslash, dot-dot, drive-letter, whitespace) through
#     the target/name join before any shadow check or filesystem use.
function Test-ValidName([string]$n) {
  if ([string]::IsNullOrEmpty($n)) { return $false }
  return ($n -match '^[A-Za-z0-9_-]+$')
}

# --- minimal schema-pinned YAML reader (no external dependency)
$Required = @("name","category","provenance","source_url","license","license_status","bundle_status","install_status","notes")
function Read-Manifest {
  $records = New-Object System.Collections.ArrayList
  $cur = $null
  foreach ($line in (Get-Content $Manifest)) {
    if ($line -match '^\s*#') { continue }
    if ($line -match '^\s*-\s*name:\s*(.*)$') {
      if ($cur -ne $null) { [void]$records.Add($cur) }
      $cur = @{}
      $cur["name"] = ($matches[1].Trim() -replace '^"|"$','')
      continue
    }
    if ($line -match '^\s+([a-z_]+):\s*(.*)$') {
      if ($cur -eq $null) { continue }
      $cur[$matches[1]] = ($matches[2].Trim() -replace '^"|"$','')
    }
  }
  if ($cur -ne $null) { [void]$records.Add($cur) }
  foreach ($r in $records) {
    foreach ($k in $Required) {
      if (-not $r.ContainsKey($k)) { Write-Error "$PFX manifest record '$($r['name'])' missing field: $k"; exit 3 }
    }
  }
  return $records
}

function Test-Shadow([string]$n) {
  if (Test-Path (Join-Path $Target $n)) { return "user-global" }
  if (Test-Path (Join-Path $Root ".claude\skills\$n")) { return "project-local" }
  return ""
}

$mode = if ($Apply) { "APPLY" } else { "DRY-RUN" }
Write-Output "$PFX skill-fetch - mode: $mode"
Write-Output "$PFX manifest: $Manifest"
Write-Output "$PFX target:   $Target"
if (-not $Apply) { Write-Output "$PFX dry-run: no network, no writes. Re-run with -Apply to install (still prompts)." }
Write-Output ""

$eligible = 0; $refused = 0; $installed = 0
$records = Read-Manifest

foreach ($r in $records) {
  $n = $r["name"]
  if ($Name.Count -gt 0 -and ($Name -notcontains $n)) { continue }

  # name validation FIRST — before Test-Shadow or any path use (anti-traversal)
  if (-not (Test-ValidName $n)) {
    Write-Output ("{0} REFUSE  {1,-26} - {2}" -f $PFX, $n, "invalid name (only A-Za-z0-9_- allowed)")
    $refused++
    continue
  }

  $reason = ""
  if ($r["provenance"] -eq "AUTH-P") { $reason = "AUTH-P project-coupled (never fetched)" }
  elseif ($r["install_status"] -ne "installable") { $reason = "install_status=$($r['install_status']) (catalog-only, not installable)" }
  elseif ($r["license_status"] -ne "cleared") { $reason = "license_status=$($r['license_status']) (must be cleared)" }
  elseif ([string]::IsNullOrEmpty($r["source_url"])) { $reason = "empty source_url" }
  elseif (Test-PrivateUrl $r["source_url"]) { $reason = "private/non-public source_url" }
  else {
    $sh = Test-Shadow $n
    if ($sh -ne "" -and -not $Force) { $reason = "name collision in $sh scope (use -Force + confirm)" }
  }

  if ($reason -ne "") {
    Write-Output ("{0} REFUSE  {1,-26} - {2}" -f $PFX, $n, $reason)
    $refused++
    continue
  }

  $eligible++
  Write-Output ("{0} WOULD-FETCH {1,-22} FROM {2}  INTO {3}\{4}" -f $PFX, $n, $r["source_url"], $Target, $n)

  if (-not $Apply) { continue }

  if ((Test-Shadow $n) -ne "") {
    $ans2 = Read-Host "$PFX collision for $n - overwrite existing skill? [y/N]"
    if ($ans2 -notmatch '^[yY]$') { Write-Output "$PFX skipped $n (collision not confirmed)"; continue }
  }
  $ans = Read-Host "$PFX fetch $n from $($r['source_url'])? [y/N]"
  if ($ans -match '^[yY]$') {
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ([System.IO.Path]::GetRandomFileName())
    New-Item -ItemType Directory -Path $tmp -Force | Out-Null
    Write-Output "$PFX cloning (shallow, files only - never executed)..."
    & git clone --depth 1 $r["source_url"] (Join-Path $tmp "src") | Out-Null
    if ($LASTEXITCODE -eq 0) {
      # symlink preflight: refuse if the fetched tree contains ANY symlink/reparse point
      # (a symlink could materialize arbitrary file content into the target).
      $links = Get-ChildItem -Path (Join-Path $tmp "src") -Recurse -Force -ErrorAction SilentlyContinue |
               Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }
      if ($links) {
        Remove-Item $tmp -Recurse -Force
        Write-Error "$PFX symlink found in fetched tree for $n - refused, nothing copied."
        continue
      }
      if (-not (Test-Path $Target)) { New-Item -ItemType Directory -Path $Target -Force | Out-Null }
      $srcSkill = Join-Path $tmp "src\$n"
      if (Test-Path $srcSkill) { Copy-Item $srcSkill (Join-Path $Target $n) -Recurse -Force }
      else { Copy-Item (Join-Path $tmp "src") (Join-Path $Target $n) -Recurse -Force }
      Remove-Item $tmp -Recurse -Force
      $installed++
      Write-Output "$PFX installed $n -> $Target\$n (files copied, not run)"
      Write-Output "$PFX smoke-test: runtime lists it; /$n resolves in ONE scope; run once on a safe target; status shows no unexpected tracked changes; output has no private paths."
    } else {
      Remove-Item $tmp -Recurse -Force
      Write-Error "$PFX fetch failed for $n - nothing installed."
    }
  } else {
    Write-Output "$PFX skipped $n (not confirmed)"
  }
}

Write-Output ""
Write-Output "$PFX summary: eligible=$eligible refused=$refused installed=$installed  (mode=$mode)"
if (-not $Apply) { Write-Output "$PFX no network and no writes were performed." }
exit 0
