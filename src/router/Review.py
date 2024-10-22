from flask.views import MethodView
from flask import jsonify, request
from src.config.settings import db
# from flasgger import swag_from
from werkzeug.security import generate_password_hash
from src.services.AuthService import Authentication

class ReviewView(MethodView):
    def get(self):
        # Example data to return
        reviews = [
            {"id": 1, "product": "Laptop", "rating": 5, "review": "Excellent product!"},
            {"id": 2, "product": "Phone", "rating": 4, "review": "Great value for money."},
            {"id": 3, "product": "Headphones", "rating": 3, "review": "Good sound quality, but uncomfortable."},
        ]
        # Returning the data as a JSON response
        return jsonify(reviews), 200
    
    # method_decorators = [Authentication.token_required, Authentication.auth_role("admin")]
    @Authentication.token_required
    @Authentication.auth_role('admin')  # Only admin can access this
    def post(self, current_user):
        # Get data from request body (assumed to be in JSON format)
        data = request.get_json()
        
        # Validate the received data (this is a simple example)
        if not data or not all(key in data for key in ("product", "rating", "review")):
            return jsonify({"error": "Invalid data"}), 400

        # Example of adding a new review (ID would be generated dynamically)
        new_review = {
            "id": 4,  # Normally, this would be generated by the database
            "product": data["product"],
            "rating": data["rating"],
            "review": data["review"]
        }

        # Respond with the created review and 201 status
        return jsonify({"message": "Review created", "review": new_review}), 201