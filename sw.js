/* בר השגה · Service Worker
   שומר את האתר בטלפון כדי שיעבוד גם בלי אינטרנט.
   הדף עצמו נטען תמיד קודם מהרשת (כדי שעדכונים יופיעו מיד), ורק אם אין רשת – מהעותק השמור.
   אחרי שינוי באייקונים או בקבצים האלה: להעלות את מספר הגרסה ב-VERSION. */
const VERSION = "bar-hasaga-v36-pwa1";
const PAGE_CACHE = VERSION + "-page";
const ASSET_CACHE = VERSION + "-assets";
const FONT_CACHE = "bar-hasaga-fonts-v1";
const FONT_CSS = "https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&family=Frank+Ruhl+Libre:wght@400;500;700;900&display=swap";
const ASSETS = [
  "./manifest.webmanifest",
  "./favicon.svg",
  "./favicon-32.png",
  "./favicon.ico",
  "./apple-touch-icon.png",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-maskable-192.png",
  "./icon-maskable-512.png"
];
const SCOPE = self.registration.scope;
const PAGE_KEY = new URL("./", SCOPE).href;

async function cacheFonts() {
  const cache = await caches.open(FONT_CACHE);
  const res = await fetch(FONT_CSS, { mode: "cors" });
  if (!res.ok) return;
  const css = await res.clone().text();
  await cache.put(FONT_CSS, res);
  const urls = [...new Set(css.match(/https:\/\/fonts\.gstatic\.com\/[^)'"\s]+/g) || [])];
  await Promise.all(urls.map(async u => {
    if (await cache.match(u)) return;
    const r = await fetch(u, { mode: "cors" });
    if (r.ok) await cache.put(u, r);
  }));
}

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const page = await caches.open(PAGE_CACHE);
    const res = await fetch(PAGE_KEY, { cache: "reload" });
    if (res.ok) await page.put(PAGE_KEY, res);
    const assets = await caches.open(ASSET_CACHE);
    await assets.addAll(ASSETS.map(u => new Request(u, { cache: "reload" })));
    try { await cacheFonts(); } catch (e) { /* בלי גופנים הדף עדיין עובד */ }
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keep = [PAGE_CACHE, ASSET_CACHE, FONT_CACHE];
    for (const k of await caches.keys()) if (k.startsWith("bar-hasaga-") && !keep.includes(k)) await caches.delete(k);
    await self.clients.claim();
  })());
});

function timeout(ms) { return new Promise(r => setTimeout(r, ms)); }

async function pageFromNetwork(request) {
  const res = await fetch(request);
  if (res.ok && res.type === "basic") {
    const cache = await caches.open(PAGE_CACHE);
    await cache.put(PAGE_KEY, res.clone());
  }
  return res;
}

async function handlePage(event) {
  const network = pageFromNetwork(event.request);
  event.waitUntil(network.catch(() => {}));
  const cached = await caches.match(PAGE_KEY, { cacheName: PAGE_CACHE });
  if (!cached) return network;
  // רשת קודם; אם אין רשת או שהיא איטית מאוד – העותק השמור
  try {
    const res = await Promise.race([network, timeout(6000).then(() => null)]);
    if (res && res.ok) return res;
  } catch (e) {}
  return cached;
}

async function cacheFirst(request, cacheName) {
  const hit = await caches.match(request, { ignoreVary: true });
  if (hit) return hit;
  const res = await fetch(request);
  if (res.ok || res.type === "opaque") {
    const cache = await caches.open(cacheName);
    await cache.put(request, res.clone());
  }
  return res;
}

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (req.mode === "navigate" && url.href.startsWith(SCOPE)) {
    event.respondWith(handlePage(event));
    return;
  }
  if (url.origin === "https://fonts.googleapis.com" || url.origin === "https://fonts.gstatic.com") {
    event.respondWith(cacheFirst(req, FONT_CACHE));
    return;
  }
  if (url.href.startsWith(SCOPE)) {
    event.respondWith(cacheFirst(req, ASSET_CACHE));
  }
});
