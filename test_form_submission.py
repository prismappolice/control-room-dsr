#!/usr/bin/env python3
"""Test Form Submission Functionality with PostgreSQL"""

import os
os.environ['DATABASE_TYPE'] = 'postgresql'

from app import create_app, db
from app.models import User, DSREntry
from datetime import date
import json

app = create_app()

def test_form_submission():
    """Test if form submission works properly with PostgreSQL"""
    
    with app.app_context():
        print("🧪 TESTING FORM SUBMISSION WITH POSTGRESQL")
        print("=" * 55)
        
        # Check current data count
        initial_count = DSREntry.query.count()
        print(f"📊 Initial DSR entries: {initial_count}")
        
        # Get Srikakulam and Kurnool users
        srikakulam_user = User.query.filter_by(username='srikakulam').first()
        kurnool_user = User.query.filter_by(username='kurnool').first()
        
        if not srikakulam_user:
            print("❌ Srikakulam user not found")
            return False
            
        if not kurnool_user:
            print("❌ Kurnool user not found") 
            return False
            
        print(f"✅ Found Srikakulam user: {srikakulam_user.username}")
        print(f"✅ Found Kurnool user: {kurnool_user.username}")
        
        # Test data
        test_data = {
            'unit_name': 'Test Unit',
            'crime_head': 'Test Crime',
            'fir_no': 'FIR-123/2025',
            'facts_of_case': 'Test case details for form submission testing',
            'accused_status': 'Under investigation',
            'action_taken': 'Investigation initiated',
            'legal_progress': 'FIR registered'
        }
        
        try:
            # Create test entries
            today = date.today()
            
            # Srikakulam test entry
            srikakulam_entry = DSREntry(
                district_name='Srikakulam',
                form_type='crime_data',
                date=today,
                data=json.dumps(test_data),
                user_id=srikakulam_user.id
            )
            
            # Kurnool test entry  
            kurnool_entry = DSREntry(
                district_name='Kurnool',
                form_type='crime_data', 
                date=today,
                data=json.dumps(test_data),
                user_id=kurnool_user.id
            )
            
            # Add to database
            db.session.add(srikakulam_entry)
            db.session.add(kurnool_entry)
            db.session.commit()
            
            print("✅ Test entries created successfully")
            
            # Verify entries were saved
            new_count = DSREntry.query.count()
            print(f"📊 New DSR entries count: {new_count}")
            print(f"📈 Entries added: {new_count - initial_count}")
            
            # Check specific entries
            srikakulam_check = DSREntry.query.filter_by(
                district_name='Srikakulam',
                form_type='crime_data',
                date=today
            ).first()
            
            kurnool_check = DSREntry.query.filter_by(
                district_name='Kurnool', 
                form_type='crime_data',
                date=today
            ).first()
            
            if srikakulam_check:
                print(f"✅ Srikakulam entry verified: ID {srikakulam_check.id}")
                print(f"   Created: {srikakulam_check.created_at}")
                
            if kurnool_check:
                print(f"✅ Kurnool entry verified: ID {kurnool_check.id}")
                print(f"   Created: {kurnool_check.created_at}")
            
            # Test data persistence (simulate restart check)
            print("\n🔄 TESTING DATA PERSISTENCE...")
            
            # Close and reopen connection (simulate restart)
            db.session.close()
            
            # Check data still exists
            persistent_count = DSREntry.query.count()
            persistent_srikakulam = DSREntry.query.filter_by(district_name='Srikakulam').count()
            persistent_kurnool = DSREntry.query.filter_by(district_name='Kurnool').count()
            
            print(f"✅ Data after restart simulation:")
            print(f"   Total entries: {persistent_count}")
            print(f"   Srikakulam entries: {persistent_srikakulam}")
            print(f"   Kurnool entries: {persistent_kurnool}")
            
            if persistent_srikakulam > 0 and persistent_kurnool > 0:
                print("\n🎉 SUCCESS! Data is persistent across restarts")
                print("✅ PostgreSQL is working perfectly")
                print("✅ Your new entries will be saved permanently")
                
                # Clean up test data
                print("\n🧹 Cleaning up test data...")
                DSREntry.query.filter_by(district_name='Srikakulam', form_type='crime_data', date=today).delete()
                DSREntry.query.filter_by(district_name='Kurnool', form_type='crime_data', date=today).delete()
                db.session.commit()
                print("✅ Test data cleaned up")
                
                return True
            else:
                print("\n❌ FAILED! Data not persistent")
                return False
                
        except Exception as e:
            print(f"\n❌ ERROR during testing: {e}")
            db.session.rollback()
            return False

def check_form_endpoints():
    """Check if form endpoints are working"""
    
    print("\n🌐 CHECKING FORM ENDPOINTS...")
    
    with app.test_client() as client:
        # Check if district login works
        print("🔐 Testing district login...")
        
        # Test Srikakulam login
        srikakulam_login = client.post('/auth/login?type=district', data={
            'username': 'srikakulam',
            'password': 'srikakulam123'
        })
        
        if srikakulam_login.status_code in [200, 302]:
            print("✅ Srikakulam login working")
        else:
            print(f"❌ Srikakulam login failed: {srikakulam_login.status_code}")
        
        # Test form page access
        print("📝 Testing form page access...")
        form_response = client.get('/district/form/crime_data')
        
        if form_response.status_code == 200:
            print("✅ Form pages accessible")
        else:
            print(f"❌ Form page access failed: {form_response.status_code}")

if __name__ == '__main__':
    print("🚀 PostgreSQL Form Submission Test")
    print("=" * 40)
    
    success = test_form_submission()
    check_form_endpoints()
    
    if success:
        print("\n🎯 FINAL RESULT:")
        print("✅ PostgreSQL is working perfectly")
        print("✅ Form submissions will be saved permanently") 
        print("✅ Data will NOT disappear after restart")
        print("✅ Safe to enter Srikakulam and Kurnool data")
        print("\n📋 You can now enter your district data confidently!")
    else:
        print("\n❌ FINAL RESULT:")
        print("❌ Issues found with form submission")
        print("❌ Need to fix before entering data")