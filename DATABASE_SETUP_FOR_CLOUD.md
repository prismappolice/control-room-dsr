# DATABASE SETUP FOR CLOUD DEPLOYMENT

## Current Database Structure - Control Room DSR Management System

### Database Information
- **Database Type:** SQLite (local) / PostgreSQL (recommended for cloud)
- **Database Name:** `dsr_management.db` (SQLite) or configure in cloud
- **Total Tables:** 3 main tables

---

## TABLE 1: USER TABLE

### Table Structure:
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL,
    district_name VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_password_change DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### User Types:
1. **admin** - Administrator access
2. **district** - District-level users (28 districts)
3. **controlroom** - Control Room user for file uploads

---

## INITIAL USERS TO CREATE (30 Total)

### 1. Admin User (1 user)
```python
Username: admin
Password: admin123  # Change after deployment
User Type: admin
District Name: NULL
```

### 2. District Users (28 users)
All district usernames are lowercase with underscores:

```python
# District Users - Format: username | password | user_type | district_name
srikakulam | srikakulam123 | district | Srikakulam
vizianagaram | vizianagaram123 | district | Vizianagaram
visakhapatnam | visakhapatnam123 | district | Visakhapatnam
east_godavari | east_godavari123 | district | East Godavari
west_godavari | west_godavari123 | district | West Godavari
krishna | krishna123 | district | Krishna
guntur | guntur123 | district | Guntur
prakasam | prakasam123 | district | Prakasam
nellore | nellore123 | district | Nellore
kadapa | kadapa123 | district | Kadapa
kurnool | kurnool123 | district | Kurnool
anantapur | anantapur123 | district | Anantapur
chittoor | chittoor123 | district | Chittoor
tirupati | tirupati123 | district | Tirupati
nandyal | nandyal123 | district | Nandyal
bapatla | bapatla123 | district | Bapatla
palnadu | palnadu123 | district | Palnadu
eluru | eluru123 | district | Eluru
konaseema | konaseema123 | district | Konaseema
kakinada | kakinada123 | district | Kakinada
anakapalli | anakapalli123 | district | Anakapalli
alluri_sitarama_raju | alluri_sitarama_raju123 | district | Alluri Sitarama Raju
parvathipuram_manyam | parvathipuram_manyam123 | district | Parvathipuram Manyam
annamayya | annamayya123 | district | Annamayya
sri_sathya_sai | sri_sathya_sai123 | district | Sri Sathya Sai
ntr | ntr123 | district | NTR
srp_vja | srp_vja123 | district | SRP VJA
srp_gtl | srp_gtl123 | district | SRP GTL
```

### 3. Control Room User (1 user)
```python
Username: controlroom
Password: controlroom123  # Change after deployment
User Type: controlroom
District Name: Control Room
```

---

## TABLE 2: DSR_ENTRY TABLE

### Table Structure:
```sql
CREATE TABLE dsr_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district_name VARCHAR(100) NOT NULL,
    form_type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    data TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Initial Data:
- Start with **EMPTY table**
- Users will create entries after login

---

## TABLE 3: CONTROL_ROOM_UPLOAD TABLE

### Table Structure:
```sql
CREATE TABLE control_room_upload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    upload_type VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Upload Types:
- `periscope`
- `vip_engagements`
- `ps_rtm`

### Initial Data:
- Start with **EMPTY table**
- Control room user will upload files

---

## PYTHON SCRIPT TO INITIALIZE DATABASE

### Create file: `initialize_database.py`

```python
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
        
        # 3. Create Control Room User
        controlroom = User(
            username='controlroom',
            password_hash=generate_password_hash('controlroom123'),
            user_type='controlroom',
            district_name='Control Room',
            is_active=True
        )
        db.session.add(controlroom)
        
        # Commit all users
        db.session.commit()
        
        print(f"✅ Database initialized successfully!")
        print(f"✅ Total users created: {User.query.count()}")
        print(f"   - Admin users: {User.query.filter_by(user_type='admin').count()}")
        print(f"   - District users: {User.query.filter_by(user_type='district').count()}")
        print(f"   - Control Room users: {User.query.filter_by(user_type='controlroom').count()}")
```

---

## CLOUD DEPLOYMENT STEPS

### Step 1: Setup Cloud Database
1. Create PostgreSQL database on cloud platform (Heroku, AWS, Azure, etc.)
2. Get database connection URL
3. Update `config.py` with cloud database URL

### Step 2: Update config.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # For Cloud: Use DATABASE_URL environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///dsr_management.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
```

### Step 3: Run Database Initialization
```bash
# On cloud server, run:
python initialize_database.py
```

### Step 4: Verify Users Created
```bash
# Check users created:
python check_users_info.py
```

---

## LOGIN CREDENTIALS SUMMARY

### For Testing/Initial Access:

| User Type | Username | Password | Access Level |
|-----------|----------|----------|--------------|
| Admin | admin | admin123 | Full system access |
| District (example) | visakhapatnam | visakhapatnam123 | Own district only |
| Control Room | controlroom | controlroom123 | Upload files only |

**⚠️ IMPORTANT:** Change all default passwords after first login!

---

## PASSWORD SECURITY

### Current Implementation:
- ✅ Passwords are **hashed** using `werkzeug.security`
- ✅ NOT stored as plain text in database
- ✅ Hash algorithm: `pbkdf2:sha256`
- ✅ Password verification: `check_password_hash()`

### Password Hash Example:
```
Plain: admin123
Hashed: pbkdf2:sha256:600000$randomsalt$hashedvalue...
```

---

## SESSION CONFIGURATION

```python
# Current Session Settings
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
SESSION_PERMANENT = False
SESSION_TYPE = 'filesystem'

# Session Tracking
- Login time stored in session
- Last activity tracked
- Auto logout after 10 min idle
- Browser close = logout
```

---

## FILE STRUCTURE FOR DEPLOYMENT

```
Required Files for Cloud:
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   ├── templates/
│   └── uploads/ (create directory)
├── instance/ (for SQLite - not needed for PostgreSQL)
├── config.py
├── run.py
├── requirements.txt
└── initialize_database.py (NEW - create this)
```

---

## REQUIREMENTS.TXT

```txt
Flask==2.3.0
Flask-SQLAlchemy==3.0.3
Flask-Login==0.6.2
Werkzeug==2.3.0
openpyxl==3.1.2
pytz==2023.3
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

---

## VERIFICATION CHECKLIST

After cloud deployment:

- [ ] Database tables created (user, dsr_entry, control_room_upload)
- [ ] 30 users created (1 admin + 28 districts + 1 control room)
- [ ] Admin can login with: admin / admin123
- [ ] District user can login with: visakhapatnam / visakhapatnam123
- [ ] Control room can login with: controlroom / controlroom123
- [ ] All users redirect to correct dashboards
- [ ] Session timeout working (10 minutes)
- [ ] File upload directory exists and writable
- [ ] Change all default passwords

---

## SUPPORT CONTACT

For deployment issues, verify:
1. Database connection URL is correct
2. All environment variables set
3. initialize_database.py ran successfully
4. File permissions correct for uploads directory

**Database is ready for cloud deployment with this exact structure!**
