#!/usr/bin/env python3
"""Direct PostgreSQL Setup using Python"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from pathlib import Path

def setup_postgresql_database():
    """Set up PostgreSQL database for Control Room DSR"""
    
    # Database configuration
    admin_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',  # Default PostgreSQL database
        'user': 'postgres',
        'password': 'postgres123'  # Default password we set during installation
    }
    
    db_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'control_room_dsr',
        'user': 'dsr_user',
        'password': 'dsr_pass123'
    }
    
    print("🚀 Setting up PostgreSQL database for Control Room DSR")
    print("=" * 55)
    
    try:
        # Step 1: Connect to PostgreSQL as admin
        print("📡 Connecting to PostgreSQL...")
        
        # Try different common passwords
        passwords = ['postgres123', 'postgres', 'admin', '123456', '']
        admin_conn = None
        
        for password in passwords:
            try:
                admin_config['password'] = password
                admin_conn = psycopg2.connect(**admin_config)
                admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                print(f"✅ Connected to PostgreSQL with password: {password}")
                break
            except psycopg2.OperationalError:
                continue
        
        if not admin_conn:
            print("❌ Could not connect to PostgreSQL. Please check if:")
            print("   - PostgreSQL service is running")
            print("   - Password is correct (try: postgres, postgres123, admin)")
            return False
        
        cursor = admin_conn.cursor()
        
        # Step 2: Create user if not exists
        print(f"👤 Creating user '{db_config['user']}'...")
        try:
            cursor.execute(f"""
                CREATE USER {db_config['user']} 
                WITH PASSWORD '{db_config['password']}'
            """)
            print(f"✅ User '{db_config['user']}' created")
        except psycopg2.Error as e:
            if "already exists" in str(e):
                print(f"ℹ️  User '{db_config['user']}' already exists")
            else:
                print(f"❌ Error creating user: {e}")
        
        # Step 3: Create database if not exists
        print(f"🗄️  Creating database '{db_config['database']}'...")
        try:
            cursor.execute(f"""
                CREATE DATABASE {db_config['database']} 
                OWNER {db_config['user']}
            """)
            print(f"✅ Database '{db_config['database']}' created")
        except psycopg2.Error as e:
            if "already exists" in str(e):
                print(f"ℹ️  Database '{db_config['database']}' already exists")
            else:
                print(f"❌ Error creating database: {e}")
        
        # Step 4: Grant privileges
        print("🔐 Granting privileges...")
        cursor.execute(f"""
            GRANT ALL PRIVILEGES ON DATABASE {db_config['database']} 
            TO {db_config['user']}
        """)
        print("✅ Privileges granted")
        
        cursor.close()
        admin_conn.close()
        
        # Step 5: Test connection to new database
        print("🔌 Testing connection to DSR database...")
        try:
            test_conn = psycopg2.connect(**db_config)
            test_cursor = test_conn.cursor()
            test_cursor.execute("SELECT version()")
            version = test_cursor.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"📊 PostgreSQL version: {version[:50]}...")
            
            # Step 6: Create tables
            print("📋 Creating tables...")
            
            # Create users table
            test_cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    password_hash VARCHAR(120) NOT NULL,
                    user_type VARCHAR(20) NOT NULL,
                    district_name VARCHAR(100)
                )
            """)
            
            # Create dsr_entries table
            test_cursor.execute("""
                CREATE TABLE IF NOT EXISTS dsr_entries (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    district_name VARCHAR(100) NOT NULL,
                    entry_date DATE NOT NULL,
                    form_type VARCHAR(50) NOT NULL,
                    form_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Create control_room_uploads table
            test_cursor.execute("""
                CREATE TABLE IF NOT EXISTS control_room_uploads (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    upload_date DATE NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            test_conn.commit()
            print("✅ All tables created successfully")
            
            test_cursor.close()
            test_conn.close()
            
            print("\n🎉 PostgreSQL setup completed successfully!")
            print(f"\n📋 Database Details:")
            print(f"   Host: {db_config['host']}")
            print(f"   Port: {db_config['port']}")
            print(f"   Database: {db_config['database']}")
            print(f"   Username: {db_config['user']}")
            print(f"   Password: {db_config['password']}")
            
            # Save environment variables
            print("\n🔧 To use PostgreSQL, run these commands:")
            print('$env:DATABASE_TYPE="postgresql"')
            print('python run_postgresql.py')
            
            return True
            
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ PostgreSQL setup failed: {e}")
        return False

if __name__ == '__main__':
    success = setup_postgresql_database()
    if success:
        print("\n✅ Setup complete! Your PostgreSQL database is ready.")
    else:
        print("\n❌ Setup failed. Please check PostgreSQL installation.")