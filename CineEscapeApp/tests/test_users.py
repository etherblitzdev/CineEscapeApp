"""User‑related functional tests for 🎬 CineEscapeApp.

This module verifies:
- Homepage rendering
- User creation
- User deletion
- Correct propagation of user data into templates

All tests run against an isolated in‑memory database provided by the
pytest client fixture in conftest.py.
"""

from CineEscapeApp.app import app, db  # Imported for consistency with test suite structure.
from CineEscapeApp.models import User, Movie  # Movie imported for future extensibility.


def test_homepage_loads(client):
    """Ensure the homepage renders successfully and displays seeded users.

    Args:
        client (FlaskClient): The test client fixture.

    Asserts:
        - HTTP 200 OK status
        - Presence of seeded user names in the response body
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Athena" in response.data
    assert b"Demetri" in response.data


def test_create_user(client):
    """Verify that a new user can be created via POST request.

    Args:
        client (FlaskClient): The test client fixture.

    Asserts:
        - HTTP 200 OK after redirect
        - Newly created user appears in the rendered page
    """
    response = client.post(
        "/create_user",
        data={"name": "Xavier"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Xavier" in response.data


def test_delete_user(client):
    """Confirm that deleting a user removes them from the homepage.

    Args:
        client (FlaskClient): The test client fixture.

    Asserts:
        - HTTP 200 OK after redirect
        - Deleted user no longer appears in the response body
    """
    response = client.post("/users/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Athena" not in response.data
