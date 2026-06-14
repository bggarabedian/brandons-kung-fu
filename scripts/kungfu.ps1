<#
Brandon's Kung Fu - thin wrapper. Calls the Python CLI only.
Contains NO install logic; all safety checks live in scripts/kungfu.py.
#>
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = "python"
& $py (Join-Path $here "kungfu.py") @args
exit $LASTEXITCODE
