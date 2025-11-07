"""
SQLite to PostgreSQL Data Migration Script
Exports all existing data from SQLite for PostgreSQL import
Maintains data integrity and relationships
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

class SQLiteExporter:
    """Export data from SQLite database"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to current database location
            self.db_path = Path(__file__).parent / 'instance' / 'control_room_dsr.db'
        else:
            self.db_path = Path(db_path)
        
        self.export_dir = Path(__file__).parent / 'migration_data'
        self.export_dir.mkdir(exist_ok=True)
        
    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
            return True
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return False
    
    def export_table_structure(self):
        """Export table structures"""
        print("📋 Exporting table structures...")
        
        cursor = self.conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        structures = {}
        for table in tables:
            table_name = table['name']
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            structures[table_name] = []
            for col in columns:
                structures[table_name].append({
                    'name': col['name'],
                    'type': col['type'],
                    'notnull': col['notnull'],
                    'default_value': col['dflt_value'],
                    'primary_key': col['pk']
                })
        
        # Save structure
        structure_file = self.export_dir / 'table_structures.json'
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump(structures, f, indent=2, default=str)
        
        print(f"✅ Table structures exported to {structure_file}")
        return structures
    
    def export_users_table(self):
        """Export users table data"""
        print("👥 Exporting users table...")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        
        users_data = []
        for user in users:
            # Handle SQLite Row object
            user_dict = dict(user)
            users_data.append({
                'id': user_dict['id'],
                'username': user_dict['username'],
                'password': user_dict.get('password', ''),
                'password_hash': user_dict.get('password_hash', ''),
                'user_type': user_dict['user_type'],
                'district_name': user_dict.get('district_name', ''),
                'is_active': user_dict.get('is_active', True),
                'created_at': user_dict.get('created_at', ''),
                'last_password_change': user_dict.get('last_password_change', '')
            })
        
        # Save users data
        users_file = self.export_dir / 'users_data.json'
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(users_data)} users exported to {users_file}")
        return users_data
    
    def export_dsr_entries(self):
        """Export DSR entries table data"""
        print("📊 Exporting DSR entries...")
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dsr_entry")
        entries = cursor.fetchall()
        
        entries_data = []
        for entry in entries:
            # Handle SQLite Row object
            entry_dict = dict(entry)
            entries_data.append({
                'id': entry_dict['id'],
                'user_id': entry_dict.get('user_id', ''),
                'district_name': entry_dict.get('district_name', ''),
                'form_type': entry_dict['form_type'],
                'date': entry_dict.get('date', ''),
                'data': entry_dict.get('data', ''),
                'created_at': entry_dict.get('created_at', ''),
                'updated_at': entry_dict.get('updated_at', '')
            })
        
        # Save DSR entries
        entries_file = self.export_dir / 'dsr_entries_data.json'
        with open(entries_file, 'w', encoding='utf-8') as f:
            json.dump(entries_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ {len(entries_data)} DSR entries exported to {entries_file}")
        return entries_data
    
    def export_control_room_uploads(self):
        """Export control room uploads table data"""
        print("📁 Exporting control room uploads...")
        
        cursor = self.conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='control_room_upload';")
        if not cursor.fetchone():
            print("ℹ️  No control_room_upload table found, skipping...")
            return []
        
        cursor.execute("SELECT * FROM control_room_upload")
        uploads = cursor.fetchall()
        
        uploads_data = []
        for upload in uploads:
            # Handle SQLite Row object
            upload_dict = dict(upload)
            uploads_data.append({
                'id': upload_dict['id'],
                'date': upload_dict.get('date', ''),
                'upload_type': upload_dict.get('upload_type', ''),
                'filename': upload_dict.get('filename', ''),
                'original_filename': upload_dict.get('original_filename', ''),
                'file_path': upload_dict.get('file_path', ''),
                'uploaded_at': upload_dict.get('uploaded_at', ''),
                'user_id': upload_dict.get('user_id', '')
            })
        
        # Save uploads data
        uploads_file = self.export_dir / 'uploads_data.json'
        with open(uploads_file, 'w', encoding='utf-8') as f:
            json.dump(uploads_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ {len(uploads_data)} uploads exported to {uploads_file}")
        return uploads_data
    
    def create_export_summary(self, users_count, entries_count, uploads_count):
        """Create export summary report"""
        summary = {
            'export_date': datetime.now().isoformat(),
            'database_path': str(self.db_path),
            'export_directory': str(self.export_dir),
            'tables_exported': {
                'users': users_count,
                'dsr_entries': entries_count,
                'control_room_uploads': uploads_count
            },
            'total_records': users_count + entries_count + uploads_count,
            'export_status': 'completed'
        }
        
        summary_file = self.export_dir / 'export_summary.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Export summary saved to {summary_file}")
        return summary
    
    def full_export(self):
        """Perform complete database export"""
        print("🚀 Starting SQLite database export...")
        print(f"📂 Database: {self.db_path}")
        print(f"📁 Export directory: {self.export_dir}")
        
        if not self.connect():
            return False
        
        try:
            # Export table structures
            self.export_table_structure()
            
            # Export data
            users_data = self.export_users_table()
            entries_data = self.export_dsr_entries()
            uploads_data = self.export_control_room_uploads()
            
            # Create summary
            summary = self.create_export_summary(
                len(users_data), 
                len(entries_data), 
                len(uploads_data)
            )
            
            print("\n🎉 Export completed successfully!")
            print(f"📊 Total records exported: {summary['total_records']}")
            print(f"👥 Users: {len(users_data)}")
            print(f"📊 DSR Entries: {len(entries_data)}")
            print(f"📁 Uploads: {len(uploads_data)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False
        finally:
            self.conn.close()

def main():
    """Main export function"""
    exporter = SQLiteExporter()
    
    # Check if database exists
    if not exporter.db_path.exists():
        print(f"❌ Database not found at {exporter.db_path}")
        print("Looking for alternative locations...")
        
        # Try alternative paths
        alt_paths = [
            Path(__file__).parent / 'control_room_dsr.db',
            Path(__file__).parent / 'instance' / 'database.db',
            Path(__file__).parent / 'database.db'
        ]
        
        for alt_path in alt_paths:
            if alt_path.exists():
                print(f"✅ Found database at {alt_path}")
                exporter.db_path = alt_path
                break
        else:
            print("❌ No database file found!")
            return False
    
    # Perform export
    return exporter.full_export()

if __name__ == '__main__':
    success = main()
    if success:
        print("\n✅ Data export ready for PostgreSQL migration!")
    else:
        print("\n❌ Export failed!")