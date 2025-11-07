from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py (supports both SQLite and PostgreSQL)
    app.config.from_object(Config)
    
    # Backwards compatibility: if no DATABASE_TYPE set, use SQLite (current behavior)
    if 'SQLALCHEMY_DATABASE_URI' not in app.config or not app.config['SQLALCHEMY_DATABASE_URI']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///control_room_dsr.db'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import main_bp, auth_bp, admin_bp, district_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(district_bp, url_prefix='/district')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app