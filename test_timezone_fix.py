#!/usr/bin/env python3
"""Test if timezone fix is working"""

import os
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import DSREntry, User, ist_now
import json
from datetime import date, datetime

app = create_app()

def test_timezone_fix():
    """Test if new entries show correct IST time"""
    
    with app.app_context():
        print("🕐 TESTING TIMEZONE FIX")
        print("=" * 30)
        
        # Current IST time
        current_ist = ist_now()
        current_system = datetime.now()
        
        print(f"System time: {current_system.strftime('%H:%M:%S')}")
        print(f"IST function: {current_ist.strftime('%H:%M:%S')}")
        
        try:
            # Create test entry
            user = User.query.filter_by(username='prakasam').first()
            test_entry = DSREntry(
                district_name='Prakasam',
                form_type='timezone_test',
                date=date.today(),
                data=json.dumps({'test': 'timezone fix'}),
                user_id=user.id
            )
            
            db.session.add(test_entry)
            db.session.commit()
            
            # Check saved time
            saved_time = test_entry.created_at
            display_time = saved_time.strftime('%H:%M')
            
            print(f"Entry saved at: {saved_time}")
            print(f"Display time: {display_time}")
            
            # Check if times match (within 1 minute)
            time_diff = abs((current_system.hour * 60 + current_system.minute) - 
                           (saved_time.hour * 60 + saved_time.minute))
            
            if time_diff <= 1:
                print("✅ SUCCESS! Time zone fixed")
                print("✅ New entries will show correct IST time")
            else:
                print(f"❌ Still {time_diff} minutes difference")
            
            # Clean up
            db.session.delete(test_entry)
            db.session.commit()
            print("✅ Test entry cleaned up")
            
            return time_diff <= 1
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

if __name__ == '__main__':
    if test_timezone_fix():
        print("\n🎯 RESULT:")
        print("✅ Timezone issue FIXED!")
        print("✅ Your next form entries will show correct time")
        print("✅ Time will match your system time")
        print("\nRestart Flask server to apply changes completely.")
    else:
        print("\n❌ Timezone fix didn't work completely")