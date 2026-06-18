@echo off
REM Double-click this to put the latest version of the app online.
REM It bumps the cache version, commits, and pushes to GitHub Pages.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy.ps1"
echo.
echo You can close this window now.
pause
