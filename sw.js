/* Network-first service worker.
   When online, every file is fetched live so new deploys appear immediately on the
   next open — no waiting for iOS to notice a service-worker update. The cache is kept
   up to date on each fetch and used as a fallback, so the app still runs fully offline.
   In dev (localhost / LAN IP) it's pure network passthrough. */
const CACHE = "box-v2.2";
const host = self.location.hostname;
const DEV = host === "localhost" || host === "127.0.0.1" ||
  /^(192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)/.test(host) || host.endsWith(".local");
const ASSETS = [
  ".",
  "index.html",
  "manifest.webmanifest",
  "bell-start.mp3",
  "bell-end.mp3",
  "icon-192.png",
  "icon-512.png",
  "icon-maskable-512.png",
  "apple-touch-icon.png"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE).then(c =>
      Promise.all(ASSETS.map(a =>
        fetch(a, {cache:"no-store"}).then(r => c.put(a, r)).catch(() => {})
      ))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  if (DEV) return;   // dev: let the browser hit the network directly — always fresh
  e.respondWith(
    fetch(e.request, {cache:"no-store"}).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
      return res;
    }).catch(() =>
      caches.match(e.request).then(hit => hit || caches.match("index.html"))
    )
  );
});
