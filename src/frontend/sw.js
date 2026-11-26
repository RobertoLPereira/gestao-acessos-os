const CACHE_NAME = "portal-os-v1";
const ASSETS_ESTATICOS = [
    "/",
    "/index.html",
    "/css/style.css",
    "/js/app.js",
    "/js/api.js",
    "/js/ui.js",
    "/manifest.json"
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_ESTATICOS))
    );
});

self.addEventListener("fetch", (event) => {
    const url = new URL(event.request.url);

    // Requisições de API sempre tentam a rede primeiro
    if (url.pathname.startsWith("/api/")) {
        event.respondWith(
            fetch(event.request).catch(() =>
                new Response(JSON.stringify({ erro: "Você está offline. Conecte-se à rede para atualizar os menus." }), {
                    status: 503,
                    headers: { "Content-Type": "application/json" }
                })
            )
        );
        return;
    }

    // Arquivos estáticos do PWA usam Cache com fallback para rede
    event.respondWith(
        caches.match(event.request).then((cached) => cached || fetch(event.request))
    );
});
