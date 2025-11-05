"""
Database migration script to handle transition from plain password to hashed passwords
Run this script once to migrate existing users to the new password hashing system
"""

from app import create_app, db
from werkzeug.security import generate_password_hash
from sqlalchemy import text
import sqlite3

def migrate_passwords():
    app = create_app()
    
    with app.app_context():
        print("Starting password migration...")
        
        # Connect to database directly
        db_path = "instance/control_room_dsr.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check if password_hash column exists
            cursor.execute("PRAGMA table_info(user)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'password_hash' not in columns:
                print("Adding password_hash column...")
                cursor.execute('ALTER TABLE user ADD COLUMN password_hash VARCHAR(255)')
            else:
                print("password_hash column already exists")
                
            if 'last_password_change' not in columns:
                print("Adding last_password_change column...")
                cursor.execute('ALTER TABLE user ADD COLUMN last_password_change DATETIME')
            else:
                print("last_password_change column already exists")
            
            # Get existing users
            cursor.execute("SELECT id, username, password, user_type, district_name FROM user")
            users = cursor.fetchall()
            
            if not users:
                print("No existing users found")
                conn.close()
                return
                
            # Migrate each user
            for user_id, username, old_password, user_type, district_name in users:
                if old_password:  # If there's an old password
                    # Generate hash for the old password
                    password_hash = generate_password_hash(old_password)
                    
                    # Update the user record
                    cursor.execute(
                        'UPDATE user SET password_hash = ?, last_password_change = CURRENT_TIMESTAMP WHERE id = ?',
                        (password_hash, user_id)
                    )
                    
                    print(f"Migrated user: {username} ({user_type})")
            
            # Commit all changes
            conn.commit()
            print("Password migration completed successfully!")
            
            # Try to remove old password column (optional)
            try:
                # SQLite doesn't support DROP COLUMN easily, so we'll recreate the table
                print("Recreating user table without password column...")
                
                cursor.execute("""
                CREATE TABLE user_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(80) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    user_type VARCHAR(20) NOT NULL,
                    district_name VARCHAR(100),
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_password_change DATETIME
                )
                """)
                
                cursor.execute("""
                INSERT INTO user_new (id, username, password_hash, user_type, district_name, is_active, created_at, last_password_change)
                SELECT id, username, password_hash, user_type, district_name, is_active, created_at, last_password_change FROM user
                """)
                
                cursor.execute("DROP TABLE user")
                cursor.execute("ALTER TABLE user_new RENAME TO user")
                
                conn.commit()
                print("Successfully removed old password column")
                
            except Exception as e:
                print(f"Could not remove old column (this is okay): {e}")
                conn.rollback()
            
        except Exception as e:
            print(f"Error during migration: {e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == '__main__':
    migrate_passwords()