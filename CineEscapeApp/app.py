"""Main Flask application module for 🎬 CineEscapeApp.

This module initializes the Flask application, configures logging,
loads environment variables, registers database models, and defines
the core routes for user and movie management.
"""

# ============================================================
# 1. Standard Library Imports
# ============================================================
import os
import logging
from logging.handlers import RotatingFileHandler

# ============================================================
# 2. Third‑Party Library Imports
# ============================================================
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, abort
import requests

# ============================================================
# 3. Local Application Imports
# ============================================================
from CineEscapeApp.config import Config
from CineEscapeApp.data_manager import DataManager
from CineEscapeApp.models import db, User, Movie

# ============================================================
# 4. Environment Setup
# ============================================================
load_dotenv()

app = Flask(__name__)
# Logging configuration
if not os.path.exists("logs"):
    os.mkdir("logs")

file_handler = RotatingFileHandler(
    "logs/cineescape.log", maxBytes=10240, backupCount=10
)

file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
)

file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info("CineEscapeApp startup")

app.config.from_object(Config)

db.init_app(app)
data_manager = DataManager()

# ============================================================
# Ensure database tables exist when the app is imported
# (pytest imports the app module, so this MUST run here)
# ============================================================
with app.app_context():
    db.create_all()


OMDB_API_KEY = os.getenv("OMDB_API_KEY")


@app.route("/")
def index():
    """Render the homepage showing all users."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/create_user", methods=["POST"])
def create_user():
    """Create a new user from form input."""
    name = request.form.get("name")
    if not name:
        abort(400)
    data_manager.create_user(name)
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user by ID."""
    deleted = data_manager.delete_user(user_id)
    if not deleted:
        abort(404)
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    """Display all movies for a specific user."""
    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies/add", methods=["POST"])
def add_movie(user_id):
    """Add a movie to a user's collection using OMDb lookup."""
    title = request.form.get("title")
    if not title:
        abort(400)

    try:
        response = requests.get(
            f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}", timeout=5
        )
        data = response.json()
    except Exception as e:  # pylint: disable=broad-exception-caught
        app.logger.error("OMDb fetch failed: %s", e)
        abort(500)

    if data.get("Response") == "False":
        abort(404)

    movie = Movie(
        title=data["Title"],
        year=data.get("Year"),
        director=data.get("Director"),
        poster_url=data.get("Poster"),
        user_id=user_id,
    )

    data_manager.add_movie(movie)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """Update a movie's title."""
    new_title = request.form.get("new_title")
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's collection."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for("get_movies", user_id=user_id))


@app.errorhandler(400)
def bad_request(e):
    """Handle 400 Bad Request errors."""
    app.logger.error("OMDb fetch failed: %s", e)
    return render_template("400.html"), 400


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 Not Found errors."""
    app.logger.warning("404 error: %s", e)
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 Internal Server errors."""
    app.logger.error("500 error: %s", e)
    return render_template("500.html"), 500

if __name__ == "__main__":
    """Run the Flask development server."""
    import platform

    system = platform.system()

    if system == "Darwin":  # macOS
        app.run(host="127.0.0.1", port=5001, debug=True)
    else:  # Linux (Codio Ubuntu 22.04.3 LTS)
        app.run(host="0.0.0.0", port=5000, debug=True)
