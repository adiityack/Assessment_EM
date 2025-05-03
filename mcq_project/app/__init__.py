from flask import Flask
import logging
from .routes.publish_routes import publish_bp
from .routes.review_routes import review_bp

def create_app():
    app = Flask(__name__)

    # Setup Logging
    logging.basicConfig(
        filename='publish.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )

    # Register blueprints
    app.register_blueprint(publish_bp)
    app.register_blueprint(review_bp)

    return app
