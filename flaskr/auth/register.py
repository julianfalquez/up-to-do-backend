from flask import (request, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import SessionLocal
from ..models import User
from datetime import datetime


def register_user():
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

    error_details = {}

    if not username:
        error_details["username"] = "Username is required."
    if not password:
        error_details["password"] = "Password is required."
    if not email:
        error_details["email"] = "Email is required."
    if not dob:
        error_details["dob"] = "Date of birth is required."

    if error_details:
        return jsonify({
            "error": "Registration failed",
            "details": error_details
        }), 400

    db_session = SessionLocal()
    date_format_alt = "%d/%m/%Y"

    try:
        existing_user = db_session.query(
            User).filter_by(username=username).first()
        if existing_user:
            error_details["username"] = "This username is already taken."

        existing_email = db_session.query(User).filter_by(email=email).first()
        if existing_email:
            error_details["email"] = "This email is already registered."

        if error_details:
            return jsonify({
                "error": "Registration failed",
                "details": error_details
            }), 400

        try:
            date_object = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            try:
                date_object = datetime.strptime(dob, date_format_alt).date()
            except ValueError:
                error_details["dob"] = "Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY."
                return jsonify({
                    "error": "Registration failed",
                    "details": error_details
                }), 400

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            dob=date_object,
            email=email
        )

        db_session.add(new_user)
        db_session.commit()

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        }), 201

    except Exception as e:
        db_session.rollback()
        print(f"Registration error: {e}")
        return jsonify({
            "error": "Registration failed",
            "details": {"general": str(e)}
        }), 500
    finally:
        db_session.close()
