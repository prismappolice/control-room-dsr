#!/usr/bin/env python3
"""Simple Direct PostgreSQL Data Import"""

import json
import psycopg2
from pathlib import Path

def import_data_to_postgresql():
    """Import SQLite data directly to PostgreSQL"""
    
    print("🚀 Importing SQLite data to PostgreSQL...")
    
    # PostgreSQL connection config
    pg_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'control_room_dsr',
        'user': 'dsr_user',
        'password': 'dsr_pass123'
    }
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL")
        
        # Clear existing data (in case of re-import)
        print("🧹 Clearing existing data...")
        cursor.execute("DELETE FROM control_room_uploads")
        cursor.execute("DELETE FROM dsr_entries") 
        cursor.execute("DELETE FROM users")
        
        # Load exported data
        migration_dir = Path(__file__).parent / 'migration_data'
        
        # Import users
        print("👥 Importing users...")
        with open(migration_dir / 'users_data.json', 'r') as f:
            users = json.load(f)
        
        for user in users:
            cursor.execute("""
                INSERT INTO users (id, username, password_hash, user_type, district_name)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user['id'],
                user['username'],
                user['password_hash'],
                user['user_type'],
                user['district_name']
            ))
        
        print(f"✅ Imported {len(users)} users")
        
        # Import DSR entries
        print("📊 Importing DSR entries...")
        with open(migration_dir / 'dsr_entries_data.json', 'r') as f:
            entries = json.load(f)
        
        for entry in entries:
            cursor.execute("""
                INSERT INTO dsr_entries (id, user_id, district_name, entry_date, 
                                       form_type, form_data, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                entry['id'],
                entry['user_id'], 
                entry['district_name'],
                entry['date'],  # Fixed: use 'date' field from JSON
                entry['form_type'],
                entry['data'],  # Fixed: use 'data' field from JSON
                entry['created_at']
            ))
        
        print(f"✅ Imported {len(entries)} DSR entries")
        
        # Import uploads
        print("📁 Importing uploads...")
        with open(migration_dir / 'uploads_data.json', 'r') as f:
            uploads = json.load(f)
        
        for upload in uploads:
            cursor.execute("""
                INSERT INTO control_room_uploads (id, filename, upload_date, uploaded_at)
                VALUES (%s, %s, %s, %s)
            """, (
                upload['id'],
                upload['filename'],
                upload['date'],  # Fixed: use 'date' field from JSON
                upload['uploaded_at']
            ))
        
        print(f"✅ Imported {len(uploads)} uploads")
        
        # Commit and verify
        conn.commit()
        
        # Verify data
        print("\n🔍 Verifying imported data...")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM dsr_entries")
        entry_count = cursor.fetchone()[0] 
        
        cursor.execute("SELECT COUNT(*) FROM control_room_uploads")
        upload_count = cursor.fetchone()[0]
        
        print(f"✅ PostgreSQL Database verified:")
        print(f"   👥 Users: {user_count}")
        print(f"   📊 DSR Entries: {entry_count}")
        print(f"   📁 Uploads: {upload_count}")
        
        # Show sample users
        cursor.execute("SELECT username, user_type, district_name FROM users LIMIT 5")
        sample_users = cursor.fetchall()
        print(f"\n👤 Sample users:")
        for user in sample_users:
            print(f"   - {user[0]} ({user[1]}) - {user[2] or 'Admin'}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Data import successful!")
        print("✅ All SQLite data has been migrated to PostgreSQL")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Migration data file not found: {e}")
        print("💡 Run export_sqlite_data.py first to create migration files")
        return False
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == '__main__':
    print("🗄️  Direct PostgreSQL Import")
    print("=" * 30)
    
    success = import_data_to_postgresql()
    if success:
        print("\n📋 Next steps to switch to PostgreSQL:")
        print('1. Set environment: $env:DATABASE_TYPE="postgresql"')
        print('2. Run: python run_postgresql.py')
        print('3. Your app now uses PostgreSQL with all your data!')
    else:
        print("\n❌ Import failed. Please check errors above.")