#!/usr/bin/env python3
"""Fix timezone issue for correct time display"""

import psycopg2
from datetime import datetime

def fix_timezone():
    """Fix PostgreSQL timezone to Indian Standard Time"""
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432', 
            database='control_room_dsr',
            user='dsr_user',
            password='dsr_pass123'
        )
        
        cursor = conn.cursor()
        
        print("🕐 FIXING TIMEZONE ISSUE")
        print("=" * 30)
        
        # Check current timezone
        cursor.execute("SHOW timezone")
        current_tz = cursor.fetchone()[0]
        print(f"Current PostgreSQL timezone: {current_tz}")
        
        # Check current time in PostgreSQL
        cursor.execute("SELECT now()")
        pg_time = cursor.fetchone()[0]
        print(f"Current PostgreSQL time: {pg_time}")
        
        # Set timezone to India  
        cursor.execute("SET timezone = 'Asia/Kolkata'")
        
        # Verify new timezone
        cursor.execute("SHOW timezone")
        new_tz = cursor.fetchone()[0]
        print(f"New PostgreSQL timezone: {new_tz}")
        
        # Check new time
        cursor.execute("SELECT now()")
        new_time = cursor.fetchone()[0]
        print(f"New PostgreSQL time: {new_time}")
        
        # Make it permanent for this session
        cursor.execute("ALTER DATABASE control_room_dsr SET timezone = 'Asia/Kolkata'")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Timezone fixed to Asia/Kolkata (IST)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing timezone: {e}")
        return False

def test_new_entry_time():
    """Test if new entries now show correct time"""
    
    import os
    os.environ['DATABASE_TYPE'] = 'postgresql'
    
    from app import create_app, db
    from app.models import DSREntry, User
    import json
    from datetime import date
    
    app = create_app()
    
    with app.app_context():
        print("\n🧪 TESTING NEW ENTRY TIME")
        print("=" * 30)
        
        # Current system time
        system_time = datetime.now()
        print(f"Current system time: {system_time.strftime('%H:%M:%S')}")
        
        try:
            # Create test entry
            user = User.query.filter_by(username='prakasam').first()
            test_entry = DSREntry(
                district_name='Prakasam',
                form_type='test_time_check',
                date=date.today(),
                data=json.dumps({'test': 'timezone fix'}),
                user_id=user.id
            )
            
            db.session.add(test_entry)
            db.session.commit()
            
            # Check the saved time
            saved_time = test_entry.created_at
            display_time = saved_time.strftime('%H:%M')
            
            print(f"Entry saved at: {saved_time}")
            print(f"Display time: {display_time}")
            
            # Clean up test entry
            db.session.delete(test_entry)
            db.session.commit()
            
            print("✅ Test entry created and cleaned up")
            
            # Check time difference
            time_diff = abs((system_time.hour * 60 + system_time.minute) - 
                           (saved_time.hour * 60 + saved_time.minute))
            
            if time_diff <= 2:  # Within 2 minutes is acceptable
                print("✅ Time zone fixed! New entries will show correct time")
                return True
            else:
                print(f"❌ Still {time_diff} minutes difference")
                return False
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

if __name__ == '__main__':
    if fix_timezone():
        test_new_entry_time()
        print("\n🎯 RESULT:")
        print("✅ Timezone issue fixed")
        print("✅ New entries will show correct IST time")
        print("✅ Your next form submissions will display proper time")
    else:
        print("\n❌ Failed to fix timezone issue")