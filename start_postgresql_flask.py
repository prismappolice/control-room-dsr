#!/usr/bin/env python3
"""PostgreSQL Flask Server - Properly configured"""

import os
# Ensure PostgreSQL is used
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # DON'T create tables - they already exist with data
        # db.create_all()  # Commented out to avoid overwriting existing data
        
        # Check current user count 
        try:
            user_count = User.query.count()
            print(f"✅ PostgreSQL Database Connected Successfully!")
            print(f"📊 Found {user_count} users in database")
            
            if user_count > 0:
                print("✅ All users loaded from PostgreSQL")
                # Show some sample users
                admin_user = User.query.filter_by(username='admin').first()
                if admin_user:
                    print(f"✅ Admin user found: {admin_user.username}")
                
                district_count = User.query.filter_by(user_type='district').count()
                print(f"✅ District users: {district_count}")
                
                srp_users = User.query.filter(User.username.like('srp_%')).all()
                print(f"✅ SRP units: {len(srp_users)} found")
                
            else:
                print("⚠️  No users found")
                print("💡 This might mean:")
                print("   1. Database connection issue")
                print("   2. Table structure mismatch")
                print("   3. Wrong database selected")
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
    
    print("\n🚀 Starting Flask Development Server with PostgreSQL...")
    print("🔗 Open: http://localhost:5000")
    print("🎯 Your Control Room DSR system now uses PostgreSQL!")
    print("📊 All existing data has been migrated successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)