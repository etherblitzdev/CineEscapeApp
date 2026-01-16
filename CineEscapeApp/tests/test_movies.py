"""Movie‑related functional tests for 🎬 CineEscapeApp.

This module verifies:
- Movie page rendering
- Adding movies
- Updating movies
- Deleting movies

All tests operate on an isolated in‑memory database seeded with users
via the client fixture in conftest.py.
"""

from CineEscapeApp.app import app, db  # Imported for consistency with the rest of the suite.
from CineEscapeApp.models import User, Movie  # User imported in case of future user‑movie assertions.


def test_movies_page_loads(client):
    """Ensure the movies page loads for a valid user.

    Args:
        client (FlaskClient): The test client fixture.

    Asserts:
        - HTTP 200 OK status
        - Correct page title containing the user's name
    """
    response = client.get("/users/1/movies")
    assert response.status_code == 200
    assert b"Movies for Athena" in response.data


def test_add_movie(client):
    """Verify that a movie can be added for a user.

    Args:
        client (FlaskClient): The test client fixture.

    Asserts:
        - HTTP 200 OK after redirect
        - Newly added movie appears in the rendered page
    """
    response = client.post(
        "/users/1/movies/add",
        data={"title": "Inception", "year": "2010"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Inception" in response.data


def test_update_movie(client):
    """Confirm that updating a movie title works correctly.

    Args:
        client (FlaskClient): The test client fixture.

    Steps:
        - Add a movie
        - Update its title

    Asserts:
        - Updated title appears in the response body
    """
    client.post(
        "/users/1/movies/add",
        data={"title": "Matrix"},
        follow_redirects=True,
    )

    response = client.post(
        "/users/1/movies/1/update",
        data={"new_title": "The Matrix"},
        follow_redirects=True,
    )
    assert b"The Matrix" in response.data


def test_delete_movie(client):
    """Verify that deleting a movie removes it from the list.

    Args:
        client (FlaskClient): The test client fixture.

    Asserts:
        - Deleted movie no longer appears in the rendered page
    """
    client.post(
        "/users/1/movies/add",
        data={"title": "Titanic"},
        follow_redirects=True,
    )

    response = client.post(
        "/users/1/movies/1/delete", follow_redirects=True
    )
    assert b"Titanic" not in response.data
