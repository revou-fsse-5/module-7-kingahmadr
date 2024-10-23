from flask.views import MethodView
from flask import jsonify, request
from src.config.settings import db
from src.models.Review import Review
# from flasgger import swag_from
from werkzeug.security import generate_password_hash
from src.services.AuthService import Authentication

class ReviewView(MethodView):
    @Authentication.token_required
    @Authentication.auth_role('admin')  # Only admin can access this
    def get(self, current_user, review_id=None):
        review_fields = ['id', 'product', 'rating', 'description']

        if review_id is None:
            reviews = Review.query.filter_by(is_deleted = False).all()
            print(f"Review query result: {reviews}")
            if not reviews:
                return jsonify({"error": "Review not found"}), 404
            
            results = [{field: getattr(review, field) for field in review_fields} for review in reviews]
            return jsonify({"Product List": results}), 200
        else: 
            review = Review.query.filter(Review.id == review_id and Review.is_deleted == False).first()
            
            if not review:
                return jsonify({"error": "Product review not Found"}), 404

            results = {field: getattr(review, field) for field in review_fields}
            return jsonify({"Product Detail": results})

        
    @Authentication.token_required
    @Authentication.auth_role('admin')  # Only admin can access this
    def post(self, current_user):
        # Get data from request body (assumed to be in JSON format)
        data = request.get_json()
        review_fields = ['id', 'product', 'rating', 'description']
        
        required_fields = ['product', 'rating', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": "Invalid data"}), 400
        
        new_review = Review()
        for field in review_fields:
            setattr(new_review, field, data.get(field, None))
        
        db.session.add(new_review)
        db.session.commit()
        db.session.close_all

        review_data = {field: getattr(new_review, field) for field in review_fields}

        # Respond with the created review and 201 status
        return jsonify({
            "message": "Review created", 
            "review": review_data
            }), 201
    
    @Authentication.token_required
    @Authentication.auth_role('admin')  # Only admin can access this
    def put(self, current_user, review_id):
        review = Review.query.filter(Review.id == review_id and Review.is_deleted == False).first()

        if not review:
            return jsonify({"error": "Review not found"}), 404
        
        review_fields = ['id', 'product', 'rating', 'description']
        
        for field in review_fields:
            value = request.json.get(field)
            if value:
                setattr(review, field, value)
        
        db.session.commit()
        review_data = {field: getattr(review, field) for field in review_fields}

        return jsonify({
            "message": "Product review updated succesfully",
            "review": review_data
        })


    
    @Authentication.token_required
    @Authentication.auth_role('admin')  # Only admin can access this
    def delete(self, current_user, review_id):
        review = Review.query.filter(Review.id == review_id, Review.is_deleted == False).first()
        # print(f"query result: {review}") # debugging
        if review:
            review.is_deleted = True
            db.session.commit()
            return jsonify({"message": "Review deleted successfully"}), 200
        
        else:
            return jsonify({"message": "Review not Found"}), 400


