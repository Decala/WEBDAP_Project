const CACHE_NAME = 'carelink-static-v1';
const OFFLINE_URL = '/offline.html';

const STATIC_ASSETS = [
  '/',
  OFFLINE_URL,
  '/static/style.css',
  '/static/images/carelink_logo.png',
  '/static/downloads/seizure_guide.pdf',
  // Add other essential assets here
];

// Install: Pre-cache essential assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      // Ensure offline.html is fetched fresh
      const offlineResponse = await fetch(OFFLINE_URL);
      await cache.put(OFFLINE_URL, offlineResponse.clone());

      // Add other static assets
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting(); // Activate immediately
});

// Activate: Take control of clients
self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

// Fetch: Serve cached assets or fallback to offline.html
self.addEventListener('fetch', event => {
  const { request } = event;

  // Handle navigation requests (e.g., clicking links)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // Handle other requests (CSS, JS, images, PDFs)
  event.respondWith(
    caches.match(request).then(cachedResponse => {
      return cachedResponse || fetch(request);
    })
  );
});
