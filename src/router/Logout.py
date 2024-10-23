from flask.views import MethodView
from flask import jsonify, make_response


class LogoutView(MethodView):
    def get(self):
        # Create a response object
        response = make_response(jsonify({
            "message": "Logout successful!"
        }), 200)

        # Clear the JWT token cookie by setting it to an empty value
        response.set_cookie('jwt_token', '', max_age=0, expires=0)

        return response
