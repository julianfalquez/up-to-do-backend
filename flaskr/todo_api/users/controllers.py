from flask import jsonify, request
from ...config import SessionLocal
from .models import User
from ...utils.jwt import verify_token
from .utils import generate_and_save_profile_picture, get_user_by_username, format_user_response
from ...utils.s3_utils import generate_presigned_upload_url, validate_file_for_upload

def get_user():
    # Get username from token
    token = request.cookies.get('token')
    username = verify_token(token)
    
    # Get user from the database
    db_session = SessionLocal()
    try:
        # Get user and handle profile picture
        user = get_user_by_username(username, db_session)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Format user data for response
        user_data = format_user_response(user, db_session)
        return jsonify(user_data), 200
    
    except Exception as e:
        return jsonify({"error": f"Error retrieving user data: {str(e)}"}), 500
    finally:
        db_session.close()
    
def get_presigned_url():
    # Get username from token
    token = request.cookies.get('token')
    username = verify_token(token)
    
    data = request.json
    file_name = data.get('fileName')
    file_type = data.get('fileType')
    # Validate file details
    validation_result = validate_file_for_upload(file_name, file_type)
    if isinstance(validation_result, tuple):
        return validation_result
    
    # Generate and return presigned URL
    result = generate_presigned_upload_url(username, file_name, file_type)
    print("Presigned URL generated:", result)
    return jsonify(result)

def update_profile_pic():
    # Get username from token
    print("Updating profile picture!!!!!!!!!!!!!!!")
    token = request.cookies.get('token')
    username = verify_token(token)
    
    data = request.json
    profile_url = data.get('profileUrl')
    if not profile_url:
        return jsonify({"error": "Missing profileUrl"}), 400

    db_session = SessionLocal()
    try:
        user = get_user_by_username(username, db_session)
        print("User found:", user,profile_url)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.profile_picture = profile_url
        db_session.commit()
        result = {"message": "Profile picture updated successfully", "profileUrl": profile_url}
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": f"Error updating profile picture: {str(e)}"}), 500
    finally:
        db_session.close()
    return jsonify(result)

