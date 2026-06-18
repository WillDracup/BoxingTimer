# One-command deploy to GitHub Pages.
# Auto-bumps the service-worker cache version (so phones pick up the new build),
# commits everything, and pushes. Pages rebuilds in ~1 minute.
#
# Usage:  .\deploy.ps1            (uses a default commit message)
#         .\deploy.ps1 "message"  (custom commit message)
#
# First-time setup (once):
#   git init; git branch -M main
#   git remote add origin https://github.com/<you>/<repo>.git
#   ...then in the repo's Settings -> Pages, deploy from branch "main" / root.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$msg = if ($args.Count -gt 0) { $args[0] } else { "Update app" }

# --- bump CACHE = "box-vN" -> "box-v(N+1)" in sw.js ---
$swPath = Join-Path $PSScriptRoot "sw.js"
$sw = Get-Content $swPath -Raw
$m = [regex]::Match($sw, 'const CACHE = "box-v(\d+)";')
if (-not $m.Success) { throw "Could not find the CACHE version line in sw.js" }
$old = [int]$m.Groups[1].Value
$new = $old + 1
$sw = $sw -replace 'const CACHE = "box-v\d+";', "const CACHE = `"box-v$new`";"
Set-Content $swPath -Value $sw -NoNewline
Write-Host "  Cache version: box-v$old -> box-v$new" -ForegroundColor Yellow

# --- stamp the same number into the front-screen version label in index.html ---
$htmlPath = Join-Path $PSScriptRoot "index.html"
$html = Get-Content $htmlPath -Raw
if ($html -match 'const APP_VERSION = "\d+";') {
  $html = $html -replace 'const APP_VERSION = "\d+";', "const APP_VERSION = `"$new`";"
  Set-Content $htmlPath -Value $html -NoNewline
  Write-Host "  App version label: v$new" -ForegroundColor Yellow
}

# --- commit & push ---
git add -A
git commit -m "$msg`n`nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push origin main

Write-Host ""
Write-Host "  Pushed. GitHub Pages rebuilds in ~1 min." -ForegroundColor Green
Write-Host "  Live: https://willdracup.github.io/BoxingTimer/" -ForegroundColor Cyan
