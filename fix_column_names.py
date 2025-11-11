#!/usr/bin/env python3
"""Fix PostgreSQL column names to match Flask models"""

import psycopg2

def fix_column_names():
    """Rename PostgreSQL columns to match Flask model expectations"""
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='control_room_dsr',
            user='dsr_user',
            password='dsr_pass123'
        )
        
        cursor = conn.cursor()
        
        print("🔧 Fixing PostgreSQL column names for Flask compatibility...")
        
        # Check current dsr_entry columns
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'dsr_entry' AND table_schema = 'public'
        """)
        current_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Current dsr_entry columns: {current_columns}")
        
        # Rename entry_date to date if needed
        if 'entry_date' in current_columns and 'date' not in current_columns:
            cursor.execute('ALTER TABLE dsr_entry RENAME COLUMN entry_date TO date')
            print("✅ Renamed 'entry_date' to 'date'")
        
        # Rename form_data to data if needed  
        if 'form_data' in current_columns and 'data' not in current_columns:
            cursor.execute('ALTER TABLE dsr_entry RENAME COLUMN form_data TO data')
            print("✅ Renamed 'form_data' to 'data'")
        
        # Check control_room_upload columns
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'control_room_upload' AND table_schema = 'public'
        """)
        upload_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Current control_room_upload columns: {upload_columns}")
        
        # Add missing columns to control_room_upload if needed
        required_upload_columns = ['upload_type', 'original_filename', 'file_path', 'user_id']
        
        for col in required_upload_columns:
            if col not in upload_columns:
                if col == 'upload_type':
                    cursor.execute('ALTER TABLE control_room_upload ADD COLUMN upload_type VARCHAR(50) DEFAULT \'periscope\'')
                elif col == 'original_filename':
                    cursor.execute('ALTER TABLE control_room_upload ADD COLUMN original_filename VARCHAR(255) DEFAULT \'unknown\'')
                elif col == 'file_path':
                    cursor.execute('ALTER TABLE control_room_upload ADD COLUMN file_path VARCHAR(500) DEFAULT \'\'')
                elif col == 'user_id':
                    cursor.execute('ALTER TABLE control_room_upload ADD COLUMN user_id INTEGER DEFAULT 2')  # controlroom user
                print(f"✅ Added missing column: {col}")
        
        # Rename upload_date to date if needed
        if 'upload_date' in upload_columns and 'date' not in upload_columns:
            cursor.execute('ALTER TABLE control_room_upload RENAME COLUMN upload_date TO date')
            print("✅ Renamed 'upload_date' to 'date' in control_room_upload")
        
        # Commit changes
        conn.commit()
        
        # Verify final structure
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'dsr_entry' AND table_schema = 'public'
            ORDER BY column_name
        """)
        final_dsr_columns = [row[0] for row in cursor.fetchall()]
        print(f"\n✅ Final dsr_entry columns: {final_dsr_columns}")
        
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'control_room_upload' AND table_schema = 'public'
            ORDER BY column_name
        """)
        final_upload_columns = [row[0] for row in cursor.fetchall()]
        print(f"✅ Final control_room_upload columns: {final_upload_columns}")
        
        # Test data access
        cursor.execute('SELECT COUNT(*) FROM dsr_entry')
        dsr_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM control_room_upload')
        upload_count = cursor.fetchone()[0]
        
        print(f"\n📊 Data verification:")
        print(f"   DSR Entries: {dsr_count}")
        print(f"   Uploads: {upload_count}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostgreSQL columns fixed for Flask compatibility!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing columns: {e}")
        return False

if __name__ == '__main__':
    fix_column_names()