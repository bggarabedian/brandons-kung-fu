#Requires -Version 5
# =============================================================================
# brandons-kung-fu - offline installer (PowerShell)
#
# Local only. Does NOT: run git init, stage, commit, push, create remotes,
# install packages, or make any network call.
#
# Steps:
#   1. Verify we are at the brandons-kung-fu root.
#   2. If a git repo already exists here, wire the hook via
#      'git config core.hooksPath git-hooks' (never runs 'git init').
#   3. Seed git-hooks/denylist.local.txt from the example (never overwrites).
# =============================================================================

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ScriptDir

# --- root detection via required marker files
$markers = @('git-hooks\pre-push.sh', 'git-hooks\denylist.example.txt', 'README.md')
$missing = @()
foreach ($m in $markers) {
  if (-not (Test-Path -LiteralPath $m)) { $missing += $m }
}
if ($missing.Count -gt 0) {
  Write-Host "ERROR: this is not the brandons-kung-fu root. Run install.ps1 from there."
  $missing | ForEach-Object { Write-Host "  missing: $_" }
  exit 1
}
Write-Host "[bkf] root detected: $ScriptDir"

# --- hook wiring (local config only; never runs 'git init')
#     Wire ONLY when this kit root is itself the git top-level, so a parent repo
#     is never reconfigured.
$topLevel = $null
try {
  $topLevel = (& git rev-parse --show-toplevel 2>$null)
  if ($LASTEXITCODE -ne 0) { $topLevel = $null }
} catch {
  $topLevel = $null
}

if ([string]::IsNullOrWhiteSpace($topLevel)) {
  Write-Host "[bkf] NOTE: no git repo here yet - hook wiring skipped (installer never runs 'git init')."
  Write-Host "[bkf]   create a repo here, then run:  git config core.hooksPath git-hooks"
} else {
  # normalize both paths (resolve, trim trailing slashes) for a reliable compare
  $topNorm = $null
  $rootNorm = $null
  try { $topNorm = (Resolve-Path -LiteralPath $topLevel).Path } catch { $topNorm = $null }
  try { $rootNorm = (Resolve-Path -LiteralPath $ScriptDir).Path } catch { $rootNorm = $null }
  if ($topNorm) { $topNorm = $topNorm.TrimEnd('\', '/') }
  if ($rootNorm) { $rootNorm = $rootNorm.TrimEnd('\', '/') }

  if ($topNorm -and $rootNorm -and ($topNorm -ieq $rootNorm)) {
    & git config core.hooksPath git-hooks
    Write-Host "[bkf] hooks wired: core.hooksPath = git-hooks"
  } else {
    Write-Host "[bkf] WARNING: Detected parent git repo; hook wiring skipped to avoid modifying the parent repo."
    Write-Host "[bkf]   Make the kit its own repo, then run:  git config core.hooksPath git-hooks"
  }
}

# --- seed local denylist (never overwrite an existing one)
$localList = 'git-hooks\denylist.local.txt'
$exampleList = 'git-hooks\denylist.example.txt'
if (Test-Path -LiteralPath $localList) {
  Write-Host "[bkf] $localList already exists - left unchanged."
} else {
  Copy-Item -LiteralPath $exampleList -Destination $localList
  Write-Host "[bkf] seeded $localList from the example."
}

# --- next steps
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit git-hooks/denylist.local.txt - replace placeholders with your own"
Write-Host "     real protected terms (one literal term per line). It is gitignored."
Write-Host "  2. In a PRIVATE repo, make a test commit and push to confirm the pre-push"
Write-Host "     hook runs and blocks any denylist term."
Write-Host "  3. Keep real tokens OUT of committed files - put them only in *.local files."
Write-Host ""
Write-Host "Done. No network, no installs, no git init, no commits were performed."
