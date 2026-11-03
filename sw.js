/* ============================================================
   Festi Dibi — Service Worker
   Stratégies : app shell en cache-first, pages en network-first
   ============================================================ */

const VERSION = "festidibi-v10";
const SHELL = [
  "./",
  "./index.html",
  "./lineup.html",
  "./galerie.html",
  "./css/styles.css",
  "./css/header.css",
  "./css/pages.css",
  "./js/vendor/motion.min.js",
  "./js/motion.js",
  "./js/header.js",
  "./js/gallery.js",
  "./js/lineup.js",
  "./js/app.js",
  "./manifest.webmanifest",
  "./assets/logo.png",
  "./assets/logo-mark.png",
  "./assets/icon-192.png",
  "./assets/icon-512.png",
  "./assets/icon-maskable-512.png",
  "./assets/apple-touch-icon.png",
  "./assets/photos/aerial-800.webp",
  "./assets/photos/aerial-1600.webp",
  "./assets/photos/crowd-girls-800.webp",
  "./assets/photos/crowd-girls-1600.webp",
  "./assets/photos/grill-close-800.webp",
  "./assets/photos/grill-close-1600.webp",
  "./assets/photos/grill-skewers-800.webp",
  "./assets/photos/grill-skewers-1600.webp",
  "./assets/photos/grill-stall-800.webp",
  "./assets/photos/grill-stall-1600.webp",
  "./assets/photos/singer-blue-800.webp",
  "./assets/photos/singer-blue-1600.webp",
  "./assets/photos/singer-white-800.webp",
  "./assets/photos/singer-white-1600.webp",
  "./assets/photos/stage-tradition-800.webp",
  "./assets/photos/stage-tradition-1600.webp"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(VERSION);
      await Promise.all(
        SHELL.map((url) =>
          cache.add(new Request(url, { cache: "reload" })).catch(() => null)
        )
      );
      self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)));
      await self.clients.claim();
    })()
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Navigation : réseau d'abord, cache en secours (mode hors-ligne)
  if (request.mode === "navigate") {
    event.respondWith(
      (async () => {
        try {
          const fresh = await fetch(request);
          const path = new URL(request.url).pathname;
          // ne mettre en cache que l'accueil : sinon une visite sur /lineup.html
          // remplacerait la page de secours hors-ligne
          if (/\/(index\.html)?$/.test(path)) {
            const cache = await caches.open(VERSION);
            cache.put("./index.html", fresh.clone());
          }
          return fresh;
        } catch {
          const cache = await caches.open(VERSION);
          return (await cache.match("./index.html")) || (await cache.match("./")) ||
            new Response("Hors connexion", { status: 503, headers: { "Content-Type": "text/plain" } });
        }
      })()
    );
    return;
  }

  // Polices et ressources distantes : cache d'abord
  if (url.origin !== location.origin) {
    event.respondWith(
      (async () => {
        const cache = await caches.open(VERSION + "-ext");
        const hit = await cache.match(request);
        if (hit) return hit;
        try {
          const fresh = await fetch(request);
          if (fresh && (fresh.ok || fresh.type === "opaque")) cache.put(request, fresh.clone());
          return fresh;
        } catch {
          return new Response("", { status: 504 });
        }
      })()
    );
    return;
  }

  // Assets locaux : cache d'abord, puis réseau
  event.respondWith(
    (async () => {
      const cache = await caches.open(VERSION);
      const hit = await cache.match(request);
      if (hit) return hit;
      try {
        const fresh = await fetch(request);
        if (fresh.ok) cache.put(request, fresh.clone());
        return fresh;
      } catch {
        return new Response("", { status: 504 });
      }
    })()
  );
});
