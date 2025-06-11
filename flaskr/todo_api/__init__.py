from flask import Blueprint
from .users import users_bp
from .auth import auth_bp

todo_api_bp = Blueprint('todo_api', __name__)

todo_api_bp.register_blueprint(users_bp, url_prefix='/users')
todo_api_bp.register_blueprint(auth_bp, url_prefix='/auth')