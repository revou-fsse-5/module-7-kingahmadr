from flask.views import MethodView
from flask import jsonify, make_response
from flasgger import swag_from


class LogoutView(MethodView):
    @swag_from({
        'tags': ['Authentication'],
        'summary': 'User Logount',
        'description': 'Logs out the user by clearing the JWT token cookie.',
        'responses': {
                    200: {
                        'description': 'Logout successful response',
                        'content': {
                            'application/json': {
                                'example': {
                                    'message': 'Logout successful!'
                                }
                            }
                        }
                    }
                }
    })
    def get(self):
        # Create a response object
        response = make_response(jsonify({
            "message": "Logout successful!"
        }), 200)

        # Clear the JWT token cookie by setting it to an empty value
        response.set_cookie('jwt_token', '', max_age=0, expires=0)

        return response
