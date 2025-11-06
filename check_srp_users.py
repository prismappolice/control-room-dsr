"""
Check SRP VJA and SRP GTL user accounts and their functionality
"""
import sqlite3
from werkzeug.security import check_password_hash

def check_srp_users():
    print("Checking SRP VJA and SRP GTL user accounts...")
    
    # Connect to database
    conn = sqlite3.connect("instance/control_room_dsr.db")
    cursor = conn.cursor()
    
    try:
        # Check if SRP users exist
        cursor.execute("SELECT username, password_hash, user_type, district_name, is_active FROM user WHERE username IN ('srp_vja', 'srp_gtl')")
        srp_users = cursor.fetchall()
        
        print(f"Found {len(srp_users)} SRP users:")
        
        for username, password_hash, user_type, district_name, is_active in srp_users:
            print(f"\nUser: {username}")
            print(f"  Type: {user_type}")
            print(f"  District: {district_name}")
            print(f"  Active: {is_active}")
            print(f"  Has Password Hash: {'Yes' if password_hash else 'No'}")
            
            # Test expected passwords
            expected_passwords = [f'{username}123', 'srp_vja123', 'srp_gtl123']
            
            if password_hash:
                for test_pwd in expected_passwords:
                    if check_password_hash(password_hash, test_pwd):
                        print(f"  ✅ Working Password: '{test_pwd}'")
                        break
                else:
                    print(f"  ❌ None of expected passwords work")
            else:
                print(f"  ❌ No password hash found")
        
        # Check total district users
        cursor.execute("SELECT COUNT(*) FROM user WHERE user_type = 'district'")
        district_count = cursor.fetchone()[0]
        print(f"\nTotal District Users: {district_count}")
        
        # List all district users
        cursor.execute("SELECT username, district_name FROM user WHERE user_type = 'district' ORDER BY username")
        all_districts = cursor.fetchall()
        
        print("\nAll District Users:")
        for username, district_name in all_districts:
            print(f"  {username} → {district_name}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_srp_users()