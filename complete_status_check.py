#!/usr/bin/env python3
"""Complete System Status Check"""

import os
import sys
from pathlib import Path

# Force PostgreSQL environment
os.environ['DATABASE_TYPE'] = 'postgresql'

print("🔍 COMPLETE SYSTEM STATUS CHECK")
print("=" * 50)

# 1. Check environment
print("🌐 Environment Status:")
print(f"   DATABASE_TYPE: {os.environ.get('DATABASE_TYPE', 'NOT SET')}")

# 2. Check config
try:
    from config import DatabaseConfig
    print(f"   Config Database Type: {DatabaseConfig.get_database_type()}")
    print(f"   Database URI: {DatabaseConfig.get_database_uri()}")
    print(f"   Using PostgreSQL: {DatabaseConfig.is_postgresql()}")
except Exception as e:
    print(f"   Config Error: {e}")

# 3. Direct PostgreSQL test
print("\n🗄️  Direct PostgreSQL Status:")
try:
    import psycopg2
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='control_room_dsr',
        user='dsr_user',
        password='dsr_pass123'
    )
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM "user"')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM dsr_entry')
    dsr_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM control_room_upload')
    upload_count = cursor.fetchone()[0]
    
    print(f"   ✅ PostgreSQL Connection: SUCCESS")
    print(f"   👥 Users: {user_count}")
    print(f"   📊 DSR Entries: {dsr_count}")
    print(f"   📁 Uploads: {upload_count}")
    
    cursor.execute('SELECT username, user_type FROM "user" WHERE user_type = \'admin\' LIMIT 1')
    admin = cursor.fetchone()
    if admin:
        print(f"   🔑 Admin User: {admin[0]} found")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"   ❌ PostgreSQL Error: {e}")

# 4. Flask integration test  
print("\n🌐 Flask Integration Status:")
try:
    from app import create_app, db
    from app.models import User, DSREntry, ControlRoomUpload
    
    app = create_app()
    with app.app_context():
        print(f"   Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        user_count = User.query.count()
        print(f"   👥 Flask sees {user_count} users")
        
        if user_count > 0:
            admin = User.query.filter_by(username='admin').first()
            print(f"   🔑 Admin via Flask: {admin.username if admin else 'NOT FOUND'}")
            
            dsr_count = DSREntry.query.count()
            upload_count = ControlRoomUpload.query.count()
            
            print(f"   📊 DSR Entries via Flask: {dsr_count}")
            print(f"   📁 Uploads via Flask: {upload_count}")
        
except Exception as e:
    print(f"   ❌ Flask Error: {e}")

# 5. Check SQLite status
print("\n📁 SQLite Database Status:")
sqlite_path = Path(__file__).parent / 'instance' / 'database.db'
if sqlite_path.exists():
    sqlite_size = sqlite_path.stat().st_size
    print(f"   📄 SQLite file exists: {sqlite_size} bytes")
    print(f"   📅 Last modified: {sqlite_path.stat().st_mtime}")
    
    # Check if SQLite has recent data
    try:
        import sqlite3
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM user")
        sqlite_users = cursor.fetchone()[0]
        print(f"   👥 SQLite Users: {sqlite_users}")
        conn.close()
    except Exception as e:
        print(f"   ❌ SQLite read error: {e}")
else:
    print("   ✅ SQLite file doesn't exist")

print("\n🎯 FINAL STATUS:")
if os.environ.get('DATABASE_TYPE') == 'postgresql':
    print("   ✅ System is configured for PostgreSQL")
    print("   🚀 Ready to run with: python start_postgresql_flask.py")
else:
    print("   ⚠️  Environment not set for PostgreSQL")
    print("   🔧 Run: $env:DATABASE_TYPE='postgresql'")

print("\n" + "=" * 50)
print("🎉 Status check complete!")