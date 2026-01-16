"""Configuration settings for 🎬 CineEscapeApp."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:# pylint: disable=R0903
    """Flask configuration settings for 🎬 CineEscapeApp."""
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance/movies.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "change-this-in-production"
