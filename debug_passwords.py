"""
Debug script to check what passwords are in the database after migration
"""
import sqlite3
from werkzeug.security import check_password_hash

def check_passwords():
    # Connect to database
    conn = sqlite3.connect("instance/control_room_dsr.db")
    cursor = conn.cursor()
    
    print("Checking users and their password hashes...")
    cursor.execute("SELECT username, password_hash, user_type FROM user WHERE user_type IN ('admin', 'controlroom') OR username = 'prakasam'")
    users = cursor.fetchall()
    
    test_passwords = {
        'admin': 'admin123',
        'controlroom': 'controlroom123', 
        'prakasam': 'prakasam123'
    }
    
    # Also test with original format passwords since these are already hashed
    original_passwords = {
        'admin': 'admin123',
        'controlroom': 'controlroom123',
        'prakasam': 'prakasam123'
    }
    
    for username, password_hash, user_type in users:
        print(f"\nUser: {username} ({user_type})")
        print(f"Hash: {password_hash}")
        
        if username in test_passwords:
            expected_password = test_passwords[username]
            if password_hash:
                is_valid = check_password_hash(password_hash, expected_password)
                print(f"Testing '{expected_password}': {is_valid}")
            else:
                print("No password hash found!")
        
        # Test some other possibilities
        for test_pwd in ['admin', 'admin123', 'controlroom', 'controlroom123', 'prakasam', 'prakasam123']:
            if password_hash and check_password_hash(password_hash, test_pwd):
                print(f"*** WORKING PASSWORD: '{test_pwd}' ***")
    
    conn.close()

if __name__ == '__main__':
    check_passwords()