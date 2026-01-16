# Changelog
All notable changes to **CineEscapeApp** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to **Semantic Versioning**.

---

## [0.1.0] - Initial Project Bootstrap
### Added
- **Core Python package structure** under `CineEscapeApp/` including:
  - `__init__.py`
  - `app.py` (Flask application factory, SQLAlchemy initialization)
  - `config.py` (centralized configuration management)
  - `data_manager.py` (OOP data access layer)
  - `models.py` (SQLAlchemy ORM models)
  - `reset_db.py` (deterministic database reset script)

- **Runtime directories**
  - `CineEscapeApp/instance/` for SQLite runtime state (`movies.db`)
  - `CineEscapeApp/logs/` for application logging
  - Root-level `logs/` for rotated log archives

- **Jinja2 templates** for UI rendering:
  - `base.html`, `index.html`, `movies.html`, `macros.html`
  - Error pages: `400.html`, `404.html`, `500.html`

- **Static assets**
  - `static/style.css` for baseline styling

- **Automated testing suite**
  - `tests/conftest.py` for Flask/SQLAlchemy test fixtures
  - `test_movies.py` and `test_users.py` for CRUD and model validation

- **Tooling and environment files**
  - `pytest.ini` for root-level test discovery and import stability
  - `codio.postman_environment.json` and `macOS.postman_environment.json`
  - `create_cineescape.sh` cross‑platform bootstrap script

### Infrastructure
- Added `.gitignore` rules to exclude:
  - `instance/` and `CineEscapeApp/instance/`
  - `logs/` and `CineEscapeApp/logs/`
  - Python caches, venvs, and platform artifacts

### Notes
- This release establishes the deterministic, package‑based foundation for all future CineEscapeApp development.
- Database initialization and ORM behavior are now reproducible across macOS, Linux, and Codio environments.

---

## [Unreleased]
- Additional API endpoints  
- OMDb integration  
- Authentication and session management  
- Docker packaging  
