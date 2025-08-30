import os
from functools import wraps
from flask import request, jsonify
import jwt
from dotenv import load_dotenv

load_dotenv()

class ClerkAuth:
    def __init__(self):
        self.publishable_key = os.getenv('CLERK_PUBLISHABLE_KEY')
        self.secret_key = os.getenv('CLERK_SECRET_KEY')
        
    def verify_token(self, token: str) -> dict:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=['RS256'])
            return decoded
        except jwt.InvalidTokenError:
            return None

    def get_user_from_request(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        return self.verify_token(token)

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        clerk_auth = ClerkAuth()
        user = clerk_auth.get_user_from_request()
        
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
            
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function