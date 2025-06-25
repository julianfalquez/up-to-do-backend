from flask_sqlalchemy import SQLAlchemy
from flask import g, current_app
import click
from sqlalchemy.orm import scoped_session
import os
from .config import engine, SessionLocal
from .models import Base

# Initialize SQLAlchemy
db = SQLAlchemy()


def get_db():
    """Get the database connection for the current request"""
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request"""
    db_session = g.pop('db', None)
    if db_session is not None:
        db_session.close()


def init_app(app):
    """Initialize the database with the given app"""
    print('hola')

    db.init_app(app)
    app.teardown_appcontext(close_db)

    # with app.app_context():
    #     from .todo_api.users.models import User
    #     # Import other models here if needed
    #     Base.metadata.create_all(engine)
    #     print("Database tables created.")