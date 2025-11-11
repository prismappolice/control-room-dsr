#!/usr/bin/env python3
"""Check for missing Srikakulam and Kurnool data"""

import os
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import User, DSREntry
from datetime import datetime, date

app = create_app()

def check_missing_data():
    """Check for missing Srikakulam and Kurnool data"""
    
    with app.app_context():
        print("🔍 CHECKING FOR MISSING DATA")
        print("=" * 50)
        
        # Check all DSR entries by date
        print("📊 All DSR entries in database:")
        all_entries = DSREntry.query.order_by(DSREntry.date.desc(), DSREntry.created_at.desc()).all()
        
        for entry in all_entries:
            created_date = entry.created_at.strftime("%Y-%m-%d %H:%M") if entry.created_at else "Unknown"
            print(f"   {entry.district_name}: {entry.form_type}")
            print(f"      Date: {entry.date} | Created: {created_date}")
            print()
        
        print(f"\n📈 Total entries found: {len(all_entries)}")
        
        # Check by district
        print("\n🏛️  Entries by District:")
        districts = db.session.query(DSREntry.district_name).distinct().all()
        for district_tuple in districts:
            district = district_tuple[0]
            count = DSREntry.query.filter_by(district_name=district).count()
            print(f"   {district}: {count} entries")
            
            # Show dates for this district
            dates = db.session.query(DSREntry.date).filter_by(district_name=district).distinct().all()
            date_list = [d[0].strftime("%Y-%m-%d") for d in dates]
            print(f"      Dates: {', '.join(date_list)}")
        
        # Specifically check for Srikakulam and Kurnool
        print("\n🔍 Checking specifically for Srikakulam and Kurnool:")
        
        srikakulam_entries = DSREntry.query.filter_by(district_name='Srikakulam').all()
        print(f"\n📊 Srikakulam entries ({len(srikakulam_entries)}):")
        for entry in srikakulam_entries:
            print(f"   {entry.form_type} - {entry.date} (Created: {entry.created_at})")
        
        kurnool_entries = DSREntry.query.filter_by(district_name='Kurnool').all()
        print(f"\n📊 Kurnool entries ({len(kurnool_entries)}):")
        for entry in kurnool_entries:
            print(f"   {entry.form_type} - {entry.date} (Created: {entry.created_at})")
        
        # Check entries for specific dates
        print("\n📅 Entries by specific dates:")
        target_dates = ['2025-11-04', '2025-11-10', '2025-11-11']
        
        for target_date in target_dates:
            try:
                date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
                entries = DSREntry.query.filter_by(date=date_obj).all()
                print(f"\n📅 {target_date} ({len(entries)} entries):")
                for entry in entries:
                    print(f"   {entry.district_name}: {entry.form_type}")
            except Exception as e:
                print(f"   Error checking {target_date}: {e}")
        
        # Check for entries created on specific dates
        print("\n🕐 Entries by creation date:")
        creation_dates = ['2025-11-10', '2025-11-11']
        
        for creation_date in creation_dates:
            try:
                start_date = datetime.strptime(f"{creation_date} 00:00:00", '%Y-%m-%d %H:%M:%S')
                end_date = datetime.strptime(f"{creation_date} 23:59:59", '%Y-%m-%d %H:%M:%S')
                
                entries = DSREntry.query.filter(
                    DSREntry.created_at >= start_date,
                    DSREntry.created_at <= end_date
                ).all()
                
                print(f"\n📅 Created on {creation_date} ({len(entries)} entries):")
                for entry in entries:
                    print(f"   {entry.district_name}: {entry.form_type} (Entry date: {entry.date})")
                    
            except Exception as e:
                print(f"   Error checking creation date {creation_date}: {e}")

if __name__ == '__main__':
    check_missing_data()