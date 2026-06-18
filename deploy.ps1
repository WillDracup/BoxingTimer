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

# --- bump the version by 0.1, in lockstep across index.html + sw.js ---
# Read the current version from index.html (e.g. "1.0"), add 0.1 using integer tenths
# (avoids float/locale issues), then stamp the new value into both files.
$htmlPath = Join-Path $PSScriptRoot "index.html"
$swPath   = Join-Path $PSScriptRoot "sw.js"
$html = Get-Content $htmlPath -Raw
$vm = [regex]::Match($html, 'const APP_VERSION = "([\d.]+)";')
if (-not $vm.Success) { throw "Could not find the APP_VERSION line in index.html" }
$old = $vm.Groups[1].Value
$tenths = [int][math]::Round([double]::Parse($old, [Globalization.CultureInfo]::InvariantCulture) * 10) + 1
$new = "{0}.{1}" -f [int][math]::Floor($tenths / 10.0), ($tenths % 10)

$html = $html -replace 'const APP_VERSION = "[\d.]+";', "const APP_VERSION = `"$new`";"
# bump the icon cache-buster so iOS/Android fetch the new home-screen icon on re-add
$html = $html -replace 'apple-touch-icon\.png\?v=[\d.]+', "apple-touch-icon.png?v=$new"
Set-Content $htmlPath -Value $html -NoNewline

# same cache-buster for the manifest icons
$manPath = Join-Path $PSScriptRoot "manifest.webmanifest"
$man = Get-Content $manPath -Raw
$man = $man -replace '\.png\?v=[\d.]+', ".png?v=$new"
Set-Content $manPath -Value $man -NoNewline

$sw = Get-Content $swPath -Raw
if (-not ([regex]::IsMatch($sw, 'const CACHE = "box-v[\d.]+";'))) { throw "Could not find the CACHE version line in sw.js" }
$sw = $sw -replace 'const CACHE = "box-v[\d.]+";', "const CACHE = `"box-v$new`";"
Set-Content $swPath -Value $sw -NoNewline
Write-Host "  Version: v$old -> v$new  (cache box-v$new)" -ForegroundColor Yellow

# --- commit & push ---
git add -A
git commit -m "$msg`n`nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push origin main

Write-Host ""
Write-Host "  Pushed. GitHub Pages rebuilds in ~1 min." -ForegroundColor Green
Write-Host "  Live: https://willdracup.github.io/BoxingTimer/" -ForegroundColor Cyan
