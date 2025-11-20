from flask import Flask, session, request, g, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
import os
from datetime import datetime, timedelta
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
    
    # Session timeout configuration (1 hour = 3600 seconds)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['SESSION_PERMANENT'] = True
    
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
    
    # Session timeout handler
    @app.before_request
    def check_session_timeout():
        # Skip timeout check for static files and login/logout routes
        if (request.endpoint and 
            (request.endpoint.startswith('static') or 
             request.endpoint in ['auth.login', 'auth.logout', 'main.index'])):
            return
        
        # Check if user is authenticated
        if current_user.is_authenticated:
            # Make session permanent to use PERMANENT_SESSION_LIFETIME
            session.permanent = True
            
            # Update last activity time
            session['last_activity'] = datetime.now().isoformat()
            
            # Check if session has expired (additional check)
            if 'login_time' in session:
                login_time = datetime.fromisoformat(session['login_time'])
                if datetime.now() - login_time > app.config['PERMANENT_SESSION_LIFETIME']:
                    logout_user()
                    session.clear()
                    return redirect(url_for('main.index'))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app