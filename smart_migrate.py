"""
Smart migration script - only updates schema, doesn't double-hash passwords
"""
import sqlite3

def smart_migrate():
    print("Starting smart migration...")
    
    # Connect to database
    conn = sqlite3.connect("instance/control_room_dsr.db")
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
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
        
        # Copy existing password hashes to password_hash column
        cursor.execute("UPDATE user SET password_hash = password WHERE password_hash IS NULL")
        cursor.execute("UPDATE user SET last_password_change = CURRENT_TIMESTAMP WHERE last_password_change IS NULL")
        
        print("Updated password_hash column with existing passwords")
        
        conn.commit()
        print("Smart migration completed successfully!")
        
        # Verify the update worked
        cursor.execute("SELECT username, password_hash, user_type FROM user WHERE user_type IN ('admin', 'controlroom') OR username = 'prakasam'")
        users = cursor.fetchall()
        
        print("\nVerification:")
        for username, password_hash, user_type in users:
            hash_preview = password_hash[:30] + "..." if password_hash else "None"
            print(f"User: {username} ({user_type}) - Hash: {hash_preview}")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    smart_migrate()