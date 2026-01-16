"""Pytest configuration and fixtures for 🎬 CineEscapeApp.

This module sets up an isolated in‑memory SQLite database for each test
session and provides a Flask test client fixture. The database is created
fresh for every test run to ensure deterministic, reproducible behavior.
"""

import pytest
from CineEscapeApp.app import app, db
from CineEscapeApp.models import User, Movie  # Movie imported for completeness if needed later.


@pytest.fixture
def client():
    """Create a Flask test client with an isolated in‑memory database.

    This fixture:
    - Enables Flask testing mode
    - Uses an in‑memory SQLite database (sqlite:///:memory:)
    - Creates all tables before yielding the client
    - Seeds deterministic test users
    - Drops all tables after tests complete

    Yields:
        FlaskClient: A test client for sending requests to the app.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        db.session.add_all(
            [
                User(name="Athena"),
                User(name="Demetri"),
            ]
        )
        db.session.commit()

        yield app.test_client()

        db.drop_all()
