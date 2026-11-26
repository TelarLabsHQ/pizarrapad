// Offline support: the board (and any page you've opened) works without internet after the first visit.
// Pages always come from the network first, so updates show right away; the saved copy is used only when offline.
const CACHE = 'pizarrapad-v6';
const CORE = ['/board/', '/favicon.svg', '/manifest.webmanifest', '/icons/icon-192.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
const keep = (req, r) => { if (r && r.ok && r.type !== 'opaque') { const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)); } return r; };
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const page = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
  if (url.origin === location.origin && page) {
    // pages: network first, saved copy when offline (the board falls back to its saved copy too)
    const key = url.pathname === '/board/index.html' ? '/board/' : url.pathname;
    e.respondWith(fetch(req).then(r => keep(key, r)).catch(() => caches.match(key).then(hit => hit || caches.match('/board/'))));
    return;
  }
  if (url.origin === location.origin) {
    // files (scripts, styles, icons): use the saved copy right away, and refresh it in the background
    e.respondWith(caches.match(req).then(hit => { const net = fetch(req).then(r => keep(req, r)).catch(() => hit); return hit || net; }));
    return;
  }
  if (url.hostname.endsWith('fonts.googleapis.com') || url.hostname.endsWith('fonts.gstatic.com')) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => keep(req, r))));
  }
});
