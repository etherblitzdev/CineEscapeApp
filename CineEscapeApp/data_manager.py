"""Data access layer for 🎬 CineEscapeApp.

Provides CRUD operations for users and movies using SQLAlchemy models.
"""

from CineEscapeApp.models import db, User, Movie



class DataManager:
    """Handles database operations for users and movies."""

    def create_user(self, name):
        """Create and persist a new user."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        """Return all users."""
        return User.query.all()

    def delete_user(self, user_id):
        """Delete a user by ID."""
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    def get_movies(self, user_id):
        """Return all movies for a given user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a new movie to the database."""
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id, new_title):
        """Update a movie's title."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        """Delete a movie by ID."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
        return movie
