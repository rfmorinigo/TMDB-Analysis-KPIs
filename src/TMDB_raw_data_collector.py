"""
TMDB Raw Data Collector
----------------------

Descarga:
- 100 peliculas mas vistas
- 100 series mas vistas

Desde la API de TMDB y las guarda en SQLite.

Flujo:
TMDB API -> JSON (memoria) -> SQLite
"""

# 1. Imports
import os
import time
import requests
import sqlite3
from dotenv import load_dotenv


# 2. Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("La variable de entorno TMDB_API_KEY no esta definida")

BASE_URL = "https://api.themoviedb.org/3"


# 3. Resolver rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DB_DIR = os.path.join(PROJECT_DIR, "db")
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "tmdb_content.db")
print(f"Base de datos: {DB_PATH}")


# 4. Conexion a SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# 5. Crear esquema de tablas
cursor.executescript("""
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT,
    release_date TEXT,
    popularity REAL,
    vote_average REAL,
    vote_count INTEGER,
    budget INTEGER,
    revenue INTEGER
);

CREATE TABLE IF NOT EXISTS tv_shows (
    tv_id INTEGER PRIMARY KEY,
    name TEXT,
    first_air_date TEXT,
    popularity REAL,
    vote_average REAL,
    vote_count INTEGER
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE IF NOT EXISTS tv_show_genres (
    tv_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (tv_id, genre_id),
    FOREIGN KEY (tv_id) REFERENCES tv_shows(tv_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);
""")

conn.commit()


# 6. Funciones para consumir la API
def get_popular(endpoint, page):
    url = f"{BASE_URL}/{endpoint}/popular"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": page
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["results"]


def get_details(endpoint, content_id):
    url = f"{BASE_URL}/{endpoint}/{content_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


# 7. Ingesta de peliculas (100)
print("Descargando peliculas mas vistas", end="", flush=True)
counter = 0

for page in range(1, 6):
    movies = get_popular("movie", page)

    for movie in movies:
        details = get_details("movie", movie["id"])

        cursor.execute("""
            INSERT OR IGNORE INTO movies
            (movie_id, title, release_date, popularity,
             vote_average, vote_count, budget, revenue)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            details["id"],
            details["title"],
            details["release_date"],
            details["popularity"],
            details["vote_average"],
            details["vote_count"],
            details["budget"],
            details["revenue"]
        ))

        for g in details.get("genres", []):
            cursor.execute(
                "INSERT OR IGNORE INTO genres VALUES (?, ?)",
                (g["id"], g["name"])
            )
            cursor.execute(
                "INSERT OR IGNORE INTO movie_genres VALUES (?, ?)",
                (details["id"], g["id"])
            )

        conn.commit()
        counter += 1
        if counter % 10 == 0:
            print(".", end="", flush=True)
        time.sleep(0.25)

print(" OK")


# 8. Ingesta de series (100)
print("Descargando series mas vistas", end="", flush=True)
counter = 0

for page in range(1, 6):
    shows = get_popular("tv", page)

    for show in shows:
        details = get_details("tv", show["id"])

        cursor.execute("""
            INSERT OR IGNORE INTO tv_shows
            (tv_id, name, first_air_date, popularity,
             vote_average, vote_count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            details["id"],
            details["name"],
            details["first_air_date"],
            details["popularity"],
            details["vote_average"],
            details["vote_count"]
        ))

        for g in details.get("genres", []):
            cursor.execute(
                "INSERT OR IGNORE INTO genres VALUES (?, ?)",
                (g["id"], g["name"])
            )
            cursor.execute(
                "INSERT OR IGNORE INTO tv_show_genres VALUES (?, ?)",
                (details["id"], g["id"])
            )

        conn.commit()
        counter += 1
        if counter % 10 == 0:
            print(".", end="", flush=True)
        time.sleep(0.25)

print(" OK")


# 9. Cierre
conn.close()
print("Ingesta finalizada. Base lista para analisis.")
