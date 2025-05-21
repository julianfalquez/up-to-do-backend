from flask import Blueprint, jsonify, request, abort
from ..db import SessionLocal
from ..models import User
# You'll need to create this utility function
from ..utils.jwt import verify_token

users_bp = Blueprint('users', __name__)


@users_bp.route('/get-user', methods=['GET'])
def get_user():
    print("get_user")
    token = request.cookies.get('token')
    print("Token", token)
    if not token:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        # Verify the token and get the username
        username = verify_token(token)
        if not username:
            return jsonify({"error": "Invalid token"}), 401

        # Get user from the database
        db_session = SessionLocal()
        try:
            user = db_session.query(User).filter_by(username=username).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

            # Return user information
            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "dob": user.dob,
            }), 200
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 500
