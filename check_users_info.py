from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    
    print('\n' + '='*80)
    print('DATABASE LOGIN INFORMATION - 3 TYPES OF USERS')
    print('='*80)
    
    print(f'\nTotal Users in Database: {len(users)}')
    
    # Group by user type
    admin_users = [u for u in users if u.user_type == 'admin']
    district_users = [u for u in users if u.user_type == 'district']
    controlroom_users = [u for u in users if u.user_type == 'controlroom']
    
    print(f'\n1. Admin Users: {len(admin_users)}')
    print(f'2. District Users: {len(district_users)}')
    print(f'3. Control Room Users: {len(controlroom_users)}')
    
    print('\n' + '='*80)
    print('USER TABLE STRUCTURE:')
    print('='*80)
    print('Columns: id, username, password_hash, user_type, district_name, is_active, created_at, last_password_change')
    
    print('\n' + '='*80)
    print('1. ADMIN USERS')
    print('='*80)
    print(f'User Type: admin')
    print(f'District Field: NULL (not required)')
    print(f'Login Format: username + password + user_type=admin')
    for u in admin_users:
        print(f'  - Username: {u.username} | Active: {u.is_active}')
    
    print('\n' + '='*80)
    print('2. DISTRICT USERS')
    print('='*80)
    print(f'User Type: district')
    print(f'District Field: Required (stores district name)')
    print(f'Login Format: username + password + user_type=district')
    for u in district_users[:5]:  # Show first 5 only
        print(f'  - Username: {u.username} | District: {u.district_name} | Active: {u.is_active}')
    if len(district_users) > 5:
        print(f'  ... and {len(district_users) - 5} more district users')
    
    print('\n' + '='*80)
    print('3. CONTROL ROOM USERS')
    print('='*80)
    print(f'User Type: controlroom')
    print(f'District Field: NULL or specific value')
    print(f'Login Format: username + password + user_type=controlroom')
    for u in controlroom_users:
        print(f'  - Username: {u.username} | District: {u.district_name or "N/A"} | Active: {u.is_active}')
    
    print('\n' + '='*80)
    print('LOGIN AUTHENTICATION PROCESS:')
    print('='*80)
    print('1. User enters: username, password, user_type (dropdown)')
    print('2. System queries: User.query.filter_by(username=username, user_type=user_type).first()')
    print('3. Password check: user.check_password(password) - compares hash using werkzeug.security')
    print('4. Redirect based on user_type:')
    print('   - admin -> /admin/dashboard')
    print('   - district -> /district/dashboard')
    print('   - controlroom -> /district/controlroom_dashboard')
    
    print('\n' + '='*80)
    print('PASSWORD STORAGE:')
    print('='*80)
    print('- Passwords are HASHED using werkzeug.security.generate_password_hash()')
    print('- NOT stored as plain text')
    print('- Column: password_hash (255 characters)')
    print('- Verification: check_password_hash() function')
    
    print('\n' + '='*80)
    print('SESSION MANAGEMENT:')
    print('='*80)
    print('- Session Timeout: 10 minutes of inactivity')
    print('- Session Type: Non-permanent (clears on browser close)')
    print('- Tracking: last_activity timestamp in session')
    print('='*80 + '\n')
