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
    
    # Session idle timeout configuration (10 minutes)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['SESSION_PERMANENT'] = False  # Session cookie expires on browser close
    
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
            # Make session non-permanent: expires on browser close
            session.permanent = False

            now = datetime.now()
            last_activity = session.get('last_activity')
            if last_activity:
                last_activity_time = datetime.fromisoformat(last_activity)
                # If idle for more than timeout, logout
                if now - last_activity_time > app.config['PERMANENT_SESSION_LIFETIME']:
                    logout_user()
                    session.clear()
                    return redirect(url_for('main.index'))
            # Update last activity time on every request
            session['last_activity'] = now.isoformat()
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app