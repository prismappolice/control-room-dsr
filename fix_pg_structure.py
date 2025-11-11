#!/usr/bin/env python3
"""Fix PostgreSQL table structure to match Flask models"""

import psycopg2

def fix_postgresql_structure():
    """Add missing columns to PostgreSQL tables"""
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='control_room_dsr',
            user='dsr_user',
            password='dsr_pass123'
        )
        
        cursor = conn.cursor()
        
        print("🔧 Fixing PostgreSQL table structure for Flask...")
        
        # Check current user table columns
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'user' AND table_schema = 'public'
        """)
        current_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Current user table columns: {current_columns}")
        
        # Add missing columns to user table
        missing_columns = []
        
        if 'is_active' not in current_columns:
            cursor.execute('ALTER TABLE "user" ADD COLUMN is_active BOOLEAN DEFAULT true')
            missing_columns.append('is_active')
            
        if 'created_at' not in current_columns:
            cursor.execute('ALTER TABLE "user" ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            missing_columns.append('created_at')
            
        if 'last_password_change' not in current_columns:
            cursor.execute('ALTER TABLE "user" ADD COLUMN last_password_change TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            missing_columns.append('last_password_change')
        
        print(f"✅ Added missing columns: {missing_columns}")
        
        # Update password_hash column size if needed
        cursor.execute("""
            SELECT character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'user' AND column_name = 'password_hash'
        """)
        current_length = cursor.fetchone()[0]
        if current_length < 255:
            cursor.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(255)')
            print("✅ Updated password_hash column length")
        
        # Fix DSR entry table if needed
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'dsr_entry' AND table_schema = 'public'
        """)
        dsr_columns = [row[0] for row in cursor.fetchall()]
        
        if 'form_data' not in dsr_columns and 'data' in dsr_columns:
            cursor.execute('ALTER TABLE dsr_entry RENAME COLUMN data TO form_data')
            print("✅ Renamed 'data' to 'form_data' in dsr_entry table")
            
        if 'entry_date' not in dsr_columns and 'date' in dsr_columns:
            cursor.execute('ALTER TABLE dsr_entry RENAME COLUMN date TO entry_date')
            print("✅ Renamed 'date' to 'entry_date' in dsr_entry table")
            
        if 'updated_at' not in dsr_columns:
            cursor.execute('ALTER TABLE dsr_entry ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
            print("✅ Added 'updated_at' column to dsr_entry table")
        
        # Commit changes
        conn.commit()
        
        # Verify final structure
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'user' AND table_schema = 'public'
            ORDER BY column_name
        """)
        final_columns = cursor.fetchall()
        print(f"\n✅ Final user table structure:")
        for col in final_columns:
            length = f"({col[2]})" if col[2] else ""
            nullable = "NULL" if col[3] == "YES" else "NOT NULL"
            print(f"   - {col[0]}: {col[1]}{length} {nullable}")
        
        # Test data access
        cursor.execute('SELECT COUNT(*) FROM "user"')
        user_count = cursor.fetchone()[0]
        print(f"\n📊 Total users: {user_count}")
        
        cursor.execute('SELECT username, user_type, is_active FROM "user" LIMIT 3')
        sample_users = cursor.fetchall()
        print("👤 Sample users:")
        for user in sample_users:
            print(f"   - {user[0]} ({user[1]}) Active: {user[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL structure fixed for Flask compatibility!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing structure: {e}")
        return False

if __name__ == '__main__':
    fix_postgresql_structure()