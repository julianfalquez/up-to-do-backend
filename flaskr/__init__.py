import os
from flask import Flask
from flask import session
from flask import redirect, url_for
# import the actual Blueprint object, not the module
from flaskr.auth.auth import auth
from flaskr.auth.auth import login_required
from flask_cors import CORS
from flaskr.todo_api import todo_api_bp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Update configuration to use PostgreSQL
    app.config.from_mapping(
        SECRET_KEY=os.environ.get(
            'SECRET_KEY',
            'dev'
        ),
        # PostgreSQL connection string
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/flaskr'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    from . import db, models
    db.init_app(app)

    # a simple page that says hello
    CORS(app, origins="http://localhost:3000", supports_credentials=True)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todo_api_bp, url_prefix='/todo-api')

    return app
