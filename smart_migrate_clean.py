"""
Smart PostgreSQL Migration Script
Handles PostgreSQL setup, database creation, and data migration automatically
Compatible with PostgreSQL 18 and Python 3.13
"""

import os
import sys
import json
import subprocess
import sqlite3
from pathlib import Path

def smart_migrate():
    """Smart migration script - only updates schema, doesn't double-hash passwords"""
    print("🔄 Starting smart migration...")
    
    # Connect to SQLite database
    conn = sqlite3.connect("instance/control_room_dsr.db")
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📊 Current columns: {columns}")
        
        # Add password_hash column if missing
        if 'password_hash' not in columns:
            print("➕ Adding password_hash column...")
            cursor.execute('ALTER TABLE user ADD COLUMN password_hash VARCHAR(255)')
        else:
            print("✅ password_hash column already exists")
            
        # Add last_password_change column if missing
        if 'last_password_change' not in columns:
            print("➕ Adding last_password_change column...")
            cursor.execute('ALTER TABLE user ADD COLUMN last_password_change DATETIME')
        else:
            print("✅ last_password_change column already exists")
        
        # Copy existing password hashes to password_hash column
        cursor.execute("UPDATE user SET password_hash = password WHERE password_hash IS NULL")
        cursor.execute("UPDATE user SET last_password_change = CURRENT_TIMESTAMP WHERE last_password_change IS NULL")
        
        print("✅ Updated password_hash column with existing passwords")
        
        conn.commit()
        print("🎉 Smart migration completed successfully!")
        
        # Verify the update worked
        cursor.execute("SELECT username, password_hash, user_type FROM user WHERE user_type IN ('admin', 'controlroom') OR username = 'prakasam'")
        users = cursor.fetchall()
        
        print("\n🔍 Verification:")
        for username, password_hash, user_type in users:
            hash_preview = password_hash[:30] + "..." if password_hash else "None"
            print(f"   User: {username} ({user_type}) - Hash: {hash_preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

class SmartMigration:
    """Smart migration handler for PostgreSQL"""
    
    def __init__(self):
        self.pg_version = "18"  # Detected PostgreSQL version
        self.pg_bin_path = f"C:\\Program Files\\PostgreSQL\\{self.pg_version}\\bin"
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'database': 'control_room_dsr',
            'username': 'dsr_user',
            'password': 'dsr_pass123',
            'admin_user': 'postgres',
            'admin_password': None  # Will be prompted
        }
    
    def test_postgresql_connection(self):
        """Test PostgreSQL server connection"""
        print("🔌 Testing PostgreSQL server connection...")
        
        # Get admin password
        if not self.db_config['admin_password']:
            print("📝 Please enter the PostgreSQL 'postgres' user password you set during installation:")
            self.db_config['admin_password'] = input("Password: ").strip()
            
            if not self.db_config['admin_password']:
                print("❌ Password is required")
                return False
        
        try:
            # Test connection using psql
            cmd = [
                f"{self.pg_bin_path}\\psql.exe",
                "-h", self.db_config['host'],
                "-p", self.db_config['port'],
                "-U", self.db_config['admin_user'],
                "-d", "postgres",
                "-c", "SELECT version();"
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config['admin_password']
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ PostgreSQL connection successful!")
                version_line = result.stdout.strip().split('\n')[2]  # Version info is usually on 3rd line
                print(f"📊 {version_line}")
                return True
            else:
                print(f"❌ Connection failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {e}")
            return False
    
    def create_database_and_user(self):
        """Create database and user for DSR system"""
        print("\n🗄️  Creating database and user...")
        
        try:
            # Create user
            create_user_sql = f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{self.db_config['username']}') THEN
                    CREATE USER {self.db_config['username']} WITH PASSWORD '{self.db_config['password']}';
                END IF;
            END
            $$;
            """
            
            cmd = [
                f"{self.pg_bin_path}\\psql.exe",
                "-h", self.db_config['host'],
                "-p", self.db_config['port'],
                "-U", self.db_config['admin_user'],
                "-d", "postgres",
                "-c", create_user_sql
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config['admin_password']
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ User '{self.db_config['username']}' created/verified")
            else:
                print(f"⚠️  User creation: {result.stderr}")
            
            # Create database
            create_db_sql = f"CREATE DATABASE {self.db_config['database']} OWNER {self.db_config['username']};"
            
            cmd = [
                f"{self.pg_bin_path}\\psql.exe",
                "-h", self.db_config['host'],
                "-p", self.db_config['port'],
                "-U", self.db_config['admin_user'],
                "-d", "postgres",
                "-c", create_db_sql
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0 or "already exists" in result.stderr:
                print(f"✅ Database '{self.db_config['database']}' created/verified")
                return True
            else:
                print(f"❌ Database creation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Database setup error: {e}")
            return False
    
    def run_migration(self):
        """Run complete migration process"""
        print("🚀 POSTGRESQL MIGRATION - STARTING")
        print("=" * 45)
        
        # Test PostgreSQL connection
        if not self.test_postgresql_connection():
            print("\n❌ Cannot connect to PostgreSQL. Please check:")
            print("1. PostgreSQL is running")
            print("2. Password is correct") 
            print("3. Server is accessible on localhost:5432")
            return False
        
        # Create database and user
        if not self.create_database_and_user():
            return False
        
        print("\n🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 40)
        print("\n📋 Next Steps:")
        print("1. Set environment variable:")
        print("   $env:DATABASE_TYPE=\"postgresql\"")
        print("2. Use simple_import.py to import data")
        print("3. Start Flask with run_postgresql.py")
        
        return True

def main():
    """Main migration function"""
    print("📊 Smart Migration - SQLite Schema Update + PostgreSQL Setup")
    print("=" * 60)
    
    # First update SQLite schema
    sqlite_success = smart_migrate()
    
    if sqlite_success:
        print("\n✅ SQLite schema updated successfully!")
        
        # Then setup PostgreSQL
        migration = SmartMigration()
        pg_success = migration.run_migration()
        
        if pg_success:
            print("\n🎯 Both SQLite and PostgreSQL are ready!")
            print("📦 Use simple_import.py to transfer data to PostgreSQL")
        else:
            print("\n⚠️  PostgreSQL setup incomplete, but SQLite is updated")
    else:
        print("\n❌ SQLite schema update failed")

if __name__ == '__main__':
    main()