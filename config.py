"""
Database Configuration Module for Control Room DSR
PostgreSQL Database Configuration
"""

import os
from pathlib import Path

# Try to load environment variables from .env file (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, will use system environment variables
    pass

class DatabaseConfig:
    """
    PostgreSQL Database configuration
    All settings loaded from environment variables
    Default: PostgreSQL (no SQLite support)
    """
    
    # PostgreSQL settings from environment variables
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'control_room_dsr')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'dsr_user')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'dsr_pass123')
    
    @classmethod
    def get_database_uri(cls):
        """
        Returns PostgreSQL database URI
        Format: postgresql://user:password@host:port/database
        """
        return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
    
    @classmethod
    def get_database_type(cls):
        """Returns database type (always postgresql)"""
        return 'postgresql'
    
    @classmethod
    def is_postgresql(cls):
        """Check if using PostgreSQL (always True)"""
        return True

# Configuration settings for Flask app
class Config:
    """
    Flask configuration class
    Maintains all existing settings while adding database flexibility
    """
    
    # Existing Flask settings (unchanged)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database configuration (flexible)
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings (unchanged)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Helper function for configuration info
def print_config_info():
    """Print current database configuration"""
    config = DatabaseConfig()
    print(f"Database Type: {config.get_database_type()}")
    print(f"Database URI (masked): postgresql://{config.POSTGRES_USER}:***@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")
    print(f"Using PostgreSQL: {config.is_postgresql()}")

if __name__ == '__main__':
    print("=== Database Configuration Info ===")
    print_config_info()