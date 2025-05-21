from flask import (Blueprint, session, g, jsonify, make_response)
import functools
from ..db import SessionLocal
from ..models import User
from .login import login
from .register import register_user

# Create a blueprint instance
auth = Blueprint('auth', __name__, template_folder='templates')


@auth.before_app_request
def load_logged_in_user():
    print("load_logged_in_user")
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        sessionLocal = SessionLocal()
        g.user = sessionLocal.query(User).filter_by(id=user_id).first()


@auth.route('/login', methods=['POST'])
def login_route():
    return login()


@auth.route('/register', methods=['POST'])
def register_route():
    return register_user()


@auth.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({"message": "Log Out successful"}), 200)
    resp.set_cookie('token', '', httponly=True,
                    secure=True, samesite='None', max_age=0)
    return resp


def login_required(view):
    print("login_required")

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
