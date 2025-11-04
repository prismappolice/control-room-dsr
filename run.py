from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin', user_type='admin').first()
        if not admin:
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),
                user_type='admin',
                district_name=None
            )
            db.session.add(admin_user)
        
        # Create control room user
        controlroom = User.query.filter_by(username='controlroom', user_type='controlroom').first()
        if not controlroom:
            controlroom_user = User(
                username='controlroom',
                password=generate_password_hash('controlroom123'),
                user_type='controlroom',
                district_name='Control Room'
            )
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
                    password=generate_password_hash(f'{username}123'),
                    user_type='district',
                    district_name=district
                )
                db.session.add(district_user)
        
        db.session.commit()
        print("Database initialized with sample users!")
        print("Admin credentials: admin / admin123")
        print("Control Room credentials: controlroom / controlroom123")
        print("District users: {district_name} / {district_name}123")
    
    app.run(debug=True, host='0.0.0.0', port=5000)