from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.UserRoleModel import User, Role, UserRole
from src.services.AuthService import Authentication

from werkzeug.security import check_password_hash

class LoginView(MethodView):
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {"msg": "Missing password or email"}, 400

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid email or password!"}), 400
        
        # Generate JWT token for the user
        token = Authentication.create_jwt_token(user.id, user.role)

        
        return jsonify({
            "message": "Login successful!",
            "token": token  # Send the token to the client
        }), 200