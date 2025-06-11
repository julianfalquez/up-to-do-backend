from .todo_api import todo_api_bp


def register_blueprints(app):
    app.register_blueprint(todo_api_bp, url_prefix='/todo-api')
