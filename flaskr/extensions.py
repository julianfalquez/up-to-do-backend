# extensions.py
from flask_cors import CORS

def init_cors(app):
    CORS(app, 
         origins=["http://localhost:3000"], 
         supports_credentials=True,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'])