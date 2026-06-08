// CareEZ Service Worker — v1.2 — 2026-06-09
const CACHE_VERSION = 'careez-v1.2-2026-06-09';

const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/site.webmanifest',
  '/favicon.ico',
  '/favicon.svg',
  '/favicon-16.png',
  '/favicon-32.png',
  '/favicon-96.png',
  '/apple-touch-icon.png',
  '/android-chrome-192.png',
  '/android-chrome-512.png',
  '/og-image.png',
  '/about/',
  '/about/index.html',
  '/team/',
  '/team/index.html',
  '/governance/',
  '/governance/index.html',
  '/press/',
  '/press/index.html',
  '/standards/',
  '/standards/index.html',
  '/status/',
  '/status/index.html',
  '/compare/',
  '/compare/index.html',
  '/changelog/',
  '/changelog/index.html',
  '/adoption-index/',
  '/adoption-index/index.html',
  '/api-docs/',
  '/api-docs/index.html',
  '/security/',
  '/security/index.html',
  '/trial/',
  '/trial/index.html',
  '/faq/',
  '/faq/index.html',
  '/pricing/',
  '/pricing/index.html',
  '/opensource/',
  '/opensource/index.html',
  '/partners/',
  '/partners/index.html',
  '/roadmap/',
  '/roadmap/index.html',
  '/contact/',
  '/contact/index.html',
  '/research/voice-biomarker-protocol/',
  '/research/voice-biomarker-protocol/index.html',
];

// ─── Install: pre-cache shell ───────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      // Cache what we can; don't fail install if some assets 404
      return Promise.allSettled(
        SHELL_ASSETS.map((url) =>
          cache.add(url).catch(() => {
            console.warn('[SW] Failed to cache:', url);
          })
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// ─── Activate: purge old caches ─────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_VERSION)
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// ─── Fetch: routing strategy ─────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // 1. Skip non-GET requests
  if (request.method !== 'GET') return;

  // 2. Skip cross-origin requests (Cloudflare Analytics, etc.)
  if (url.origin !== self.location.origin) return;

  // 3. Skip /api/* — always network, never cache
  if (url.pathname.startsWith('/api/')) return;

  // 4. Navigation requests — network-first, fallback to cache, then offline.html
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache a fresh copy
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_VERSION).then((cache) => cache.put(request, clone));
          }
          return response;
        })
        .catch(() =>
          caches.match(request).then(
            (cached) => cached || caches.match('/offline.html')
          )
        )
    );
    return;
  }

  // 5. Static assets — cache-first, fallback to network
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_VERSION).then((cache) => cache.put(request, clone));
        }
        return response;
      });
    })
  );
});
