# config/settings.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flasgger import Swagger

# Load environment variables
load_dotenv()

# Initialize the database and migration objects (but don't attach them to the app yet)
db = SQLAlchemy()
migrate = Migrate()

def create_app(settings_conf=None):
    """Application factory to create a Flask app instance."""
    app = Flask(__name__)

    # Swagger configuration for securityDefinitions
    swagger_config = {
        "swagger": "2.0",
        "title": "Your API Title",
        "description": "API documentation with JWT authentication",
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        # Include the 'specs' key to resolve KeyError
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",  # URL for accessing the Swagger UI
        # Add a headers key to prevent TypeError
        "headers": []
    }
   
    # Load configuration
    swagger = Swagger(app, config=swagger_config)
    # app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('DBNAME')}"
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    os.environ.setdefault("FLASK_SETTINGS_MODULE", "src.config.prod")
    conf = settings_conf or os.getenv("FLASK_SETTINGS_MODULE")
    app.config.from_object(conf)
    app.config['DEBUG'] = True

    # Initialize the app with extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import view
    # from src.router.Animals import AnimalView
    # from src.router.Employees import EmployeeView
    # from src.router.Login import LoginView
    # from src.router.Register import RegisterView

    # animal_view = AnimalView.as_view('animal_view')
    # app.add_url_rule('/v2/animal', view_func=animal_view, methods=['GET', 'POST'])
    # app.add_url_rule('/v2/animal/<int:animal_id>', view_func=animal_view, methods=['GET','DELETE', 'PUT'])

    # employee_view = EmployeeView.as_view('employee_view')
    # app.add_url_rule('/v2/employee', view_func=employee_view, methods=['GET', 'POST'])
    # app.add_url_rule('/v2/employee/<int:employee_id>', view_func=employee_view, methods=['GET', 'DELETE', 'PUT'])

    # login_view = LoginView.as_view('login_view')
    # app.add_url_rule('/v2/login', view_func=login_view, methods=['POST'])

    # register_view = RegisterView.as_view('register_view')
    # app.add_url_rule('/v2/register', view_func=register_view, methods=['POST'])

    
    @app.route('/')
    def hello_from_api():
        return 'Mad API v2'

    return app