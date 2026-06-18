# Boxing Timer — round timer

A small web app that installs onto your phone like a normal app and works offline.
It runs a boxing workout: a volume-check bell, a "gloves on" get-ready minute, a set of
warm-up rounds, then sparring rounds, with a rest gap between every round. The ring bell
and the round announcer are generated in the app, so there are no audio files to go missing.

## How a workout runs
1. Press Start — a single bell rings so you can set the phone volume.
2. "Get ready" (green) — the gloves-on countdown before round 1.
3. Warm-up rounds (blue) — each starts with a "ding ding" and ends with three quick dings.
4. Sparring rounds (light orange) — same bells, and 10 seconds before each one a voice
   calls "Seconds out, round N".
5. A green rest period sits between every round.
6. The big number is always the time remaining in the current phase.

## Defaults (all editable via "Adjust", saved on the device)
- Warm-up rounds: 3
- Sparring rounds: 6
- Gloves on (get-ready): 1:00
- Round length: 1:30
- Rest between rounds: 0:45
- Volume-check ping: on
- Round announcer voice: on

## What's in this folder
- index.html .............. the app
- manifest.webmanifest .... lets it install as a standalone app
- sw.js ................... makes it work offline (network-first)
- make_icons.py ........... regenerates the icons (not needed to run the app)
- icon-*.png / apple-touch-icon.png .. app icons
- dev.ps1 ................. local live-reload dev server (desktop + phone on same WiFi)
- deploy.ps1 .............. bump cache version, commit, push to GitHub Pages

## Run it locally
  .\dev.ps1
Then open the Desktop or Phone URL it prints. Edit a file, save, it reloads.

## Put it on your phone (GitHub Pages)
First time only:
  git init; git branch -M main
  git remote add origin https://github.com/<you>/<repo>.git
  git add -A; git commit -m "Initial boxing timer"
  git push -u origin main
Then in the repo's Settings -> Pages, deploy from branch "main" / root ("/").
Open the link it gives you on your phone, then "Add to Home Screen".
After the first push, future updates are just:  .\deploy.ps1 "what changed"

### Add to Home Screen
- iPhone (Safari): Share -> "Add to Home Screen" -> Add.
- Android (Chrome): menu (3 dots) -> "Install app".

## Credits
- Ring bell: "Boxing Bell 1" by lazychillzone, from Pixabay (royalty-free Pixabay
  Content License — free for commercial use, no attribution required). Stored as
  bell.mp3. If it ever fails to load, the app falls back to a synthesised bell.

## Notes
- The announcer uses the phone's built-in text-to-speech, so the exact voice depends on the
  device. iOS plays a male English voice where one is installed. If you'd prefer a real
  recorded boxing announcer, recorded clips can be dropped in instead — ask.
- To change the bell tone, edit the `bell()` function near the top of the <script> in
  index.html (the `fund` frequency and `partials` list).
- If you update the app, deploy.ps1 bumps CACHE = "box-vN" in sw.js so phones pick it up.
