from flask import Blueprint
# Create a blueprint instance
auth_bp = Blueprint('auth', __name__)

from . import routes