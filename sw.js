// CareEZ Service Worker — v1.3 — 2026-06-09
const CACHE_VERSION = 'careez-v1.3-2026-06-09';

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
  '/opensource/contributing/',
  '/opensource/contributing/index.html',
  '/partners/',
  '/partners/index.html',
  '/roadmap/',
  '/roadmap/index.html',
  '/contact/',
  '/contact/index.html',
  '/privacy/',
  '/privacy/index.html',
  '/terms/',
  '/terms/index.html',
  '/research/voice-biomarker-protocol/',
  '/research/voice-biomarker-protocol/index.html',
];

// ─── Offline fallback response (constructed in SW context, no network needed) ─
function offlineFallback() {
  return caches.match('/offline.html').then((cached) => {
    if (cached) return cached;
    // offline.html itself wasn't cached — return a bare-bones inline response
    return new Response(
      '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Offline</title></head>' +
      '<body><h1>You\'re offline</h1><p>Please check your network and try again.</p></body></html>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
    );
  });
}

// ─── Write-behind cache helper — fire-and-forget with explicit error logging ─
function cachePut(request, response) {
  caches.open(CACHE_VERSION).then((cache) => {
    return cache.put(request, response);
  }).catch((err) => {
    console.warn('[SW] cache.put failed:', request.url, err);
  });
}

// ─── Install: pre-cache shell ───────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      // Cache what we can; do not fail install if some assets 404
      return Promise.allSettled(
        SHELL_ASSETS.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('[SW] Failed to pre-cache:', url, err);
          })
        )
      );
    })
    .then(() => self.skipWaiting())
    .catch((err) => {
      console.error('[SW] Install failed:', err);
    })
  );
});

// ─── Activate: purge old caches ─────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) =>
        Promise.allSettled(
          keys
            .filter((key) => key !== CACHE_VERSION)
            .map((key) =>
              caches.delete(key).catch((err) => {
                console.warn('[SW] Failed to delete old cache:', key, err);
              })
            )
        )
      )
      .then(() => self.clients.claim())
      .catch((err) => {
        console.error('[SW] Activate failed:', err);
      })
  );
});

// ─── Fetch: routing strategy ─────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // 1. Skip non-GET requests
  if (request.method !== 'GET') return;

  // 2. Guard against malformed request URLs (e.g. chrome-extension://)
  let url;
  try {
    url = new URL(request.url);
  } catch {
    return;
  }

  // 3. Skip cross-origin requests (Cloudflare Analytics, etc.)
  if (url.origin !== self.location.origin) return;

  // 4. Skip /api/* — always network, never cache
  if (url.pathname.startsWith('/api/')) return;

  // 5. Navigation requests — network-first, fallback to cache, then offline page
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache a fresh copy on success
          if (response.ok) {
            cachePut(request, response.clone());
          }
          return response;
        })
        .catch(() =>
          caches.match(request).then(
            (cached) => cached || offlineFallback()
          )
        )
    );
    return;
  }

  // 6. Static assets — cache-first, fallback to network, surface network errors
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;
      return fetch(request).then((response) => {
        if (response.ok) {
          cachePut(request, response.clone());
        }
        return response;
      }).catch((err) => {
        console.warn('[SW] Network fetch failed for:', request.url, err);
        // Return a 503 rather than letting the promise reject uncaught
        return new Response('Network error', {
          status: 503,
          headers: { 'Content-Type': 'text/plain' },
        });
      });
    })
  );
});
