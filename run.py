from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Handle database migration for existing users (if any)
        try:
            # Check if there are users with old password format
            existing_users = User.query.all()
            for user in existing_users:
                # If user doesn't have password_hash but has old-style data, it needs migration
                if not hasattr(user, 'password_hash') or not user.password_hash:
                    print(f"Note: Database migration needed for user {user.username}")
                    print("Please run migrate_passwords.py script if upgrading from older version")
                    break
        except Exception:
            # New installation, no migration needed
            pass
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin', user_type='admin').first()
        if not admin:
            admin_user = User(
                username='admin',
                user_type='admin',
                district_name=None
            )
            admin_user.set_password('admin123')  # Use the new method
            db.session.add(admin_user)
        
        # Create control room user
        controlroom = User.query.filter_by(username='controlroom', user_type='controlroom').first()
        if not controlroom:
            controlroom_user = User(
                username='controlroom',
                user_type='controlroom',
                district_name='Control Room'
            )
            controlroom_user.set_password('controlroom123')  # Use the new method
            db.session.add(controlroom_user)
        
        # Create sample district users
        districts = [
            'Srikakulam', 'Vizianagaram', 'Visakhapatnam', 'East Godavari', 'West Godavari',
            'Krishna', 'Guntur', 'Prakasam', 'Nellore', 'Kadapa', 'Kurnool', 'Anantapur',
            'Chittoor', 'Tirupati', 'Nandyal', 'Bapatla', 'Palnadu', 'Eluru', 'Konaseema',
            'Kakinada', 'Anakapalli', 'Alluri Sitarama Raju', 'Parvathipuram Manyam',
            'Annamayya', 'Sri Sathya Sai', 'NTR', 'SRP VJA', 'SRP GTL'
        ]
        
        for district in districts:
            username = district.lower().replace(' ', '_')
            existing_user = User.query.filter_by(username=username, user_type='district').first()
            if not existing_user:
                district_user = User(
                    username=username,
                    user_type='district',
                    district_name=district
                )
                district_user.set_password(f'{username}123')  # Use the new method
                db.session.add(district_user)
        
        db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)