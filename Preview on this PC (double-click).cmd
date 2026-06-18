@echo off
REM Double-click this to preview the app on this computer (and your phone on the
REM same WiFi). It prints two web addresses - open one in a browser.
REM Close the window (or press Ctrl+C) when you're done.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0dev.ps1"
pause
