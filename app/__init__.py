import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the database instance once and share it across the app.
db = SQLAlchemy()


def create_app(test_config=None):
    """Create and configure the Flask application."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, 'templates'),
        static_folder=os.path.join(project_root, 'app', 'static'),
    )

    # Default configuration.
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override with test settings when provided.
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # Remove the SQLAlchemy session after each request to avoid lingering connections.
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # Import and register the application blueprints.
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Create database tables when the app context is first used.
    with app.app_context():
        db.create_all()

    return app