"""
Database Configuration Module
Supports both SQLite (current) and PostgreSQL (future) with environment switching
NO changes to existing functionality - identical behavior guaranteed
"""

import os
from pathlib import Path

class DatabaseConfig:
    """
    Database configuration supporting both SQLite and PostgreSQL
    Uses environment variable to switch between databases
    Default: SQLite (maintains current behavior)
    """
    
    # Base directory for database files
    BASE_DIR = Path(__file__).parent
    INSTANCE_DIR = BASE_DIR / 'instance'
    
    # Ensure instance directory exists
    INSTANCE_DIR.mkdir(exist_ok=True)
    
    # Database configurations
    SQLITE_PATH = INSTANCE_DIR / 'database.db'
    
    # PostgreSQL settings (will be configured during setup)
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'control_room_dsr')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'dsr_user')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'dsr_pass123')
    
    @classmethod
    def get_database_uri(cls):
        """
        Returns appropriate database URI based on environment
        Default: SQLite (maintains current system behavior)
        Set DATABASE_TYPE=postgresql to use PostgreSQL
        """
        db_type = os.environ.get('DATABASE_TYPE', 'sqlite').lower()
        
        if db_type == 'postgresql':
            # PostgreSQL connection string
            return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
        else:
            # SQLite connection string (default - current behavior)
            return f"sqlite:///{cls.SQLITE_PATH}"
    
    @classmethod
    def get_database_type(cls):
        """Returns current database type"""
        return os.environ.get('DATABASE_TYPE', 'sqlite').lower()
    
    @classmethod
    def is_postgresql(cls):
        """Check if using PostgreSQL"""
        return cls.get_database_type() == 'postgresql'
    
    @classmethod
    def is_sqlite(cls):
        """Check if using SQLite"""
        return cls.get_database_type() == 'sqlite'

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

# Helper functions for migration
def print_config_info():
    """Print current database configuration"""
    config = DatabaseConfig()
    print(f"Database Type: {config.get_database_type()}")
    print(f"Database URI: {config.get_database_uri()}")
    print(f"Using PostgreSQL: {config.is_postgresql()}")
    print(f"Using SQLite: {config.is_sqlite()}")

if __name__ == '__main__':
    print("=== Database Configuration Info ===")
    print_config_info()