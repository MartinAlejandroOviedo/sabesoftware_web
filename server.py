"""Servidor web: sirve los archivos estáticos y la API JSON respaldada por SQLite."""
import json
import sys
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import db

# URLs limpias -> archivo físico servido
CLEAN_ROUTES = {
    '/': '/pages/index.html',
    '/index.html': '/pages/index.html',
    '/about': '/pages/about.html',
    '/products': '/pages/products.html',
    '/contact': '/pages/contact.html',
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=db.BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/'):
            self.serve_api(path)
            return
        # Rutas limpias para páginas estáticas
        target = CLEAN_ROUTES.get(path)
        if target:
            self.path = target + (('?' + parsed.query) if parsed.query else '')
            super().do_GET()
            return
        # Rutas dinámicas: /products/<slug> -> detalle de producto
        if path.startswith('/products/') and path != '/products':
            slug = path.split('/')[-1]
            self.path = f'/pages/product-detail.html?slug={slug}'
            super().do_GET()
            return
        super().do_GET()

    def serve_api(self, path):
        route = path[len('/api/'):].strip('/')
        # Endpoint para producto individual: /api/products/<slug>
        if route.startswith('products/'):
            slug = route.split('/')[-1]
            if slug:
                self.send_json(db.get_product_by_slug(slug))
                return
        routes = {
            'products': db.get_products,
            'values': db.get_value_cards,
            'stats': db.get_stats,
            'site': db.get_site,
        }
        handler = routes.get(route)
        if handler is None:
            self.send_json({'error': 'Ruta no encontrada'}, 404)
            return
        try:
            self.send_json(handler())
        except Exception as exc:
            self.send_json({'error': str(exc)}, 500)

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)


def main():
    db.init_db()
    host, port = '', 8000
    try:
        server = ThreadingHTTPServer((host, port), Handler)
    except OSError as exc:
        print(f'No se pudo iniciar en el puerto {port}: {exc}')
        print('Otro servidor ya está corriendo en ese puerto (por ejemplo, un "python -m http.server 8000" viejo).')
        print('Cerrá esa ventana/proceso y volvé a ejecutar run_server.bat.')
        sys.exit(1)
    print(f'Servidor en http://localhost:{port}  (Ctrl+C para salir)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nDetenido.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
