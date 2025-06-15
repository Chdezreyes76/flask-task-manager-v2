"""
Inicializa la aplicación Flask y registra los blueprints.
"""

from flask import Flask
from .routes.routes import bp
from .routes.ai_routes import ai_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.register_blueprint(ai_bp)
    return app

