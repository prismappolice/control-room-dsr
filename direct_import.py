"""
Direct Import from SQLite to PostgreSQL
Uses the exported data we already have
"""

import json
import os
from pathlib import Path

# Set environment to PostgreSQL
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import User

def import_users():
    """Import users from exported JSON data"""
    
    migration_dir = Path(__file__).parent / 'migration_data'
    users_file = migration_dir / 'users_data.json'
    
    if not users_file.exists():
        print("❌ No user data found. Please run export_sqlite_data.py first")
        return False
    
    print("📦 Importing users from SQLite export...")
    
    with open(users_file, 'r') as f:
        users_data = json.load(f)
    
    imported_count = 0
    
    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        
        if not existing_user:
            # Create new user
            new_user = User(
                username=user_data['username'],
                password=user_data.get('password', ''),
                password_hash=user_data.get('password_hash', ''),
                user_type=user_data['user_type'],
                district_name=user_data.get('district_name', ''),
                is_active=user_data.get('is_active', True)
            )
            
            db.session.add(new_user)
            imported_count += 1
            print(f"✅ Added user: {user_data['username']} ({user_data['user_type']})")
        else:
            print(f"ℹ️  User {user_data['username']} already exists")
    
    db.session.commit()
    print(f"\n🎉 Import completed! Added {imported_count} users")
    
    return True

def verify_import():
    """Verify that users were imported correctly"""
    print("\n🔍 Verifying import...")
    
    total_users = User.query.count()
    admin_users = User.query.filter_by(user_type='admin').count()
    district_users = User.query.filter_by(user_type='district').count()
    controlroom_users = User.query.filter_by(user_type='controlroom').count()
    
    print(f"📊 Total Users: {total_users}")
    print(f"👑 Admin Users: {admin_users}")
    print(f"🏛️  District Users: {district_users}")
    print(f"🏢 Control Room Users: {controlroom_users}")
    
    # Check SRP units
    srp_users = User.query.filter(User.username.like('srp_%')).all()
    if srp_users:
        print(f"🚔 SRP Units: {len(srp_users)}")
        for srp in srp_users:
            print(f"   - {srp.username} ({srp.district_name})")
    
    return total_users > 0

def main():
    """Main import function"""
    
    print("🚀 PostgreSQL Data Import")
    print("=" * 30)
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✅ Tables created/verified")
        
        # Import users
        success = import_users()
        
        if success:
            # Verify import
            verify_import()
            print("\n✅ All data imported successfully!")
            print("🎯 Your PostgreSQL database is ready!")
        else:
            print("\n❌ Import failed")

if __name__ == '__main__':
    main()
