from flask import jsonify, session, request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from ..users.models import User
from ...config import SessionLocal


def validate_login_data(data):
    if not data:
        return False, jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return False, jsonify({"error": "Username and password are required"}), 400

    return True, (username, password)


def get_user_by_username(username):
    sessionLocal = SessionLocal()
    user = sessionLocal.query(User).filter_by(username=username).first()
    sessionLocal.close()
    return user


def verify_password(user, password):
    if not user:
        return False, {"username": "This username is not registered."}
    if not check_password_hash(user.password, password):
        return False, {"password": "Incorrect password."}
    return True, None


def create_login_response(user, generate_token):
    session.clear()
    session['user_id'] = user.id
    session['username'] = user.username

    token = generate_token(user.username)
    resp = jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "profile_picture": user.profile_picture
        }
    })

    response = make_response(resp, 200)
    response.set_cookie('token', token, httponly=True,
                        secure=True, samesite='None')
    return response


def extract_registration_data():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        dob = data.get('dob')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        dob = request.form.get('dob')
    return username, password, email, dob


def validate_registration_fields(username, password, email, dob):
    errors = {}
    if not username:
        errors["username"] = "Username is required."
    if not password:
        errors["password"] = "Password is required."
    if not email:
        errors["email"] = "Email is required."
    if not dob:
        errors["dob"] = "Date of birth is required."
    return errors


def parse_dob(dob):
    date_format_alt = "%d/%m/%Y"
    try:
        return datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(dob, date_format_alt).date()
        except ValueError:
            return None


def check_existing_user_email(username, email):
    db_session = SessionLocal()
    errors = {}
    if db_session.query(User).filter_by(username=username).first():
        errors["username"] = "This username is already taken."
    if db_session.query(User).filter_by(email=email).first():
        errors["email"] = "This email is already registered."
    db_session.close()
    return errors


def create_new_user(username, password, dob_date, email):
    db_session = SessionLocal()
    try:
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            dob=dob_date,
            email=email,
            profile_picture=f'https://ui-avatars.com/api/?name={username}&background=random'
        )
        db_session.add(new_user)
        db_session.commit()
        return True, None
    except Exception as e:
        db_session.rollback()
        return False, str(e)
    finally:
        db_session.close()
def get_token_from_cookies():
    return request.cookies.get('token')


def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return False, {"error": "Invalid token"}, 401


def validate_auth_token():
    token = get_token_from_cookies()
    if not token:
        return False, jsonify({"error": "Authentication token is missing"}), 401

    valid, payload_or_error, *status = decode_token(token)
    if not valid:
        error_response = jsonify(payload_or_error)
        return False, error_response, status[0] if status else 401

    user_id = payload_or_error.get('user_id')
    if not user_id:
        return False, jsonify({"error": "Invalid token"}), 401

    g.user = user_id
    return True, None, None
