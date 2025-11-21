from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if users already exist
    if User.query.count() > 0:
        print("Database already has users. Skipping initialization.")
        print(f"Current user count: {User.query.count()}")
    else:
        print("Initializing database with users...")
        
        # 1. Create Admin User
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            user_type='admin',
            district_name=None,
            is_active=True
        )
        db.session.add(admin)
        print("✅ Created admin user")
        
        # 2. Create District Users (28 districts)
        districts = [
            ('srikakulam', 'Srikakulam'),
            ('vizianagaram', 'Vizianagaram'),
            ('visakhapatnam', 'Visakhapatnam'),
            ('east_godavari', 'East Godavari'),
            ('west_godavari', 'West Godavari'),
            ('krishna', 'Krishna'),
            ('guntur', 'Guntur'),
            ('prakasam', 'Prakasam'),
            ('nellore', 'Nellore'),
            ('kadapa', 'Kadapa'),
            ('kurnool', 'Kurnool'),
            ('anantapur', 'Anantapur'),
            ('chittoor', 'Chittoor'),
            ('tirupati', 'Tirupati'),
            ('nandyal', 'Nandyal'),
            ('bapatla', 'Bapatla'),
            ('palnadu', 'Palnadu'),
            ('eluru', 'Eluru'),
            ('konaseema', 'Konaseema'),
            ('kakinada', 'Kakinada'),
            ('anakapalli', 'Anakapalli'),
            ('alluri_sitarama_raju', 'Alluri Sitarama Raju'),
            ('parvathipuram_manyam', 'Parvathipuram Manyam'),
            ('annamayya', 'Annamayya'),
            ('sri_sathya_sai', 'Sri Sathya Sai'),
            ('ntr', 'NTR'),
            ('srp_vja', 'SRP VJA'),
            ('srp_gtl', 'SRP GTL')
        ]
        
        for username, district_name in districts:
            user = User(
                username=username,
                password_hash=generate_password_hash(f'{username}123'),
                user_type='district',
                district_name=district_name,
                is_active=True
            )
            db.session.add(user)
        
        print(f"✅ Created {len(districts)} district users")
        
        # 3. Create Control Room User
        controlroom = User(
            username='controlroom',
            password_hash=generate_password_hash('controlroom123'),
            user_type='controlroom',
            district_name='Control Room',
            is_active=True
        )
        db.session.add(controlroom)
        print("✅ Created control room user")
        
        # Commit all users
        db.session.commit()
        
        print("\n" + "="*80)
        print("DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*80)
        print(f"✅ Total users created: {User.query.count()}")
        print(f"   - Admin users: {User.query.filter_by(user_type='admin').count()}")
        print(f"   - District users: {User.query.filter_by(user_type='district').count()}")
        print(f"   - Control Room users: {User.query.filter_by(user_type='controlroom').count()}")
        print("\n📝 DEFAULT LOGIN CREDENTIALS:")
        print("   Admin: admin / admin123")
        print("   District (example): visakhapatnam / visakhapatnam123")
        print("   Control Room: controlroom / controlroom123")
        print("\n⚠️  IMPORTANT: Change passwords after first login!")
        print("="*80)
