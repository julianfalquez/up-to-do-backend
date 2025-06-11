from . import auth_bp

from .controllers import (
    login, register_user, log_out, login_required
)

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()


@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register_user()


@auth_bp.route('/logout', methods=['POST'])
def logout_route():
    return log_out()
