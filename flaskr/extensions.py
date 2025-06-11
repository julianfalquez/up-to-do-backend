# extensions.py
from flask_cors import CORS

def init_cors(app):
    CORS(app, origins="http://localhost:3000", supports_credentials=True)