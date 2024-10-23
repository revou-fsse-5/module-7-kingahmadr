from flask.views import MethodView
from flask import jsonify, request
from src.models.UserRoleModel import User, Role
from src.config.settings import db
# from flasgger import swag_from
from werkzeug.security import generate_password_hash


class RegisterView(MethodView):
    def post(self):
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_name = data.get('role')
        
        # User checking in database
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User already exists!"}), 400

        # Hash the user's password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        
        # Find the role and add to the user
        role = Role.query.filter_by(slug=role_name).first()  # Query role by slug
        if role:
            new_user.roles.append(role)  # Append the actual Role object
        else:
            return jsonify({"error": f"Role '{role_name}' not found!"}), 400

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201



