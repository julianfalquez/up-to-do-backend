import functools
from flask import g, redirect, url_for, jsonify, request, make_response
from ...config import SessionLocal
from ..users.models import User
from ...utils.jwt import (
    generate_token, verify_token, generate_refresh_token
)
from .utils import (
    validate_login_data, get_user_by_username, verify_password, create_login_response,
    extract_registration_data, validate_registration_fields, parse_dob,
    check_existing_user_email, create_new_user
)


def login():
    data = request.get_json()
    valid, result = validate_login_data(data)
    if not valid:
        return result

    username, password = result
    user = get_user_by_username(username)

    verified, error_details = verify_password(user, password)
    if not verified:
        return jsonify({"error": "Login failed", "details": error_details}), 400

    # Generate token and set it as a cookie in the response
    token = generate_token(username)
    refresh_token = generate_refresh_token(username)
    print('Generated token:', token)
    resp = create_login_response(user, generate_token)
    resp.set_cookie('token', token, httponly=True, secure=True, samesite='None')
    resp.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='None')
    return resp


def register_user():
    username, password, email, dob = extract_registration_data()
    print(f"Registration data: username={username}, email={email}, dob={dob}")
    errors = validate_registration_fields(username, password, email, dob)
    if errors:
        return jsonify({"error": "Registration failed", "details": errors}), 400

    existing_errors = check_existing_user_email(username, email)
    if existing_errors:
        return jsonify({"error": "Registration failed", "details": existing_errors}), 400

    dob_date = parse_dob(dob)
    if dob_date is None:
        return jsonify({
            "error": "Registration failed",
            "details": {"dob": "Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY."}
        }), 400

    success, error_message = create_new_user(username, password, dob_date, email)
    if not success:
        return jsonify({
            "error": "Registration failed",
            "details": {"general": error_message}
        }), 500

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    }), 201


def log_out():
    resp = make_response(jsonify({"message": "Log Out successful"}), 200)
    resp.set_cookie('token', '', httponly=True,
                    secure=True, samesite='None', max_age=0)
    return resp


def login_required(view):
    """Decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Check token-based authentication
        token = request.cookies.get('token')
        print('Token from cookies:', token)
        if token:
            username = verify_token(token)
            print('Username from token:', username)
            if username:
                # Token is valid, we consider the user logged in
                db_session = SessionLocal()
                try:
                    user = db_session.query(User).filter_by(username=username).first()
                    if user:
                        g.user = user
                        return view(**kwargs)
                finally:
                    db_session.close()

        # If we get here, authentication failed
        print("Authentication failed, redirecting to login")
        return jsonify({"error": "Authentication required"}), 401

    return wrapped_view