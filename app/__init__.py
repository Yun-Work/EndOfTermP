# app/__init__.py
from flask import Flask
from flask_cors import CORS
from app.routes.symptom_routes import symptom_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(symptom_bp, url_prefix="/api")
    return app

