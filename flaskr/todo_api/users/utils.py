from flask_sqlalchemy import SQLAlchemy
from .models import User

def generate_and_save_profile_picture(username, db_session):
    """
    Generate a profile picture URL for the given username and save it to the database.

    Args:
        username (str): The username of the user.
        db_session (SQLAlchemy Session): The database session to use for querying and saving.

    Returns:
        str: The generated profile picture URL.
    """
    # Generate the profile picture URL
    profile_picture = f"https://ui-avatars.com/api/?name={username}&background=random"
    
    # Save the profile picture URL to the user's record in the database
    user = db_session.query(User).filter_by(username=username).first()
    if user:
        user.profile_picture = profile_picture
        db_session.commit()
    print("Profile picture URL:", profile_picture)
    return profile_picture

def get_user_by_username(username, db_session):
    """
    Get a user from the database by username.
    
    Args:
        username (str): Username to search for
        db_session: SQLAlchemy session
        
    Returns:
        User: User object if found, None otherwise
    """
    return db_session.query(User).filter_by(username=username).first()

def format_user_response(user, db_session):
    """
    Format user data for API response.
    
    Args:
        user (User): User object to format
        db_session: SQLAlchemy session
        
    Returns:
        dict: Formatted user data
    """
    profile_picture = user.profile_picture
    if not user.profile_picture:
        profile_picture = generate_and_save_profile_picture(
            user.username, db_session)
        
    # Convert date to string to make it JSON serializable
    dob = user.dob.isoformat() if user.dob else None
        
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "dob": dob,
        "profile_picture": profile_picture
    }