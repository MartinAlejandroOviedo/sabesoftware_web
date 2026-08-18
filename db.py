"""Base de datos SQLite: esquema, datos semilla y acceso a datos."""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    slug        TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    icon        TEXT NOT NULL,
    accent      TEXT NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS product_features (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    label       TEXT NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS value_cards (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    description TEXT NOT NULL,
    icon        TEXT NOT NULL,
    accent      TEXT NOT NULL,
    sort_order  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS stats (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    value      TEXT NOT NULL,
    label      TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS site (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

PRODUCTS = [
    ("Sabe Backup", "sabe-backup",
     "Backup automático para archivos y bases de datos, con programación inteligente y restauración en un clic.",
     "fas fa-database", "indigo",
     ["Copias programadas", "Cifrado de datos", "Restauración instantánea"]),
    ("Sabe Sync", "sabe-sync",
     "Sincroniza archivos entre Windows y Linux en tiempo real, sin fricciones y con control total de versiones.",
     "fas fa-sync-alt", "purple",
     ["Sincronización en tiempo real", "Historial de versiones", "Multiplataforma"]),
    ("Sabe Analyzer", "sabe-analyzer",
     "Análisis y monitoreo de rendimiento en tiempo real, con reportes claros para tomar mejores decisiones.",
     "fas fa-chart-line", "pink",
     ["Monitoreo en vivo", "Reportes inteligentes", "Alertas proactivas"]),
]

VALUE_CARDS = [
    ("Machine Care",
     "Optimizamos cada línea de código para cuidar el rendimiento y la longevidad de tu máquina.",
     "fas fa-microchip", "indigo"),
    ("User Care",
     "Diseñamos experiencias intuitivas que ponen a las personas en el centro de todo.",
     "fas fa-heart", "purple"),
    ("Multiplataforma",
     "Windows y Linux con la misma calidad, estabilidad y soporte de primera.",
     "fab fa-windows", "pink"),
    ("Confianza",
     "Seguridad, respaldo y estabilidad en cada release. Tu información siempre a salvo.",
     "fas fa-shield-halved", "emerald"),
]

STATS = [
    ("3+", "Productos"),
    ("10+", "Años de historia"),
    ("2", "Plataformas"),
    ("99.9%", "Uptime"),
]

SITE = {
    "site_name": "Sabe Software",

    "hero_badge": "Machine & User Care",
    "hero_title_part1": "Software que",
    "hero_title_gradient": "cuida tu máquina",
    "hero_title_part2": "y a tu usuario",
    "hero_subtitle": "Soluciones robustas para Windows y Linux que combinan diseño moderno, tecnología de confianza y una experiencia pensada para las personas.",

    "intro_eyebrow": "Quiénes somos",
    "intro_title": "Tecnología que trabaja a tu favor",
    "intro_text": "Desde 2015 creamos herramientas que simplifican el día a día de profesionales y entusiastas de la tecnología. Cada producto combina diseño moderno con una arquitectura robusta, pensado para Windows y Linux por igual.",

    "products_eyebrow": "Productos",
    "products_title": "Herramientas que impulsan tu trabajo",
    "products_subtitle": "Soluciones diseñadas para ser potentes por dentro y hermosas por fuera.",

    "cta_title": "¿Listo para empezar?",
    "cta_text": "Cuéntanos qué necesitas y nuestro equipo te responderá lo antes posible.",

    "about_eyebrow": "Nuestra Historia",
    "about_title": "Nacidos para simplificar la tecnología",
    "about_text": "Fundada en 2015, Sabe Software nació con la visión de crear herramientas que simplifiquen el día a día de profesionales y entusiastas de la tecnología.",
    "about_philosophy_title": "Nuestra filosofía",
    "about_philosophy": "Nuestra filosofía de Machine and User Care significa que cuidamos tanto del rendimiento del software como de la experiencia del usuario. Cada línea de código se escribe pensando en la confianza del cliente y en la longevidad del producto.",

    "contact_eyebrow": "Contacto",
    "contact_title": "Hablemos de tu próximo proyecto",
    "contact_text": "Cuéntanos qué necesitas y nuestro equipo te responderá lo antes posible.",
    "contact_email": "contacto@sabesoftware.com",
    "contact_location": "Trabajando en remoto, disponibles globalmente",
    "contact_schedule": "Lun a Vie · 9:00 – 18:00 (UTC-3)",

    "footer_tagline": "Innovación que cuida tu máquina y tu usuario. Soluciones robustas para Windows y Linux desde 2015.",
}


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            _seed_products(conn)
        if conn.execute("SELECT COUNT(*) FROM value_cards").fetchone()[0] == 0:
            _seed_value_cards(conn)
        if conn.execute("SELECT COUNT(*) FROM stats").fetchone()[0] == 0:
            _seed_stats(conn)
        _seed_site(conn)
        conn.commit()
    finally:
        conn.close()


def _seed_products(conn):
    for i, (name, slug, desc, icon, accent, features) in enumerate(PRODUCTS):
        cur = conn.execute(
            "INSERT INTO products (name, slug, description, icon, accent, sort_order) VALUES (?,?,?,?,?,?)",
            (name, slug, desc, icon, accent, i),
        )
        product_id = cur.lastrowid
        for j, label in enumerate(features):
            conn.execute(
                "INSERT INTO product_features (product_id, label, sort_order) VALUES (?,?,?)",
                (product_id, label, j),
            )


def _seed_value_cards(conn):
    for i, (title, desc, icon, accent) in enumerate(VALUE_CARDS):
        conn.execute(
            "INSERT INTO value_cards (title, description, icon, accent, sort_order) VALUES (?,?,?,?,?)",
            (title, desc, icon, accent, i),
        )


def _seed_stats(conn):
    for i, (value, label) in enumerate(STATS):
        conn.execute(
            "INSERT INTO stats (value, label, sort_order) VALUES (?,?,?)",
            (value, label, i),
        )


def _seed_site(conn):
    for key, value in SITE.items():
        conn.execute("INSERT OR IGNORE INTO site (key, value) VALUES (?,?)", (key, value))


def get_products():
    conn = get_connection()
    try:
        products = []
        for row in conn.execute(
            "SELECT id, name, slug, description, icon, accent FROM products ORDER BY sort_order, id"
        ):
            features = [
                f["label"]
                for f in conn.execute(
                    "SELECT label FROM product_features WHERE product_id=? ORDER BY sort_order, id",
                    (row["id"],),
                )
            ]
            products.append({
                "id": row["id"],
                "name": row["name"],
                "slug": row["slug"],
                "description": row["description"],
                "icon": row["icon"],
                "accent": row["accent"],
                "features": features,
            })
        return products
    finally:
        conn.close()


def get_product_by_slug(slug):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, name, slug, description, icon, accent FROM products WHERE slug = ?",
            (slug,)
        ).fetchone()
        if not row:
            return None
        features = [
            f["label"]
            for f in conn.execute(
                "SELECT label FROM product_features WHERE product_id=? ORDER BY sort_order, id",
                (row["id"],),
            )
        ]
        return {
            "id": row["id"],
            "name": row["name"],
            "slug": row["slug"],
            "description": row["description"],
            "icon": row["icon"],
            "accent": row["accent"],
            "features": features,
        }
    finally:
        conn.close()


def get_value_cards():
    conn = get_connection()
    try:
        return [
            {"id": r["id"], "title": r["title"], "description": r["description"],
             "icon": r["icon"], "accent": r["accent"]}
            for r in conn.execute(
                "SELECT id, title, description, icon, accent FROM value_cards ORDER BY sort_order, id"
            )
        ]
    finally:
        conn.close()


def get_stats():
    conn = get_connection()
    try:
        return [
            {"id": r["id"], "value": r["value"], "label": r["label"]}
            for r in conn.execute("SELECT id, value, label FROM stats ORDER BY sort_order, id")
        ]
    finally:
        conn.close()


def get_site():
    conn = get_connection()
    try:
        return {r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM site")}
    finally:
        conn.close()
