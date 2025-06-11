# Add these functions to your existing s3_utils.py file
from flask import jsonify
from flaskr.config import s3, BUCKET_NAME

def validate_file_for_upload(file_name, file_type):
    """
    Validate file details for upload.
    
    Args:
        file_name (str): Name of the file to upload
        file_type (str): MIME type of the file
        
    Returns:
        tuple or None: Error response tuple if validation fails, None if validation passes
    """
    if not file_name or not file_type:
        return jsonify({"error": "Missing fileName or fileType"}), 400
    
    if not file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return jsonify({"error": "Invalid file type"}), 400
    
    return None

def generate_presigned_upload_url(username, file_name, file_type):
    """
    Generate a presigned URL for file upload.
    
    Args:
        username (str): Username to use as prefix
        file_name (str): Name of the file
        file_type (str): MIME type of the file
        
    Returns:
        dict: Dictionary containing the URL and key
    """
    # Add the username as a prefix to prevent filename collisions
    prefixed_filename = f"profile_pictures/{username}/{file_name}"
    
    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': prefixed_filename, 'ContentType': file_type},
        ExpiresIn=3600
    )
    
    return {'url': presigned_url, 'key': prefixed_filename}