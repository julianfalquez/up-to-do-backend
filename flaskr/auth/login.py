from flask import (
    request,
    session, jsonify, make_response
)
from werkzeug.security import check_password_hash

from ..db import SessionLocal
from ..models import User
from ..utils.jwt import generate_token


def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    print("username", username)
    print("password", password)
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    sessionLocal = SessionLocal()
    user = sessionLocal.query(User).filter_by(username=username).first()
    error_details = {}
    if not user:
        error_details["username"] = "This username is not registered."
        return jsonify({
            "error": "Login failed",
            "details": error_details
        }), 400
    if not check_password_hash(user.password, password):
        error_details["password"] = "Incorrect password."
        return jsonify({
            "error": "Login failed",
            "details": error_details
        }), 400 

    # Credentials are valid
    session.clear()
    session['user_id'] = user.id
    session['username'] = user.username
    sessionLocal.close()
    token = generate_token(user.username)
    resp = make_response(jsonify({"message": "Login successful", "user": {
                         "id": user.id, "username": user.username}}), 200)

    resp.set_cookie('token', token, httponly=True,
                    secure=True, samesite='None')
    return resp
