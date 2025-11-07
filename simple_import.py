import json
import os
import sys
from pathlib import Path

# Set environment to PostgreSQL
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import User

def import_users():
    print("PostgreSQL Data Import Starting...")
    
    migration_dir = Path(__file__).parent / 'migration_data'
    users_file = migration_dir / 'users_data.json'
    
    if not users_file.exists():
        print("No user data found")
        return False
    
    print("Loading user data...")
    
    with open(users_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    imported_count = 0
    
    for user_data in users_data:
        existing_user = User.query.filter_by(username=user_data['username']).first()
        
        if not existing_user:
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
            print(f"Added user: {user_data['username']}")
        else:
            print(f"User {user_data['username']} already exists")
    
    db.session.commit()
    print(f"Import completed! Added {imported_count} users")
    
    return True

def verify_import():
    total_users = User.query.count()
    admin_users = User.query.filter_by(user_type='admin').count()
    district_users = User.query.filter_by(user_type='district').count()
    
    print(f"Total Users: {total_users}")
    print(f"Admin Users: {admin_users}")  
    print(f"District Users: {district_users}")
    
    return total_users > 0

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created")
    
    success = import_users()
    
    if success:
        verify_import()
        print("PostgreSQL database is ready!")
    else:
        print("Import failed")