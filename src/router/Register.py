from flask.views import MethodView
from flask import jsonify, request
from src.models.UserRoleModel import User
from config.settings import db
# from flasgger import swag_from
from werkzeug.security import generate_password_hash


class RegisterView(MethodView):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        
        # User checking in database
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User already exists!"}), 400

        # Hash the user's password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201



