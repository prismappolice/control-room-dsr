#!/usr/bin/env python3
"""Fix PostgreSQL table names for Flask compatibility"""

import psycopg2

def fix_postgresql_tables():
    """Rename tables to match Flask SQLAlchemy expectations"""
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='control_room_dsr',
            user='dsr_user',
            password='dsr_pass123'
        )
        
        cursor = conn.cursor()
        
        print("🔧 Fixing PostgreSQL table names for Flask compatibility...")
        
        # Check current tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [t[0] for t in cursor.fetchall()]
        print(f"📋 Current tables: {tables}")
        
        # Drop old singular tables if they exist (empty ones from setup)
        if 'user' in tables:
            cursor.execute("DROP TABLE IF EXISTS \"user\" CASCADE")
            print("🗑️  Dropped old 'user' table")
            
        if 'dsr_entry' in tables:
            cursor.execute("DROP TABLE IF EXISTS dsr_entry CASCADE")
            print("🗑️  Dropped old 'dsr_entry' table")
            
        if 'control_room_upload' in tables:
            cursor.execute("DROP TABLE IF EXISTS control_room_upload CASCADE")
            print("🗑️  Dropped old 'control_room_upload' table")
        
        # Rename plural tables to singular (Flask SQLAlchemy expects singular)
        if 'users' in tables:
            cursor.execute('ALTER TABLE users RENAME TO "user"')
            print("✅ Renamed 'users' to 'user'")
            
        if 'dsr_entries' in tables:
            cursor.execute('ALTER TABLE dsr_entries RENAME TO dsr_entry')
            print("✅ Renamed 'dsr_entries' to 'dsr_entry'")
            
        if 'control_room_uploads' in tables:
            cursor.execute('ALTER TABLE control_room_uploads RENAME TO control_room_upload')
            print("✅ Renamed 'control_room_uploads' to 'control_room_upload'")
        
        # Commit changes
        conn.commit()
        
        # Verify final tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        final_tables = [t[0] for t in cursor.fetchall()]
        print(f"📋 Final tables: {final_tables}")
        
        # Test data count
        cursor.execute('SELECT COUNT(*) FROM "user"')
        user_count = cursor.fetchone()[0]
        print(f"✅ Users in database: {user_count}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL tables fixed for Flask compatibility!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing tables: {e}")
        return False

if __name__ == '__main__':
    fix_postgresql_tables()