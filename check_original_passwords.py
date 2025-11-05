"""
Check what the original passwords were in the backup database
"""
import sqlite3

def check_original_passwords():
    # Connect to backup database
    conn = sqlite3.connect("instance/control_room_dsr_backup.db")
    cursor = conn.cursor()
    
    print("Checking original passwords from backup database...")
    
    try:
        cursor.execute("SELECT username, password, user_type FROM user WHERE user_type IN ('admin', 'controlroom') OR username = 'prakasam'")
        users = cursor.fetchall()
        
        for username, password, user_type in users:
            print(f"User: {username} ({user_type}) - Original Password: '{password}'")
            
    except Exception as e:
        print(f"Error: {e}")
    
    conn.close()

if __name__ == '__main__':
    check_original_passwords()