from functools import wraps
from flask import request, jsonify
import datetime
import jwt
from flask import current_app as app

def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'sub': username,
        'exp': expiration_time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def generate_refresh_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    payload = {
        'sub': username,
        'exp': expiration_time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_token(token):
    try:
        # Decode the token
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Function to require JWT token in request
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        # Try to get token from the cookies
        if 'token' in request.cookies:
            token = request.cookies['token']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function