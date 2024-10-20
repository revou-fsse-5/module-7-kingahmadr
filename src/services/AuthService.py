import os
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import jsonify, request
from src.models.UserRoleModel import User
from src.config.settings import db

class Authentication:
    @staticmethod
    def create_jwt_token(user_id,user_role):
        JWT_SECRET = os.getenv('JWT_SECRET')
        payload = {
            'user_id': user_id,
            'user_role': user_role,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        # print(f"Generated Token: {token}")  # Debugging
        return token
    
    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            JWT_SECRET = os.getenv('JWT_SECRET')
            token = None
            # Check if token is passed in the Authorization header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                print(f"Authorization header: {auth_header}")  # Debugging

                # Ensure the header starts with 'Bearer' and has two parts
                parts = auth_header.split(" ")
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]
                else:
                    return jsonify({"error": "Invalid Authorization header format"}), 403

            if not token:
                return jsonify({"error": "Token is missing!"}), 403

            try:
                # Decode the token to get the user ID
                data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                print(f"Decoded token data: {data}")  # Debugging the decoded token

                # current_user = User.query.get(data['user_id'])
                current_user = db.session.get(User, data['user_id'])
                if not current_user:
                    raise ValueError("User not found")
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired!"}), 403
            except jwt.InvalidTokenError as e:
                print(f"Token error: {str(e)}")  # Print the specific error message
                return jsonify({"error": "Invalid token!"}), 403

            return f(current_user, *args, **kwargs)

        return decorated

    @staticmethod
    def auth_role(role):
        @wraps(role)
        def decorated(*args, **kwargs):
            JWT_SECRET = os.getenv('JWT_SECRET')
            token = None
            try:
                # Decode the token to get the user ID
                data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                print(f"Decoded token data: {data}")  # Debugging the decoded token

                # current_user = User.query.get(data['user_id'])
                current_user = db.session.get(User, data['user_role'])
                if not current_user:
                    raise ValueError("User not found")
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired!"}), 403
            except jwt.InvalidTokenError as e:
                print(f"Token error: {str(e)}")  # Print the specific error message
                return jsonify({"error": "Invalid token!"}), 403

            return role(current_user, *args, **kwargs)
        
        return decorated
