#!/usr/bin/env python3
"""Check time zone and entry timestamps"""

import os
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import DSREntry
from datetime import datetime
import pytz

app = create_app()

def check_time_issue():
    """Check the time zone issue"""
    
    with app.app_context():
        print("🕐 TIME ZONE ANALYSIS")
        print("=" * 35)
        
        # Get system time
        now = datetime.now()
        print(f"System time now: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get latest entries
        latest_entries = DSREntry.query.order_by(DSREntry.created_at.desc()).limit(3).all()
        
        print(f"\n📊 Latest entries:")
        for i, entry in enumerate(latest_entries, 1):
            created = entry.created_at
            formatted_time = created.strftime('%H:%M')
            
            print(f"{i}. {entry.district_name}: {entry.form_type}")
            print(f"   Full timestamp: {created}")
            print(f"   Display time: {formatted_time}")
            print(f"   Date: {entry.date}")
            print()
        
        # Check if there's a new entry created today
        from datetime import date
        today = date.today()
        
        todays_entries = DSREntry.query.filter_by(date=today).all()
        print(f"📅 Entries for today ({today}):")
        
        if todays_entries:
            for entry in todays_entries:
                print(f"   {entry.district_name}: {entry.form_type} - Created: {entry.created_at}")
        else:
            print("   No entries found for today")
        
        # Check for Prakasam entries specifically
        print(f"\n🏛️  Prakasam entries:")
        prakasam_entries = DSREntry.query.filter_by(district_name='Prakasam').order_by(DSREntry.created_at.desc()).limit(5).all()
        
        for entry in prakasam_entries:
            print(f"   {entry.form_type}: Created {entry.created_at} (Display: {entry.created_at.strftime('%H:%M')})")

if __name__ == '__main__':
    check_time_issue()