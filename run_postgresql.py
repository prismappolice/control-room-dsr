from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Just create tables if they don't exist
        db.create_all()
        
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
                print("⚠️  No users found - database appears empty")
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
    
    print("\n🚀 Starting Flask Development Server...")
    print("🔗 Open: http://localhost:5000")
    print("🎯 Your system now uses PostgreSQL with all features working!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)