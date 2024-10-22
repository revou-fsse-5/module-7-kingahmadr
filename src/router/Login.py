from flask.views import MethodView
from flask import jsonify, request
from flasgger import swag_from
from src.models.UserRoleModel import User, Role, UserRole
from src.config.settings import db
from src.services.AuthService import Authentication

from werkzeug.security import check_password_hash

class LoginView(MethodView):
    def get(self, user_id=None):
        # fields = ['id', 'email', 'password_hash']

        if user_id is None:
            # users = User.query.all()
            user_details = (
                    db.session.query(User.id, User.email, User.password_hash, Role.slug)
                    .join(UserRole, User.id == UserRole.user_id)
                    .join(Role, UserRole.role_id == Role.id)    
                    .all()
                )
            # results = [{field: getattr(user, field) for field in fields} for user in users]
            results = []
            for row in user_details:
                results.append({
                    "id": row[0],
                    "email": row[1],
                    "password_hash": row[2],
                    "role": row[3]

                })

            return jsonify({"Users": results})
        else:
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            # user_data = {field: getattr(user, field) for field in fields}
            user_detail = (
                db.session.query(User.id, User.email, User.password_hash, Role.slug)
                .join(UserRole, User.id == UserRole.user_id)
                .join(Role, UserRole.role_id == Role.id)
                .filter(User.id == user_id)
                .all()
            )
            results = []
            for row in user_detail:
                results.append({
                    "id": row[0],
                    "email": row[1],
                    "password_hash": row[2],
                    "role": row[3]

                })

            return jsonify(results)
        
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

        role_slugs = (
            db.session.query(Role.slug, User.email)
            .join(UserRole, User.id == UserRole.user_id)
            .join(Role, UserRole.role_id == Role.id)
            .filter(User.email == email)
            .all()
        )
        slug = ", ".join(row.slug for row in role_slugs)
        db.session.close_all
        # token = Authentication.create_jwt_token(user.id, user.role)
        token = Authentication.create_jwt_token(user.id, slug)

        
        return jsonify({
            "message": "Login successful!",
            "token": token  # Send the token to the client
        }), 200