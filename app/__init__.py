"""
Inicializa la aplicación Flask y registra los blueprints.
"""

from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

