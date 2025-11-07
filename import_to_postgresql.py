"""
PostgreSQL Data Import Script
Imports all data from SQLite export to PostgreSQL
Run after PostgreSQL is installed and configured
"""

import json
import sys
from pathlib import Path

def check_prerequisites():
    """Check if everything is ready for import"""
    print("🔍 Checking prerequisites...")
    
    # Check if psycopg2 is available
    try:
        import psycopg2
        print("✅ psycopg2 available")
    except ImportError:
        print("❌ psycopg2 not available")
        print("💡 Install PostgreSQL first, then run:")
        print("   pip install psycopg2-binary")
        return False
    
    # Check if migration data exists
    migration_dir = Path(__file__).parent / 'migration_data'
    if not migration_dir.exists():
        print("❌ Migration data not found")
        print("💡 Run export_sqlite_data.py first")
        return False
    
    required_files = [
        'users_data.json',
        'dsr_entries_data.json',
        'uploads_data.json',
        'table_structures.json'
    ]
    
    for file in required_files:
        if not (migration_dir / file).exists():
            print(f"❌ Missing file: {file}")
            return False
        else:
            print(f"✅ Found: {file}")
    
    return True

def import_data_to_postgresql():
    """Import all data to PostgreSQL"""
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Cannot proceed with import.")
        return False
    
    print("\n🚀 Starting PostgreSQL data import...")
    
    try:
        import psycopg2
        from config import DatabaseConfig
        
        # Connect to PostgreSQL
        db_uri = DatabaseConfig.get_database_uri()
        print(f"📡 Connecting to: {db_uri}")
        
        # Parse connection string for psycopg2
        # Format: postgresql://user:password@host:port/database
        uri_parts = db_uri.replace('postgresql://', '').split('@')
        user_pass = uri_parts[0].split(':')
        host_port_db = uri_parts[1].split('/')
        host_port = host_port_db[0].split(':')
        
        conn = psycopg2.connect(
            host=host_port[0],
            port=host_port[1] if len(host_port) > 1 else '5432',
            database=host_port_db[1],
            user=user_pass[0],
            password=user_pass[1]
        )
        
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL")
        
        # Load migration data
        migration_dir = Path(__file__).parent / 'migration_data'
        
        # Import users
        print("\n👥 Importing users...")
        with open(migration_dir / 'users_data.json', 'r') as f:
            users = json.load(f)
        
        for user in users:
            cursor.execute("""
                INSERT INTO "user" (username, password, password_hash, user_type, 
                                  district_name, is_active, created_at, last_password_change)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO NOTHING
            """, (
                user['username'], user['password'], user['password_hash'],
                user['user_type'], user['district_name'], user['is_active'],
                user['created_at'], user['last_password_change']
            ))
        
        print(f"✅ Imported {len(users)} users")
        
        # Import DSR entries
        print("\n📊 Importing DSR entries...")
        with open(migration_dir / 'dsr_entries_data.json', 'r') as f:
            entries = json.load(f)
        
        for entry in entries:
            cursor.execute("""
                INSERT INTO dsr_entry (district_name, form_type, date, data, 
                                     created_at, updated_at, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                entry['district_name'], entry['form_type'], entry['date'],
                entry['data'], entry['created_at'], entry['updated_at'],
                entry['user_id']
            ))
        
        print(f"✅ Imported {len(entries)} DSR entries")
        
        # Import uploads
        print("\n📁 Importing uploads...")
        with open(migration_dir / 'uploads_data.json', 'r') as f:
            uploads = json.load(f)
        
        for upload in uploads:
            cursor.execute("""
                INSERT INTO control_room_upload (date, upload_type, filename,
                                               original_filename, file_path,
                                               uploaded_at, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                upload['date'], upload['upload_type'], upload['filename'],
                upload['original_filename'], upload['file_path'],
                upload['uploaded_at'], upload['user_id']
            ))
        
        print(f"✅ Imported {len(uploads)} uploads")
        
        # Commit all changes
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 Data import completed successfully!")
        print("📊 Summary:")
        print(f"   👥 Users: {len(users)}")
        print(f"   📊 DSR Entries: {len(entries)}")
        print(f"   📁 Uploads: {len(uploads)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Ensure PostgreSQL is running")
        print("2. Check database connection settings")
        print("3. Verify database and tables exist")
        return False

def test_imported_data():
    """Test that data was imported correctly"""
    print("\n🧪 Testing imported data...")
    
    try:
        import psycopg2
        from config import DatabaseConfig
        
        # Connect and test
        db_uri = DatabaseConfig.get_database_uri()
        uri_parts = db_uri.replace('postgresql://', '').split('@')
        user_pass = uri_parts[0].split(':')
        host_port_db = uri_parts[1].split('/')
        host_port = host_port_db[0].split(':')
        
        conn = psycopg2.connect(
            host=host_port[0],
            port=host_port[1] if len(host_port) > 1 else '5432',
            database=host_port_db[1],
            user=user_pass[0],
            password=user_pass[1]
        )
        
        cursor = conn.cursor()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM \"user\"")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM dsr_entry")
        entry_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM control_room_upload")
        upload_count = cursor.fetchone()[0]
        
        print(f"✅ PostgreSQL Database:")
        print(f"   👥 Users: {user_count}")
        print(f"   📊 DSR Entries: {entry_count}")
        print(f"   📁 Uploads: {upload_count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main import function"""
    print("🗄️  PostgreSQL Data Import Tool")
    print("=" * 35)
    
    success = import_data_to_postgresql()
    
    if success:
        test_imported_data()
        print("\n🎯 MIGRATION COMPLETE!")
        print("\n📋 Next steps:")
        print("1. Set environment variable: $env:DATABASE_TYPE=\"postgresql\"")
        print("2. Restart your Flask application")
        print("3. Test all functionality")
        print("4. Your app now uses PostgreSQL!")
    else:
        print("\n❌ Import failed. Check errors above.")

if __name__ == '__main__':
    main()