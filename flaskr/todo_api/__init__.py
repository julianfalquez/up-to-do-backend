from flask import Blueprint
from .users import users_bp

todo_api_bp = Blueprint('todo-api', __name__)

# Register sub-blueprints under /api
todo_api_bp.register_blueprint(users_bp, url_prefix='/users')