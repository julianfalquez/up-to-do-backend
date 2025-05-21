from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models import Base

# Initialize SQLAlchemy
db = SQLAlchemy()

engine = create_engine(os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/flaskr'
), echo=True)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Get the database connection for the current request"""
    if 'db' not in g:
        g.db = db
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request"""
    db_session = g.pop('db', None)

    # No explicit close needed for SQLAlchemy sessions
    # They are automatically returned to the connection pool


def init_app(app):
    """Initialize the database with the given app"""
    db.init_app(app)
    app.teardown_appcontext(close_db)

    # Create a CLI command for initializing the database
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database."""
        Base.metadata.create_all(engine)
        click.echo("Database tables created.")
