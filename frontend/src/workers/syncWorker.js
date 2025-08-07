// Worker para sincronización offline
const CACHE_NAME = 'nexustock-scan-cache-v1';
const API_ENDPOINT = '/api/v1/scan/offline';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(['/offline.html']))
  );
});

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-scanned-items') {
    event.waitUntil(syncScannedItems());
  }
});

async function syncScannedItems() {
  const cache = await caches.open(CACHE_NAME);
  const requests = await cache.keys();
  
  for (const request of requests) {
    if (request.url.includes('/scan/')) {
      const response = await cache.match(request);
      const data = await response.json();
      
      try {
        await fetch(API_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        await cache.delete(request);
      } catch (error) {
        console.error('Error en sincronización:', error);
        break;
      }
    }
  }
}
