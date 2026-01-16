"""
Reset the CineEscapeApp SQLite database and seed it with base users and movies.

reset_db.py Script:
- Deletes instance/movies.db if it exists
- Recreates all tables
- Seeds deterministic users and movies with poster URLs from OMDB_API_KEY
"""

"""
Reset the CineEscapeApp SQLite database and seed it with base users and movies.
"""

import os
import requests
from CineEscapeApp.app import app, db
from CineEscapeApp.models import User, Movie

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
DB_PATH = os.path.join(app.instance_path, "movies.db")


def fetch_poster(title: str) -> str:
    """Fetch poster URL from OMDb."""
    if not OMDB_API_KEY:
        return ""

    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return ""
        data = response.json()
        poster = data.get("Poster", "")
        return "" if poster in ("N/A", None) else poster
    except requests.RequestException:
        return ""


def seed_users() -> dict:
    """Create baseline users."""
    users = {
        "Athena": User(name="Athena"),
        "Demetri": User(name="Demetri"),
        "Steve": User(name="Steve"),
        "Xavier": User(name="Xavier")
    }
    db.session.add_all(users.values())
    db.session.commit()
    return users


def seed_movies(users: dict) -> None:
    """Create baseline movies with metadata."""
    movie_specs = [
        {
            "user": users["Athena"],
            "title": "Fried Green Tomatoes",
            "director": "Jon Avnet",
            "year": "1991"
        },
        {
            "user": users["Demetri"],
            "title": "The Matrix",
            "director": "Lana Wachowski, Lilly Wachowski",
            "year": "1999"
        },
        {
            "user": users["Steve"],
            "title": "First Blood",
            "director": "Ted Kotcheff",
            "year": "1982"
        },
        {
            "user": users["Xavier"],
            "title": "Rambo: First Blood Part II",
            "director": "George P. Cosmatos",
            "year": "1985"
        }
    ]

    for spec in movie_specs:
        poster_url = fetch_poster(spec["title"])
        movie = Movie(
            title=spec["title"],
            director=spec["director"],
            year=spec["year"],
            poster_url=poster_url,
            user_id=spec["user"].id
        )
        db.session.add(movie)

    db.session.commit()


def reset_database() -> None:
    """Reset DB and seed users/movies."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with app.app_context():
        db.create_all()
        users = seed_users()
        seed_movies(users)
        print("Database reset complete.")


if __name__ == "__main__":
    reset_database()
