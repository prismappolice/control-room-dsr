#!/usr/bin/env python3
"""Recovery Script for Missing Srikakulam and Kurnool Data"""

import sqlite3
import os
from pathlib import Path

def find_missing_data():
    """Find your missing Srikakulam and Kurnool data"""
    
    print("🔍 SEARCHING FOR MISSING DATA")
    print("=" * 50)
    
    # Check all possible database locations
    db_paths = [
        "D:/control room DSR_backup_20251107_112119/instance/database.db",
        "instance/control_room_dsr_backup.db",
        "instance/control_room_dsr.db", 
        "instance/database.db"
    ]
    
    all_found_data = []
    
    for db_path in db_paths:
        try:
            if Path(db_path).exists():
                print(f"\n📁 Checking: {db_path}")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check all entries
                cursor.execute("""
                    SELECT district_name, form_type, date, created_at, data 
                    FROM dsr_entry 
                    ORDER BY created_at DESC
                """)
                entries = cursor.fetchall()
                
                print(f"   Total entries: {len(entries)}")
                
                # Look for Srikakulam and Kurnool specifically
                srikakulam_entries = [e for e in entries if e[0] == 'Srikakulam']
                kurnool_entries = [e for e in entries if e[0] == 'Kurnool']
                
                print(f"   Srikakulam: {len(srikakulam_entries)} entries")
                print(f"   Kurnool: {len(kurnool_entries)} entries")
                
                for entry in srikakulam_entries + kurnool_entries:
                    print(f"      {entry[0]}: {entry[1]} - {entry[2]} (Created: {entry[3]})")
                    all_found_data.append(entry)
                
                # Check for entries created on 10-11-2025
                cursor.execute("""
                    SELECT district_name, form_type, date, created_at 
                    FROM dsr_entry 
                    WHERE created_at LIKE '2025-11-10%'
                    ORDER BY created_at DESC
                """)
                nov10_entries = cursor.fetchall()
                
                if nov10_entries:
                    print(f"\n   📅 Entries created on 2025-11-10: {len(nov10_entries)}")
                    for entry in nov10_entries:
                        print(f"      {entry[0]}: {entry[1]} - {entry[2]} (Created: {entry[3]})")
                        if entry not in all_found_data:
                            all_found_data.append(entry)
                
                conn.close()
                
        except Exception as e:
            print(f"   ❌ Error checking {db_path}: {e}")
    
    if all_found_data:
        print(f"\n🎉 FOUND MISSING DATA! ({len(all_found_data)} entries)")
        print("\n📋 Your Missing Data:")
        for entry in all_found_data:
            print(f"   {entry[0]}: {entry[1]} - {entry[2]} (Created: {entry[3]})")
        
        # Option to recover
        print("\n🔧 Would you like to recover this data to PostgreSQL?")
        return all_found_data
    else:
        print("\n❌ No Srikakulam/Kurnool data found in any backup")
        
        # Check what dates exist
        print("\n📅 Available dates in all databases:")
        for db_path in db_paths:
            try:
                if Path(db_path).exists():
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT DISTINCT date FROM dsr_entry ORDER BY date DESC")
                    dates = cursor.fetchall()
                    if dates:
                        date_list = [d[0] for d in dates]
                        print(f"   {db_path}: {date_list}")
                    conn.close()
            except:
                pass
        
        return []

if __name__ == '__main__':
    find_missing_data()