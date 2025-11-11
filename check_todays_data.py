#!/usr/bin/env python3
"""Check data created TODAY (11-11-2025)"""

import os
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import DSREntry
from datetime import datetime, date

app = create_app()

def check_todays_data():
    """Check what data was created today"""
    
    with app.app_context():
        print("🔍 CHECKING TODAY'S DATA (11-11-2025)")
        print("=" * 50)
        
        # Check all entries with detailed timestamps
        all_entries = DSREntry.query.order_by(DSREntry.created_at.desc()).all()
        
        print("📊 ALL ENTRIES BY CREATION TIME:")
        for entry in all_entries:
            created = entry.created_at.strftime("%Y-%m-%d %H:%M:%S") if entry.created_at else "Unknown"
            updated = entry.updated_at.strftime("%Y-%m-%d %H:%M:%S") if entry.updated_at else "Unknown"
            
            print(f"   {entry.district_name}: {entry.form_type}")
            print(f"      Entry Date: {entry.date}")
            print(f"      Created: {created}")
            print(f"      Updated: {updated}")
            print()
        
        # Check entries created TODAY
        today = date(2025, 11, 11)
        today_start = datetime(2025, 11, 11, 0, 0, 0)
        today_end = datetime(2025, 11, 11, 23, 59, 59)
        
        print("📅 ENTRIES CREATED TODAY (11-11-2025):")
        today_entries = DSREntry.query.filter(
            DSREntry.created_at >= today_start,
            DSREntry.created_at <= today_end
        ).all()
        
        if today_entries:
            print(f"   Found {len(today_entries)} entries created today:")
            for entry in today_entries:
                print(f"   ✅ {entry.district_name}: {entry.form_type} (Created: {entry.created_at})")
        else:
            print("   ❌ No entries created today")
        
        # Check entries UPDATED today  
        print("\n🔄 ENTRIES UPDATED TODAY (11-11-2025):")
        updated_today = DSREntry.query.filter(
            DSREntry.updated_at >= today_start,
            DSREntry.updated_at <= today_end
        ).all()
        
        if updated_today:
            print(f"   Found {len(updated_today)} entries updated today:")
            for entry in updated_today:
                print(f"   🔄 {entry.district_name}: {entry.form_type} (Updated: {entry.updated_at})")
        else:
            print("   ❌ No entries updated today")
        
        # Check for entries with date = 2025-11-11
        print("\n📆 ENTRIES WITH DATE = 11-11-2025:")
        date_entries = DSREntry.query.filter_by(date=today).all()
        
        if date_entries:
            print(f"   Found {len(date_entries)} entries with today's date:")
            for entry in date_entries:
                print(f"   📅 {entry.district_name}: {entry.form_type}")
        else:
            print("   ❌ No entries with today's date")

if __name__ == '__main__':
    check_todays_data()